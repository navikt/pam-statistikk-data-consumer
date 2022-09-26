"""
GRANT read-access to statistikk-read-user
"""

from yoyo import step

__depends__ = {'20220922_02_63EOG-rename-foedselsnummer', '__init__'}

steps = [
    step('GRANT SELECT ON ALL TABLES IN SCHEMA public TO "statistikk-read-user"')
]
