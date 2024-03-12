package no.nav.pam.statistikk.consumer.dto.cv_og_jobb

import com.fasterxml.jackson.annotation.JsonIgnoreProperties
import java.time.ZonedDateTime

@JsonIgnoreProperties(ignoreUnknown = true)
data class CvEndretInternCertificate(
    val certificateName: String?,
    val alternativeName: String?,
    val conceptId: String?,
    val issuer: String?,
    val fromDate: ZonedDateTime?,
    val toDate: ZonedDateTime?,
)
