from app.core.config import settings


def get_oracle_dsn() -> str:
    return settings.ORACLE_DSN


def init_oracle() -> None:
    """Initialize Oracle engine/pool here."""
    _ = get_oracle_dsn()
