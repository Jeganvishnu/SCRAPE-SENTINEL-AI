import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.failure_service import failure_service

router = APIRouter(prefix="/failures", tags=["Failures"])

@router.get("")
async def list_failures(status: Optional[str] = None, limit: int = 50, db: Session = Depends(get_db)):
    events = failure_service.get_all(db, status=status, limit=limit)
    return [
        {
            "id": str(ev.id),
            "source_id": str(ev.source_id),
            "scrape_run_id": str(ev.scrape_run_id),
            "failure_type": ev.failure_type,
            "severity": ev.severity,
            "message": ev.message,
            "details": ev.details or {},
            "detected_at": ev.detected_at.isoformat(),
            "status": ev.status
        } for ev in events
    ]

@router.get("/{id}")
async def get_failure(id: str, db: Session = Depends(get_db)):
    try:
        f_uuid = uuid.UUID(id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format for failure_id.")

    ev = failure_service.get_by_id(db, f_uuid)
    if not ev:
        raise HTTPException(status_code=404, detail=f"Failure event '{id}' not found.")

    return {
        "id": str(ev.id),
        "source_id": str(ev.source_id),
        "scrape_run_id": str(ev.scrape_run_id),
        "failure_type": ev.failure_type,
        "severity": ev.severity,
        "message": ev.message,
        "details": ev.details or {},
        "detected_at": ev.detected_at.isoformat(),
        "status": ev.status
    }
