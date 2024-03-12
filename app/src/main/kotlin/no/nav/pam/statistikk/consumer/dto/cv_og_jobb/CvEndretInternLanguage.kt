package no.nav.pam.statistikk.consumer.dto.cv_og_jobb

import com.fasterxml.jackson.annotation.JsonIgnoreProperties

@JsonIgnoreProperties(ignoreUnknown = true)
data class CvEndretInternLanguage(
    val language: String?,
    val iso3Code: String?,
    val oralProficiency: String?,
    val writtenProficiency: String?
)
