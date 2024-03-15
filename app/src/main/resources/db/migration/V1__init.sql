CREATE TABLE IF NOT EXISTS cv(
    aktorId                 VARCHAR(32)     PRIMARY KEY,
    foedselsdato            DATE,
    postnummer              VARCHAR(32),
    kommunenr               VARCHAR(32),
    synligForArbeidsgiver   BOOLEAN,
    synligForVeileder       BOOLEAN,
    hasCar                  BOOLEAN,
    otherExperience         JSON,
    workExperience          JSON,
    courses                 JSON,
    certificates            JSON,
    languages               JSON,
    education               JSON,
    vocationalCertificates  JSON,
    authorizations          JSON,
    driversLicenses         JSON,
    skills                  JSON,
    jobWishes               JSON,
    fritattKandidatsok      BOOLEAN,
    manuell                 BOOLEAN,
    erUnderOppfolging       BOOLEAN
);

create index IF NOT EXISTS cv_aktorid_idx on cv(aktorid);
