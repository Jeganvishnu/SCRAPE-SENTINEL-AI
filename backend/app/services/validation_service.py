import uuid
from typing import Any, Dict, Optional
from sqlalchemy.orm import Session
from app.models.validation_result import ValidationResult

class ValidationService:
    def create_result(
        self,
        db: Session,
        scrape_run_id: uuid.UUID,
        eval_data: Dict[str, Any]
    ) -> ValidationResult:
        result = ValidationResult(
            scrape_run_id=scrape_run_id,
            validation_status=eval_data["validation_status"],
            schema_valid=eval_data["schema_valid"],
            required_fields_valid=eval_data["required_fields_valid"],
            url_valid=eval_data["url_valid"],
            date_valid=eval_data["date_valid"],
            duplicate_free=eval_data["duplicate_free"],
            record_count_valid=eval_data["record_count_valid"],
            schema_change_detected=eval_data["schema_change_detected"],
            validation_score=eval_data["validation_score"],
            issues=eval_data.get("issues", [])
        )
        db.add(result)
        db.commit()
        db.refresh(result)
        return result

    def get_by_run_id(self, db: Session, scrape_run_id: uuid.UUID) -> Optional[ValidationResult]:
        return db.query(ValidationResult).filter(ValidationResult.scrape_run_id == scrape_run_id).first()

validation_service = ValidationService()
