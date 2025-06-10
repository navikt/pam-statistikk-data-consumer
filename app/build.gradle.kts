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
    implementation("io.javalin:javalin:6.1.3")
    implementation("io.javalin:javalin-micrometer:6.1.3")
    implementation("io.micrometer:micrometer-core:1.12.3")
    implementation("io.micrometer:micrometer-registry-prometheus:1.12.3")

    implementation("com.fasterxml.jackson.datatype:jackson-datatype-jsr310:2.16.1")
    implementation("com.fasterxml.jackson.module:jackson-module-kotlin:2.16.1")
    implementation("com.fasterxml.jackson.core:jackson-databind:2.16.1")

    implementation("ch.qos.logback:logback-classic:1.5.3")
    implementation("net.logstash.logback:logstash-logback-encoder:7.4")

    implementation("org.apache.kafka:kafka-clients:3.9.1")

    implementation("org.postgresql:postgresql:42.7.2")
    implementation("com.zaxxer:HikariCP:5.1.0")
    implementation("org.flywaydb:flyway-core:10.9.1")
    implementation("org.flywaydb:flyway-database-postgresql:10.9.1")

    testImplementation("org.jetbrains.kotlin:kotlin-test")
}
