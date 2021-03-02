from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
import os

db_driver, db_path = settings.SQLALCHEMY_DATABASE_URI.split("///")

if "sqlite" in db_driver:
    db_dir = os.path.dirname(db_path)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
        print (f"Create dir: {db_dir}")

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True, connect_args={"check_same_thread": False})
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class SQLAlchemyDBConnection:

    """SQLAlchemy database connection"""
    def __init__(self, connection_string=""):
        self.connection_string = connection_string if connection_string else settings.SQLALCHEMY_DATABASE_URI
        self.session = None
        self.SessionLocal = None

    def __enter__(self):
        # engine = create_engine(self.connection_string, pool_pre_ping=True, connect_args={"check_same_thread": False})
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        self.session = self.SessionLocal()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

with SQLAlchemyDBConnection() as db:
    SessionLocal = db.SessionLocal