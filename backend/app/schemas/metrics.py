from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class OverviewMetricsSchema(BaseModel):
    period: str
    system_health: str
    health_score: float
    total_sources: int
    total_runs: int
    successful_runs: int
    failed_runs: int
    success_rate: float
    average_validation_score: float
    active_failures: int
    healing_attempts: int
    successful_recoveries: int
    recovery_rate: Optional[float]
    mttr_seconds: Optional[float]

class SourceMetricsSchema(BaseModel):
    source_id: str
    name: str
    url: str
    collector_id: str
    health: str
    health_score: float
    explanation: str
    total_runs: int
    success_rate: float
    average_validation_score: float
    average_duration_ms: Optional[float]
    latest_record_count: int
    active_failures: int
    healing_attempts: int
    successful_recoveries: int
    last_scrape_at: Optional[str]
    last_successful_scrape_at: Optional[str]

class TimelineEventSchema(BaseModel):
    timestamp: str
    type: str  # scrape_started, scrape_completed, validation_failed, failure_detected, healing_started, healing_completed, recovery_verified
    source_id: str
    run_id: Optional[str] = None
    status: str
    message: str

class ValidationTrendSchema(BaseModel):
    timestamp: str
    validation_score: float
    validation_status: str
    schema_change_detected: bool
    record_count_valid: bool
    records_found: int

class SchemaHistorySchema(BaseModel):
    timestamp: str
    run_id: str
    schema_fingerprint: str
    schema_change_detected: bool
    issues: List[Dict[str, Any]]
