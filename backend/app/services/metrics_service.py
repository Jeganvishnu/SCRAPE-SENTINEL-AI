import uuid
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.source import Source
from app.models.scrape_run import ScrapeRun
from app.models.scraped_record import ScrapedRecord
from app.models.validation_result import ValidationResult
from app.models.failure_event import FailureEvent
from app.models.healing_attempt import HealingAttempt
from app.services.health_service import health_service

class MetricsService:
    def get_overview_metrics(self, db: Session, period: str = "7d") -> Dict[str, Any]:
        since = health_service.parse_time_window(period)

        score, sys_health, explanation = health_service.calculate_health_score_and_state(db, period=period)
        total_sources = db.query(Source).count()

        run_query = db.query(ScrapeRun)
        if since:
            run_query = run_query.filter(ScrapeRun.started_at >= since)

        total_runs = run_query.count()
        successful_runs = run_query.filter(ScrapeRun.status == "success").count()
        failed_runs = run_query.filter(ScrapeRun.status == "failed").count()

        success_rate = round((successful_runs / total_runs * 100.0), 2) if total_runs > 0 else 100.0
        avg_val = health_service.calculate_avg_validation_score(db, since=since)

        fail_query = db.query(FailureEvent).filter(FailureEvent.status == "open")
        if since:
            fail_query = fail_query.filter(FailureEvent.detected_at >= since)
        active_failures = fail_query.count()

        heal_query = db.query(HealingAttempt)
        if since:
            heal_query = heal_query.filter(HealingAttempt.started_at >= since)
        healing_attempts = heal_query.count()
        successful_recoveries = heal_query.filter(HealingAttempt.status == "verified").count()

        recovery_rate, mttr = health_service.calculate_recovery_metrics(db, since=since)

        return {
            "period": period,
            "system_health": sys_health,
            "health_score": score,
            "explanation": explanation,
            "total_sources": total_sources,
            "total_runs": total_runs,
            "successful_runs": successful_runs,
            "failed_runs": failed_runs,
            "success_rate": success_rate,
            "average_validation_score": avg_val,
            "active_failures": active_failures,
            "healing_attempts": healing_attempts,
            "successful_recoveries": successful_recoveries,
            "recovery_rate": recovery_rate,
            "mttr_seconds": mttr
        }

    def get_source_metrics(self, db: Session, source_id: uuid.UUID, period: str = "7d") -> Optional[Dict[str, Any]]:
        source = db.query(Source).filter(Source.id == source_id).first()
        if not source:
            return None

        since = health_service.parse_time_window(period)
        score, health_state, explanation = health_service.calculate_health_score_and_state(db, source_id=source.id, period=period)

        run_query = db.query(ScrapeRun).filter(ScrapeRun.source_id == source.id)
        if since:
            run_query = run_query.filter(ScrapeRun.started_at >= since)

        total_runs = run_query.count()
        successful_runs = run_query.filter(ScrapeRun.status == "success").count()
        success_rate = round((successful_runs / total_runs * 100.0), 2) if total_runs > 0 else 100.0

        avg_val = health_service.calculate_avg_validation_score(db, source_id=source.id, since=since)

        avg_dur_query = db.query(func.avg(ScrapeRun.duration_ms)).filter(ScrapeRun.source_id == source.id)
        if since:
            avg_dur_query = avg_dur_query.filter(ScrapeRun.started_at >= since)
        avg_duration = avg_dur_query.scalar()
        avg_duration_ms = round(float(avg_duration), 1) if avg_duration is not None else None

        latest_run = db.query(ScrapeRun).filter(ScrapeRun.source_id == source.id).order_by(ScrapeRun.started_at.desc()).first()
        latest_success = db.query(ScrapeRun).filter(ScrapeRun.source_id == source.id, ScrapeRun.status == "success").order_by(ScrapeRun.started_at.desc()).first()

        active_fails = db.query(FailureEvent).filter(FailureEvent.source_id == source.id, FailureEvent.status == "open").count()
        heal_count = db.query(HealingAttempt).filter(HealingAttempt.source_id == source.id).count()
        verified_count = db.query(HealingAttempt).filter(HealingAttempt.source_id == source.id, HealingAttempt.status == "verified").count()

        return {
            "source_id": str(source.id),
            "name": source.name,
            "url": source.url,
            "collector_id": source.collector_id,
            "health": health_state,
            "health_score": score,
            "explanation": explanation,
            "total_runs": total_runs,
            "success_rate": success_rate,
            "average_validation_score": avg_val,
            "average_duration_ms": avg_duration_ms,
            "latest_record_count": latest_run.records_found if latest_run else 0,
            "active_failures": active_fails,
            "healing_attempts": heal_count,
            "successful_recoveries": verified_count,
            "last_scrape_at": latest_run.started_at.isoformat() if latest_run else None,
            "last_successful_scrape_at": latest_success.started_at.isoformat() if latest_success else None
        }

    def get_timeline(self, db: Session, limit: int = 50) -> List[Dict[str, Any]]:
        timeline = []

        runs = db.query(ScrapeRun).order_by(ScrapeRun.started_at.desc()).limit(limit).all()
        for r in runs:
            timeline.append({
                "timestamp": r.started_at.isoformat(),
                "type": "scrape_completed" if r.status == "success" else "scrape_failed",
                "source_id": str(r.source_id),
                "run_id": str(r.id),
                "status": r.status,
                "message": f"Scrape run {r.status} with {r.records_found} records found."
            })

        failures = db.query(FailureEvent).order_by(FailureEvent.detected_at.desc()).limit(limit).all()
        for f in failures:
            timeline.append({
                "timestamp": f.detected_at.isoformat(),
                "type": "failure_detected",
                "source_id": str(f.source_id),
                "run_id": str(f.scrape_run_id),
                "status": f.severity,
                "message": f"[{f.failure_type}] {f.message}"
            })

        healing = db.query(HealingAttempt).order_by(HealingAttempt.started_at.desc()).limit(limit).all()
        for h in healing:
            timeline.append({
                "timestamp": h.started_at.isoformat(),
                "type": "recovery_verified" if h.status == "verified" else "healing_started",
                "source_id": str(h.source_id),
                "run_id": str(h.scrape_run_id),
                "status": h.status,
                "message": f"Healing attempt #{h.attempt_number} status: {h.status}."
            })

        timeline.sort(key=lambda x: x["timestamp"], reverse=True)
        return timeline[:limit]

    def get_validation_trends(self, db: Session, source_id: Optional[uuid.UUID] = None, limit: int = 50) -> List[Dict[str, Any]]:
        query = db.query(ValidationResult, ScrapeRun).join(ScrapeRun, ValidationResult.scrape_run_id == ScrapeRun.id)
        if source_id:
            query = query.filter(ScrapeRun.source_id == source_id)

        rows = query.order_by(ScrapeRun.started_at.desc()).limit(limit).all()
        trends = []
        for val, run in rows:
            trends.append({
                "timestamp": run.started_at.isoformat(),
                "validation_score": float(val.validation_score) if val.validation_score else 0.0,
                "validation_status": val.validation_status,
                "schema_change_detected": val.schema_change_detected,
                "record_count_valid": val.record_count_valid,
                "records_found": run.records_found
            })
        trends.reverse()  # Oldest to newest for chronological chart plotting
        return trends

    def get_schema_history(self, db: Session, source_id: uuid.UUID, limit: int = 20) -> List[Dict[str, Any]]:
        query = db.query(ValidationResult, ScrapeRun).join(
            ScrapeRun, ValidationResult.scrape_run_id == ScrapeRun.id
        ).filter(ScrapeRun.source_id == source_id).order_by(ScrapeRun.started_at.desc()).limit(limit)

        history = []
        for val, run in query.all():
            issues = val.issues or []
            schema_issues = [i for i in issues if i.get("type") == "schema_change"]
            fingerprint = "default_schema"
            if schema_issues and "fingerprint" in schema_issues[0]:
                fingerprint = schema_issues[0]["fingerprint"]

            history.append({
                "timestamp": run.started_at.isoformat(),
                "run_id": str(run.id),
                "schema_fingerprint": fingerprint,
                "schema_change_detected": val.schema_change_detected,
                "issues": schema_issues
            })
        return history

metrics_service = MetricsService()
