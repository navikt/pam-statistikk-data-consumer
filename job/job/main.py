from database import connect_with_connector
from logger import init_app_logging, get_logger
from cv import read_write_cv

init_app_logging()
logger = get_logger(__name__)


def main():
    try:
        connection = connect_with_connector()
        read_write_cv(con=connection)
    except Exception as e:
        logger.error(f"Error during run: {e}")


if __name__ == "__main__":
    logger.info("Starter statistikk-jobb")
    main()
