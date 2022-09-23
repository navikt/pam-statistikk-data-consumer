"""
Create table cv
"""

from yoyo import step

__depends__ = {}

steps = [
    step("CREATE TABLE cv (aktorId VARCHAR(32), fødselsdato DATE, postnummer VARCHAR(32), kommunenr VARCHAR(32), synligForArbeidsgiver BOOLEAN, synligForVeileder BOOLEAN, hasCar BOOLEAN, oppfolgingsinformasjon JSON, otherExperience JSON, workExperience JSON, courses JSON, certificates JSON, languages JSON, education JSON, vocationalCertificates JSON, authorizations JSON, driversLicenses JSON, skills JSON, jobWishes JSON, PRIMARY KEY (aktorId))"),
    step("GRANT ALL ON ALL TABLES IN SCHEMA public TO cloudsqliamuser"),
    # step("GRANT SELECT ON ALL TABLES IN SCHEMA public TO statistikk-read-user")
]
