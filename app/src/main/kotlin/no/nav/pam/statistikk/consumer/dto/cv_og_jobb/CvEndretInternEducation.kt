package no.nav.pam.statistikk.consumer.dto.cv_og_jobb

import com.fasterxml.jackson.annotation.JsonIgnoreProperties
import java.time.ZonedDateTime

@JsonIgnoreProperties(ignoreUnknown = true)
data class CvEndretInternEducation(
    val institution: String?,
    val field: String?,
    val nuskode: String?,
    val startDate: ZonedDateTime?,
    val endDate: ZonedDateTime?,
)
