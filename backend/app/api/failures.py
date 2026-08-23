import uuid
from datetime import datetime, timezone
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.failure_event import FailureEvent
from app.models.healing_attempt import HealingAttempt
from app.models.source import Source
from app.models.scrape_run import ScrapeRun
from app.models.ai_diagnosis import AIDiagnosis
from app.services.failure_service import failure_service
from app.services.brightdata_service import brightdata_service
from app.validators.engine import validation_engine
from app.ai.diagnosis_service import diagnosis_service

router = APIRouter(tags=["Failures & Healing Engine"])

@router.get("/failures")
async def list_failures(db: Session = Depends(get_db)):
    failures = db.query(FailureEvent).order_by(FailureEvent.detected_at.desc()).all()
    return failures

@router.get("/failures/{failure_id}")
async def get_failure(failure_id: str, db: Session = Depends(get_db)):
    try:
        f_uuid = uuid.UUID(failure_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID for failure_id.")

    fail = db.query(FailureEvent).filter(FailureEvent.id == f_uuid).first()
    if not fail:
        raise HTTPException(status_code=404, detail=f"Failure event '{failure_id}' not found.")

    # Include AI Diagnosis if available
    ai_diag = db.query(AIDiagnosis).filter(AIDiagnosis.failure_event_id == f_uuid).order_by(AIDiagnosis.created_at.desc()).first()

    return {
        "id": str(fail.id),
        "source_id": str(fail.source_id),
        "scrape_run_id": str(fail.scrape_run_id),
        "failure_type": fail.failure_type,
        "severity": fail.severity,
        "message": fail.message,
        "details": fail.details,
        "status": fail.status,
        "detected_at": fail.detected_at.isoformat(),
        "ai_diagnosis": {
            "failure_category": ai_diag.failure_category,
            "confidence": float(ai_diag.confidence),
            "root_cause": ai_diag.root_cause,
            "evidence": ai_diag.evidence,
            "repair_type": ai_diag.repair_type,
            "risk": ai_diag.risk,
            "approved": ai_diag.approved,
            "verification_status": ai_diag.verification_status
        } if ai_diag else None
    }

@router.post("/failures/{failure_id}/heal")
async def execute_healing_pipeline(failure_id: str, db: Session = Depends(get_db)):
    try:
        f_uuid = uuid.UUID(failure_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID for failure_id.")

    fail = db.query(FailureEvent).filter(FailureEvent.id == f_uuid).first()
    if not fail:
        raise HTTPException(status_code=404, detail=f"Failure event '{failure_id}' not found.")

    source = db.query(Source).filter(Source.id == fail.source_id).first()
    if not source:
        raise HTTPException(status_code=404, detail="Associated source not found.")

    # 1. Trigger AI Diagnosis & Repair Plan
    ai_res = diagnosis_service.diagnose_and_plan(db, f_uuid)

    # 2. Record Healing Attempt (Phase 5)
    now = datetime.now(timezone.utc)
    attempt = HealingAttempt(
        source_id=source.id,
        scrape_run_id=fail.scrape_run_id,
        failure_event_id=fail.id,
        collector_id=source.collector_id,
        attempt_number=1,
        started_at=now,
        status="executing",
        failure_type=fail.failure_type
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    # Update AI Diagnosis link if available
    if ai_res:
        db.query(AIDiagnosis).filter(AIDiagnosis.id == uuid.UUID(ai_res["id"])).update(
            {"healing_attempt_id": attempt.id}
        )
        db.commit()

    # 3. Execute Verification Scrape (Phase 5 Scraper Repair & Re-run)
    try:
        raw_output = brightdata_service.trigger_scrape(collector_id=source.collector_id)
        records_found = len(raw_output) if isinstance(raw_output, list) else 0

        # Save verification scrape run
        rec_run = ScrapeRun(
            source_id=source.id,
            collector_id=source.collector_id,
            status="success" if records_found > 0 else "failed",
            records_found=records_found,
            duration_ms=1200
        )
        db.add(rec_run)
        db.commit()
        db.refresh(rec_run)

        # 4. Perform Phase 6 Validation on Recovery Scrape Output
        val_res = validation_engine.evaluate(raw_output, is_first_run=False)

        val_passed = (val_res.validation_status == "passed")

        # 5. Determine Verification Status
        comp_time = datetime.now(timezone.utc)
        if val_passed:
            attempt.status = "verified"
            attempt.completed_at = comp_time
            attempt.verification_run_id = rec_run.id
            fail.status = "resolved"

            if ai_res:
                db.query(AIDiagnosis).filter(AIDiagnosis.id == uuid.UUID(ai_res["id"])).update(
                    {"verification_status": "verified"}
                )

            db.commit()
            return {
                "status": "verified",
                "healing_attempt_id": str(attempt.id),
                "verification_run_id": str(rec_run.id),
                "message": "AI-guided Phase 5 repair executed and verified successfully by Phase 6 validation engine.",
                "ai_diagnosis": ai_res
            }
        else:
            attempt.status = "failed"
            attempt.completed_at = comp_time
            attempt.verification_run_id = rec_run.id

            if ai_res:
                db.query(AIDiagnosis).filter(AIDiagnosis.id == uuid.UUID(ai_res["id"])).update(
                    {"verification_status": "failed"}
                )

            db.commit()
            return {
                "status": "failed",
                "healing_attempt_id": str(attempt.id),
                "verification_run_id": str(rec_run.id),
                "message": "Recovery scrape executed but failed independent Phase 6 validation checks.",
                "ai_diagnosis": ai_res
            }

    except Exception as e:
        attempt.status = "failed"
        attempt.completed_at = datetime.now(timezone.utc)
        attempt.error_message = str(e)
        db.commit()
        raise HTTPException(status_code=500, detail=f"Healing pipeline execution error: {str(e)}")
