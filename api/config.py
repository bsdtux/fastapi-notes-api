import os
from pydantic import BaseSettings

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Settings(BaseSettings):
    DATABASE_PORT: int
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_HOSTNAME: str

    class Config:
        env_file = os.path.join(BASE_DIR, '../.env')


settings = Settings()
