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


    POSTGRES_URL: str = os.getenv("POSTGRES_URL", "postgresql://user:pass@pgdb:5432/monitor_db")


settings = Settings()


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
