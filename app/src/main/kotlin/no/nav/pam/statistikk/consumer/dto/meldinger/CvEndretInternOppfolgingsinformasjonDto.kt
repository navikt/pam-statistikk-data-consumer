package no.nav.pam.statistikk.consumer.dto.meldinger

import com.fasterxml.jackson.annotation.JsonIgnoreProperties

@JsonIgnoreProperties(ignoreUnknown = true)
data class CvEndretInternOppfolgingsinformasjonDto(
    val formidlingsgruppe: String = "", // Ikke i bruk
    val fritattKandidatsok: Boolean = false, // ikke i bruk
    val hovedmaal: String = "", // Ikke i bruk
    val manuell: Boolean = false,
    val oppfolgingskontor: String = "", // Ikke i bruk
    val servicegruppe: String = "", // Ikke i bruk
    val veileder: String = "", // Ikke i bruk
    val tilretteleggingsbehov: Boolean = false, // Ikke i bruk
    val veilTilretteleggingsbehov: List<String?>? = emptyList(), // Ikke i bruk
    val erUnderOppfolging: Boolean = false
)
