from typing import Dict, Any
from app.ai.provider import BaseAIProvider

class MockAIProvider(BaseAIProvider):
    """
    Deterministic Mock AI Provider for testing, offline execution, and safe fallback.
    Produces high-quality structured evidence and repair plans.
    """

    ALLOWED_CATEGORIES = {
        "selector_changed", "schema_changed", "page_structure_changed",
        "missing_field", "renamed_field", "pagination_changed", "empty_result",
        "record_count_anomaly", "content_format_changed", "timeout", "rate_limit",
        "network_error", "authentication_required", "blocked_request", "validation_error", "unknown"
    }

    def analyze_failure(self, context: Dict[str, Any]) -> Dict[str, Any]:
        failure_type = context.get("failure_type", "unknown").lower()
        val_issues = context.get("validation_issues", [])

        # Check evidence from schema diff
        schema_diff = context.get("schema_diff", {})
        added = schema_diff.get("added_fields", [])
        removed = schema_diff.get("removed_fields", [])

        if "schema" in failure_type or removed or added:
            category = "schema_changed"
            confidence = 0.92
            cause = f"Schema structural drift detected: Removed fields {removed}, Added fields {added}."
            evidence = [
                f"Validation detected field drift: {removed} removed",
                f"New target structure introduces fields {added}",
                "Record count remains stable across runs"
            ]
            action = "Update schema mapping to adapt to renamed or modified fields."
            affected = removed if removed else ["title"]
        elif "missing" in failure_type or "required" in failure_type:
            category = "missing_field"
            confidence = 0.88
            cause = "Target page DOM selector mismatch resulting in missing required 'title' field."
            evidence = [
                "Extractor returned payload without required 'title' property",
                "Historical baseline contained valid text title for all records",
                "Page structure updated heading tags"
            ]
            action = "Update CSS/DOM selector for target field 'title'."
            affected = ["title"]
        elif "empty" in failure_type or context.get("records_found", 0) == 0:
            category = "empty_result"
            confidence = 0.95
            cause = "Extractor returned 0 records due to target container selector change."
            evidence = [
                "Scrape output payload is an empty array (0 records)",
                "Target URL remains accessible HTTP 200",
                "Container element class changed on target site"
            ]
            action = "Re-target main container selector for item list."
            affected = ["all"]
        else:
            category = "selector_changed"
            confidence = 0.85
            cause = f"Page layout change triggered extraction failure: {failure_type}."
            evidence = [
                f"Validation issue: {val_issues[0] if val_issues else failure_type}",
                "Historical schema fingerprint mismatch",
                "Extraction failed to extract full record object"
            ]
            action = "Update DOM selector mapping."
            affected = ["title", "published_date"]

        return {
            "failure_category": category,
            "confidence": confidence,
            "root_cause": cause,
            "evidence": evidence,
            "affected_fields": affected,
            "severity": context.get("severity", "high"),
            "recommended_action": action
        }

    def generate_repair_plan(self, diagnosis: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        cat = diagnosis.get("failure_category", "selector_changed")
        conf = float(diagnosis.get("confidence", 0.85))

        if cat == "schema_changed":
            repair_type = "field_mapping_update"
            risk = "low" if conf >= 0.85 else "medium"
            changes = [{"field": "title", "action": "remap", "new_key": "header_title"}]
            reason = "Remap renamed title selector to match target schema drift."
        elif cat in ("missing_field", "selector_changed"):
            repair_type = "selector_update"
            risk = "low" if conf >= 0.85 else "medium"
            changes = [{"field": "title", "selector": "[data-title]"}]
            reason = "Update DOM selector for target field to match new site structure."
        elif cat == "empty_result":
            repair_type = "selector_update"
            risk = "medium"
            changes = [{"container": "article.changelog-card"}]
            reason = "Update item container selector to match target layout."
        else:
            repair_type = "normalization_update"
            risk = "low"
            changes = [{"action": "trim_whitespace"}]
            reason = "Apply normalization fallback rule."

        return {
            "repair_type": repair_type,
            "target": context.get("source_name", "target_source"),
            "changes": changes,
            "reason": reason,
            "confidence": conf,
            "risk": risk,
            "verification_required": True
        }
