import asyncio
import logging
import sys

from init_bot import dp, bot

from logs.logging_config import logger
from handlers import handlers


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Выход")
    except Exception as error:
        logger.error("Exception occurred: {}", error)
