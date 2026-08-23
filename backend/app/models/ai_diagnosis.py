import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Numeric, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID, JSONB

from app.core.database import Base

class AIDiagnosis(Base):
    __tablename__ = "ai_diagnoses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id = Column(UUID(as_uuid=True), ForeignKey("sources.id", ondelete="CASCADE"), nullable=False)
    failure_event_id = Column(UUID(as_uuid=True), ForeignKey("failure_events.id", ondelete="CASCADE"), nullable=False)
    healing_attempt_id = Column(UUID(as_uuid=True), ForeignKey("healing_attempts.id", ondelete="SET NULL"), nullable=True)

    model = Column(String, nullable=False, default="mock")
    prompt_version = Column(String, nullable=False, default="scrape-sentinel-diagnosis-v1")
    failure_category = Column(String, nullable=False)
    confidence = Column(Numeric(4, 2), nullable=False)
    root_cause = Column(String, nullable=False)
    evidence = Column(JSON().with_variant(JSONB, "postgresql"), nullable=False, default=list)

    repair_type = Column(String, nullable=False)
    repair_plan = Column(JSON().with_variant(JSONB, "postgresql"), nullable=False, default=dict)
    risk = Column(String, nullable=False, default="low")
    approved = Column(Boolean, nullable=False, default=False)
    requires_manual_review = Column(Boolean, nullable=False, default=False)
    verification_status = Column(String, nullable=False, default="pending")

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
