from api import API
from consumer import create_consumer

from logger import init_app_logging, get_logger
from db.database import run_database_migrations, Database
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
        db = Database()
    except Exception as e:
        logger.error(f'Error while migrating database - {e}. Shutting down')
        return
    api.set_alive(True)
    try:
        for info in consumers:
            create_consumer(
                topic=info["topic"],
                kafka_group_id=info["group_id"],
                processor=info["processor"],
                api=api,
                db=db
            )
        api.set_ready(True)

    except Exception as e:
        print(f"Application error: {e}")
        logger.error("Application ended")
        logger.error(e)
        api.set_alive(False)

print("toppnivå")
if __name__ == "__main__":
    print("inne i main if")
    main()
