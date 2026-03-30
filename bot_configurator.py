from handlers.main_handlers import main_labeler
from handlers.predsed_team import admin_labeler
from handlers.deadlines import load_deadline

from middlewares.main_middleware import NoBotMiddleware, AdminMiddleware

from global_variables.variables import state_dispenser, labeler, deadline_scheduler
from global_variables.token import api
from loguru import logger
from vkbottle import Bot
from orm.database import init_models, create_tables, select, insert
import asyncio
import random
import sys


def start_bot(loop):
    # Настройка логов
    logger.remove()
    logger.add(sink=sys.stderr,
               format="{time:YYYY-MM-DD HH:mm:ss} {level} {message}",
               backtrace=False,
               level="ERROR",
               diagnose=True)

    # Подключение перехватчиков
    labeler.load(main_labeler)
    labeler.load(admin_labeler)

    # Подключение middleware
    labeler.message_view.register_middleware(NoBotMiddleware)
    labeler.message_view.register_middleware(AdminMiddleware)

    bot = Bot(api=api,
              labeler=labeler,
              state_dispenser=state_dispenser)

    async def startup():
        await create_tables()
        await load_deadline()
        deadline_scheduler.start()

    loop.run_until_complete(startup())

    print("Bot is started!")

    bot.run_forever()
