import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List
from sqlalchemy.orm import Session
from app.models.scraped_record import ScrapedRecord

class RecordService:
    def bulk_insert(
        self,
        db: Session,
        source_id: uuid.UUID,
        scrape_run_id: uuid.UUID,
        normalized_records: List[Dict[str, Any]]
    ) -> List[ScrapedRecord]:
        db_records = []
        for rec in normalized_records:
            pub_date_raw = rec.get("published_date")
            pub_date_dt = None
            if pub_date_raw:
                try:
                    pub_date_dt = datetime.fromisoformat(str(pub_date_raw).replace("Z", "+00:00"))
                except ValueError:
                    pub_date_dt = None

            scraped_at_raw = rec.get("scraped_at")
            scraped_at_dt = datetime.now(timezone.utc)
            if scraped_at_raw:
                try:
                    scraped_at_dt = datetime.fromisoformat(str(scraped_at_raw).replace("Z", "+00:00"))
                except ValueError:
                    pass

            db_record = ScrapedRecord(
                source_id=source_id,
                scrape_run_id=scrape_run_id,
                title=rec.get("title"),
                published_date=pub_date_dt,
                version=rec.get("version"),
                category=rec.get("category"),
                description=rec.get("description"),
                url=rec.get("url"),
                content_hash=rec.get("content_hash"),
                scraped_at=scraped_at_dt,
                raw_data=rec
            )
            db_records.append(db_record)

        if db_records:
            db.bulk_save_objects(db_records)
            db.commit()
        return db_records

record_service = RecordService()
