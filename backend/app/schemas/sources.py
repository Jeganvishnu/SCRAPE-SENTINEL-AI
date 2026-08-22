from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict

class SourceCreate(BaseModel):
    id: str = Field(..., json_schema_extra={"example": "supabase_changelog"})
    name: str = Field(..., json_schema_extra={"example": "Supabase Changelog"})
    url: str = Field(..., json_schema_extra={"example": "https://supabase.com/changelog"})
    collector_id: Optional[str] = Field(None, json_schema_extra={"example": "c_m1abc123xyz"})

class SourceResponse(BaseModel):
    id: str
    name: str
    url: str
    collector_id: str
    status: str
    created_at: str
    updated_at: str

class ScrapeResponse(BaseModel):
    status: str
    collector_id: str
    source_url: str
    records_count: int
    records: List[Dict[str, Any]]
