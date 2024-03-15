package no.nav.pam.statistikk.consumer.dto.cv_og_jobb

import com.fasterxml.jackson.annotation.JsonIgnoreProperties
import java.time.ZonedDateTime

@JsonIgnoreProperties(ignoreUnknown = true)
data class CvEndretInternDriversLicence(
    val klasse: String?,
    val acquiredDate: ZonedDateTime?,
    val expiryDate: ZonedDateTime?
)
