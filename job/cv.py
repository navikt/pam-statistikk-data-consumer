from collections import defaultdict
import pandas as pd

from sqlalchemy.engine import Engine
from gcp import write_to_gcp
from logger import get_logger

logger = get_logger(__name__)


def _read_from_db(con: Engine):
    query = "SELECT * FROM cv"
    query_result = pd.read_sql(query, con)
    return query_result


def _jobwishes_to_file(dataframe: pd.DataFrame):
    formatted_lists = defaultdict(list)

    for index, row in dataframe.iterrows():
        aktorid = row["aktorid"]
        obj = row["jobwishes"]

        for key, value in obj.items():
            if value:
                formatted_lists[key.lower()].append({"aktorid": aktorid, key.lower(): value})

    for key, value in formatted_lists.items():
        frame = pd.DataFrame(value)
        if key == "startoption":
            write_to_gcp("jobwishes/startoption", frame)
        else:
            _list_to_file(key, frame, "jobwishes")


def _list_to_file(name: str, dataframe: pd.DataFrame, directory: str):
    new_list = []
    for index, row in dataframe.iterrows():
        values = row[name]
        aktorid = row["aktorid"]

        for value in values:
            try:
                if type(value) in (list, dict):
                    new_list.append({"aktorid": aktorid, **value})
                else:
                    new_list.append({"aktorid": aktorid, name: value})
            except Exception as e:
                logger.info(f"Value: {value} - ERROR: {e}")

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

    _jobwishes_to_file(df[["aktorid", "jobwishes"]])


def read_write_cv(con: Engine):
    df = _read_from_db(con)
    _write_to_files(df)
