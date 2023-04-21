from os import getenv
from pydantic import BaseSettings

class Settings(BaseSettings):
    db_connect_url: str = getenv("DB_CONNECT_URL")

    class Config:
        env_file = ".env"

settings = Settings()
