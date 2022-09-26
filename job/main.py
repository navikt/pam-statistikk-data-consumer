import os

from google.cloud.sql.connector import Connector, IPTypes
import pg8000

import sqlalchemy


def connect_with_connector() -> sqlalchemy.engine.base.Engine:
    project_id = os.environ['GCP_PROJECT']
    db_user = os.environ["DB_USER"]
    db_pass = os.environ["DB_PASS"]
    db_name = os.environ["DB_DATABASE"]

    ip_type = IPTypes.PRIVATE if os.environ.get("PRIVATE_IP") else IPTypes.PUBLIC

    # initialize Cloud SQL Python Connector object
    connector = Connector()

    def getconn() -> pg8000.dbapi.Connection:
        conn: pg8000.dbapi.Connection = connector.connect(
            f"{project_id}:europe-north1:{db_name}",
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
        # ...
    )
    return pool


if __name__ == "__main__":
    connection = connect_with_connector()
