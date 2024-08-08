import os
from pydantic_settings import BaseSettings, SettingsConfigDict

DOTENV = os.path.join(os.path.dirname(__file__), ".env")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=DOTENV, env_file_encoding="utf-8")
    
    db_username: str
    db_password: str
    db_hostname: str
    db_name: str
    db_port: int
    db_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int


settings = Settings()
