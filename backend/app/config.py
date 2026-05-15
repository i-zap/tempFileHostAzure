import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    AZURE_STORAGE_CONNECTION_STRING: str
    CONTAINER_NAME: str = "tempfiles"
    # Default expiry in minutes
    DEFAULT_EXPIRY_MINS: int = 30
    MAX_EXPIRY_MINS: int = 180
    MAX_FILE_SIZE_BYTES: int = 1024 * 1024  # 1MB
    BASE_URL: str = "http://13.127.153.237"

    class Config:
        env_file = ".env"

settings = Settings()
