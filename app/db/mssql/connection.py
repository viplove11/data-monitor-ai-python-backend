from app.core.config import settings


def get_mssql_dsn() -> str:
    return settings.MSSQL_DSN


def init_mssql() -> None:
    """Initialize Microsoft SQL Server engine/pool here."""
    _ = get_mssql_dsn()
