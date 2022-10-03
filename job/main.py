from database import connect_with_connector
from logger import init_app_logging, get_logger
from cv import read_write_cv

init_app_logging()
logger = get_logger(__name__)


def main():
    connection = connect_with_connector()
    read_write_cv(con=connection)
    #read_write_stilling


if __name__ == "__main__":
    logger.info("Starter naisjob")
    logger.info("Tester med zero division error for å trigge alert")
    0/0
    main()
