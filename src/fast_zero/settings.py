from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
    )
    DB_USER:str = Field(init=False)
    DB_PASSWORD:str = Field(init=False)
    DB_HOST: str = Field(init=False)
    DB_PORT:int = Field(init=False)
    DB_NAME:str = Field(init=False)
    SECRET_KEY: str = Field(init=False)
    ALGORITHM: str = Field(init=False)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(init=False)
