from handlers.main_handlers import main_labeler
from handlers.predsed_team import admin_labeler
from handlers.deadlines import load_deadline
from middlewares.main_middleware import NoBotMiddleware, AdminMiddleware
from global_variables.variables import state_dispenser, deadline_scheduler
from global_variables.logger import setup_logger
from global_variables.token import api
from vkbottle import Bot
from orm.database import create_tables
import os

_initialized = False


def start_bot(loop):
    global _initialized

    if _initialized:
        return
    _initialized = True

    os.makedirs('logs', exist_ok=True)
    os.makedirs('homework', exist_ok=True)
    os.makedirs('homework_zips', exist_ok=True)

    logger = setup_logger()
    logger.info("Запуск бота...")

    bot = Bot(api=api, state_dispenser=state_dispenser)

    bot.labeler.load(main_labeler)
    logger.info("main_labeler загружен")

    bot.labeler.load(admin_labeler)
    logger.info("admin_labeler загружен")

    bot.labeler.message_view.register_middleware(NoBotMiddleware)
    bot.labeler.message_view.register_middleware(AdminMiddleware)
    logger.info("Middleware зарегистрированы")

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
    logger.info("Бот запущен!")
    bot.run_forever()
