import logging
from app.db.session import SQLAlchemyDBConnection

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
    try:
        # Try to create session to check if DB is awake

        with SQLAlchemyDBConnection() as db:
            db.check_db_is_awake()

        # db = SessionLocal()
        # db.execute("SELECT 1")

    except Exception as e:
        logger.error(e)
        raise e


def main() -> None:
    logger.info("Initializing service")
    init()
    logger.info("Service finished initializing")


if __name__ == "__main__":
    main()