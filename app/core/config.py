from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    POSTGRES_URL: str

    class Config:
        env_file = ".env"

settings = Settings()
