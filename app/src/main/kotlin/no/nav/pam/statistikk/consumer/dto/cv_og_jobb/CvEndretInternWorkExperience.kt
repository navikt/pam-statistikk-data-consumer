package no.nav.pam.statistikk.consumer.dto.cv_og_jobb

import com.fasterxml.jackson.annotation.JsonIgnoreProperties
import java.time.ZonedDateTime

@JsonIgnoreProperties(ignoreUnknown = true)
data class CvEndretInternWorkExperience(
    val employer: String?,
    val jobTitle: String?,
    val alternativeJobTitle: String?,
    val conceptId: String?,
    val location: String?,
    val fromDate: ZonedDateTime?,
    val toDate: ZonedDateTime?,
    val styrkkode: String?,
    val ikkeAktueltForFremtiden: Boolean,
)
