package no.nav.pam.statistikk.consumer

import no.nav.pam.statistikk.consumer.config.TxContext
import no.nav.pam.statistikk.consumer.config.TxTemplate
import no.nav.pam.statistikk.consumer.dto.meldinger.CvEndretInternDto
import no.nav.pam.statistikk.consumer.dto.meldinger.CvMeldingstype.SLETT
import org.slf4j.LoggerFactory

class CvService(private val cvRepository: CvRepository, private val txTemplate: TxTemplate) {
    companion object {
        val logger = LoggerFactory.getLogger(CvService::class.java)
    }

    fun lagreCv(cv: CvEndretInternDto, txContext: TxContext? = null) = cvRepository.upsertCv(cv, txContext)

    fun slettCv(aktørId: String, txContext: TxContext? = null) = cvRepository.deleteCv(aktørId, txContext)

    fun behandleCvEndretMeldinger(meldinger: List<CvEndretInternDto>) = txTemplate.doInTransaction { ctx ->
        var slettet = 0
        var eksistererIkke = 0
        var endret = 0
        var feilet = 0

        meldinger.forEach { cv ->
            when (cv.meldingstype) {
                SLETT -> handleOperation(slettCv(cv.aktorId, ctx), onSuccess = { slettet++ }, onFailure = { eksistererIkke++ })
                else -> handleOperation(lagreCv(cv, ctx), onSuccess = { endret++ }, onFailure = { feilet++ })
            }
        }

        logger.info("Behandlet ${meldinger.size} meldinger - Endret: $endret - Lagring feilet: $feilet - Slettet: $slettet - Slettet CV fantes ikke: $eksistererIkke")
    }

    private fun handleOperation(isSuccess: Boolean, onSuccess: () -> Unit, onFailure: () -> Unit) = if (isSuccess) onSuccess() else onFailure()
}
