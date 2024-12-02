import re
from aiogram.types import Message


async def validate_string(message: Message):
    try:
        message_text = message.text.strip()
        pattern = r'^[а-яА-ЯёЁ\s]+$'
        if not re.match(pattern, message_text):
            return False
        return True
    except Exception as error:
        return False
