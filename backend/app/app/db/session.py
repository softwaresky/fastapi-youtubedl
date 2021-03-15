from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from contextlib import contextmanager
import os
import logging

logger = logging.getLogger("Session")

db_driver, db_path = settings.SQLALCHEMY_DATABASE_URI.split("///")

if "sqlite" in db_driver:
    db_dir = os.path.dirname(db_path)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
        logger.info(f"Created dir: {db_dir}")

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
logger.info(f"Created engine: {engine}")

@contextmanager
def db_connection():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
