from global_variables.variables import deadline_scheduler, predsed_team_ids
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime, timedelta
from global_variables.token import api, GROUP_ID
from orm.models import *
from orm.database import delete, select, update, and_
import random
import time
import asyncio
from loguru import logger

async def send_message(user_id, text, finish=False, more_deadlines=False):
    try:
        ...
        logger.info(f"Сообщение отправлено пользователю {user_id}")
    except Exception as e:
        logger.error(f"Ошибка отправки пользователю {user_id}: {e}")

async def deadline_reminder(deadline_id, name, is_birthday, remain_time_sec, text=''):
    logger.info(f"Срабатывание дедлайна: {name}, remain_time_sec={remain_time_sec}")
    ...

def add_deadline_to_schedule(id_deadline, deadline_end, is_birthday, name, text=''):
    logger.info(f"Добавление дедлайна в расписание: {name}, время: {deadline_end}")
    ...


async def send_spam(text, pt=False, finish=False, more_deadlines=False):
    if pt:
        for vk_id in predsed_team_ids:
            await send_message(user_id=vk_id, text=text)
    else:
        # fix #1 — берём всех пользователей из БД, а не из conversations
        async with async_session as session:
            result = await session.execute(select(AlmostCurator.vk_id))
            user_ids = result.scalars().all()

        for user_id in user_ids:
            await send_message(user_id=user_id, text=text, finish=finish, more_deadlines=more_deadlines)
            await asyncio.sleep(0.05)  # небольшая пауза чтобы не словить rate limit VK


async def send_message(user_id, text, finish=False, more_deadlines=False):
    try:
        allow_message = await api.messages.is_messages_from_group_allowed(
            group_id=GROUP_ID, user_id=user_id
        )
        if not allow_message.is_allowed:
            return

        # fix #2 — используем time.time_ns() чтобы random_id был уникальным
        await api.messages.send(
            random_id=time.time_ns() % 2147483647,
            peer_id=user_id,
            message=text
        )

        if not finish:
            async with async_session as session:
                await session.execute(
                    update(AlmostCurator)
                    .where(AlmostCurator.vk_id == user_id)
                    .values(hw_completion=False)
                )
                await session.commit()
        else:
            if user_id not in predsed_team_ids:
                async with async_session as session:
                    result = await session.execute(
                        select(AlmostCurator.strikes_number)
                        .where(and_(
                            AlmostCurator.hw_completion == False,  # noqa
                            AlmostCurator.vk_id == user_id
                        ))
                    )
                    strikes_num = result.scalars().first()
                    if strikes_num is not None:
                        await session.execute(
                            update(AlmostCurator)
                            .where(AlmostCurator.vk_id == user_id)
                            .values(strikes_number=strikes_num + 1)
                        )
                        await api.messages.send(
                            random_id=time.time_ns() % 2147483647,
                            peer_id=user_id,
                            message='Тебе выдано предупреждение!'
                        )
                        await session.commit()
                        if not more_deadlines:
                            await session.execute(
                                update(AlmostCurator)
                                .where(AlmostCurator.vk_id == user_id)
                                .values(hw_completion=True)
                            )
                            await session.commit()
    except Exception as e:
        print(f'Ошибка отправки сообщения пользователю {user_id}: {e}')


async def deadline_reminder(deadline_id, name, is_birthday, remain_time_sec, text=''):
    if is_birthday:
        msg = f'Сегодня {name} 🎉'
    else:
        msg = text

    if remain_time_sec == 0 and not is_birthday:
        msg = f"Дедлайн на {name} прошел!"
        async with async_session as session:
            await session.execute(delete(Deadline).where(Deadline.id == deadline_id))
            await session.commit()
            deadlines = await session.execute(select(Deadline))
            deadlines = deadlines.scalars().first()
        await send_spam(msg, finish=True, more_deadlines=bool(deadlines))
        return

    await send_spam(msg, is_birthday)


def add_deadline_to_schedule(id_deadline: int, deadline_end: datetime, is_birthday: bool, name: str, text=''):
    now = datetime.now()
    if is_birthday:
        reminder = deadline_end.replace(hour=0, minute=0, second=0)
        deadline_scheduler.add_job(
            func=deadline_reminder,
            trigger=CronTrigger(
                month=reminder.month,
                day=reminder.day,
                hour=reminder.hour,
                minute=reminder.minute,
                second=reminder.second,
                timezone="Europe/Moscow"
            ),
            args=[id_deadline, name, is_birthday, 0, text]
        )
    else:
        # Уведомление о новом дедлайне — через 10 секунд после создания
        announcement_time = now + timedelta(seconds=10)
        deadline_scheduler.add_job(
            func=deadline_reminder,
            trigger=CronTrigger(
                year=announcement_time.year,
                month=announcement_time.month,
                day=announcement_time.day,
                hour=announcement_time.hour,
                minute=announcement_time.minute,
                second=announcement_time.second,
                timezone="Europe/Moscow"
            ),
            args=[id_deadline, name, is_birthday, 1, text]  # remain_time_sec=1 → отправит text
        )
        # Уведомление об окончании дедлайна — точно в момент дедлайна
        deadline_scheduler.add_job(
            func=deadline_reminder,
            trigger=CronTrigger(
                year=deadline_end.year,
                month=deadline_end.month,
                day=deadline_end.day,
                hour=deadline_end.hour,
                minute=deadline_end.minute,
                second=deadline_end.second,
                timezone="Europe/Moscow"
            ),
            args=[id_deadline, name, is_birthday, 0, text]  # remain_time_sec=0 → дедлайн истёк
        )


async def load_deadline():
    now = datetime.now()  # fix #3 — сравниваем datetime напрямую, а не кортежи
    async with async_session as session:
        deadlines = await session.execute(select(Deadline))
        deadlines = deadlines.scalars().all()

    for deadline in deadlines:
        if deadline.birthday:
            add_deadline_to_schedule(deadline.id, deadline.time, deadline.birthday, deadline.name)
            continue

        if deadline.time >= now:  # дедлайн ещё не прошёл — планируем
            add_deadline_to_schedule(deadline.id, deadline.time, deadline.birthday, deadline.name)
        else:  # дедлайн уже прошёл — удаляем из БД
            async with async_session as session:
                await session.execute(delete(Deadline).where(Deadline.id == deadline.id))
                await session.commit()
