import logging
from logging.config import dictConfig

from app.core.config import settings

import datetime as datetime

def LogError(err):
    print(f"ERROR:\t{datetime.datetime.now()} : {err} ")



def setup_logging() -> None:
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                }
            },
            "root": {
                "level": settings.LOG_LEVEL,
                "handlers": ["console"],
            },
        }
    )

    logging.getLogger(__name__).info("Logging initialized")
