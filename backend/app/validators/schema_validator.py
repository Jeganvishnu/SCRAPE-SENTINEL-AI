import hashlib
from typing import Any, Dict, List, Set, Tuple

EXPECTED_SCHEMA_FIELDS: Set[str] = {
    "title", "published_date", "version", "category", "description", "url"
}

def compute_schema_fingerprint(fields: Set[str]) -> str:
    """Computes a deterministic SHA-256 fingerprint based on present field names."""
    sorted_fields = "|".join(sorted(fields))
    return hashlib.sha256(sorted_fields.encode("utf-8")).hexdigest()[:16]


def detect_schema_changes(
    records: List[Dict[str, Any]],
    expected_fields: Set[str] = EXPECTED_SCHEMA_FIELDS
) -> Tuple[bool, bool, str, List[Dict[str, Any]]]:
    """
    Analyzes normalized records for field presence, schema fingerprinting, and structural drift.
    Returns: (schema_valid, schema_change_detected, schema_fingerprint, issues_list)
    """
    if not records:
        return False, True, "empty", [{
            "type": "schema_change",
            "severity": "critical",
            "message": "Cannot perform schema validation: 0 records present."
        }]

    # Collect set of all present keys across records
    observed_fields: Set[str] = set()
    for rec in records:
        if isinstance(rec, dict):
            observed_fields.update(rec.keys())

    fingerprint = compute_schema_fingerprint(observed_fields)

    # Core target fields check
    missing_core = expected_fields - observed_fields
    added_new = observed_fields - expected_fields - {"source_id", "source_name", "content_hash", "scraped_at", "collector_id", "raw_data"}

    schema_change_detected = len(missing_core) > 0 or len(added_new) > 0
    schema_valid = not ("title" in missing_core or "url" in missing_core)

    issues = []
    if schema_change_detected:
        severity = "high" if ("title" in missing_core or "url" in missing_core) else "medium"
        issues.append({
            "type": "schema_change",
            "severity": severity,
            "removed_fields": list(missing_core),
            "added_fields": list(added_new),
            "fingerprint": fingerprint,
            "message": f"Schema change detected! Removed fields: {list(missing_core)}, Added fields: {list(added_new)}."
        })

    return schema_valid, schema_change_detected, fingerprint, issues
