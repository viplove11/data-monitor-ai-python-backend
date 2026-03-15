from fastapi import HTTPException
from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.logging import setup_logging
from app.db_init.create_testdb import initDatabase


setup_logging()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    docs_url="/docs" if settings.ENABLE_DOCS else None,
    redoc_url="/redoc" if settings.ENABLE_DOCS else None,
    openapi_url="/openapi.json" if settings.ENABLE_DOCS else None,
)

app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/", tags=["root"])
def root() -> dict[str, str]:
    return {"message": "hello world"}


@app.get("/database/init-db", tags=["init_database"])
def init_database():
    err = initDatabase()
    if err is not None:
        raise HTTPException(status_code=500, detail=str(err))
    return {"status": "ok"}
