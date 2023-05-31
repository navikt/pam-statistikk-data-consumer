import json
import os

import pandas.io.sql as psql
from logger import init_app_logging, get_logger
from sqlalchemy import create_engine
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


class Database:
    def __init__(self):
        db_url = os.getenv("DB_URL")
        db_name = os.getenv("DB_DATABASE")

        if "postgres://" in db_url:
            db_url = db_url.replace("postgres://", "postgresql://")

        self.connection_pool = create_engine(db_url, pool_size=1, max_overflow=1)
        self.database_name = db_name

    def execute_query(self, query: str, params=None):
        logger.info(f'Executing query on {self.database_name}')
        result = psql.execute(query, self.connection_pool, params)
        return result

    # Test func
    def select_all(self, table: str = "ettersporsel_i_arbeidsmarkedet"):
        query = f"select * from {table}"
        return self.execute_query(query)

    def upsert(self, data: dict, table: str, primary_key: str):
        columns = [column.lower() for column in data.keys()]
        formatted_values = self.get_formatted_values(data)
        update_set_query_substrings = [f"{col} = EXCLUDED.{col}" for col in columns if col != primary_key]
        placeholders = ["%s" for _ in formatted_values]

        query = f"INSERT INTO {table}({','.join(columns)}) VALUES ({','.join(placeholders)}) " \
                f"ON CONFLICT ({primary_key}) DO UPDATE SET {','.join(update_set_query_substrings)}"

        try:
            self.execute_query(query, tuple(formatted_values))
        except Exception as e:
            logger.error(f"Error when upserting {table} - : {data['aktorId']} - Error: {e}")
            raise e

    def get_formatted_values(self, data):
        return [json.dumps(data[column]) if type(data[column]) in [dict, list]
                else data[column]
                for column in data.keys()
                ]

    def delete_cv(self, aktor_id: str, table: str = "ettersporsel_i_arbeidsmarkedet"):
        query = f"DELETE FROM {table} WHERE aktorid='{aktor_id}'"

        try:
            self.execute_query(query)
        except Exception as e:
            logger.error(f"Error when deleting CV - aktorId: {aktor_id} - Error: {e}")
            raise e
