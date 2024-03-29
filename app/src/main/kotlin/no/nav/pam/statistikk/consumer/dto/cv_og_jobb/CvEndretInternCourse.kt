package no.nav.pam.statistikk.consumer.dto.cv_og_jobb

import com.fasterxml.jackson.annotation.JsonIgnoreProperties
import java.time.ZonedDateTime

@JsonIgnoreProperties(ignoreUnknown = true)
data class CvEndretInternCourse(
    val title: String?,
    val issuer: String?,
    val duration: Int?,
    val durationUnit: String?,
    val date: ZonedDateTime?
)
