import pandas as pd

from sqlalchemy.engine import Engine
from gcp import write_to_gcp
from logger import get_logger

logger = get_logger(__name__)


def _read_from_db(con: Engine):
    query = "SELECT * FROM cv"
    query_result = pd.read_sql(query, con)
    return query_result


def _obj_to_file(name: str, dataframe: pd.DataFrame):
    for index, row in dataframe.iterrows():
        aktorid = row["aktorid"]
        jobwishes = row[name]

        for key, value in jobwishes.items():
            if key == "startoption":
                pass

            _list_to_file(key, pd.DataFrame({"aktorid": aktorid, key: value}, index=[0]), "jobwishes")


def _list_to_file(name: str, dataframe: pd.DataFrame, directory: str):
    new_list = []
    for index, row in dataframe.iterrows():
        values = row[name]
        aktorid = row["aktorid"]

        for value in values:
            new_list.append({"aktorid": aktorid, **value})

    new_df = pd.DataFrame(data=new_list)
    logger.info(f"name er ferdig formattert. Klargjør skriving til GCP-bucket")
    write_to_gcp(f"{directory}/{name}", new_df)


def _write_to_files(df):
    personalia = [
        "aktorid",  # type'str'
        "foedselsdato",  # type'datetime.date'
        "postnummer",  # type'str'
        "kommunenr",  # type'str'
        "synligforarbeidsgiver",  # type'numpy.bool_'
        "synligforveileder",  # type'numpy.bool_'
        "hascar",  # type'numpy.bool_'
        "fritattkandidatsok",  # type'str'
        "manuell",  # type'str'
        "erunderoppfolging",  # type'str'
    ]
    write_to_gcp("cv/personalia", df[personalia])
    logger.info("Ferdig med å skrive peronalia til fil")

    lists = [
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
    for name in lists:
        logger.info(f"Formatterer {name} dataframe for skriving")
        _list_to_file(name, df[["aktorid", name]], directory="cv")

    _obj_to_file("jobwishes", df[["aktorid", "jobwishes"]])


def read_write_cv(con: Engine):
    df = _read_from_db(con)
    _write_to_files(df)
