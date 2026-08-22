import time
import hashlib
import json
import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.brightdata_config import brightdata_settings
from app.core.logger_config import logger

from app.services.source_service import source_service
from app.services.scrape_run_service import scrape_run_service
from app.services.record_service import record_service
from app.services.validation_service import validation_service
from app.services.failure_service import failure_service
from app.services.brightdata_service import brightdata_service, BrightDataError
from app.services.normalizer import normalize_payload

from app.validators.engine import validation_engine

from pydantic import BaseModel, Field

router = APIRouter(prefix="/sources", tags=["Sources"])

class SourceCreateSchema(BaseModel):
    name: str = Field(..., json_schema_extra={"example": "Supabase Changelog"})
    url: str = Field(..., json_schema_extra={"example": "https://supabase.com/changelog"})
    collector_id: str = Field(..., json_schema_extra={"example": "c_mt46lngz2asqzj8tkj"})

class SourceResponseSchema(BaseModel):
    id: str
    name: str
    url: str
    collector_id: str
    status: str
    created_at: str
    updated_at: str

@router.get("", response_model=List[SourceResponseSchema])
async def list_sources(db: Session = Depends(get_db)):
    sources = source_service.get_all(db)
    return [
        SourceResponseSchema(
            id=str(s.id),
            name=s.name,
            url=s.url,
            collector_id=s.collector_id,
            status=s.status,
            created_at=s.created_at.isoformat(),
            updated_at=s.updated_at.isoformat()
        ) for s in sources
    ]

@router.post("", response_model=SourceResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_source(payload: SourceCreateSchema, db: Session = Depends(get_db)):
    source = source_service.create(
        db=db,
        name=payload.name,
        url=payload.url,
        collector_id=payload.collector_id
    )
    return SourceResponseSchema(
        id=str(source.id),
        name=source.name,
        url=source.url,
        collector_id=source.collector_id,
        status=source.status,
        created_at=source.created_at.isoformat(),
        updated_at=source.updated_at.isoformat()
    )

@router.get("/{id}", response_model=SourceResponseSchema)
async def get_source(id: str, db: Session = Depends(get_db)):
    try:
        source_uuid = uuid.UUID(id)
        source = source_service.get_by_id(db, source_uuid)
    except ValueError:
        # Fallback search by collector_id or default seed
        source = source_service.get_by_collector_id(db, id)
        if not source and id == "supabase_changelog":
            sources = source_service.get_all(db)
            source = sources[0] if sources else None

    if not source:
        raise HTTPException(status_code=404, detail=f"Source '{id}' not found.")

    return SourceResponseSchema(
        id=str(source.id),
        name=source.name,
        url=source.url,
        collector_id=source.collector_id,
        status=source.status,
        created_at=source.created_at.isoformat(),
        updated_at=source.updated_at.isoformat()
    )

@router.post("/{id}/scrape")
async def scrape_source(id: str, db: Session = Depends(get_db)):
    # 1. Resolve source
    try:
        source_uuid = uuid.UUID(id)
        source = source_service.get_by_id(db, source_uuid)
    except ValueError:
        source = source_service.get_by_collector_id(db, id)
        if not source and id == "supabase_changelog":
            sources = source_service.get_all(db)
            source = sources[0] if sources else None

    if not source:
        raise HTTPException(status_code=404, detail=f"Source '{id}' not found.")

    collector_id = source.collector_id or brightdata_settings.BRIGHT_DATA_COLLECTOR_ID
    if not collector_id or collector_id == "PENDING":
        raise HTTPException(status_code=400, detail="No valid Collector ID bound to source.")

    # 2. Start ScrapeRun in DB
    run = scrape_run_service.create_run(db, source.id, collector_id)
    start_time = time.time()

    try:
        # 3. Execute Bright Data Collector
        raw_records = brightdata_service.run_collector(collector_id, source.url)
        duration_ms = int((time.time() - start_time) * 1000)
        raw_hash = hashlib.sha256(json.dumps(raw_records).encode("utf-8")).hexdigest()

        # 4. Normalize Payload
        normalized_records = normalize_payload(
            raw_records=raw_records,
            source_id=str(source.id),
            source_name=source.name,
            collector_id=collector_id,
            default_url=source.url
        )

        # 5. Fetch recent baseline for anomaly detection
        recent_baselines = scrape_run_service.get_recent_successful_counts(db, source.id, limit=5)

        # 6. Run Validation Engine
        eval_result = validation_engine.evaluate(
            records=normalized_records,
            baseline_recent_counts=recent_baselines
        )

        val_status = eval_result["validation_status"]  # passed, warning, failed
        records_found = len(raw_records)
        records_valid = records_found if val_status != "failed" else 0
        records_invalid = 0 if val_status != "failed" else records_found

        run_status = "success" if val_status in ("passed", "warning") else "failed"

        # 7. Persist ScrapeRun, ScrapedRecords, and ValidationResult
        scrape_run_service.finish_run(
            db=db,
            run_id=run.id,
            status=run_status,
            records_found=records_found,
            records_valid=records_valid,
            records_invalid=records_invalid,
            duration_ms=duration_ms,
            raw_output_hash=raw_hash
        )

        if val_status != "failed":
            record_service.bulk_insert(db, source.id, run.id, normalized_records)

        val_obj = validation_service.create_result(db, run.id, eval_result)

        # 8. Create Failure Events if validation failed or warning issues present
        created_failures = []
        for issue in eval_result.get("issues", []):
            if issue.get("severity") in ("high", "critical"):
                f_event = failure_service.create_event(
                    db=db,
                    source_id=source.id,
                    scrape_run_id=run.id,
                    failure_type=issue.get("type", "unknown"),
                    severity=issue.get("severity", "high"),
                    message=issue.get("message", "Validation failure detected."),
                    details=issue
                )
                created_failures.append({
                    "id": str(f_event.id),
                    "type": f_event.failure_type,
                    "severity": f_event.severity,
                    "message": f_event.message
                })

        # Update Source Status
        new_source_status = "active" if val_status == "passed" else ("warning" if val_status == "warning" else "failed")
        source_service.update_status(db, source.id, new_source_status)

        return {
            "run_id": str(run.id),
            "status": run_status,
            "records_found": records_found,
            "records_valid": records_valid,
            "records_invalid": records_invalid,
            "validation": {
                "status": val_status,
                "score": float(val_obj.validation_score)
            },
            "failures": created_failures
        }

    except BrightDataError as e:
        duration_ms = int((time.time() - start_time) * 1000)
        scrape_run_service.finish_run(
            db=db,
            run_id=run.id,
            status="failed",
            records_found=0,
            records_valid=0,
            records_invalid=0,
            duration_ms=duration_ms,
            error_code="COLLECTOR_FAILURE",
            error_message=str(e)
        )
        f_event = failure_service.create_event(
            db=db,
            source_id=source.id,
            scrape_run_id=run.id,
            failure_type="collector_failure",
            severity="critical",
            message=f"Bright Data collector execution failed: {str(e)}",
            details={"error": str(e)}
        )
        source_service.update_status(db, source.id, "failed")
        raise HTTPException(status_code=502, detail=f"Scraper execution failed: {str(e)}")
