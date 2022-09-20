import os
import uuid
import uvicorn

from api import API
from consumer import Consumer
from logger import init_app_logging, get_logger

from parser import cv_kafka_to_database_mapper

init_app_logging()
logger = get_logger(__name__)

api = API()
app = api.app


def create_consumer(topic: str, kafka_group_id: str, parser):
    return Consumer(
        topic=topic,
        kafka_brokers=os.environ["KAFKA_BROKERS"],
        kafka_ca_path=os.environ["KAFKA_CA_PATH"],
        ssl_certfile=os.environ["KAFKA_CERTIFICATE_PATH"],
        ssl_keyfile=os.environ["KAFKA_PRIVATE_KEY_PATH"],
        kafka_group_id=kafka_group_id,
        kafka_schema_registry=os.environ['KAFKA_SCHEMA_REGISTRY'],
        client_id=kafka_group_id + str(uuid.uuid4().int),
        api=api,
        parser=parser
    )


def get_app():
    try:
        consumer_info = [ # Legg til nye topics her
            {
                "topic": "teampam.cv-endret-intern-v2",
                "group_id": "statistikk-data-consumer-v1",
                "parser": cv_kafka_to_database_mapper
            },
            # {
            #     "topic": "tulletopic",
            #     "group_id": "tulle_group_id",
            #     "parser": tulleparser
            # },
        ]

        consumers = [
            create_consumer(
                topic=info["topic"],
                kafka_group_id=info["group_id"],
                parser=info["parser"]
            ) for info in consumer_info
        ]

    except Exception as e:
        print(f"Application error: {e}")
        logger.error("Application ended")
        logger.error(e)


if __name__ == "__main__":
    logger.info("running uvicorn")
    uvicorn.run("main:app", host='0.0.0.0', port=8080, reload=True, debug=True, workers=3)
    logger.info("uvicorn is running")


