from pydantic import BaseSettings

class Settings(BaseSettings):
    db_connect_url: str = "mysql+pymysql://amisroot:vgHNQB0HVxP07iFd3YFO@amis.mysql.database.azure.com/amisdb"

    class Config:
        env_file = ".env"

settings = Settings()
