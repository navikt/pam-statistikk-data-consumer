"""
Rename foedselsnummer
"""

from yoyo import step

__depends__ = {'20220922_01_AEqty-create-table-cv'}

steps = [
    step("ALTER TABLE cv RENAME COLUMN fødselsdato TO foedselsdato")
]
