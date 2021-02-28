from sqlalchemy import Column, Integer, String, DateTime, JSON, Boolean
import datetime
from app.db.base_class import Base


class YdlItem(Base):

    __tablename__ = "ytditem"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String)
    do_calculate_pattern = Column(Boolean, default=False)
    status = Column(Integer)
    timestamp = Column(DateTime, default=datetime.datetime.now)
    ydl_opts = Column(JSON)
    output_log = Column(JSON)
    info = Column(JSON)

