import copy
from collections import defaultdict
import pandas as pd

from sqlalchemy.engine import Engine
from gcp import write_to_gcp
from logger import get_logger

logger = get_logger(__name__)

jobwishes_enums_template = {
    "startoption": {"None": False, "LEDIG_NAA": False, "ETTER_TRE_MND": False, "ETTER_AVTALE": False},
    "occupationtypes": {"ENGASJEMENT": False, "FAST": False, "FERIEJOBB": False, "PROSJEKT": False, "SELVSTENDIG_NAERINGSDRIVENDE": False, "SESONG": False, "VIKARIAT": False, "TRAINEE": False, "LAERLING": False, "ANNET": False},
    "worktimes": {"DAGTID": False, "KVELD": False, "NATT": False},
    "workdays": {"LOERDAG": False, "SOENDAG": False, "UKEDAGER": False},
    "workshifttypes": {"SKIFT": False, "TURNUS": False, "VAKT": False},
    "workloadtypes": {"HELTID": False, "DELTID": False}
}


def _read_from_db(con: Engine):
    query = "SELECT * FROM cv"
    query_result = pd.read_sql(query, con)
    return query_result


def _jobwishes_to_file(dataframe: pd.DataFrame):
    formatted_lists = defaultdict(list)

    for index, row in dataframe.iterrows():
        jobwishes_enums = copy.deepcopy(jobwishes_enums_template)
        aktorid = row["aktorid"]
        obj = row["jobwishes"]

        for key, value in obj.items():
            if key.lower() in jobwishes_enums.keys():
                if type(value) is list:
                    for item in value:
                        jobwishes_enums[key.lower()][item] = True
                else:
                    jobwishes_enums[key.lower()][value] = True
            elif value:
                formatted_lists[key.lower()].append({"aktorid": aktorid, key.lower(): value})

        conditions = {"aktorid": aktorid}
        for key, value in jobwishes_enums.items():
            for val_key, enum in value.items():
                conditions[f"{key}_{val_key}"] = enum
        formatted_lists["conditions"].append(conditions)

    for key, value in formatted_lists.items():
        frame = pd.DataFrame(value)
        if key == "conditions":
            write_to_gcp("jobwishes/conditions", frame)
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
