from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=True)

    PROJECT_NAME: str = "data-monitor-ai-backend"
    VERSION: str = "0.1.0"
    ENVIRONMENT: str = "development"
    API_V1_PREFIX: str = "/api/v1"

    ENABLE_DOCS: bool = True
    LOG_LEVEL: str = "INFO"

    # Database connection strings
    MYSQL_DSN: str = "mysql+mysqldb://user:password@localhost:3306/app_db"
    ORACLE_DSN: str = "oracle+oracledb://user:password@localhost:1521/?service_name=XE"
    MONGODB_URI: str = "mongodb://localhost:27017/app_db"
    MSSQL_DSN: str = "mssql+pyodbc://user:password@localhost:1433/app_db?driver=ODBC+Driver+18+for+SQL+Server"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
