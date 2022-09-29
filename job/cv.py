import copy
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


def _get_dummies(enums):
    dummies = {}
    for category, category_enums in enums.items():
        for enum_title, enum_value in category_enums.items():
            dummies[f"{category}_{enum_title}"] = enum_value
    return dummies


def _get_conditions(jobwishes: dict):
    jobwishes_enums = {
        "startoption": {"None": False, "LEDIG_NAA": False, "ETTER_TRE_MND": False, "ETTER_AVTALE": False},
        "occupationtypes": {"ENGASJEMENT": False, "FAST": False, "FERIEJOBB": False, "PROSJEKT": False,
                            "SELVSTENDIG_NAERINGSDRIVENDE": False, "SESONG": False, "VIKARIAT": False, "TRAINEE": False,
                            "LAERLING": False, "ANNET": False},
        "worktimes": {"DAGTID": False, "KVELD": False, "NATT": False},
        "workdays": {"LOERDAG": False, "SOENDAG": False, "UKEDAGER": False},
        "workshifttypes": {"SKIFT": False, "TURNUS": False, "VAKT": False},
        "workloadtypes": {"HELTID": False, "DELTID": False}
    }

    for category, alternatives in jobwishes.items():
        if type(alternatives) is list:
            for item in alternatives:
                jobwishes_enums[category.lower()][item] = True
        else:
            jobwishes_enums[category.lower()][alternatives] = True

    return _get_dummies(jobwishes_enums)


def _jobwishes_to_file(dataframe: pd.DataFrame):
    formatted_lists = defaultdict(list)
    for _, row in dataframe.iterrows():  # pr person
        jobwishes = row["jobwishes"]
        aktorid = row["aktorid"]

        locations = jobwishes.pop("locations")
        formatted_lists["locations"].append({"aktorid": aktorid, "locations": locations})

        occupations = jobwishes.pop("occupations")
        formatted_lists["occupations"].append({"aktorid": aktorid, "occupations": occupations})

        conditions = _get_conditions(jobwishes=jobwishes)
        formatted_lists["conditions"].append({"aktorid": aktorid, "conditions": conditions})

    for category, alternatives in formatted_lists.items(): # loc, occup & conditions
        frame = pd.DataFrame(alternatives)
        if category == "conditions":
            write_to_gcp("jobwishes/conditions", frame)
        else:
            _list_to_file(category, frame, "jobwishes")


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
