FROM gcr.io/distroless/java21

EXPOSE 8080
ENV JAVA_OPTS="-XX:-OmitStackTraceInFastThrow -Xms256m -Xmx1536m"
COPY app/build/libs/app-1.0-all.jar /app.jar

ENTRYPOINT ["java", "-jar", "/app.jar"]
