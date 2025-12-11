# app/core/config.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings read from environment variables (.env)."""

    APP_NAME: str = "web-ban-hang"
    DEBUG: bool = False
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
