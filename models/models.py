from datetime import datetime

from sqlalchemy.orm import declarative_base
from sqlalchemy import (
    Column,
    Integer,
    String,
    BigInteger,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    Boolean
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


Base = declarative_base()  # Создание базового класса для моделей


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, index=True)
    telegram_id = Column(BigInteger, unique=True, index=True)
    full_name = Column(String, default='')
    full_name_from_tg = Column(String, default='')
    username = Column(String, default='')
    is_active = Column(Boolean, default=True, nullable=False)

    # Связь с Ticket
    tickets = relationship("Ticket", back_populates="user")


class Lottery(Base):
    __tablename__ = "lotteries"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(String, default='')  # Описание лотереи
    create = Column(DateTime, default=func.now())  # время будет получено непосредственно из базы
    # данных

    # Связь с Ticket
    tickets = relationship("Ticket", back_populates="lottery")


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(BigInteger, primary_key=True, index=True)
    ticket_number = Column(Integer, nullable=False)  # Номер билета
    create = Column(DateTime, default=datetime.utcnow)  # Дата выдачи билета
    lottery_id = Column(BigInteger, ForeignKey('lotteries.id'))  # Ссылка на лотерею
    user_id = Column(BigInteger, ForeignKey('users.id'))  # Ссылка на пользователя

    lottery = relationship("Lottery", back_populates="tickets")
    user = relationship("User", back_populates="tickets")

    __table_args__ = (
        UniqueConstraint('user_id', 'lottery_id', name='unique_ticket_per_lottery'),
    )
