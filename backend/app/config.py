import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    AZURE_STORAGE_CONNECTION_STRING: str
    CONTAINER_NAME: str = "tempfiles"
    # Default expiry in minutes
    DEFAULT_EXPIRY_MINS: int = 30
    MAX_EXPIRY_MINS: int = 180
    BASE_DOMAIN: str = "upload.izap.fun"

    class Config:
        env_file = ".env"

settings = Settings()
