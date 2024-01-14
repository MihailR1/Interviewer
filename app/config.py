import os
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BASEDIR: str = os.path.abspath(os.path.dirname(__file__))
    ENV_FILE_PATH: str = os.path.join(BASEDIR, "..", ".env")

    MODE: Literal["DEV", "TEST", "PROD"]
    LOG_LEVEL: str
    SENTRY_DSN: str

    ACCESS_TOKEN_EXPIRE_DAYS: int
    SECRET_KEY: str
    ALGORITHM: str

    MIN_QUESTION_TITLE_TEXT_LENGTH: int = 15
    MIN_QUESTION_TEXT_LENGTH: int = 15
    SQL_ECHO: bool = True

    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_HOST: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: int
    DB_ENGINE: str = "asyncpg"
    DB_TYPE: str = "postgresql"

    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_USER: str
    TEST_DB_PASS: str
    TEST_DB_NAME: str

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"{self.DB_TYPE}+{self.DB_ENGINE}://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def TEST_DATABASE_URL(self):
        return (
            f"{self.DB_TYPE}+{self.DB_ENGINE}://{self.TEST_DB_USER}:{self.TEST_DB_PASS}@"
            f"{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}"
        )

    model_config = SettingsConfigDict(env_file=ENV_FILE_PATH)


settings = Settings()
