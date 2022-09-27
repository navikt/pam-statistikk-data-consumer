"""
Unpack oppfolgingsinformasjon
"""

from yoyo import step

__depends__ = {'20220926_01_OSMfo-grant-read-access-to-statistikk-read-user'}

steps = [
    step("ALTER TABLE cv DROP COLUMN oppfolgingsinformasjon"),
    step("ALTER TABLE cv ADD fritattKandidatsok BOOLEAN, ADD manuell BOOLEAN, ADD erUnderOppfolging BOOLEAN")
]
