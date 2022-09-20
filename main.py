import os
import uuid
import uvicorn

from consumer_app import ConsumerApp
from logger import init_app_logging, get_logger

init_app_logging()
logger = get_logger(__name__)




def get_app():
    try:
        app = ConsumerApp(
            topic="teampam.cv-endret-intern-v2",
            kafka_brokers=os.environ["KAFKA_BROKERS"],
            kafka_ca_path=os.environ["KAFKA_CA_PATH"],
            ssl_certfile=os.environ["KAFKA_CERTIFICATE_PATH"],
            ssl_keyfile=os.environ["KAFKA_PRIVATE_KEY_PATH"],
            kafka_group_id="statistikk-data-consumer-v1",
            kafka_schema_registry=os.environ['KAFKA_SCHEMA_REGISTRY'],
            client_id="pam-markedsinnsikt-datastory-consumer-" + str(uuid.uuid4().int)
        )
        return app.app

    except Exception as e:
        print(f"Application error: {e}")
        logger.error("Application ended")
        logger.error(e)


app = get_app()

if __name__ == "__main__":

    logger.info("running uvicorn")
    uvicorn.run("main:app", host='0.0.0.0', port=8080, reload=True, debug=True, workers=3)
    logger.info("uvicorn is running")


