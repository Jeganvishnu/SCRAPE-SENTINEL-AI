import uuid
from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session
from app.models.failure_event import FailureEvent

class FailureService:
    def create_event(
        self,
        db: Session,
        source_id: uuid.UUID,
        scrape_run_id: uuid.UUID,
        failure_type: str,
        severity: str,
        message: str,
        details: Optional[Dict[str, Any]] = None
    ) -> FailureEvent:
        event = FailureEvent(
            source_id=source_id,
            scrape_run_id=scrape_run_id,
            failure_type=failure_type,
            severity=severity,
            message=message,
            details=details,
            status="open"
        )
        db.add(event)
        db.commit()
        db.refresh(event)
        return event

    def get_all(self, db: Session, status: Optional[str] = None, limit: int = 50) -> List[FailureEvent]:
        query = db.query(FailureEvent)
        if status:
            query = query.filter(FailureEvent.status == status)
        return query.order_by(FailureEvent.detected_at.desc()).limit(limit).all()

    def get_by_id(self, db: Session, failure_id: uuid.UUID) -> Optional[FailureEvent]:
        return db.query(FailureEvent).filter(FailureEvent.id == failure_id).first()

failure_service = FailureService()
