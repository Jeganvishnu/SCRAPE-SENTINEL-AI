from typing import Any, Dict, List, Tuple

def detect_duplicates(records: List[Dict[str, Any]]) -> Tuple[bool, List[Dict[str, Any]]]:
    """
    Detects duplicate content_hash values within a single scrape run extraction array.
    Returns: (duplicate_free, issues_list)
    """
    seen_hashes: Dict[str, int] = {}
    issues = []
    duplicate_free = True

    for rec in records:
        h = rec.get("content_hash")
        if h:
            seen_hashes[h] = seen_hashes.get(h, 0) + 1

    for h, count in seen_hashes.items():
        if count > 1:
            duplicate_free = False
            issues.append({
                "type": "duplicate_records",
                "content_hash": h,
                "count": count,
                "severity": "medium",
                "message": f"Detected {count} duplicate records sharing content_hash '{h[:12]}...'."
            })

    return duplicate_free, issues


def detect_record_count_anomalies(
    current_count: int,
    baseline_recent_counts: List[int],
    drop_threshold_pct: float = 0.50
) -> Tuple[bool, List[Dict[str, Any]]]:
    """
    Detects empty results or significant record count drops (> 50%) compared to historical baseline.
    Returns: (record_count_valid, issues_list)
    """
    issues = []
    record_count_valid = True

    if current_count == 0:
        return False, [{
            "type": "empty_result",
            "severity": "critical",
            "message": "Bright Data collector returned 0 extracted records."
        }]

    if not baseline_recent_counts:
        return True, []

    # Calculate average baseline of recent successful runs
    avg_baseline = sum(baseline_recent_counts) / len(baseline_recent_counts)
    
    # Noise guard for small baseline counts
    if avg_baseline < 4:
        return True, []

    expected_min = avg_baseline * (1.0 - drop_threshold_pct)
    if current_count < expected_min:
        record_count_valid = False
        issues.append({
            "type": "record_count_drop",
            "severity": "high",
            "current_count": current_count,
            "baseline_avg": round(avg_baseline, 1),
            "drop_pct": round((1.0 - (current_count / avg_baseline)) * 100, 1),
            "message": f"Record count dropped by {round((1.0 - (current_count / avg_baseline)) * 100, 1)}% (current: {current_count}, baseline avg: {round(avg_baseline, 1)})."
        })

    return record_count_valid, issues
