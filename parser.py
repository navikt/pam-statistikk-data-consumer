#Nais Application

# 1 kjører konstant
# Hent kafka meldinger
    #consumer #check
# Map til riktig database struktur
    # en funksjon som trekker ut kun det vi vil ha i databasen #check
# koble mapper opp til consumer
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


def getFoedselsdato(fodselsnummer):
    birthdate = fodselsnummer[:6]
    if(int(fodselsnummer[0]) >= 4): #D-nummer
        birthdate = str(int(birthdate) - 400000) # Må trekke fra siden D-nummer
    try:
        return datetime.strptime(birthdate, "%d%m%y").strftime("%Y-%m-%d")
    except:
        return None


def cv_kafka_to_database_mapper(kafka_msg):
    def cv(param):
        return kafka_msg["cv"][param] if "cv" in kafka_msg.keys() and kafka_msg["cv"] is not None else None

    def jobWishes(param):
        return kafka_msg["jobWishes"][param] if "jobWishes" in kafka_msg.keys() and kafka_msg["jobWishes"] is not None else None

    return {
        "aktorId": kafka_msg["aktorId"],
        "fødselsdato": kafka_msg["personalia"]["fodselsnummer"] if "personalia" in kafka_msg.keys() else None,
        "postnummer": kafka_msg["personalia"]["postnummer"] if "personalia" in kafka_msg.keys() else None,
        "kommunenr": kafka_msg["personalia"]["kommunenr"] if "personalia" in kafka_msg.keys() else None,
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
            "occupationTypes": [occupation["title"] for occupation in jobWishes("occupationTypes")],
            "workTimes": [workTime["title"] for workTime in jobWishes("workTimes")],
            "workDays": [workDay["title"] for workDay in jobWishes("workDays")],
            "workShiftTypes": [workShiftType["title"] for workShiftType in jobWishes("workShiftTypes")],
            "workLoadTypes": [workLoadType["title"] for workLoadType in jobWishes("workLoadTypes")],
        }
    }

m_json = b'{"aktorId":"2654345162479","kandidatNr":"PAM0168wvf2io","fodselsnummer":"30817195624","meldingstype":"ENDRE","cv":{"uuid":"a816e128-70ad-4856-ab7e-0eaef415daf8","hasCar":false,"summary":"Kul type 8)","otherExperience":[{"description":"Var Kvakksalver","role":"Kvakksalver","fromDate":"2004-03-01T00:00:00+01:00","toDate":null}],"workExperience":[{"employer":"Ladegutta & Co","jobTitle":"Lader","alternativeJobTitle":null,"conceptId":"103101","location":"Helsingfors","description":null,"fromDate":"2022-03-01T00:00:00+01:00","toDate":null,"styrkkode":"7542","ikkeAktueltForFremtiden":false},{"employer":"Fiskeridirektoratet","jobTitle":"Fiskerir\xc3\xa5d","alternativeJobTitle":"P\xc3\xb8lse","conceptId":"361497","location":"Oslo","description":"D","fromDate":"2021-01-01T00:00:00+01:00","toDate":"2022-02-01T00:00:00+01:00","styrkkode":null,"ikkeAktueltForFremtiden":false}],"courses":[{"title":"Fredriksens p\xc3\xb8lsekurs","issuer":"Fredriksen","duration":34,"durationUnit":"MND","date":"2021-10-17T00:00:00+02:00"}],"certificates":[{"certificateName":"Spikerpistol sertifikat","alternativeName":null,"conceptId":null,"issuer":null,"fromDate":"2021-02-01T00:00:00+01:00","toDate":"2062-01-01T00:00:00+01:00"}],"languages":[{"language":"Afar/Danakil","iso3Code":"aar","oralProficiency":"GODT","writtenProficiency":"FOERSTESPRAAK"},{"language":"Badini (S\xc3\xb8r-\xc3\x98st-Kurdisk)","iso3Code":"kur","oralProficiency":"VELDIG_GODT","writtenProficiency":"NYBEGYNNER"}],"education":[{"institution":"Dasda","field":"Das","nuskode":"4","hasAuthorization":false,"vocationalCollege":null,"startDate":"2021-08-01T00:00:00+02:00","endDate":null,"description":null},{"institution":"Tr\xc3\xa6lleborg skole, T\xc3\xb8nsberg","field":"Dataingeni\xc3\xb8r","nuskode":"2","hasAuthorization":false,"vocationalCollege":null,"startDate":"1998-08-01T00:00:00+02:00","endDate":"2005-06-01T00:00:00+02:00","description":null}],"vocationalCertificates":[{"title":"Fagbrev IKT-servicemedarbeider","certificateType":"SVENNEBREV_FAGBREV"},{"title":"Fagbrev finmekaniker","certificateType":"SVENNEBREV_FAGBREV"}],"authorizations":[{"title":"Truckkontroll\xc3\xb8rbevis","conceptId":"403572","issuer":"Truckgutta","fromDate":"2021-10-17T00:00:00+02:00","toDate":"2027-08-15T00:00:00+02:00"}],"driversLicenses":[{"klasse":"S","description":"Sn\xc3\xb8scooter","acquiredDate":null,"expiryDate":null},{"klasse":"AM","description":"Moped","acquiredDate":null,"expiryDate":null}],"skillDrafts":[],"synligForArbeidsgiver":false,"synligForVeileder":false,"createdAt":"2022-08-02T12:53:16.774377+02:00","updatedAt":"2022-09-20T13:19:01.779754+02:00"},"personalia":{"fornavn":"Real","etternavn":"B\xc3\xb8rste","foedselsdato":"1971-01-30","gateadresse":"Peter Egges vei 17","postnummer":"8019","kommunenr":"1804","poststed":"Bod\xc3\xb8","epost":null,"telefon":null},"jobWishes":{"id":669291,"active":true,"startOption":"ETTER_AVTALE","occupations":[{"title":"Fiskekokk"},{"title":"Fiskerir\xc3\xa5d"}],"occupationDrafts":[],"skills":[{"title":"Fisk"},{"title":"DAB"}],"locations":[{"location":"Oslo","code":"NO03"},{"location":"Rana","code":"NO18.1833"}],"occupationTypes":[{"title":"VIKARIAT"},{"title":"PROSJEKT"}],"workTimes":[],"workDays":[],"workShiftTypes":[{"title":"TURNUS"}],"workLoadTypes":[{"title":"DELTID"},{"title":"HELTID"}],"createdAt":"2022-08-11T10:04:40.834135+02:00","updatedAt":"2022-09-20T13:19:01.666625+02:00"},"updatedBy":"PERSONBRUKER","oppfolgingsinformasjon":null}'
m_dict = json.loads(m_json.decode('utf-8'))

print(cv_kafka_to_database_mapper(m_dict))
#m = {'aktorId': '2535676746622', 'fodselsnummer': '48089598782', 'meldingstype': 'ENDRE', 'cv': {'uuid': '5b09b950-dc7d-4fee-82ca-496007eb4ea0', 'hasCar': False, 'summary': None, 'draft': None, 'otherExperience': [], 'workExperience': [], 'courses': [], 'certificates': [], 'languages': [], 'education': [], 'vocationalCertificates': [{'title': 'Fagbrev blomsterdekoratør', 'conceptId': '60300', 'type': 'SVENNEBREV_FAGBREV', 'createdAt': '2022-07-04T14:40:38+02:00', 'updatedAt': '2022-07-04T14:40:38+02:00'}, {'title': 'Fagbrev aluminiumskonstruktør', 'conceptId': '351208', 'type': 'SVENNEBREV_FAGBREV', 'createdAt': '2022-06-16T15:45:27+02:00', 'updatedAt': '2022-07-01T13:06:38+02:00'}, {'title': 'Fagbrev ambulansearbeider', 'conceptId': '351269', 'type': 'SVENNEBREV_FAGBREV', 'createdAt': '2022-07-01T13:06:49+02:00', 'updatedAt': '2022-07-01T13:06:49+02:00'}, {'title': 'Fagbrev aktivitør', 'conceptId': '350753', 'type': 'SVENNEBREV_FAGBREV', 'createdAt': '2022-06-16T14:57:27+02:00', 'updatedAt': '2022-07-01T13:06:38+02:00'}], 'authorizations': [], 'driversLicenses': [], 'skillDrafts': [], 'lastEditedByNav': False, 'converted': False, 'convertedTimestamp': None, 'createdAt': '2022-06-16T14:48:22.867734+02:00', 'updatedAt': '2022-07-04T14:40:38.459445+02:00'}, 'personalia': {'navn': 'Kantete Hjelm', 'fornavn': 'Kantete', 'etternavn': 'Hjelm', 'gateadresse': 'Mølnhusveien 1', 'postnummer': '9415', 'poststed': 'Harstad', 'epost': None, 'telefon': None, 'opprettetDato': '2022-06-16T14:46:11.041248+02:00', 'sistEndretDato': '2022-06-16T14:46:11.041251+02:00'}, 'jobWishes': {'active': True, 'startOption': 'ETTER_TRE_MND', 'personId': 667905, 'occupations': [{'title': 'Abbed', 'conceptId': 108074, 'styrk08': '2636', 'createdAt': '2022-07-04T14:40:38.308336+02:00', 'updatedAt': '2022-07-04T14:40:38.308337+02:00'}], 'occupationDrafts': [], 'skills': [], 'locations': [{'location': 'Sel', 'code': 'NO34.3437', 'conceptId': 567564, 'createdAt': '2022-07-04T14:40:38.308359+02:00', 'updatedAt': '2022-07-04T14:40:38.308359+02:00'}], 'occupationTypes': [], 'workTimes': [{'title': 'KVELD', 'createdAt': '2022-07-04T14:40:38.308473+02:00', 'updatedAt': '2022-07-04T14:40:38.308473+02:00'}], 'workDays': [], 'workShiftTypes': [], 'workLoadTypes': [{'title': 'HELTID', 'createdAt': '2022-07-04T14:40:38.308491+02:00', 'updatedAt': '2022-07-04T14:40:38.308491+02:00'}, {'title': 'DELTID', 'createdAt': '2022-07-04T14:40:38.308493+02:00', 'updatedAt': '2022-07-04T14:40:38.308493+02:00'}], 'createdAt': '2022-06-16T14:48:22.86901+02:00', 'updatedAt': '2022-07-04T14:40:38.3085+02:00'}, 'updatedBy': 'PERSONBRUKER', 'lastUpdated': '2022-07-04T14:41:11.171166+02:00', 'erUnderOppfolging': False}
#k = cv_kafka_to_database_mapper(m)
#pprint(k)