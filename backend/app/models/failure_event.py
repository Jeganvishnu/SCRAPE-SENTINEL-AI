import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.core.database import Base

class FailureEvent(Base):
    __tablename__ = "failure_events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id = Column(UUID(as_uuid=True), ForeignKey("sources.id", ondelete="CASCADE"), nullable=False, index=True)
    scrape_run_id = Column(UUID(as_uuid=True), ForeignKey("scrape_runs.id", ondelete="CASCADE"), nullable=False, index=True)
    failure_type = Column(Text, nullable=False)  # empty_result, record_count_drop, schema_change, required_field_missing, etc.
    severity = Column(Text, nullable=False)      # low, medium, high, critical
    message = Column(Text, nullable=False)
    details = Column(JSON().with_variant(JSONB, "postgresql"), nullable=True)
    detected_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    status = Column(Text, nullable=False, default="open") # open, acknowledged, resolved

    source = relationship("Source", back_populates="failures")
    scrape_run = relationship("ScrapeRun", back_populates="failures")
