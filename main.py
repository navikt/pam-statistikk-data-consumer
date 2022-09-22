import uvicorn

from api import API
from consumer import create_consumer

from logger import init_app_logging, get_logger
from db.database import run_database_migrations
from processors.cv_processor import CvProcessor

init_app_logging()
logger = get_logger(__name__)

api = API()
app = api.app


consumers = [  # Legg til nye topics her
    {
        "topic": "teampam.cv-endret-intern-v3",
        "group_id": "statistikk-data-consumer-v2",
        "processor": CvProcessor()
    },
]


def main():
    try:
        run_database_migrations()
    except Exception as e:
        logger.error(f'Error while migrating database - {e}. Shutting down')
        return

    try:
        for info in consumers:
            create_consumer(
                topic=info["topic"],
                kafka_group_id=info["group_id"],
                processor=info["processor"],
                api=api
            )
        api.set_ready(True)

    except Exception as e:
        print(f"Application error: {e}")
        logger.error("Application ended")
        logger.error(e)
        api.set_alive(False)

    logger.info("running uvicorn")
    uvicorn.run("main:app", host='0.0.0.0', port=8080, reload=True, debug=True, workers=3)


if __name__ == "__main__":
    main()
