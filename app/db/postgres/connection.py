from app.core.config import settings
import psycopg2 


class Postgres_Engine:
    def __init__(self):
        self.connection = psycopg2.connect(settings.POSTGRES_URL)
