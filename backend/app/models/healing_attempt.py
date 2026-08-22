import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.core.database import Base

class HealingAttempt(Base):
    __tablename__ = "healing_attempts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id = Column(UUID(as_uuid=True), ForeignKey("sources.id", ondelete="CASCADE"), nullable=False, index=True)
    scrape_run_id = Column(UUID(as_uuid=True), ForeignKey("scrape_runs.id", ondelete="CASCADE"), nullable=False, index=True)
    failure_event_id = Column(UUID(as_uuid=True), ForeignKey("failure_events.id", ondelete="CASCADE"), nullable=False, index=True)
    collector_id = Column(Text, nullable=False)
    attempt_number = Column(Integer, nullable=False, default=1)
    started_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    completed_at = Column(DateTime(timezone=True), nullable=True)
    status = Column(Text, nullable=False, default="queued")  # queued, running, success, failed, verified
    failure_type = Column(Text, nullable=True)
    previous_schema_fingerprint = Column(Text, nullable=True)
    new_schema_fingerprint = Column(Text, nullable=True)
    old_instruction_hash = Column(Text, nullable=True)
    new_instruction_hash = Column(Text, nullable=True)
    verification_run_id = Column(UUID(as_uuid=True), ForeignKey("scrape_runs.id", ondelete="SET NULL"), nullable=True)
    error_code = Column(Text, nullable=True)
    error_message = Column(Text, nullable=True)
    details = Column(JSON().with_variant(JSONB, "postgresql"), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    source = relationship("Source", foreign_keys=[source_id])
    scrape_run = relationship("ScrapeRun", foreign_keys=[scrape_run_id])
    failure_event = relationship("FailureEvent", foreign_keys=[failure_event_id])
    verification_run = relationship("ScrapeRun", foreign_keys=[verification_run_id])
