package no.nav.pam.statistikk.consumer

import io.javalin.apibuilder.ApiBuilder.get
import io.javalin.http.HttpStatus
import io.micrometer.prometheus.PrometheusMeterRegistry
import io.prometheus.client.exporter.common.TextFormat
import org.slf4j.LoggerFactory
import java.util.concurrent.atomic.AtomicInteger

class NaisController(private val healthService: HealthService, private val prometheusMeterRegistry: PrometheusMeterRegistry) {
    companion object {
        private val logger = LoggerFactory.getLogger(NaisController::class.java)
    }

    fun setupRoutes() {
        get("/internal/isReady") { it.status(200) }
        get("/internal/isAlive") {
            if (healthService.isHealthy()) {
                it.status(HttpStatus.OK)
                logger.info("SVARER OK PÅ ISALIVE")
            } else {
                it.status(HttpStatus.SERVICE_UNAVAILABLE)
                logger.warn("SVARER IKKE OK PÅ ISALIVE")
            }
        }
        get("/internal/prometheus") {
            it.contentType(TextFormat.CONTENT_TYPE_004).result(prometheusMeterRegistry.scrape())
        }
    }
}

class HealthService {
    private val unhealthyVotes = AtomicInteger(0)
    fun addUnhealthyVote() = unhealthyVotes.addAndGet(1)
    fun isHealthy() = unhealthyVotes.get() == 0
}
