#Nais Application

# 1 kjører konstant
# Hent kafka meldinger
    #consumer
# Map til riktig database struktur
    # en funksjon som trekker ut kun det vi vil ha i databasen #check
# Dytt inn i database
    # Sett opp oppsett for gcp database

from pprint import pprint;

# 2, kjører 1 gang om dagen
# Lese fra datbase
    # Gjenbruke oppsett fra å skrive til database?
# Omgjøre til pandas dataframe
    # Funskjon som leser det nogenlunde gode databasen og setter det godt opp i en df
# skriv til fil
    # pandas dataframe til fil
# last opp fil til gcp
    # Gjenbruke oppsettet til database bare med buckets?

from datetime import datetime

def getFoedselsdato(fodselsnummer):
    birthdate = fodselsnummer[:6]
    if(int(fodselsnummer[0]) >= 4): #D-nummer
        birthdate = str(int(birthdate) - 400000) # Må trekke fra siden D-nummer 
    return datetime.strptime(birthdate, "%d%m%y").strftime("%Y-%m-%d")



def cv_kafka_to_database_mapper(kafka_msg):

    def cv(param):
        return kafka_msg["cv"][param] if "cv" in kafka_msg.keys() and kafka_msg["cv"] is not None else None

    def jobWishes(param):
        return kafka_msg["jobWishes"][param] if "jobWishes" in kafka_msg.keys() and kafka_msg["jobWishes"] is not None else None

    return {
        "aktorId": kafka_msg["aktorId"],
        "erUnderOppfolging": kafka_msg["erUnderOppfolging"],
        "fødselsdato": getFoedselsdato(kafka_msg["fodselsnummer"]),
        "postnummer": kafka_msg["personalia"]["postnummer"] if "personalia" in kafka_msg.keys() else None,
        "hasCar": cv("hasCar"),
        "otherExperience": [
            {
                "role": exp["role"],
                "fromDate": exp["fromDate"],
                "toDate": exp["toDate"],
                "ongoing": exp["ongoing"]
            } for exp in cv("otherExperience")
        ],
        "workExperience": [
            {
                "jobTitle": exp["jobTitle"],
                "styrkkode": exp["styrkkode"],
                "alternativeJobTitle": exp["alternativeJobTitle"],
                "employer": exp["employer"],
                "location": exp["location"],
                "fromDate": exp["fromDate"],
                "toDate": exp["toDate"],
                "ongoing": exp["ongoing"],
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
                "conceptId": cert["conceptId"],
                "issuer": cert["issuer"],
                "fromDate": cert["fromDate"],
                "toDate": cert["toDate"],
            } for cert in cv("certificates")
        ],
        "languages": [
            {
                "langauge": lang["langauge"],
                "oralProficiency": lang["oralProficiency"],
                "writtenProficiency": lang["writtenProficiency"],
            } for lang in cv("languages")
        ],
        "education": [
            {
                "nuskode": edu["nuskode"],
                "insitution": edu["insitution"],
                "field": edu["field"],
                "startDate": edu["startDate"],
                "endDate": edu["endDate"],
                "ongoing": edu["ongoing"],
            } for edu in cv("education")
        ],
        "vocationalCertificates": [
            {
                "title": voc["title"],
                "conceptId": voc["conceptId"],
                "type": voc["type"],
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
                "type": licence["type"],
                "aquiredDate": licence["aquiredDate"],
                "expiryDate": licence["expiryDate"],
            } for licence in cv("driversLicenses")
        ],
        "skills": [
            {
                "title": s["title"],
                "conceptId": s["conceptId"],
            } for s in jobWishes("skills")      
        ],
        "jobWishes": {
            "startOption": jobWishes("startOption"),
            "occupations": [
                {
                    "title": occupation["title"],
                    "conceptId": occupation["conceptId"],
                    "styrk08": occupation["styrk08"],
                } for occupation in jobWishes("occupations")
            ],
            "locations": [
                {
                    "location": loc["location"],
                    "code": loc["code"],
                    "conceptId": loc["conceptId"],
                } for loc in jobWishes("locations")
            ],
            "occupationTypes": [ occupation["title"]  for occupation in jobWishes("occupationTypes")],
            "workTimes": [ workTime["title"] for workTime in jobWishes("workTimes")],
            "workDays": [ workDay["title"] for workDay in jobWishes("workDays")],
            "workShiftTypes": [ workShiftType["title"] for workShiftType in jobWishes("workShiftTypes")],
            "workLoadTypes": [ workLoadType["title"] for workLoadType in jobWishes("workLoadTypes")],
        }
    }


m = {'aktorId': '2535676746622', 'fodselsnummer': '48089598782', 'meldingstype': 'ENDRE', 'cv': {'uuid': '5b09b950-dc7d-4fee-82ca-496007eb4ea0', 'hasCar': False, 'summary': None, 'draft': None, 'otherExperience': [], 'workExperience': [], 'courses': [], 'certificates': [], 'languages': [], 'education': [], 'vocationalCertificates': [{'title': 'Fagbrev blomsterdekoratør', 'conceptId': '60300', 'type': 'SVENNEBREV_FAGBREV', 'createdAt': '2022-07-04T14:40:38+02:00', 'updatedAt': '2022-07-04T14:40:38+02:00'}, {'title': 'Fagbrev aluminiumskonstruktør', 'conceptId': '351208', 'type': 'SVENNEBREV_FAGBREV', 'createdAt': '2022-06-16T15:45:27+02:00', 'updatedAt': '2022-07-01T13:06:38+02:00'}, {'title': 'Fagbrev ambulansearbeider', 'conceptId': '351269', 'type': 'SVENNEBREV_FAGBREV', 'createdAt': '2022-07-01T13:06:49+02:00', 'updatedAt': '2022-07-01T13:06:49+02:00'}, {'title': 'Fagbrev aktivitør', 'conceptId': '350753', 'type': 'SVENNEBREV_FAGBREV', 'createdAt': '2022-06-16T14:57:27+02:00', 'updatedAt': '2022-07-01T13:06:38+02:00'}], 'authorizations': [], 'driversLicenses': [], 'skillDrafts': [], 'lastEditedByNav': False, 'converted': False, 'convertedTimestamp': None, 'createdAt': '2022-06-16T14:48:22.867734+02:00', 'updatedAt': '2022-07-04T14:40:38.459445+02:00'}, 'personalia': {'navn': 'Kantete Hjelm', 'fornavn': 'Kantete', 'etternavn': 'Hjelm', 'gateadresse': 'Mølnhusveien 1', 'postnummer': '9415', 'poststed': 'Harstad', 'epost': None, 'telefon': None, 'opprettetDato': '2022-06-16T14:46:11.041248+02:00', 'sistEndretDato': '2022-06-16T14:46:11.041251+02:00'}, 'jobWishes': {'active': True, 'startOption': 'ETTER_TRE_MND', 'personId': 667905, 'occupations': [{'title': 'Abbed', 'conceptId': 108074, 'styrk08': '2636', 'createdAt': '2022-07-04T14:40:38.308336+02:00', 'updatedAt': '2022-07-04T14:40:38.308337+02:00'}], 'occupationDrafts': [], 'skills': [], 'locations': [{'location': 'Sel', 'code': 'NO34.3437', 'conceptId': 567564, 'createdAt': '2022-07-04T14:40:38.308359+02:00', 'updatedAt': '2022-07-04T14:40:38.308359+02:00'}], 'occupationTypes': [], 'workTimes': [{'title': 'KVELD', 'createdAt': '2022-07-04T14:40:38.308473+02:00', 'updatedAt': '2022-07-04T14:40:38.308473+02:00'}], 'workDays': [], 'workShiftTypes': [], 'workLoadTypes': [{'title': 'HELTID', 'createdAt': '2022-07-04T14:40:38.308491+02:00', 'updatedAt': '2022-07-04T14:40:38.308491+02:00'}, {'title': 'DELTID', 'createdAt': '2022-07-04T14:40:38.308493+02:00', 'updatedAt': '2022-07-04T14:40:38.308493+02:00'}], 'createdAt': '2022-06-16T14:48:22.86901+02:00', 'updatedAt': '2022-07-04T14:40:38.3085+02:00'}, 'updatedBy': 'PERSONBRUKER', 'lastUpdated': '2022-07-04T14:41:11.171166+02:00', 'erUnderOppfolging': False}
k = cv_kafka_to_database_mapper(m)
pprint(k)