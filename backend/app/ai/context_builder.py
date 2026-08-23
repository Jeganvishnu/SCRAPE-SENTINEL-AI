import uuid
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session

from app.models.source import Source
from app.models.scrape_run import ScrapeRun
from app.models.scraped_record import ScrapedRecord
from app.models.validation_result import ValidationResult
from app.models.failure_event import FailureEvent
from app.models.healing_attempt import HealingAttempt

class FailureContextBuilder:
    def build_context(self, db: Session, failure_event_id: uuid.UUID) -> Optional[Dict[str, Any]]:
        fail_event = db.query(FailureEvent).filter(FailureEvent.id == failure_event_id).first()
        if not fail_event:
            return None

        source = db.query(Source).filter(Source.id == fail_event.source_id).first()
        scrape_run = db.query(ScrapeRun).filter(ScrapeRun.id == fail_event.scrape_run_id).first()
        val_result = db.query(ValidationResult).filter(ValidationResult.scrape_run_id == fail_event.scrape_run_id).first()

        # Previous successful sample
        prev_success_run = db.query(ScrapeRun).filter(
            ScrapeRun.source_id == fail_event.source_id,
            ScrapeRun.status == "success"
        ).order_by(ScrapeRun.started_at.desc()).first()

        successful_sample = {}
        if prev_success_run:
            rec = db.query(ScrapedRecord).filter(ScrapedRecord.scrape_run_id == prev_success_run.id).first()
            if rec:
                successful_sample = {
                    "title": rec.title,
                    "published_date": rec.published_date,
                    "category": rec.category,
                    "url": rec.url
                }

        # Failed sample record if present
        failed_sample = {}
        if scrape_run:
            f_rec = db.query(ScrapedRecord).filter(ScrapedRecord.scrape_run_id == scrape_run.id).first()
            if f_rec:
                failed_sample = {
                    "title": f_rec.title,
                    "published_date": f_rec.published_date,
                    "category": f_rec.category,
                    "url": f_rec.url
                }

        # Deterministic schema diff calculation
        schema_diff = self._calculate_schema_diff(successful_sample, failed_sample)

        # Historical failure frequency
        hist_fail_count = db.query(FailureEvent).filter(FailureEvent.source_id == fail_event.source_id).count()

        # Repeat healing attempts for loop protection
        heal_attempts_count = db.query(HealingAttempt).filter(
            HealingAttempt.source_id == fail_event.source_id,
            HealingAttempt.failure_event_id == fail_event.id
        ).count()

        return {
            "failure_event_id": str(fail_event.id),
            "source_id": str(fail_event.source_id),
            "source_name": source.name if source else "Unknown Target",
            "source_url": source.url if source else "",
            "collector_id": source.collector_id if source else "c_mt46lngz2asqzj8tkj",
            "scrape_run_id": str(fail_event.scrape_run_id),
            "failure_type": fail_event.failure_type,
            "severity": fail_event.severity,
            "message": fail_event.message,
            "validation_score": val_result.validation_score if val_result else 0.0,
            "validation_issues": val_result.issues if val_result else [],
            "schema_diff": schema_diff,
            "successful_sample": successful_sample,
            "failed_sample": failed_sample,
            "records_found": scrape_run.records_found if scrape_run else 0,
            "historical_failure_count": hist_fail_count,
            "healing_attempts_count": heal_attempts_count
        }

    def _calculate_schema_diff(self, success_sample: Dict[str, Any], failed_sample: Dict[str, Any]) -> Dict[str, Any]:
        s_keys = set(k for k, v in success_sample.items() if v)
        f_keys = set(k for k, v in failed_sample.items() if v)

        removed = list(s_keys - f_keys)
        added = list(f_keys - s_keys)
        unchanged = list(s_keys & f_keys)

        return {
            "removed_fields": removed,
            "added_fields": added,
            "unchanged_fields": unchanged
        }

context_builder = FailureContextBuilder()
