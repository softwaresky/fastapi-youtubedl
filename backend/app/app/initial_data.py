import logging

from app.db.init_db import init_db
from app.db.session import SQLAlchemyDBConnection

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:

    with SQLAlchemyDBConnection() as db:
        init_db(db.session)


def main() -> None:
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()