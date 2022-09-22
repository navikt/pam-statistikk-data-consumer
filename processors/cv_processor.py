#Nais Application

# 1 kjører konstant
# Hent kafka meldinger
    #consumer #check
# Map til riktig database struktur
    # en funksjon som trekker ut kun det vi vil ha i databasen #check
# koble mapper opp til consumer #check
    # Er alle datafelter riktige og feiler den på null verdier?
# Dytt inn i database
    # Sett opp oppsett for gcp database
    # Slettemeldinger slettes fra databasen
    # endremeldinger skrives over

# 2, kjører 1 gang om dagen
# Lese fra datbase
    # Gjenbruke oppsett fra å skrive til database?
# Omgjøre til pandas dataframe
    # Funskjon som leser det nogenlunde gode databasen og setter det godt opp i en df
# skriv til fil
    # pandas dataframe til fil
# last opp fil til gcp
    # Gjenbruke oppsettet til database bare med buckets?

import json
from pprint import pprint
from datetime import datetime

from kafka3.consumer.fetcher import ConsumerRecord
from processors.processor import Processor
from logger import get_logger
logger = get_logger(__name__)


class CvProcessor(Processor):
    def __init__(self):
        super().__init__()

        self._table = "cv"
        self._primary_key = "aktorId"

    def process(self, msg: ConsumerRecord):
        if msg.value["meldingstype"] == "SLETT":
            return None

        parsed_msg = self.parse(msg.value)
        logger.info(parsed_msg)

        self.insert_to_db(parsed_msg)

    def insert_to_db(self, msg: dict):
        logger.info(f"upserting {msg['aktorId']}")
        self.db.upsert(data=msg, table=self._table, primary_key=self._primary_key)

    def parse(self, kafka_msg):
        def cv(param):
            return kafka_msg["cv"][param] if "cv" in kafka_msg.keys() and kafka_msg["cv"] is not None else None

        def job_wishes(param):
            return kafka_msg["jobWishes"][param] if "jobWishes" in kafka_msg.keys() and kafka_msg["jobWishes"] is not None else None

        # kafka_msg = json.load(kafka_msg)
        logger.info(kafka_msg)

        return {
            "aktorId": kafka_msg["aktorId"],
            "foedselsdato": kafka_msg["personalia"]["foedselsdato"] if "personalia" in kafka_msg.keys() else None,
            "postnummer": kafka_msg["personalia"]["postnummer"] if "personalia" in kafka_msg.keys() else None,
            "kommunenr": kafka_msg["personalia"]["kommunenr"] if "personalia" in kafka_msg.keys() else None,
            "synligForArbeidsgiver": cv("synligForArbeidsgiver"),
            "synligForVeileder": cv("synligForVeileder"),
            "hasCar": cv("hasCar"),
            "oppfolgingsinformasjon": {
                "fritattKandidatsok": kafka_msg["oppfolgingsinformasjon"]["fritattKandidatsok"],
                "manuell": kafka_msg["oppfolgingsinformasjon"]["manuell"],
                "erUnderOppfolging": kafka_msg["oppfolgingsinformasjon"]["erUnderOppfolging"],
            } if kafka_msg["oppfolgingsinformasjon"] else None,
            "otherExperience": [
                {
                    "role": exp["role"],
                    "fromDate": exp["fromDate"],
                    "toDate": exp["toDate"],
                } for exp in cv("otherExperience")
            ],
            "workExperience": [
                {
                    "jobTitle": exp["jobTitle"],
                    "styrkkode": exp["styrkkode"],
                    "ikkeAktueltForFremtiden": exp["ikkeAktueltForFremtiden"],
                    "conceptId": exp["conceptId"],
                    "alternativeJobTitle": exp["alternativeJobTitle"],
                    "employer": exp["employer"],
                    "location": exp["location"],
                    "fromDate": exp["fromDate"],
                    "toDate": exp["toDate"],
                } for exp in cv("workExperience")
            ],
            "courses": [
                {
                    "title": course["title"],
                    "issuer": course["issuer"],
                    "duration": course["duration"],
                    "durationUnit": course["durationUnit"],
                    "date": course["date"],
                } for course in cv("courses")
            ],
            "certificates": [
                {
                    "certificateName": cert["certificateName"],
                    "alternativeName": cert["alternativeName"],
                    "conceptId": cert["conceptId"],
                    "issuer": cert["issuer"],
                    "fromDate": cert["fromDate"],
                    "toDate": cert["toDate"],
                } for cert in cv("certificates")
            ],
            "languages": [
                {
                    "language": lang["language"],
                    "iso3Code": lang["iso3Code"],
                    "oralProficiency": lang["oralProficiency"],
                    "writtenProficiency": lang["writtenProficiency"],
                } for lang in cv("languages")
            ],
            "education": [
                {
                    "nuskode": edu["nuskode"],
                    "institsution": edu["institution"],
                    "field": edu["field"],
                    "startDate": edu["startDate"],
                    "endDate": edu["endDate"],
                } for edu in cv("education")
            ],
            "vocationalCertificates": [
                {
                    "title": voc["title"],
                    "certificateType": voc["certificateType"],
                    "conceptId": voc["conceptId"],
                } for voc in cv("vocationalCertificates")
            ],
            "authorizations": [
                {
                    "title": auth["title"],
                    "conceptId": auth["conceptId"],
                    "issuer": auth["issuer"],
                    "fromDate": auth["fromDate"],
                    "toDate": auth["toDate"],
                } for auth in cv("authorizations")
            ],
            "driversLicenses": [
                {
                    "klasse": licence["klasse"],
                    "acquiredDate": licence["acquiredDate"],
                    "expiryDate": licence["expiryDate"],
                } for licence in cv("driversLicenses")
            ],
            "skills": [
                {
                    "title": s["title"],
                    "conceptId": s["conceptId"],
                } for s in job_wishes("skills")
            ],
            "jobWishes": {
                "startOption": job_wishes("startOption"),
                "occupations": [
                    {
                        "title": occupation["title"],
                        "conceptId": occupation["conceptId"],
                        "styrk08": occupation["styrk08"],
                    } for occupation in job_wishes("occupations")
                ],
                "locations": [
                    {
                        "location": loc["location"],
                        "code": loc["code"],
                        "conceptId": loc["conceptId"],
                    } for loc in job_wishes("locations")
                ],
                "occupationTypes": [occupation["title"] for occupation in job_wishes("occupationTypes")],
                "workTimes": [workTime["title"] for workTime in job_wishes("workTimes")],
                "workDays": [workDay["title"] for workDay in job_wishes("workDays")],
                "workShiftTypes": [workShiftType["title"] for workShiftType in job_wishes("workShiftTypes")],
                "workLoadTypes": [workLoadType["title"] for workLoadType in job_wishes("workLoadTypes")],
            }
        }
