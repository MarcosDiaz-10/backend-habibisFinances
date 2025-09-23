from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    USER_DB : str
    PASSWORD_DB : str
    HOST_DB : str
    PORT_DB : int 
    DB_NAME : str
    DB_POOL_MIN_SIZE: int
    DB_POOL_MAX_SIZE: int
    SECRET_KEY: str
    ALGORITHM_TOKEN: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    model_config = SettingsConfigDict(env_file=".env")


@lru_cache()
def getSettings() -> Settings:
    return Settings()
