from typing import Optional
import datetime
from pydantic import BaseModel


# Shared properties
class YdlItemBase(BaseModel):
    url: Optional[str]
    do_calculate_pattern: Optional[bool] = False
    ydl_opts: Optional[dict]
    status: Optional[int] = 1
    info: Optional[dict] = {}

# Properties to receive on YdlItem creation
class YdlItemCreate(YdlItemBase):
    pass


# Properties to receive on YdlItem update
class YdlItemUpdate(YdlItemBase):
    pass


# Properties shared by models stored in DB
class YdlItemInDBBase(YdlItemBase):
    id: int
    url: Optional[str]
    ydl_opts: Optional[dict]
    output_log: Optional[dict]
    timestamp: Optional[datetime.datetime]
    status: Optional[int]

    class Config:
        orm_mode = True


# Properties to return to client
class YdlItem(YdlItemInDBBase):
    pass


# Properties properties stored in DB
class YdlItemInDB(YdlItemInDBBase):
    pass


class YdlUrl(BaseModel):
    url: str = ""
    ydl_opts: Optional[dict] = {}
