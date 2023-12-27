import os

import pytz
from pydantic_settings import BaseSettings, SettingsConfigDict
from pytz.tzinfo import DstTzInfo


class Settings(BaseSettings):
    LOG_LEVEL: str = "INFO"
    TIMEZONE: DstTzInfo = pytz.timezone("Europe/Moscow")

    MIN_QUESTION_TITLE_TEXT_LENGTH: int = 15
    MAX_QUESTION_TITLE_TEXT_LENGTH: int = 500
    MIN_QUESTION_TEXT_LENGTH: int = 15
    MAX_QUESTION_TEXT_LENGTH: int = 500

    BASEDIR: str = os.path.abspath(os.path.dirname(__file__))
    ENV_FILE_PATH: str = os.path.join(BASEDIR, "..", ".env")

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    REDIS_HOST: str
    REDIS_PORT: int

    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_HOST: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: int
    DB_ENGINE: str = "asyncpg"
    DB_TYPE: str = "postgresql"

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"{self.DB_TYPE}+{self.DB_ENGINE}://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    model_config = SettingsConfigDict(env_file=ENV_FILE_PATH)


settings = Settings()
