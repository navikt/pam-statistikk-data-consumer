package no.nav.pam.statistikk.consumer.dto.cv_og_jobb

import com.fasterxml.jackson.annotation.JsonIgnoreProperties
import java.time.ZonedDateTime

@JsonIgnoreProperties(ignoreUnknown = true)
data class CvEndretInternJobwishesDto(
    val id: Long? = null,
    val active: Boolean? = true,
    val startOption: String? = null,
    val occupations: List<CvEndretInternOccupation> = emptyList(),
    val occupationDrafts: List<CvEndretInternEntity> = emptyList(),
    val skills: List<CvEndretInternSkill> = emptyList(),
    val locations: List<CvEndretInternLocation> = emptyList(),
    val occupationTypes: List<CvEndretInternEntity> = emptyList(),
    val workTimes: List<CvEndretInternEntity> = emptyList(),
    val workDays: List<CvEndretInternEntity> = emptyList(),
    val workShiftTypes: List<CvEndretInternEntity> = emptyList(),
    val workLoadTypes: List<CvEndretInternEntity> = emptyList(),
    val createdAt: ZonedDateTime? = ZonedDateTime.now(),
    val updatedAt: ZonedDateTime? = ZonedDateTime.now(),
)
