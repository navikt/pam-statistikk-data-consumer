package no.nav.pam.statistikk.consumer

import no.nav.pam.statistikk.consumer.config.TxContext
import no.nav.pam.statistikk.consumer.config.TxTemplate
import no.nav.pam.statistikk.consumer.dto.meldinger.CvEndretInternDto
import no.nav.pam.statistikk.consumer.dto.meldinger.CvMeldingstype
import org.slf4j.LoggerFactory

class CvService(private val cvRepository: CvRepository, private val txTemplate: TxTemplate) {
    companion object {
        val logger = LoggerFactory.getLogger(CvService::class.java)
    }

    fun lagreCv(cv: CvEndretInternDto, txContext: TxContext? = null) = cvRepository.upsertCv(cv, txContext)

    fun slettCv(aktørId: String, txContext: TxContext? = null) = cvRepository.deleteCv(aktørId, txContext)

    fun behandleCvEndretMeldinger(meldinger: List<CvEndretInternDto>) = txTemplate.doInTransaction { ctx ->
        var slettet = 0
        var endret = 0
        var feilet = 0

        meldinger.forEach {
            val slette = it.meldingstype == CvMeldingstype.SLETT
            val success = if (slette) slettCv(it.aktorId, ctx) else lagreCv(it, ctx)

            if (success) {
                if (slette) slettet++ else endret++
            } else feilet++
        }

        logger.info("Behandlet ${meldinger.size} meldinger - Endret: $endret - Slettet: $slettet - Feilet: $feilet")
    }
}
