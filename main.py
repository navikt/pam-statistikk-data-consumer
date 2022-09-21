import uvicorn

from api import API
from consumer import create_consumer
from logger import init_app_logging, get_logger

from parsers.cv_parser import cv_kafka_to_database_mapper

init_app_logging()
logger = get_logger(__name__)

api = API()
app = api.app


consumers = [  # Legg til nye topics her
    {
        "topic": "teampam.cv-endret-intern-v3",
        "group_id": "statistikk-data-consumer-v2",
        "parser": cv_kafka_to_database_mapper
    },
]


if __name__ == "__main__":
    logger.info("running uvicorn")
    uvicorn.run("main:app", host='0.0.0.0', port=8080, reload=True, debug=True, workers=3)
    logger.info("uvicorn is running")

    try:
        for info in consumers:
            create_consumer(
                topic=info["topic"],
                kafka_group_id=info["group_id"],
                parser=info["parser"],
                api=api
            )
        api.set_ready(True)

    except Exception as e:
        print(f"Application error: {e}")
        logger.error("Application ended")
        logger.error(e)
        api.set_alive(False)
