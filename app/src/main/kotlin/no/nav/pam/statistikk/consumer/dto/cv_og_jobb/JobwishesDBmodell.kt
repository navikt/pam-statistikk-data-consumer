package no.nav.pam.statistikk.consumer.dto.cv_og_jobb

class JobwishesDBmodell(
    val startOption: String? = null,
    val occupations: List<CvEndretInternOccupation> = emptyList(),
    val locations: List<CvEndretInternLocation> = emptyList(),
    val occupationTypes: List<CvEndretInternEntity> = emptyList(),
    val workTimes: List<CvEndretInternEntity> = emptyList(),
    val workDays: List<CvEndretInternEntity> = emptyList(),
    val workShiftTypes: List<CvEndretInternEntity> = emptyList(),
    val workLoadTypes: List<CvEndretInternEntity> = emptyList(),
) {
    companion object {
        fun fromCvEndretInternJobwishesDto(jobwishesDto: CvEndretInternJobwishesDto?) = jobwishesDto?.let {
            JobwishesDBmodell(
                it.startOption, it.occupations, it.locations, it.occupationTypes,
                it.workTimes, it.workDays, it.workShiftTypes, it.workLoadTypes
            )
        }
    }
}
