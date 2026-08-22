import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base

class Source(Base):
    __tablename__ = "sources"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(Text, nullable=False)
    url = Column(Text, nullable=False)
    collector_id = Column(Text, nullable=False, index=True)
    status = Column(Text, nullable=False, default="active")
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    runs = relationship("ScrapeRun", back_populates="source", cascade="all, delete-orphan")
    records = relationship("ScrapedRecord", back_populates="source", cascade="all, delete-orphan")
    failures = relationship("FailureEvent", back_populates="source", cascade="all, delete-orphan")
