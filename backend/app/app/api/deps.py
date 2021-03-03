from typing import Generator
from app.db.session import SQLAlchemyDBConnection

def get_db() -> Generator:

    with SQLAlchemyDBConnection() as db:
        try:
            yield db.session
        finally:
            db.session.close()
