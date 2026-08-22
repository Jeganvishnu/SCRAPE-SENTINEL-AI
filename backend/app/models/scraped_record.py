import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.core.database import Base

class ScrapedRecord(Base):
    __tablename__ = "scraped_records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id = Column(UUID(as_uuid=True), ForeignKey("sources.id", ondelete="CASCADE"), nullable=False, index=True)
    scrape_run_id = Column(UUID(as_uuid=True), ForeignKey("scrape_runs.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(Text, nullable=True)
    published_date = Column(DateTime(timezone=True), nullable=True)
    version = Column(Text, nullable=True)
    category = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    url = Column(Text, nullable=True)
    content_hash = Column(Text, nullable=False, index=True)
    scraped_at = Column(DateTime(timezone=True), nullable=False)
    raw_data = Column(JSON().with_variant(JSONB, "postgresql"), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    source = relationship("Source", back_populates="records")
    scrape_run = relationship("ScrapeRun", back_populates="records")
