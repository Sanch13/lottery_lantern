from aiogram import Dispatcher, Bot, Router

from config import settings


bot = Bot(token=settings.API_TELEGRAM_TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)
