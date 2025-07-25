package no.nav.pam.statistikk.consumer

import com.fasterxml.jackson.core.JsonGenerator
import com.fasterxml.jackson.databind.DeserializationFeature
import com.fasterxml.jackson.databind.ObjectMapper
import com.fasterxml.jackson.databind.SerializationFeature
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule
import com.fasterxml.jackson.module.kotlin.jacksonObjectMapper
import io.javalin.Javalin
import io.javalin.micrometer.MicrometerPlugin
import io.micrometer.prometheusmetrics.PrometheusConfig
import io.micrometer.prometheusmetrics.PrometheusMeterRegistry
import no.nav.pam.statistikk.consumer.config.DatabaseConfig
import no.nav.pam.statistikk.consumer.config.TxTemplate
import no.nav.pam.statistikk.consumer.kafka.KafkaConfig
import no.nav.pam.statistikk.consumer.kafka.KafkaCvEndretListener
import no.nav.pam.statistikk.consumer.kafka.variable
import org.flywaydb.core.Flyway
import org.slf4j.Logger
import org.slf4j.LoggerFactory

import java.util.*
import javax.sql.DataSource

val defaultObjectMapper: ObjectMapper =
    jacksonObjectMapper().registerModule(JavaTimeModule()).disable(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES)
        .disable(DeserializationFeature.ADJUST_DATES_TO_CONTEXT_TIME_ZONE)
        .disable(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS).setTimeZone(TimeZone.getTimeZone("Europe/Oslo"))
        .enable(JsonGenerator.Feature.IGNORE_UNKNOWN)

fun kjørFlywayMigreringer(dataSource: DataSource) {
    Flyway.configure().loggers("slf4j").baselineOnMigrate(true).dataSource(dataSource).load().migrate()
}

val logger: Logger = LoggerFactory.getLogger(CvService::class.java)

fun main() {
    val env = System.getenv()

    val datasource = DatabaseConfig(env).lagDatasource()
    kjørFlywayMigreringer(datasource)

    val txTemplate = TxTemplate(datasource)
    val cvRepository = CvRepository(defaultObjectMapper, txTemplate)
    val cvService = CvService(cvRepository, txTemplate)

    val prometheusRegistry = PrometheusMeterRegistry(PrometheusConfig.DEFAULT)
    val healthService = HealthService()
    val naisController = NaisController(healthService, prometheusRegistry)

    val topic = env.variable("CV_ENDRET_INTERN_TOPIC")
    val groupId = env.variable("CONSUMER_GROUP_ID")
    val kafkaConsumer = KafkaConfig(env).kafkaConsumer(topic, groupId)
    val kafkaCvEndretListener = KafkaCvEndretListener(kafkaConsumer, cvService, defaultObjectMapper, healthService)

    val javalin = Javalin.create {
        it.registerPlugin(MicrometerPlugin { cfg -> cfg.registry = prometheusRegistry })
        it.router.apiBuilder {
            naisController.setupRoutes()
        }
    }

    javalin.start()
    kafkaCvEndretListener.startListener()
    logger.info("Startet javalin og listeners")
}
