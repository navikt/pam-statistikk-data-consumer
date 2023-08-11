import os
import sqlalchemy
import pg8000

from google.cloud.sql.connector import Connector, IPTypes


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
        connect_args={'ssl_context': True}
    ).execution_options(stream_results=True)
    return pool
