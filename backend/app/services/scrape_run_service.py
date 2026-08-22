import uuid
from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.scrape_run import ScrapeRun

class ScrapeRunService:
    def create_run(self, db: Session, source_id: uuid.UUID, collector_id: str) -> ScrapeRun:
        run = ScrapeRun(
            source_id=source_id,
            collector_id=collector_id,
            started_at=datetime.now(timezone.utc),
            status="running"
        )
        db.add(run)
        db.commit()
        db.refresh(run)
        return run

    def finish_run(
        self,
        db: Session,
        run_id: uuid.UUID,
        status: str,
        records_found: int,
        records_valid: int,
        records_invalid: int,
        duration_ms: Optional[int] = None,
        error_code: Optional[str] = None,
        error_message: Optional[str] = None,
        raw_output_hash: Optional[str] = None
    ) -> Optional[ScrapeRun]:
        run = db.query(ScrapeRun).filter(ScrapeRun.id == run_id).first()
        if run:
            run.completed_at = datetime.now(timezone.utc)
            run.status = status
            run.records_found = records_found
            run.records_valid = records_valid
            run.records_invalid = records_invalid
            run.duration_ms = duration_ms
            run.error_code = error_code
            run.error_message = error_message
            run.raw_output_hash = raw_output_hash
            db.commit()
            db.refresh(run)
        return run

    def get_by_id(self, db: Session, run_id: uuid.UUID) -> Optional[ScrapeRun]:
        return db.query(ScrapeRun).filter(ScrapeRun.id == run_id).first()

    def get_all(self, db: Session, limit: int = 50) -> List[ScrapeRun]:
        return db.query(ScrapeRun).order_by(ScrapeRun.started_at.desc()).limit(limit).all()

    def get_recent_successful_counts(self, db: Session, source_id: uuid.UUID, limit: int = 5) -> List[int]:
        runs = db.query(ScrapeRun).filter(
            ScrapeRun.source_id == source_id,
            ScrapeRun.status == "success"
        ).order_by(ScrapeRun.started_at.desc()).limit(limit).all()
        return [r.records_valid for r in runs if r.records_valid > 0]

scrape_run_service = ScrapeRunService()
