package no.nav.pam.statistikk.consumer.kafka

import com.fasterxml.jackson.databind.ObjectMapper
import com.fasterxml.jackson.module.kotlin.readValue
import no.nav.pam.statistikk.consumer.CvService
import no.nav.pam.statistikk.consumer.HealthService
import no.nav.pam.statistikk.consumer.dto.meldinger.CvEndretInternDto
import org.apache.kafka.clients.consumer.ConsumerRecords
import org.apache.kafka.clients.consumer.KafkaConsumer
import org.apache.kafka.common.KafkaException
import org.apache.kafka.common.errors.AuthorizationException
import org.slf4j.LoggerFactory
import java.time.Duration
import kotlin.concurrent.thread

open class KafkaCvEndretListener(
    private val kafkaConsumer: KafkaConsumer<String?, ByteArray>,
    private val cvService: CvService,
    private val objectMapper: ObjectMapper,
    private val healthService: HealthService,
) {
    companion object {
        private val logger = LoggerFactory.getLogger(KafkaCvEndretListener::class.java)
    }

    fun startListener() : Thread {
        return thread { startListenerInternal() }
    }

    private fun startListenerInternal() {
        logger.info("Starter cv-listener")
        var records: ConsumerRecords<String?, ByteArray>?
        while (true) {
            try {
                records = kafkaConsumer.poll(Duration.ofSeconds(10))
                if (records.count() > 0) {
                    logger.info("cv-listener leste ${records.count()} rader.")
                    handleRecords(records!!)
                    kafkaConsumer.commitSync()
                }
            } catch (e: AuthorizationException) {
                logger.error("AuthorizationException i consumerloop, restarter app ${e.message}", e)
                healthService.addUnhealthyVote()
            } catch (ke: KafkaException) {
                logger.error("KafkaException i consumeLoop", ke)
                healthService.addUnhealthyVote()
            } catch (e: Exception) {
                logger.error("Uventet Exception i consumerloop, restarter app ${e.message}", e)
                healthService.addUnhealthyVote()
            }
        }
    }

    fun handleRecords(records: ConsumerRecords<String?, ByteArray>) {
        val cvEndretMeldinger = records.mapNotNull {objectMapper.readValue<CvEndretInternDto>(it.value()) }
        cvService.behandleCvEndretMeldinger(cvEndretMeldinger)
    }
}
