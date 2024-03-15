package no.nav.pam.statistikk.consumer.dto.cv_og_jobb

import com.fasterxml.jackson.annotation.JsonIgnoreProperties
import java.time.ZonedDateTime

@JsonIgnoreProperties(ignoreUnknown = true)
data class CvEndretInternOtherExperience(
    val role: String?,
    val fromDate: ZonedDateTime?,
    val toDate: ZonedDateTime?,
)
