import pytest
from app.validators.record_validator import validate_records, validate_url_syntax
from app.validators.anomaly_detector import detect_duplicates, detect_record_count_anomalies
from app.validators.schema_validator import detect_schema_changes, compute_schema_fingerprint
from app.validators.engine import validation_engine

def test_url_syntax_validator():
    assert validate_url_syntax("https://supabase.com/changelog") is True
    assert validate_url_syntax("http://localhost:8000") is True
    assert validate_url_syntax("ftp://invalid.com") is False
    assert validate_url_syntax("not-a-url") is False
    assert validate_url_syntax("") is False

def test_valid_record_evaluation():
    records = [{
        "title": "Supabase Auth Update",
        "url": "https://supabase.com/changelog/auth-update",
        "content_hash": "a" * 64,
        "scraped_at": "2026-08-22T09:00:00Z",
        "published_date": "2026-08-20T00:00:00Z",
        "version": "v2.4.0",
        "category": "Security",
        "description": "Improved Auth rate limits"
    }]

    eval_res = validation_engine.evaluate(records)
    assert eval_res["validation_status"] == "passed"
    assert eval_res["validation_score"] == 100.0
    assert eval_res["required_fields_valid"] is True
    assert eval_res["schema_change_detected"] is False

def test_missing_required_title():
    records = [{
        "title": "",
        "url": "https://supabase.com/changelog/test",
        "content_hash": "b" * 64,
        "scraped_at": "2026-08-22T09:00:00Z"
    }]
    eval_res = validation_engine.evaluate(records)
    assert eval_res["required_fields_valid"] is False
    assert eval_res["validation_status"] == "failed"
    assert any(i["type"] == "required_field_missing" for i in eval_res["issues"])

def test_invalid_url_record():
    records = [{
        "title": "Valid Title",
        "url": "bad-url-syntax",
        "content_hash": "c" * 64,
        "scraped_at": "2026-08-22T09:00:00Z"
    }]
    eval_res = validation_engine.evaluate(records)
    assert eval_res["url_valid"] is False
    assert any(i["type"] == "invalid_url" for i in eval_res["issues"])

def test_duplicate_records_detection():
    hash_val = "d" * 64
    records = [
        {"title": "T1", "url": "https://example.com/1", "content_hash": hash_val, "scraped_at": "2026-08-22T09:00:00Z"},
        {"title": "T1 Duplicate", "url": "https://example.com/1", "content_hash": hash_val, "scraped_at": "2026-08-22T09:00:00Z"}
    ]
    dup_free, issues = detect_duplicates(records)
    assert dup_free is False
    assert len(issues) == 1
    assert issues[0]["type"] == "duplicate_records"

def test_empty_result_detection():
    eval_res = validation_engine.evaluate([])
    assert eval_res["validation_status"] == "failed"
    assert eval_res["validation_score"] == 0.0
    assert any(i["type"] == "empty_result" for i in eval_res["issues"])

def test_record_count_drop_anomaly():
    # Baseline avg = 100, current = 40 (60% drop)
    count_valid, issues = detect_record_count_anomalies(
        current_count=40,
        baseline_recent_counts=[100, 100, 100]
    )
    assert count_valid is False
    assert len(issues) == 1
    assert issues[0]["type"] == "record_count_drop"
    assert issues[0]["severity"] == "high"

def test_schema_change_detection():
    # Record missing 'title' field entirely (key removed)
    records = [{
        "published_date": "2026-08-22",
        "url": "https://supabase.com/changelog/1"
    }]
    schema_valid, schema_changed, fingerprint, issues = detect_schema_changes(records)
    assert schema_changed is True
    assert any(i["type"] == "schema_change" for i in issues)

def test_schema_fingerprint_determinism():
    fields_1 = {"title", "url", "description"}
    fields_2 = {"description", "title", "url"}
    assert compute_schema_fingerprint(fields_1) == compute_schema_fingerprint(fields_2)
