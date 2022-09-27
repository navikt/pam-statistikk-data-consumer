import asyncio
import os

import pandas as pd
from google.cloud.sql.connector import Connector, IPTypes
import pg8000
import sqlalchemy
from sqlalchemy.engine import Engine

from logger import init_app_logging, get_logger

init_app_logging()
logger = get_logger(__name__)


def connect_with_connector() -> sqlalchemy.engine.base.Engine:
    db_instance = os.environ["DB_INSTANCE"]
    db_user = os.environ["DB_USER"]
    db_pass = os.environ["DB_PASS"]
    db_name = os.environ["DB_NAME"]

    ip_type = IPTypes.PRIVATE if os.environ.get("PRIVATE_IP") else IPTypes.PUBLIC

    # initialize Cloud SQL Python Connector object
    connector = Connector()

    def getconn() -> pg8000.dbapi.Connection:
        conn: pg8000.dbapi.Connection = connector.connect(
            db_instance,
            "pg8000",
            user=db_user,
            password=db_pass,
            db=db_name,
            ip_type=ip_type,
        )
        return conn

    # The Cloud SQL Python Connector can be used with SQLAlchemy
    # using the 'creator' argument to 'create_engine'
    pool = sqlalchemy.create_engine(
        "postgresql+pg8000://",
        creator=getconn,
    )
    return pool


def read_from_db(con: Engine):
    query = "SELECT * FROM cv"
    query_result = pd.read_sql(query, con)
    return query_result
    # logger.info(query_result)
    # logger.info(query_result.to_csv(index=False))
    # print(query_result.to_csv(index=False))

import ast

def write_to_files(df):
    for (columnName, columnData) in df.items():
        try:
            k = ast.literal_eval(columnData)
            print({"name": columnName, "type": type(k)})
        except:
            print(f"except: {columnName} : type {type(columnData)}")

    # for all columns, if list, write to file end pop from df
    # for all objects, make dummy columns
    # write df to file

def main():
    connection = connect_with_connector()
    df = read_from_db(connection)
    write_to_files(df)


if __name__ == "__main__":
    logger.info("Starter naisjob")
    main()
