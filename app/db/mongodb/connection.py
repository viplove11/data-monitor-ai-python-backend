from app.core.config import settings


def get_mongodb_uri() -> str:
    return settings.MONGODB_URI


def init_mongodb() -> None:
    """Initialize MongoDB client here."""
    _ = get_mongodb_uri()
