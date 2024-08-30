from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    
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
