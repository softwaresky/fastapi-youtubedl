from typing import Generator
from app.db.session import SessionLocal, db_connection

# def get_db() -> Generator:
#
#     try:
#         db = SessionLocal()
#         yield db
#     finally:
#         db.close()

def get_db() -> Generator:

    with db_connection() as db:
        yield db