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

from pprint import pprint

def write_to_files(df):
    def to_file(name: str, aktorids: pd.Series, values: pd.Series):
        new_list = []
        for aktorid in aktorids:
            for personal_values in values:
                for value in personal_values:
                    value["aktorid"] = aktorid
                    new_list.append(value)
        new_df = pd.DataFrame(data=new_list)
        print(new_df.head().to_string())

    main_df = [
        "aktorid",  # type'str'
        "foedselsdato",  # type'datetime.date'
        "postnummer",  # type'str'
        "kommunenr",  # type'str'
        "synligforarbeidsgiver",  # type'numpy.bool_'
        "synligforveileder",  # type'numpy.bool_'
        "hascar",  # type'numpy.bool_'
        "oppfolgingsinformasjon",  # type' obj# type'
    ]
    # make_dummy(oppfolgingsinformasjon)
    # tofile(main_df)


    list_to_file = [
        "otherexperience", # type'list'
        "workexperience", # type'list'
        "courses", # type'list'
        "certificates", # type'list'
        "languages", # type'list'
        "education", # type'list'
        "vocationalcertificates", # type'list'
        "authorizations", # type'list'
        "driverslicenses", # type'list'
        "skills", # type'list'
    ]
    for name in list_to_file:
        to_file(name, df["aktorid"], df[name])



def main():
    connection = connect_with_connector()
    df = read_from_db(connection)
    write_to_files(df)


if __name__ == "__main__":
    logger.info("Starter naisjob")
    main()




    # for (columnName, columnData) in df.items():
    #     index = 0
    #     data = None
    #     while data == None or index == columnData.size - 1:
    #         columnData.iloc[index]
    #         index += 1
    #
    #     print(f"{columnName}: type {type(data)}")

    # for all columns, if list, write to file end pop from df
    # for all objects, make dummy colum