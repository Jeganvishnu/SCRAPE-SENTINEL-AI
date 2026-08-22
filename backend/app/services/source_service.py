import uuid
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.source import Source
from app.core.brightdata_config import brightdata_settings

class SourceService:
    def get_all(self, db: Session) -> List[Source]:
        sources = db.query(Source).all()
        # Seed default primary source if empty
        if not sources:
            default_source = self.create(
                db=db,
                name="Supabase Changelog",
                url="https://supabase.com/changelog",
                collector_id=brightdata_settings.BRIGHT_DATA_COLLECTOR_ID or "c_mt46lngz2asqzj8tkj"
            )
            return [default_source]
        return sources

    def get_by_id(self, db: Session, source_id: uuid.UUID) -> Optional[Source]:
        return db.query(Source).filter(Source.id == source_id).first()

    def get_by_collector_id(self, db: Session, collector_id: str) -> Optional[Source]:
        return db.query(Source).filter(Source.collector_id == collector_id).first()

    def create(self, db: Session, name: str, url: str, collector_id: str) -> Source:
        source = Source(
            name=name,
            url=url,
            collector_id=collector_id,
            status="active"
        )
        db.add(source)
        db.commit()
        db.refresh(source)
        return source

    def update_status(self, db: Session, source_id: uuid.UUID, status: str) -> Optional[Source]:
        source = self.get_by_id(db, source_id)
        if source:
            source.status = status
            db.commit()
            db.refresh(source)
        return source

source_service = SourceService()
