import secrets
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn, validator

class Settings(BaseSettings):

    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str

    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[str] = []

    SQLALCHEMY_DATABASE_URI: Optional[str] = None
    YOUTUBE_DL_DST: Optional[str] = None
    MAXIMUM_QUEUE = 3

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()