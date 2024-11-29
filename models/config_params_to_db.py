import os

from dotenv import load_dotenv

load_dotenv()


def get_configuration_psql_db():
    return {
        "user": os.environ.get("DB_USER_PSQL"),
        "password": os.environ.get("DB_PASSWORD_PSQL"),
        "host": os.environ.get("DB_HOST_PSQL"),
        "port": os.environ.get("DB_PORT_PSQL"),
        "dbname": os.environ.get("DB_DATABASE_PSQL")
    }
