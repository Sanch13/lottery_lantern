import asyncio
import aiosmtplib
from email.message import EmailMessage

from aiogram.types import Message

from config import settings
from logs.logging_config import logger


async def send_email(telegram_id, full_name, full_name_from_tg, username):
    message = EmailMessage()
    message["From"] = settings.SENDER_EMAIL
    message["To"] = settings.TO_EMAILS
    message["Subject"] = "Новая регистрация в телеграм Канале"

    # HTML-разметка для письма
    html_content = f"""
        <html>
            <body>
                <h1>Новая регистрация в телеграм Канале</h1>
                <p><strong>Telegram ID:</strong> {telegram_id}</p>
                <p><strong>Введенное ФИО при регистрации:</strong> {full_name}</p>
                <p><strong>Полное имя из Telegram:</strong> {full_name_from_tg}</p>
                <p><strong>Username из Telegram:</strong> {username}</p>
            </body>
        </html>
        """

    # Устанавливаем HTML-разметку как содержимое письма
    message.set_content(html_content, subtype='html')

    try:
        await aiosmtplib.send(message,
                              hostname=settings.SMTP_SERVER,
                              port=587,
                              start_tls=True,
                              username=settings.SENDER_EMAIL,
                              password=settings.PASSWORD)
        logger.info(f"Письмо успешно отправлено на адрес {settings.TO_EMAILS}!")
    except asyncio.TimeoutError:
        logger.error("Ошибка: время ожидания истекло при подключении или отправке письма.")
    except Exception as e:
        logger.exception(f"Ошибка при отправке письма: {str(e)}")


async def get_data_user(message: Message, data: dict) -> tuple:
    return (
        message.from_user.id,
        f"{data.get('last_name', '')} {data.get('first_name', '')} {data.get('middle_name', '')}",
        message.from_user.full_name or "",
        message.from_user.username or ""
    )
