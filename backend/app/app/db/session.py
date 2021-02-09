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
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)