import uuid
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.source import Source
from app.models.scrape_run import ScrapeRun
from app.models.scraped_record import ScrapedRecord
from app.models.validation_result import ValidationResult
from app.models.failure_event import FailureEvent
from app.models.healing_attempt import HealingAttempt

class HealthService:
    def parse_time_window(self, period: str = "7d") -> Optional[datetime]:
        now = datetime.now(timezone.utc)
        if period == "24h":
            return now - timedelta(hours=24)
        elif period == "7d":
            return now - timedelta(days=7)
        elif period == "30d":
            return now - timedelta(days=30)
        elif period == "all":
            return None
        return now - timedelta(days=7)

    def calculate_success_rate(self, db: Session, source_id: Optional[uuid.UUID] = None, since: Optional[datetime] = None) -> float:
        query = db.query(ScrapeRun)
        if source_id:
            query = query.filter(ScrapeRun.source_id == source_id)
        if since:
            query = query.filter(ScrapeRun.started_at >= since)

        total = query.count()
        if total == 0:
            return 100.0

        successes = query.filter(ScrapeRun.status == "success").count()
        return round((successes / total) * 100.0, 2)

    def calculate_avg_validation_score(self, db: Session, source_id: Optional[uuid.UUID] = None, since: Optional[datetime] = None) -> float:
        query = db.query(func.avg(ValidationResult.validation_score)).join(
            ScrapeRun, ValidationResult.scrape_run_id == ScrapeRun.id
        )
        if source_id:
            query = query.filter(ScrapeRun.source_id == source_id)
        if since:
            query = query.filter(ScrapeRun.started_at >= since)

        result = query.scalar()
        return round(float(result), 2) if result is not None else 100.0

    def calculate_recovery_metrics(self, db: Session, source_id: Optional[uuid.UUID] = None, since: Optional[datetime] = None) -> Tuple[Optional[float], Optional[float]]:
        """
        Calculates (recovery_rate_pct, mttr_seconds).
        Returns (None, None) if zero healing attempts exist.
        """
        query = db.query(HealingAttempt)
        if source_id:
            query = query.filter(HealingAttempt.source_id == source_id)
        if since:
            query = query.filter(HealingAttempt.started_at >= since)

        total_attempts = query.count()
        if total_attempts == 0:
            return None, None

        verified_attempts = query.filter(HealingAttempt.status == "verified").all()
        recovery_rate = round((len(verified_attempts) / total_attempts) * 100.0, 2)

        mttr_seconds = None
        if verified_attempts:
            durations = []
            for h in verified_attempts:
                if h.completed_at and h.started_at:
                    durations.append((h.completed_at - h.started_at).total_seconds())
            if durations:
                mttr_seconds = round(sum(durations) / len(durations), 1)

        return recovery_rate, mttr_seconds

    def calculate_health_score_and_state(
        self,
        db: Session,
        source_id: Optional[uuid.UUID] = None,
        period: str = "7d"
    ) -> Tuple[float, str, str]:
        since = self.parse_time_window(period)

        # 1. Component Metrics
        sr = self.calculate_success_rate(db, source_id, since)
        vq = self.calculate_avg_validation_score(db, source_id, since)
        rec_rate, mttr = self.calculate_recovery_metrics(db, source_id, since)

        # Active failure check
        fail_query = db.query(FailureEvent).filter(FailureEvent.status == "open")
        if source_id:
            fail_query = fail_query.filter(FailureEvent.source_id == source_id)
        open_failures = fail_query.all()
        critical_open = any(f.severity in ("critical", "high") for f in open_failures)

        # Schema drift check
        val_query = db.query(ValidationResult).join(ScrapeRun, ValidationResult.scrape_run_id == ScrapeRun.id)
        if source_id:
            val_query = val_query.filter(ScrapeRun.source_id == source_id)
        if since:
            val_query = val_query.filter(ScrapeRun.started_at >= since)
        recent_vals = val_query.limit(10).all()

        schema_drift_count = sum(1 for v in recent_vals if v.schema_change_detected)
        schema_stability = max(0.0, 100.0 - (schema_drift_count * 20.0))

        count_anomaly_count = sum(1 for v in recent_vals if not v.record_count_valid)
        count_stability = max(0.0, 100.0 - (count_anomaly_count * 25.0))

        failure_stability = 0.0 if critical_open else (70.0 if open_failures else 100.0)
        effective_rec_rate = rec_rate if rec_rate is not None else 100.0

        # Weighted Score Formula
        score = (
            (sr * 0.25) +
            (vq * 0.20) +
            (failure_stability * 0.15) +
            (effective_rec_rate * 0.15) +
            (count_stability * 0.10) +
            (schema_stability * 0.10) +
            (100.0 * 0.05)  # Execution reliability baseline
        )
        score = round(min(100.0, max(0.0, score)), 2)

        # State Determination
        if critical_open and sr < 50.0:
            state = "critical"
            explanation = f"Critical failures unresolved and success rate at {sr}%. Urgent attention required."
        elif critical_open or sr < 75.0 or vq < 70.0:
            state = "degraded"
            explanation = f"Pipeline degraded. Active failures or low validation score ({vq}/100)."
        elif open_failures or vq < 85.0:
            state = "warning"
            explanation = f"Minor warnings present. Validation score is {vq}/100."
        else:
            state = "healthy"
            explanation = f"Scraper healthy. {sr}% success rate, validation score {vq}/100, and zero active failures."

        return score, state, explanation

health_service = HealthService()
