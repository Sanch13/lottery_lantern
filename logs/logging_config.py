import os
import sys

from loguru import logger


if not os.path.exists('logs'):
    os.makedirs('logs')

logger.remove()


# Настройка логера
logger.add("logs/app.log", level="INFO", rotation="10 MB", retention="10 days", compression="zip")
logger.add(sys.stdout, level="DEBUG", format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}")
