from pathlib import Path

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    DB_URL: str = ''

    class Config:
        env_file = f'{BASE_DIR}/.env'


settings = Settings()
