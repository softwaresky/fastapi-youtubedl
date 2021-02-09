from sqlalchemy import Column, Integer, String, DateTime, JSON
import datetime
from app.db.base_class import Base


class YdlItem(Base):

    __tablename__ = "ytditem"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String)
    status = Column(Integer)
    timestamp = Column(DateTime, default=datetime.datetime.now)
    ydl_opts = Column(JSON)


