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


def start_bot(loop):
    # Настройка логов
    logger.remove()
    logger.add(
        sink=sys.stderr,
        format="{time:YYYY-MM-DD HH:mm:ss} {level} {message}",
        backtrace=False,
        level="ERROR",
        diagnose=True
    )

    # Подключение лейблеров (с защитой от двойной загрузки)
    if main_labeler not in labeler.custom_rules:
        labeler.load(main_labeler)
    if admin_labeler not in labeler.custom_rules:
        labeler.load(admin_labeler)

    # Подключение middleware (с защитой от двойной регистрации)
    existing_middlewares = [type(m) for m in labeler.message_view.middlewares]
    if NoBotMiddleware not in existing_middlewares:
        labeler.message_view.register_middleware(NoBotMiddleware)
    if AdminMiddleware not in existing_middlewares:
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
