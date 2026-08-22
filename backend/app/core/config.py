import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Scrape Sentinel AI"
    VERSION: str = "0.1.0"
    API_PREFIX: str = ""
    
    # Environment & URLs
    FRONTEND_URL: str = "http://localhost:5173"
    BACKEND_URL: str = "http://localhost:8000"
    
    # Bright Data Configuration (Placeholders)
    BRIGHT_DATA_API_TOKEN: str = ""
    BRIGHT_DATA_COLLECTOR_ID: str = ""
    
    # Database Configuration (Placeholder)
    DATABASE_URL: str = ""
    
    # AI Service Configuration (Placeholder)
    AI_API_KEY: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
