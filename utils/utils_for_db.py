from sqlalchemy import exists, join
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from models.database import AsyncSession, SessionLocal
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


async def get_user_by_telegram_id(telegram_id: int) -> User:
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


async def check_user_ticket(telegram_id: int, lottery_name: str):
    """
    Проверяет есть ли уже билет у пользователя в текущей лотерее
    """
    async with AsyncSession() as session:
        query = (
            select(Ticket)
            .join(Ticket.lottery)
            .join(Ticket.user)
            .where(Lottery.name == lottery_name, User.telegram_id == telegram_id)
        )
        result = await session.execute(query)  # Выполнение запроса
        ticket = result.scalars().first()
        return ticket is not None


async def get_lottery_by_name(lottery_name: str):
    """
    Возвращает объект лотереи по имени
    """
    async with AsyncSession() as session:
        query_lottery = select(Lottery).filter(Lottery.name == lottery_name)
        result_lottery = await session.execute(query_lottery)
        lottery = result_lottery.scalar_one_or_none()
        return lottery


async def create_ticket(telegram_id: int, lottery_name: str):
    """
    Сохраняет и возвращает билет определенного пользователя в определенной лотереи
    """
    async with AsyncSession() as session:
        lottery = await get_lottery_by_name(lottery_name=lottery_name)
        user = await get_user_by_telegram_id(telegram_id=telegram_id)

        query_ticket = select(Ticket).filter(Ticket.lottery_id == lottery.id).order_by(
            Ticket.ticket_number.desc()).limit(1)
        result_ticket = await session.execute(query_ticket)
        max_ticket = result_ticket.scalar_one_or_none()

        # Начинаем с 100, если нет билетов
        next_ticket_number = 100 if not max_ticket else max_ticket.ticket_number + 1

        # Создаём новый билет
        new_ticket = Ticket(user_id=user.id, lottery_id=lottery.id, ticket_number=next_ticket_number)
        session.add(new_ticket)
        await session.commit()
        await session.refresh(new_ticket)

    return f"{next_ticket_number}"

##############################################################################################
# Этот подход возвращает только булево значение и может быть быстрее, если нет необходимости
# загружать сам объект билета.
#
# async def check_user_ticket(session: AsyncSession, telegram_id: int, lottery_name: str) -> bool:
#     query = (
#         select(exists().where(
#             Ticket.user.has(telegram_id=telegram_id),
#             Ticket.lottery.has(name=lottery_name)
#         ))
#     )
#     result = await session.execute(query)
#     return result.scalar()
##############################################################################################


def create_lottery(session: SessionLocal, name: str, description: str = ''):
    """
    Создает объект лотереи
    """
    try:
        lottery = Lottery(name=name, description=description)
        session.add(lottery)
        session.commit()
        session.refresh(lottery)  # Обновление объекта для получения ID и других данных
        return {"success": True, "lottery": lottery}
    except IntegrityError:
        session.rollback()  # Откат изменений в случае ошибки
        return {"success": False, "error": "Лотерея с таким именем уже существует."}
