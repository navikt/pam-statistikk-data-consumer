FROM ghcr.io/navikt/baseimages/temurin:21

COPY build/libs/app-1.0-all.jar ./app.jar
EXPOSE 8080
ENV JAVA_OPTS="-XX:-OmitStackTraceInFastThrow -Xms256m -Xmx1536m"
