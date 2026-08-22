from pydantic import BaseModel, Field

class HealthResponse(BaseModel):
    status: str = Field(..., json_schema_extra={"example": "ok"})
    service: str = Field(..., json_schema_extra={"example": "scrape-sentinel-api"})
    version: str = Field(..., json_schema_extra={"example": "0.1.0"})
