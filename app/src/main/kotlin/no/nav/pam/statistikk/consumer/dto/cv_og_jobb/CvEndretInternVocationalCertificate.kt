package no.nav.pam.statistikk.consumer.dto.cv_og_jobb

import com.fasterxml.jackson.annotation.JsonIgnoreProperties

@JsonIgnoreProperties(ignoreUnknown = true)
data class CvEndretInternVocationalCertificate(
    val title: String?,
    val certificateType: String?,
    val conceptId: String?
)
