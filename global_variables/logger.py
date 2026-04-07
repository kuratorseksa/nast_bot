import sys
from loguru import logger

def setup_logger():
    logger.remove()

    # Логи в консоль — все уровни
    logger.add(
        sink=sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{name}</cyan>:<cyan>{line}</cyan> | {message}",
        level="DEBUG",
        colorize=True
    )

    # Логи в файл — все уровни, ротация каждый день
    logger.add(
        sink="logs/bot.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{line} | {message}",
        level="DEBUG",
        rotation="1 day",
        retention="7 days",  # хранить логи 7 дней
        encoding="utf-8"
    )

    # Отдельный файл только для ошибок
    logger.add(
        sink="logs/errors.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{line} | {message}",
        level="ERROR",
        rotation="1 week",
        retention="1 month",
        encoding="utf-8",
        backtrace=True,
        diagnose=True
    )

    return logger
