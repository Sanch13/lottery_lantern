from sqlalchemy import exists, join
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError

from models.database import AsyncSession
from models.models import User, Lottery, Ticket

from logs.logging_config import logger


async def is_exists_user(telegram_id: int) -> bool:
    """
    Функция для проверки существования в БД пользователя по telegram_id
    :param telegram_id:
    :return: bool:
    """
    async with AsyncSession() as session:
        # Создание запроса на проверку существования
        query = select(exists().where(User.telegram_id == telegram_id))
        result = await session.execute(query)  # Выполнение запроса
        return result.scalar()  # Получение результата (True или False)


async def get_user_by_id(telegram_id: int) -> User:
    """
    Возвращает пользователя по telegram_id
    :param telegram_id:
    :return: user:
    """
    async with AsyncSession() as session:
        query = select(User).where(User.telegram_id == telegram_id)
        result = await session.execute(query)
        user = result.scalar_one_or_none()
        return user


async def update_is_active_user_by_id(telegram_id: int, full_name: str) -> User:
    """
    Возвращает пользователя по telegram_id
    :param telegram_id:
    :param full_name:
    :return: user:
    """
    async with AsyncSession() as session:
        query = select(User).where(User.telegram_id == telegram_id)
        result = await session.execute(query)
        user = result.scalar_one_or_none()
        user.full_name = full_name
        user.is_active = True
        await session.commit()
        await session.refresh(user)
        return user


async def save_user(
        telegram_id: int,
        full_name: str,
        full_name_from_tg: str,
        username: str
) -> None:
    """
    Функция для сохранения пользователя в БД
    :param telegram_id: int:
    :param full_name: str:
    :param full_name_from_tg: str:
    :param username: str:
    :return: None:
    """
    try:
        async with AsyncSession() as session:
            new_user = User(
                telegram_id=telegram_id,
                full_name=full_name,
                full_name_from_tg=full_name_from_tg,
                username=username
            )  # Создаём новый объект User

            session.add(new_user)
            await session.commit()
            logger.info(f"Пользователь {full_name} с ID {telegram_id} успешно добавлен.")

    except SQLAlchemyError as e:
        logger.error(f"Ошибка при добавлении пользователя{full_name} с ID {telegram_id}: {e}")


async def get_lottery_data(name):
    """
    Получить данные о пользователях и билетах для определенной лотереи.
    :param name: Название лотереи.
    :return: Список с данными пользователей и их билетами.
    """
    async with AsyncSession() as session:
        query = (
            select(
                User.telegram_id,
                User.full_name,
                User.full_name_from_tg,
                Lottery.name,
                Ticket.ticket_number
            )
            .select_from(
                join(Ticket, User, Ticket.user_id == User.id)  # Объединение Ticket с User
                .join(Lottery, Ticket.lottery_id == Lottery.id)  # Объединение с Lottery
            ).where(Lottery.name == name)
        )

        # Выполняем запрос
        result = await session.execute(query)

        # Извлекаем все данные
        data = result.fetchall()

        # Преобразуем результат в список словарей
        result_data = [
            {
                "telegram_id": row.telegram_id,
                "full_name": row.full_name,
                "full_name_from_tg": row.full_name_from_tg,
                "lottery_name": row.name,
                "ticket_number": row.ticket_number
            }
            for row in data
        ]
        return result_data
