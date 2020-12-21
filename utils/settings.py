from typing import Optional
from pydantic import BaseSettings


class Settings(BaseSettings):
    token: Optional[str]
    prefix: Optional[str]

    class Config:
        case_sensitive = False
        env_file = ".env"
