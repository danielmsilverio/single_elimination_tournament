from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    """
    Confs used in application
    """
    API_V1_STR: str = "/api/v1"
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "tournament")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    DB_URL_BASE: str = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432"
    DB_URL: str = f"{DB_URL_BASE}/{POSTGRES_DB}"

    class ConfigDict:
        case_sensitive = True

    
settings = Settings()