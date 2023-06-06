from os import getenv
from pydantic import BaseSettings

class Settings(BaseSettings):
    db_connect_url: str = getenv("DB_CONNECT_URL", default="sqlite:///./test.db")

    class Config:
        env_file = ".env"

settings = Settings()
