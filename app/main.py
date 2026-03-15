from fastapi import HTTPException
from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.logging import setup_logging
from app.TEST_DB_API.api import initDatabase
from app.TEST_DB_API.api import print_db
from sqlalchemy import create_engine

import os

db_url = os.getenv('DATABASE_URL', 'mysql+pymysql://root:31415@db:3306/testdb')
engine = create_engine(db_url)

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


@app.get("/database/show", tags=["show"])
def show():
    tables, err = print_db(engine)
    if err is not None:
        raise HTTPException(status_code=500, detail=str(err))
    return {"tables": tables}


@app.get("/database/init-db", tags=["init_database"])
def init_database():
    err = initDatabase(engine)
    if err is not None:
        raise HTTPException(status_code=500, detail=str(err))
    return {"status": "ok"}
