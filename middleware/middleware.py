from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config import settings
from init_bot import bot
from utils.utils_for_db import is_exists_user


def check_subscribe(func):
    """Checking user subscribing on the group or channel"""
    async def wrapper(message: Message):
        user_id = message.from_user.id
        status = await bot.get_chat_member(chat_id=settings.CHANNEL_ID_MIRAN, user_id=user_id)
        if status.status in ('member', 'creator', 'administrator'):
            await func(message)
        else:
            await message.answer(f"""Вы не зарегистрированы!\n Для регистрации перейдите по ссылке: {settings.CHANNEL_LINK_REG_BOT}""")
    return wrapper


def check_registration(func):
    """Checking user registrations"""
    async def wrapper(message: Message, state: FSMContext):
        user_id = message.from_user.id
        if await is_exists_user(telegram_id=user_id):
            await message.answer(f"""Упс!\nВы уже зарегистрированы.""")
        else:
            await func(message, state)
    return wrapper


def is_exists_user_in_channel_and_table(func):
    """Checking user subscribing on the group or channel"""
    async def wrapper(message: Message):
        user_id = message.from_user.id
        status = await bot.get_chat_member(chat_id=settings.CHANNEL_ID_MIRAN, user_id=user_id)
        if status.status in ('member', 'creator', 'administrator') and await is_exists_user(telegram_id=user_id):
            await message.answer(f"""Вы уже зарегистрированы.""")
        else:
            await func(message)

    return wrapper
