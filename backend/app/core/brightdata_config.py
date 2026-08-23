import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class BrightDataSettings(BaseSettings):
    BRIGHTDATA_API_KEY: Optional[str] = None
    BRIGHT_DATA_API_KEY: Optional[str] = None
    BRIGHT_DATA_API_TOKEN: Optional[str] = None
    BRIGHT_DATA_COLLECTOR_ID: Optional[str] = "c_mt46lngz2asqzj8tkj"
    BRIGHTDATA_TIMEOUT_SECONDS: int = 120

    model_config = SettingsConfigDict(
        env_file=(".env", "../.env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @property
    def api_key(self) -> Optional[str]:
        return (
            self.BRIGHTDATA_API_KEY or
            self.BRIGHT_DATA_API_KEY or
            self.BRIGHT_DATA_API_TOKEN or
            os.getenv("BRIGHTDATA_API_KEY") or
            os.getenv("BRIGHT_DATA_API_KEY") or
            os.getenv("BRIGHT_DATA_API_TOKEN")
        )

    def validate_config(self) -> None:
        """Validates that essential collector configurations exist without logging secrets."""
        if not self.BRIGHT_DATA_COLLECTOR_ID:
            raise ValueError("BRIGHT_DATA_COLLECTOR_ID is not configured in environment or .env file.")

brightdata_settings = BrightDataSettings()
