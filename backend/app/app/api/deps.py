from typing import Generator
# from app.db.session import SessionLocal
from app.db.session import SQLAlchemyDBConnection

def get_db() -> Generator:
    try:
        with SQLAlchemyDBConnection() as db:
            yield db.session
    finally:
        db.session.close()