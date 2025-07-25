import com.github.jengelman.gradle.plugins.shadow.tasks.ShadowJar

plugins {
    kotlin("jvm") version "1.9.21"
    id("com.github.johnrengelman.shadow") version "8.1.1"
    application
}

group = "no.nav.pam.statistikk.consumer"
version = "1.0"

application {
    mainClass.set("no.nav.pam.statistikk.consumer.ApplicationKt")
}

repositories {
    mavenCentral()
}

tasks.test {
    useJUnitPlatform()
    testLogging {
        events("STANDARD_OUT", "PASSED", "FAILED", "SKIPPED")
        exceptionFormat = org.gradle.api.tasks.testing.logging.TestExceptionFormat.FULL
    }
}

tasks.withType<ShadowJar> {
    mergeServiceFiles()
}

kotlin {
    jvmToolchain(21)
}

dependencies {
    implementation(kotlin("stdlib"))
    implementation("io.javalin:javalin:6.7.0")
    implementation("io.javalin:javalin-micrometer:6.7.0")
    implementation("io.micrometer:micrometer-core:1.15.2")
    implementation("io.micrometer:micrometer-registry-prometheus:1.15.2")

    implementation("com.fasterxml.jackson.datatype:jackson-datatype-jsr310:2.19.2")
    implementation("com.fasterxml.jackson.module:jackson-module-kotlin:2.19.2")
    implementation("com.fasterxml.jackson.core:jackson-databind:2.19.2")

    implementation("ch.qos.logback:logback-classic:1.5.18")
    implementation("net.logstash.logback:logstash-logback-encoder:8.1")

    implementation("org.apache.kafka:kafka-clients:3.9.1")

    implementation("org.postgresql:postgresql:42.7.7")
    implementation("com.zaxxer:HikariCP:6.3.0")
    implementation("org.flywaydb:flyway-core:11.10.3")
    implementation("org.flywaydb:flyway-database-postgresql:11.10.3")

    testImplementation("org.jetbrains.kotlin:kotlin-test")
}
