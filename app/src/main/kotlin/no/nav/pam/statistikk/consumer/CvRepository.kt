package no.nav.pam.statistikk.consumer

import com.fasterxml.jackson.databind.ObjectMapper
import no.nav.pam.statistikk.consumer.config.TxContext
import no.nav.pam.statistikk.consumer.config.TxTemplate
import no.nav.pam.statistikk.consumer.dto.cv_og_jobb.JobwishesDBmodell.Companion.fromCvEndretInternJobwishesDto
import no.nav.pam.statistikk.consumer.dto.meldinger.CvEndretInternDto
import org.postgresql.util.PGobject

class CvRepository(private val objectMapper: ObjectMapper, private val txTemplate: TxTemplate) {
    fun upsertCv(cvMelding: CvEndretInternDto, txContext: TxContext? = null) =
        txTemplate.doInTransaction(txContext) { ctx ->
            val sql = """
                INSERT INTO cv(
                    aktorid, foedselsdato, postnummer, kommunenr, synligforarbeidsgiver, synligforveileder, hascar, 
                    otherexperience, workexperience, courses, certificates, languages, education, vocationalcertificates, 
                    authorizations, driverslicenses, skills, jobwishes, fritattkandidatsok, manuell, erunderoppfolging
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT (aktorid) DO UPDATE
                SET foedselsdato = EXCLUDED.foedselsdato,
                    postnummer = EXCLUDED.postnummer,
                    kommunenr = EXCLUDED.kommunenr,
                    synligforarbeidsgiver = EXCLUDED.synligforarbeidsgiver,
                    synligforveileder = EXCLUDED.synligforveileder,
                    hascar = EXCLUDED.hascar,
                    otherexperience = EXCLUDED.otherexperience,
                    workexperience = EXCLUDED.workexperience,
                    courses = EXCLUDED.courses,
                    certificates = EXCLUDED.certificates,
                    languages = EXCLUDED.languages,
                    education = EXCLUDED.education,
                    vocationalcertificates = EXCLUDED.vocationalcertificates,
                    authorizations = EXCLUDED.authorizations,
                    driverslicenses = EXCLUDED.driverslicenses,
                    skills = EXCLUDED.skills,
                    jobwishes = EXCLUDED.jobwishes,
                    fritattkandidatsok = EXCLUDED.fritattkandidatsok,
                    manuell = EXCLUDED.manuell,
                    erunderoppfolging = EXCLUDED.erunderoppfolging
            """.trimIndent()

            ctx.connection().prepareStatement(sql).apply {
                this.setString(1, cvMelding.aktorId)
                this.setObject(2, cvMelding.personalia?.foedselsdato)
                this.setString(3, cvMelding.personalia?.postnummer)
                this.setString(4, cvMelding.personalia?.kommunenr)
                this.setObject(5, cvMelding.cv?.synligForArbeidsgiver)
                this.setObject(6, cvMelding.cv?.synligForVeileder)
                this.setObject(7, cvMelding.cv?.hasCar)
                this.setObject(8, objektTilJson(cvMelding.cv?.otherExperience))
                this.setObject(9, objektTilJson(cvMelding.cv?.workExperience))
                this.setObject(10, objektTilJson(cvMelding.cv?.courses))
                this.setObject(11, objektTilJson(cvMelding.cv?.certificates))
                this.setObject(12, objektTilJson(cvMelding.cv?.languages))
                this.setObject(13, objektTilJson(cvMelding.cv?.education))
                this.setObject(14, objektTilJson(cvMelding.cv?.vocationalCertificates))
                this.setObject(15, objektTilJson(cvMelding.cv?.authorizations))
                this.setObject(16, objektTilJson(cvMelding.cv?.driversLicenses))
                this.setObject(17, objektTilJson(cvMelding.jobWishes?.skills))
                this.setObject(18, objektTilJson(fromCvEndretInternJobwishesDto(cvMelding.jobWishes)))
                this.setObject(19, cvMelding.oppfolgingsInformasjon?.fritattKandidatsok)
                this.setObject(20, cvMelding.oppfolgingsInformasjon?.manuell)
                this.setObject(21, cvMelding.oppfolgingsInformasjon?.erUnderOppfolging)
            }.use { statement ->
                return@doInTransaction statement.executeUpdate()
            }
        } > 0

    fun deleteCv(aktørId: String, txContext: TxContext? = null) = txTemplate.doInTransaction(txContext) { ctx ->
        ctx.connection().prepareStatement("DELETE FROM cv WHERE aktorid = ?")
            .apply { this.setString(1, aktørId) }
            .use { return@doInTransaction it.executeUpdate() }
    } > 0

    private fun objektTilJson(objektTilSerialisering: Any?) = PGobject().apply {
        type = "json"
        value = objectMapper.writeValueAsString(objektTilSerialisering)
    }
}
