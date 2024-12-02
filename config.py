from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    API_TELEGRAM_TOKEN: str
    CHANNEL_LINK_MIRAN: str
    CHANNEL_ID_MIRAN: str
    CHANNEL_LINK_REG_BOT: str

    LOTTERY_NAME: str

    DB_USER_PSQL: str
    DB_PASSWORD_PSQL: SecretStr
    DB_HOST_PSQL: str
    DB_PORT_PSQL: int
    DB_DATABASE_PSQL: str

    SMTP_SERVER: str
    PORT: int
    SENDER_EMAIL: str
    PASSWORD: str
    SUBJECT: str
    BODY: str
    TO_EMAIL: str
    TO_EMAILS: str
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


settings = Settings()
