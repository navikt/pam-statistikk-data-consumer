package no.nav.pam.statistikk.consumer.dto.meldinger

import com.fasterxml.jackson.annotation.JsonIgnoreProperties
import no.nav.pam.statistikk.consumer.dto.cv_og_jobb.CvEndretInternCvDto
import no.nav.pam.statistikk.consumer.dto.cv_og_jobb.CvEndretInternJobwishesDto
import java.time.ZonedDateTime

@JsonIgnoreProperties(ignoreUnknown = true)
data class CvEndretInternDto(
    val aktorId: String,
    val kandidatNr: String?,
    val fodselsnummer: String?,
    val meldingstype: CvMeldingstype,
    val cv: CvEndretInternCvDto?,
    val personalia: CvEndretInternPersonaliaDto?,
    val jobWishes: CvEndretInternJobwishesDto?,
    val oppfolgingsInformasjon: CvEndretInternOppfolgingsinformasjonDto?,
    val updatedBy: String?,
    val sistEndret: ZonedDateTime?
)
