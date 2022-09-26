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
    logger.info(query_result)
    logger.info(query_result.to_csv(index=False))
    print(query_result.to_csv(index=False))


def main():
    connection = connect_with_connector()
    read_from_db(connection)


if __name__ == "__main__":
    logger.info("Starter naisjob")
    main()
