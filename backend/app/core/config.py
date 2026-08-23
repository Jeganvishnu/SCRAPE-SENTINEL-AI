from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Scrape Sentinel AI"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DATABASE_URL: str
    FRONTEND_URL: str = "http://localhost:5173"

    # AI Configuration (Phase 7)
    AI_PROVIDER: str = "mock"
    AI_MODEL: str = "gpt-4o-mini"
    AI_API_KEY: str = ""
    AI_ENABLED: bool = True
    AI_TIMEOUT_SECONDS: int = 15
    AI_MAX_TOKENS: int = 1000
    AI_PROMPT_VERSION: str = "scrape-sentinel-diagnosis-v1"

    # AI Safety & Thresholds
    AI_HIGH_CONFIDENCE_THRESHOLD: float = 0.85
    AI_MEDIUM_CONFIDENCE_THRESHOLD: float = 0.65
    AI_MAX_REPAIR_ATTEMPTS: int = 3

    class Config:
        env_file = (".env", "../.env")
        extra = "ignore"

settings = Settings()
