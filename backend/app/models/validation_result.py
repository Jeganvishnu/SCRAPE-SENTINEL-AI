import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, Boolean, Numeric, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.core.database import Base

class ValidationResult(Base):
    __tablename__ = "validation_results"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scrape_run_id = Column(UUID(as_uuid=True), ForeignKey("scrape_runs.id", ondelete="CASCADE"), nullable=False, index=True)
    validation_status = Column(Text, nullable=False)  # passed, warning, failed
    schema_valid = Column(Boolean, nullable=False)
    required_fields_valid = Column(Boolean, nullable=False)
    url_valid = Column(Boolean, nullable=False)
    date_valid = Column(Boolean, nullable=False)
    duplicate_free = Column(Boolean, nullable=False)
    record_count_valid = Column(Boolean, nullable=False)
    schema_change_detected = Column(Boolean, nullable=False, default=False)
    validation_score = Column(Numeric(5, 2), nullable=True)
    issues = Column(JSON().with_variant(JSONB, "postgresql"), nullable=True)
    validated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    scrape_run = relationship("ScrapeRun", back_populates="validation")
