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

from kafka3.consumer.fetcher import ConsumerRecord
from processors.processor import Processor
from logger import get_logger
logger = get_logger(__name__)


class CvProcessor(Processor):
    def __init__(self):
        super().__init__()

        self._table = "cv"
        self._primary_key = "aktorid"

    def process(self, msg: ConsumerRecord):
        if msg.value["meldingstype"] == "SLETT":
            self.delete_from_db(msg.value["aktorId"])
            return

        parsed_msg = self.parse(msg.value)
        self.insert_to_db(parsed_msg)

    def insert_to_db(self, msg: dict):
        logger.info(f"Upserting CV for aktørId: {msg['aktorId']}")
        self.db.upsert(data=msg, table=self._table, primary_key=self._primary_key)

    def delete_from_db(self, aktor_id: str):
        logger.info(f"Deleting CV for aktørId: {aktor_id}")
        self.db.delete_cv(aktor_id=aktor_id, table=self._table)

    def parse(self, kafka_msg):
        def get_value(parent, child):
            return kafka_msg[parent][child] if parent in kafka_msg.keys() and kafka_msg[parent] is not None else None

        def cv(param):
            return get_value("cv", param)

        def job_wishes(param):
            return get_value("jobWishes", param) or []

        return {
            "aktorId": kafka_msg["aktorId"],
            "foedselsdato": get_value("personalia", "foedselsdato"),
            "postnummer": get_value("personalia", "postnummer"),
            "kommunenr": get_value("personalia", "kommunenr"),
            "fritattKandidatsok": get_value("oppfolgingsinformasjon", "fritattKandidatsok"),
            "manuell": get_value("oppfolgingsinformasjon", "manuell"),
            "erUnderOppfolging": get_value("oppfolgingsinformasjon", "erUnderOppfolging"),
            "synligForArbeidsgiver": cv("synligForArbeidsgiver"),
            "synligForVeileder": cv("synligForVeileder"),
            "hasCar": cv("hasCar"),
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
