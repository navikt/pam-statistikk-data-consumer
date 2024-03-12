package no.nav.pam.statistikk.consumer

import no.nav.pam.statistikk.consumer.config.TxContext
import no.nav.pam.statistikk.consumer.config.TxTemplate
import no.nav.pam.statistikk.consumer.dto.meldinger.CvEndretInternDto
import no.nav.pam.statistikk.consumer.dto.meldinger.CvMeldingstype

class CvService(private val cvRepository: CvRepository, private val txTemplate: TxTemplate) {
    fun lagreCv(cv: CvEndretInternDto, txContext: TxContext? = null) = cvRepository.upsertCv(cv, txContext)

    fun slettCv(aktørId: String, txContext: TxContext? = null) = cvRepository.deleteCv(aktørId, txContext)

    fun behandleCvEndretMeldinger(meldinger: List<CvEndretInternDto>) = txTemplate.doInTransaction { ctx ->
        meldinger.forEach {
            if (it.meldingstype == CvMeldingstype.SLETT) slettCv(it.aktorId, ctx)
            else lagreCv(it, ctx)
        }
    }
}
