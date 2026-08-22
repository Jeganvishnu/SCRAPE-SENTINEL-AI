from typing import Any, Dict, List
from app.validators.record_validator import validate_records
from app.validators.anomaly_detector import detect_duplicates, detect_record_count_anomalies
from app.validators.schema_validator import detect_schema_changes

class ValidationEngine:
    def evaluate(
        self,
        records: List[Dict[str, Any]],
        baseline_recent_counts: List[int] = None
    ) -> Dict[str, Any]:
        """
        Orchestrates mandatory validations, structural anomaly checks, transparent scoring,
        and failure event generation for scraped payload runs.
        """
        all_issues = []

        # 1. Empty Result Check
        if not records:
            all_issues.append({
                "type": "empty_result",
                "severity": "critical",
                "message": "Bright Data collector returned 0 extracted records."
            })
            return {
                "validation_status": "failed",
                "validation_score": 0.0,
                "schema_valid": False,
                "required_fields_valid": False,
                "url_valid": False,
                "date_valid": False,
                "duplicate_free": True,
                "record_count_valid": False,
                "schema_change_detected": True,
                "issues": all_issues
            }

        # 2. Record & Field Validations
        req_valid, url_valid, date_valid, rec_issues = validate_records(records)
        all_issues.extend(rec_issues)

        # 3. Duplicate Detection
        dup_free, dup_issues = detect_duplicates(records)
        all_issues.extend(dup_issues)

        # 4. Record Count Anomaly Detection
        count_valid, count_issues = detect_record_count_anomalies(
            current_count=len(records),
            baseline_recent_counts=baseline_recent_counts or []
        )
        all_issues.extend(count_issues)

        # 5. Schema Change & Fingerprinting
        schema_valid, schema_change, fingerprint, schema_issues = detect_schema_changes(records)
        all_issues.extend(schema_issues)

        # 6. Transparent Scoring Calculation
        score = 0.0
        if req_valid: score += 30.0
        if url_valid: score += 15.0
        if date_valid: score += 10.0
        if dup_free: score += 15.0
        if count_valid: score += 15.0
        if not schema_change: score += 15.0

        # 7. Decision Matrix
        has_critical_or_high = any(
            iss.get("severity") in ("critical", "high") for iss in all_issues
        )

        if score >= 85.0 and not has_critical_or_high:
            validation_status = "passed"
        elif score >= 70.0 and not has_critical_or_high:
            validation_status = "warning"
        else:
            validation_status = "failed"

        return {
            "validation_status": validation_status,
            "validation_score": round(score, 2),
            "schema_valid": schema_valid,
            "required_fields_valid": req_valid,
            "url_valid": url_valid,
            "date_valid": date_valid,
            "duplicate_free": dup_free,
            "record_count_valid": count_valid,
            "schema_change_detected": schema_change,
            "schema_fingerprint": fingerprint,
            "issues": all_issues
        }

validation_engine = ValidationEngine()
