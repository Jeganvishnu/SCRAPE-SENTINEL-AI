import uuid
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db, check_database_connection
from app.core.brightdata_config import brightdata_settings
from app.services.metrics_service import metrics_service
from app.services.health_service import health_service
from app.schemas.metrics import OverviewMetricsSchema

router = APIRouter(tags=["Metrics & Monitoring"])

@router.get("/metrics/overview", response_model=OverviewMetricsSchema)
async def get_overview_metrics(period: str = Query("7d", pattern="^(24h|7d|30d|all)$"), db: Session = Depends(get_db)):
    return metrics_service.get_overview_metrics(db, period=period)

@router.get("/metrics/sources/{source_id}")
async def get_source_metrics(source_id: str, period: str = Query("7d", pattern="^(24h|7d|30d|all)$"), db: Session = Depends(get_db)):
    try:
        s_uuid = uuid.UUID(source_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID for source_id.")

    res = metrics_service.get_source_metrics(db, s_uuid, period=period)
    if not res:
        raise HTTPException(status_code=404, detail=f"Source metrics for '{source_id}' not found.")
    return res

@router.get("/metrics/timeline")
async def get_timeline(limit: int = 50, db: Session = Depends(get_db)):
    return metrics_service.get_timeline(db, limit=limit)

@router.get("/metrics/validation")
async def get_validation_trends(source_id: Optional[str] = None, limit: int = 50, db: Session = Depends(get_db)):
    s_uuid = None
    if source_id:
        try:
            s_uuid = uuid.UUID(source_id)
        except ValueError:
            pass
    return metrics_service.get_validation_trends(db, source_id=s_uuid, limit=limit)

@router.get("/metrics/schema/{source_id}")
async def get_schema_history(source_id: str, limit: int = 20, db: Session = Depends(get_db)):
    try:
        s_uuid = uuid.UUID(source_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID for source_id.")
    return metrics_service.get_schema_history(db, s_uuid, limit=limit)

@router.get("/metrics/healing")
async def get_healing_metrics(period: str = Query("7d", pattern="^(24h|7d|30d|all)$"), db: Session = Depends(get_db)):
    since = health_service.parse_time_window(period)
    rec_rate, mttr = health_service.calculate_recovery_metrics(db, since=since)
    return {
        "period": period,
        "recovery_rate": rec_rate,
        "mttr_seconds": mttr,
        "explanation": "No healing attempts yet" if rec_rate is None else f"Recovery rate is {rec_rate}% with MTTR of {mttr}s."
    }

@router.get("/metrics/activity")
async def get_activity_feed(limit: int = 20, db: Session = Depends(get_db)):
    return metrics_service.get_timeline(db, limit=limit)

@router.get("/metrics/export")
async def export_metrics(period: str = Query("7d", pattern="^(24h|7d|30d|all)$"), db: Session = Depends(get_db)):
    overview = metrics_service.get_overview_metrics(db, period=period)
    timeline = metrics_service.get_timeline(db, limit=100)
    return {
        "export_timestamp": datetime.now(timezone.utc).isoformat(),
        "period": period,
        "overview": overview,
        "recent_timeline": timeline
    }

@router.get("/ready")
async def readiness_check():
    db_ok = check_database_connection()
    bd_configured = bool(brightdata_settings.BRIGHT_DATA_COLLECTOR_ID)
    if not db_ok:
        raise HTTPException(status_code=503, detail="Database not connected.")
    return {
        "status": "ready",
        "database": "connected",
        "bright_data": "configured" if bd_configured else "unconfigured"
    }

@router.get("/system/status")
async def system_status(db: Session = Depends(get_db)):
    score, sys_health, explanation = health_service.calculate_health_score_and_state(db)
    return {
        "system_health": sys_health,
        "health_score": score,
        "explanation": explanation,
        "database": "connected" if check_database_connection() else "disconnected",
        "bright_data_collector_id": brightdata_settings.BRIGHT_DATA_COLLECTOR_ID or "PENDING"
    }
