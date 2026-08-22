import pytest
from app.services.normalizer import compute_content_hash, normalize_record, normalize_payload

def test_compute_content_hash_deterministic():
    hash1 = compute_content_hash(
        title="Read replicas moved",
        published_date="2026-08-21",
        version=None,
        category="Improvement",
        description="Read replica management now lives on Project Settings",
        url="https://supabase.com/changelog/read-replicas-moved"
    )
    hash2 = compute_content_hash(
        title="Read replicas moved",
        published_date="2026-08-21",
        version=None,
        category="Improvement",
        description="Read replica management now lives on Project Settings",
        url="https://supabase.com/changelog/read-replicas-moved"
    )
    assert hash1 == hash2
    assert len(hash1) == 64  # SHA-256 length

def test_compute_content_hash_different_content():
    hash1 = compute_content_hash("Title A", "2026-08-21", None, "Improvement", "Desc A", "https://supabase.com/changelog/a")
    hash2 = compute_content_hash("Title B", "2026-08-21", None, "Improvement", "Desc B", "https://supabase.com/changelog/b")
    assert hash1 != hash2

def test_normalize_record_complete():
    raw = {
        "title": "Read replicas moved",
        "published_date": "2026-08-21",
        "category": "Improvement",
        "description": "Read replica management now lives on Project Settings",
        "url": "https://supabase.com/changelog/read-replicas-moved"
    }
    normalized = normalize_record(
        raw=raw,
        source_id="supabase_changelog",
        source_name="Supabase Changelog",
        collector_id="c_test12345",
        default_url="https://supabase.com/changelog"
    )

    assert normalized["source_id"] == "supabase_changelog"
    assert normalized["title"] == "Read replicas moved"
    assert normalized["published_date"] == "2026-08-21"
    assert normalized["category"] == "Improvement"
    assert normalized["collector_id"] == "c_test12345"
    assert normalized["content_hash"] is not None
    assert normalized["scraped_at"] is not None

def test_normalize_record_missing_optional_fields():
    raw = {
        "name": "Quick Fix Update"
    }
    normalized = normalize_record(
        raw=raw,
        source_id="supabase_changelog",
        source_name="Supabase Changelog",
        collector_id="c_test12345"
    )

    assert normalized["title"] == "Quick Fix Update"
    assert normalized["version"] is None
    assert normalized["category"] == "General"
    assert normalized["url"] == "https://supabase.com/changelog"

def test_normalize_payload_array():
    raw_list = [
        {"title": "Update 1", "url": "https://supabase.com/changelog/1"},
        {"title": "Update 2", "url": "https://supabase.com/changelog/2"},
    ]
    normalized_list = normalize_payload(
        raw_records=raw_list,
        source_id="supabase_changelog",
        source_name="Supabase Changelog",
        collector_id="c_test12345"
    )

    assert len(normalized_list) == 2
    assert normalized_list[0]["title"] == "Update 1"
    assert normalized_list[1]["title"] == "Update 2"
