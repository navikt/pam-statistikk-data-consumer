# pam-statistikk-data-consumer

Denne applikasjonen er todelt i en consumer-applikasjon og en cron-job.
Consumer-applikasjonen lytter til kafkatopics, spesielt cv-endret-intern og skriver meldingene videre til en postgress-db i et dataminimimalisert format for brukt til statistikk. Grunnen til at den skriver til en db er pga CRUD funksjonenen. BigQuery var vurdert, men siden den er en append only db var det vanskelig å gjør endringer spesielt for cv data når personbrukere oppdataterer dataen sin.

Nais-job "pam.statistikk-nais.job" har som oppgave å lese fra databasen og skrive den til csv filer i gcp bucket. Dette er begrunnet med at jobben kjører daglig og skaper derfor historiske data og at csv er lettere for statistikse programmer å håndtere enn en sql db som inneholder noen JSON elementer.