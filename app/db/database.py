import json
import os
from logger import init_app_logging, get_logger

import pandas.io.sql as psql
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.sql import null
from yoyo import read_migrations, get_backend

init_app_logging()
logger = get_logger(__name__)


def run_database_migrations():
    logger.info("Running migrations")
    db_url = os.getenv("DB_URL")
    backend = get_backend(db_url)
    migrations = read_migrations("./db/migrations")
    logger.info(f"Reading migrations: {migrations}")

    with backend.lock():
        backend.apply_migrations(backend.to_apply(migrations))
        logger.info("Migrations applied")


class DatabaseEngine:
    def __init__(self, db_url: str):
        self.db_url = db_url

    def __enter__(self) -> Engine:
        self.engine = create_engine(self.db_url)
        logger.info('Opened connection to the database.')
        return self.engine

    def __exit__(self, exc_type, exc_value, tb):
        self.engine.dispose()
        logger.info('Closed connection to the database.')


class Database:
    def __init__(self):
        db_url = os.getenv("DB_URL")
        db_name = os.getenv("DB_DATABASE")

        if "postgres://" in db_url:
            db_url = db_url.replace("postgres://", "postgresql://")

        self.database_engine = DatabaseEngine(db_url)
        self.database_name = db_name

    def execute_query(self, query: str, params=None):
        logger.info(f'Executing query on {self.database_name}')
        with self.database_engine as engine:
            result = psql.execute(query, engine, params)
        return result

    # Test func
    def select_all(self, table: str = "ettersporsel_i_arbeidsmarkedet"):
        query = f"select * from {table}"
        return self.execute_query(query)

    def upsert(self, data: dict, table: str, primary_key: str):
        columns = [column.lower() for column in data.keys()]
        formatted_values = self.get_formatted_values(data)
        logger.info(formatted_values)
        update_set_query_substrings = [f"{col} = EXCLUDED.{col}" for col in columns if col != primary_key]
        placeholders = ["%s" for _ in formatted_values]

        query = f"INSERT INTO {table}({','.join(columns)}) VALUES ({','.join(placeholders)}) " \
                f"ON CONFLICT ({primary_key}) DO UPDATE SET {','.join(update_set_query_substrings)}"

        try:
            self.execute_query(query, tuple(formatted_values))
        except Exception as e:
            logger.error(f"Error when upserting {table} - : {data[primary_key]} - Error: {e}")
            raise e

    def get_formatted_values(self, data):
        return [
            json.dumps(data[column]) if type(data[column]) is dict
            else data[column] if data[column] is not None
            else null()
            for column in data.keys()
        ]

    def delete_cv(self, aktor_id: str, table: str = "ettersporsel_i_arbeidsmarkedet"):
        query = f"DELETE FROM {table} WHERE aktorid='{aktor_id}'"

        try:
            self.execute_query(query)
        except Exception as e:
            logger.error(f"Error when deleting CV - aktorId: {aktor_id} - Error: {e}")
            raise e
