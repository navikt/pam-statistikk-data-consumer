from collections import defaultdict
import pandas as pd

from sqlalchemy.engine import Engine
from gcp import write_to_gcp
from logger import get_logger

logger = get_logger(__name__)


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


def _jobwishes_to_file(dataframe: pd.DataFrame, chunk_index: int):
    formatted_lists = defaultdict(list)
    for _, row in dataframe.iterrows():  # pr person
        jobwishes = row["jobwishes"]
        aktorid = row["aktorid"]

        locations = jobwishes.pop("locations")
        formatted_lists["locations"].append({"aktorid": aktorid, "locations": locations})

        occupations = jobwishes.pop("occupations")
        formatted_lists["occupations"].append({"aktorid": aktorid, "occupations": occupations})

        conditions = _get_conditions(jobwishes=jobwishes)
        formatted_lists["conditions"].append({"aktorid": aktorid, **conditions})

    for category, alternatives in formatted_lists.items():  # loc, occup & conditions
        frame = pd.DataFrame(alternatives)
        if category == "conditions":
            write_to_gcp("jobwishes/conditions", frame, chunk_index)
        else:
            _list_to_file(category, frame, "jobwishes", chunk_index)


def _list_to_file(name: str, dataframe: pd.DataFrame, directory: str, chunk_index: int):
    new_list = []

    try:
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
                    logger.error(f"ERROR in list_to_file inner for field {name}: {e}")
    except Exception as e:
        logger.error(f"ERROR in list_to_file outer for field {name}: {e}")
        return

    new_df = pd.DataFrame(data=new_list)
    logger.info(f"{name} er ferdig formattert. Klargjør skriving til GCP-bucket")
    write_to_gcp(f"{directory}/{name}", new_df, chunk_index)


def _write_to_files(df, chunk_index):
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
    write_to_gcp("cv/personalia", df[personalia], chunk_index)
    logger.info("Ferdig med å skrive peronalia til fil")

    lists = [
        "otherexperience",  # type'list'
        "workexperience",  # type'list'
        "courses",  # type'list'
        "certificates",  # type'list'
        "languages",  # type'list'
        "education",  # type'list'
        "vocationalcertificates",  # type'list'
        "authorizations",  # type'list'
        "driverslicenses",  # type'list'
        "skills",  # type'list'
    ]
    for name in lists:
        logger.info(f"Formatterer {name} dataframe for skriving")
        _list_to_file(name, df[["aktorid", name]], directory="cv", chunk_index=chunk_index)

    _jobwishes_to_file(df[["aktorid", "jobwishes"]], chunk_index)


def read_write_cv(con: Engine):
    logger.info("Fetching data from DB")

    index = 1
    for chunk in pd.read_sql("SELECT * FROM cv", con, chunksize=100000):
        logger.info(f"Read chunk #{index} - Processing")
        _write_to_files(chunk, index)
        logger.info(f"Finished processing chunk #{index}")
        index += 1

    logger.info(f"Finished processing {index - 1} chunks")
