import os
import psycopg2
from psycopg2.extensions import connection as pg_conn, cursor as pg_cursor
from app.faker.fakerdefs import setup_schema, generate_data
from app.core.logging import LogError

class Postgres:
    connection: pg_conn
    cursor: pg_cursor

    def __init__(self):
        db_url = os.getenv("POSTGRES_URL")
        if not db_url:
            raise ValueError("POSTGRES_URL environment variable is missing.")
            
        self.connection = psycopg2.connect(db_url)
        self.cursor = self.connection.cursor()

    def __del__(self):
        if hasattr(self, 'cursor') and self.cursor and not self.cursor.closed:
            self.cursor.close()
        if hasattr(self, 'connection') and self.connection and not self.connection.closed:
            self.connection.close()

    def init_test(self):
        try:
            setup_schema(self.cursor)
            generate_data(self.cursor)
            return None
        except Exception as err:
            self.connection.rollback()
            return err

    def show_test(self):
        try:
            query = """
                SELECT tablename 
                FROM pg_catalog.pg_tables 
                WHERE schemaname != 'pg_catalog' 
                AND schemaname != 'information_schema';
            """

            self.cursor.execute(query)
            tables = self.cursor.fetchall()
            entries = {}
            for table in tables:
                query = f" SELECT * FROM {table[0]}"
                self.cursor.execute(query)
                entry = self.cursor.fetchall()
                entries[table[0]] = entry
            return entries

        except Exception as err:
            self.connection.rollback()
            LogError(err)
            return None
