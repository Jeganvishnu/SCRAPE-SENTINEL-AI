import os
import sys

backend_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if backend_root not in sys.path:
    sys.path.insert(0, backend_root)

from app.validators.engine import validation_engine
from app.validators.anomaly_detector import detect_record_count_anomalies
from app.validators.schema_validator import detect_schema_changes

def run_failure_simulation():
    print("=== PHASE 4 CONTROLLED FAILURE SIMULATION ===")

    # 1. Schema Drift Test Fixture
    healthy_record = [{
        "title": "v2.1.0 Released",
        "published_date": "2026-08-20",
        "version": "2.1.0",
        "category": "Release",
        "description": "New features",
        "url": "https://supabase.com/changelog/2-1-0"
    }]

    changed_record = [{
        "title": "v2.1.0 Released",
        "date": "2026-08-20",  # 'published_date' renamed/removed -> 'date' added
        "category": "Release",
        "url": "https://supabase.com/changelog/2-1-0"
    }]

    schema_valid, schema_changed, fingerprint, issues = detect_schema_changes(changed_record)
    print(f"1. Schema Change Test -> Detected: {schema_changed} (Expected: True)")
    assert schema_changed is True, "Schema change detection failed!"

    # 2. Record Count Drop Test Fixture (Healthy = 100, Current = 40)
    count_valid, count_issues = detect_record_count_anomalies(
        current_count=40,
        baseline_recent_counts=[100, 100, 100]
    )
    print(f"2. Record Count Drop Test -> Valid: {count_valid} (Expected: False), Issues: {count_issues[0]['type']}")
    assert count_valid is False, "Record count anomaly detection failed!"
    assert count_issues[0]["type"] == "record_count_drop"

    # 3. Complete Engine Evaluation against broken payload
    eval_res = validation_engine.evaluate(changed_record, baseline_recent_counts=[100, 100, 100])
    print(f"3. Overall Engine Status: {eval_res['validation_status']} (Score: {eval_res['validation_score']})")
    assert eval_res["validation_status"] == "failed"

    print("=== ALL FAILURE SIMULATIONS PASSED PERFECTLY ===")

if __name__ == "__main__":
    run_failure_simulation()
