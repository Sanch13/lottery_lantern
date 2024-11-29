from sqlalchemy import create_engine

from models.models import Base
from config_params_to_db import get_configuration_psql_db


user, password, host, port, dbname = get_configuration_psql_db().values()

# Создание синхронного движка для PostgreSQL
DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"

# Создание синхронного движка
engine = create_engine(DATABASE_URL, echo=True)


def init_db():
    with engine.begin() as conn:
        conn.run_sync(Base.metadata.create_all)
