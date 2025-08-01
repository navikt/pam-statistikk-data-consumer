package no.nav.pam.statistikk.consumer

import io.javalin.apibuilder.ApiBuilder.get
import io.javalin.http.HttpStatus
import io.micrometer.prometheusmetrics.PrometheusMeterRegistry
import java.util.concurrent.atomic.AtomicInteger

class NaisController(
    private val healthService: HealthService,
    private val prometheusMeterRegistry: PrometheusMeterRegistry
) {
    fun setupRoutes() {
        get("/internal/isReady") { it.status(200) }
        get("/internal/isAlive") {
            if (healthService.isHealthy()) it.status(HttpStatus.OK)
            else it.status(HttpStatus.SERVICE_UNAVAILABLE)

        }
        get("/internal/prometheus") {
            it.contentType("text/plain; version=0.0.4; charset=utf-8").result(prometheusMeterRegistry.scrape())
        }
    }
}

class HealthService {
    private val unhealthyVotes = AtomicInteger(0)
    fun addUnhealthyVote() = unhealthyVotes.addAndGet(1)
    fun isHealthy() = unhealthyVotes.get() == 0
}
