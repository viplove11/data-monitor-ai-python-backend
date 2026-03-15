from app.core.config import settings


def get_mysql_dsn() -> str:
    return settings.MYSQL_DSN


def init_mysql() -> None:
    """Initialize MySQL engine/pool here."""
    _ = get_mysql_dsn()
