from functools import lru_cache
import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "data-monitor-ai-backend"
    VERSION: str = "0.1.0"
    ENVIRONMENT: str = "development"
    API_V1_PREFIX: str = "/api/v1"

    ENABLE_DOCS: bool = True
    LOG_LEVEL: str = "INFO"


    POSTGRES_URL  : str = os.getenv("POSTGRES_URL").__str__()
    POSTGRES_HOST : str = os.getenv("POSTGRES_HOST")
    POSTGRES_USER : str = os.getenv("POSTGRES_USER")
    POSTGRES_PASS : str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DATABASE : str = os.getenv("POSTGRES_DB")
    POSTGRES_PORT : str = "5433"


settings = Settings()


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
