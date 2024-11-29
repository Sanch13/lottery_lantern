from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from models.config_params_to_db import get_configuration_psql_db


user, password, host, port, dbname = get_configuration_psql_db().values()

# Создание асинхронного движка для PostgreSQL
DATABASE_URL = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{dbname}"

engine = create_async_engine(DATABASE_URL, echo=True)
# Если echo=True, то все SQL-запросы, которые выполняются, будут выводиться в консоль.
# Это полезно для отладки, чтобы видеть, какие запросы отправляются в базу данных

AsyncSession = sessionmaker(bind=engine, class_=AsyncSession)
# class_=AsyncSession — указывает, что создаваемые сессии должны быть асинхронными:
# AsyncSession — это асинхронная версия Session в SQLAlchemy, которая позволяет использовать await
# для асинхронного выполнения запросов.
