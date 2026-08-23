import uuid
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.database import get_db
from app.core.config import settings
from app.models.ai_diagnosis import AIDiagnosis
from app.services.health_service import health_service
from app.ai.diagnosis_service import diagnosis_service

router = APIRouter(tags=["AI Scraper Intelligence"])

@router.get("/ai/status")
async def get_ai_status(db: Session = Depends(get_db)):
    total_diagnoses = db.query(AIDiagnosis).count()
    total_approved = db.query(AIDiagnosis).filter(AIDiagnosis.approved == True).count()
    verified_repairs = db.query(AIDiagnosis).filter(AIDiagnosis.verification_status == "verified").count()
    failed_repairs = db.query(AIDiagnosis).filter(AIDiagnosis.verification_status == "failed").count()

    avg_conf = db.query(func.avg(AIDiagnosis.confidence)).scalar()
    avg_confidence = round(float(avg_conf), 2) if avg_conf is not None else None

    # AI Verification Rate (verified / (verified + failed))
    total_executed = verified_repairs + failed_repairs
    verification_rate = round((verified_repairs / total_executed * 100.0), 2) if total_executed > 0 else None

    return {
        "enabled": settings.AI_ENABLED,
        "provider": settings.AI_PROVIDER,
        "model": settings.AI_MODEL,
        "prompt_version": settings.AI_PROMPT_VERSION,
        "total_diagnoses": total_diagnoses,
        "total_approved": total_approved,
        "verified_repairs": verified_repairs,
        "failed_repairs": failed_repairs,
        "verification_rate": verification_rate,
        "average_confidence": avg_confidence,
        "max_repair_attempts": settings.AI_MAX_REPAIR_ATTEMPTS,
        "high_confidence_threshold": settings.AI_HIGH_CONFIDENCE_THRESHOLD
    }

@router.post("/ai/diagnose/{failure_id}")
async def diagnose_failure(failure_id: str, db: Session = Depends(get_db)):
    try:
        f_uuid = uuid.UUID(failure_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format for failure_id.")

    diag = diagnosis_service.diagnose_and_plan(db, f_uuid)
    if not diag:
        raise HTTPException(status_code=404, detail=f"Failure event '{failure_id}' not found.")
    return diag

@router.post("/ai/repair-plan/{failure_id}")
async def get_repair_plan(failure_id: str, db: Session = Depends(get_db)):
    try:
        f_uuid = uuid.UUID(failure_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format for failure_id.")

    diag = db.query(AIDiagnosis).filter(AIDiagnosis.failure_event_id == f_uuid).order_by(AIDiagnosis.created_at.desc()).first()
    if not diag:
        # Run diagnosis first if not present
        diag_dict = diagnosis_service.diagnose_and_plan(db, f_uuid)
        if not diag_dict:
            raise HTTPException(status_code=404, detail=f"Failure event '{failure_id}' not found.")
        return diag_dict

    return {
        "id": str(diag.id),
        "failure_event_id": str(diag.failure_event_id),
        "diagnosis": {
            "failure_category": diag.failure_category,
            "confidence": float(diag.confidence),
            "root_cause": diag.root_cause,
            "evidence": diag.evidence
        },
        "repair_plan": diag.repair_plan,
        "risk": diag.risk,
        "approved": diag.approved,
        "requires_manual_review": diag.requires_manual_review,
        "verification_status": diag.verification_status
    }

@router.get("/ai/history")
async def get_ai_history(source_id: Optional[str] = None, limit: int = 50, db: Session = Depends(get_db)):
    s_uuid = None
    if source_id:
        try:
            s_uuid = uuid.UUID(source_id)
        except ValueError:
            pass
    return diagnosis_service.get_history(db, source_id=s_uuid, limit=limit)
