package no.nav.pam.statistikk.consumer.dto.cv_og_jobb

import com.fasterxml.jackson.annotation.JsonIgnoreProperties
import java.time.ZonedDateTime
import java.util.*

@JsonIgnoreProperties(ignoreUnknown = true)
data class CvEndretInternCvDto(
    val uuid: UUID? = UUID.randomUUID(),
    val hasCar: Boolean? = false,
    val summary: String? = "",
    val otherExperience: List<CvEndretInternOtherExperience> = emptyList(),
    val workExperience: List<CvEndretInternWorkExperience> = emptyList(),
    val courses: List<CvEndretInternCourse> = emptyList(),
    val certificates: List<CvEndretInternCertificate> = emptyList(),
    val languages: List<CvEndretInternLanguage> = emptyList(),
    val education: List<CvEndretInternEducation> = emptyList(),
    val vocationalCertificates: List<CvEndretInternVocationalCertificate> = emptyList(),
    val authorizations: List<CvEndretInternAuthorization> = emptyList(),
    val driversLicenses: List<CvEndretInternDriversLicence> = emptyList(),
    val skillDrafts: List<CvEndretInternEntity> = emptyList(),
    val synligForArbeidsgiver: Boolean = false, // Dette skal alltid være false (egentlig vært deprecated siden... 2019?)
    val synligForVeileder: Boolean = false, // Dette skal alltid være false (egentlig vært deprecated siden... 2019?)
    val createdAt: ZonedDateTime? = ZonedDateTime.now(),
    val updatedAt: ZonedDateTime? = ZonedDateTime.now()
)
