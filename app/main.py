from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.logging import setup_logging
from app.db.postgres.connection import Postgres 
import http
import json

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


# init Postgres , :)
postgres_engine = Postgres()


@app.get("/postgres/", tags=["postgres_root"])
def postgres_root():
    return {"message" : "postgres root"}


#for test not production!!
@app.get("/postgres/init-test", tags=["init_test"])
def init_test():
    err = postgres_engine.init_test()
    if err is not None:
        return {"err" : err.args}
    return {"status" : http.HTTPStatus.OK}

@app.get("/postgres/show-test" , tags=["show_test"])
def show_test():
    entries = postgres_engine.show_test()
    return {"entries" : entries}
