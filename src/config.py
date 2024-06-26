from pathlib import Path

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    DB_URL: str = ''
    RABBIT_URL: str = ''

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    RABBITMQ_USER: str
    RABBITMQ_PASS: str

    SMTP_USER: str
    SMTP_PASSWORD: str
    SMTP_HOST: str
    SMTP_PORT: int

    class Config:
        env_file = f'{BASE_DIR}/.env'


settings = Settings()
