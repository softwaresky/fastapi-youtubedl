import secrets
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn, validator

class Settings(BaseSettings):

    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str
    SQLALCHEMY_DATABASE_URI: Optional[str] = None
    YOUTUBE_DL_DST: Optional[str] = None
    MAXIMUM_QUEUE = 3
    STATIC_FOLDER: Optional[str] = ""

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()