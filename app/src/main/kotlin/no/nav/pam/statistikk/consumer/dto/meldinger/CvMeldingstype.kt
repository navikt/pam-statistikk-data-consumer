package no.nav.pam.statistikk.consumer.dto.meldinger

import com.fasterxml.jackson.annotation.JsonIgnoreProperties

@JsonIgnoreProperties(ignoreUnknown = true)
enum class CvMeldingstype {
    OPPRETT, ENDRE, SLETT
}
