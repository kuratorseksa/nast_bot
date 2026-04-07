from handlers.main_handlers import main_labeler
from handlers.predsed_team import admin_labeler
from handlers.deadlines import load_deadline
from middlewares.main_middleware import NoBotMiddleware, AdminMiddleware
from global_variables.variables import state_dispenser, labeler, deadline_scheduler
from global_variables.token import api
from loguru import logger
from vkbottle import Bot
from orm.database import create_tables
import sys

_initialized = False  # ← флаг


def start_bot(loop):
    global _initialized

    if _initialized:
        logger.warning("start_bot вызван повторно — игнорируем")
        return
    _initialized = True

    logger.remove()
    logger.add(
        sink=sys.stderr,
        format="{time:YYYY-MM-DD HH:mm:ss} {level} {message}",
        backtrace=False,
        level="ERROR",
        diagnose=True
    )

    labeler.load(main_labeler)
    labeler.load(admin_labeler)

    labeler.message_view.register_middleware(NoBotMiddleware)
    labeler.message_view.register_middleware(AdminMiddleware)

    bot = Bot(
        api=api,
        labeler=labeler,
        state_dispenser=state_dispenser
    )

    async def startup():
        try:
            await create_tables()
            logger.info("Таблицы БД созданы/проверены")
        except Exception as e:
            logger.error(f"Ошибка при создании таблиц: {e}")
            raise
        try:
            await load_deadline()
            logger.info("Дедлайны загружены")
        except Exception as e:
            logger.error(f"Ошибка при загрузке дедлайнов: {e}")
            raise
        try:
            deadline_scheduler.start()
            logger.info("Планировщик запущен")
        except Exception as e:
            logger.error(f"Ошибка при запуске планировщика: {e}")
            raise

    loop.run_until_complete(startup())
    print("Bot is started!")
    bot.run_forever()
