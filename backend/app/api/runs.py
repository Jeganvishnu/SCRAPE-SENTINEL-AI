import uuid
from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.scrape_run_service import scrape_run_service
from app.services.validation_service import validation_service

router = APIRouter(prefix="/runs", tags=["Runs"])

@router.get("")
async def list_runs(limit: int = 50, db: Session = Depends(get_db)):
    runs = scrape_run_service.get_all(db, limit=limit)
    return [
        {
            "id": str(r.id),
            "source_id": str(r.source_id),
            "collector_id": r.collector_id,
            "started_at": r.started_at.isoformat(),
            "completed_at": r.completed_at.isoformat() if r.completed_at else None,
            "status": r.status,
            "records_found": r.records_found,
            "records_valid": r.records_valid,
            "records_invalid": r.records_invalid,
            "duration_ms": r.duration_ms,
            "error_message": r.error_message,
        } for r in runs
    ]

@router.get("/{id}")
async def get_run(id: str, db: Session = Depends(get_db)):
    try:
        run_uuid = uuid.UUID(id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format for run_id.")

    run = scrape_run_service.get_by_id(db, run_uuid)
    if not run:
        raise HTTPException(status_code=404, detail=f"Scrape run '{id}' not found.")

    return {
        "id": str(run.id),
        "source_id": str(run.source_id),
        "collector_id": run.collector_id,
        "started_at": run.started_at.isoformat(),
        "completed_at": run.completed_at.isoformat() if run.completed_at else None,
        "status": run.status,
        "records_found": run.records_found,
        "records_valid": run.records_valid,
        "records_invalid": run.records_invalid,
        "duration_ms": run.duration_ms,
        "error_message": run.error_message,
    }

@router.get("/{id}/validation")
async def get_run_validation(id: str, db: Session = Depends(get_db)):
    try:
        run_uuid = uuid.UUID(id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format for run_id.")

    val = validation_service.get_by_run_id(db, run_uuid)
    if not val:
        raise HTTPException(status_code=404, detail=f"Validation result for run '{id}' not found.")

    return {
        "id": str(val.id),
        "scrape_run_id": str(val.scrape_run_id),
        "validation_status": val.validation_status,
        "validation_score": float(val.validation_score) if val.validation_score else 0.0,
        "schema_valid": val.schema_valid,
        "required_fields_valid": val.required_fields_valid,
        "url_valid": val.url_valid,
        "date_valid": val.date_valid,
        "duplicate_free": val.duplicate_free,
        "record_count_valid": val.record_count_valid,
        "schema_change_detected": val.schema_change_detected,
        "issues": val.issues or [],
        "validated_at": val.validated_at.isoformat()
    }
