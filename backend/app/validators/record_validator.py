import re
from datetime import datetime
from typing import Any, Dict, List, Tuple

URL_REGEX = re.compile(
    r"^https?://"
    r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|"
    r"localhost|"
    r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
    r"(?::\d+)?"
    r"(?:/?|[/?]\S+)$", re.IGNORECASE
)

def validate_url_syntax(url: str) -> bool:
    if not url or not isinstance(url, str):
        return False
    return bool(URL_REGEX.match(url.strip()))

def validate_records(records: List[Dict[str, Any]]) -> Tuple[bool, bool, bool, List[Dict[str, Any]]]:
    """
    Validates mandatory fields (title, url, content_hash, scraped_at) and syntaxes across normalized records.
    Returns: (required_fields_valid, url_valid, date_valid, issues_list)
    """
    issues = []
    required_valid = True
    urls_valid = True
    dates_valid = True

    for idx, rec in enumerate(records):
        # 1. Required Title
        title = rec.get("title")
        if not title or not str(title).strip() or str(title).strip() == "Untitled Update":
            required_valid = False
            issues.append({
                "type": "required_field_missing",
                "field": "title",
                "record_index": idx,
                "severity": "high",
                "message": f"Record #{idx} missing required non-empty 'title'."
            })

        # 2. Required URL
        url = rec.get("url")
        if not url or not validate_url_syntax(url):
            urls_valid = False
            issues.append({
                "type": "invalid_url",
                "field": "url",
                "record_index": idx,
                "severity": "high",
                "message": f"Record #{idx} contains invalid URL syntax: '{url}'."
            })

        # 3. Content Hash
        content_hash = rec.get("content_hash")
        if not content_hash or len(str(content_hash)) != 64:
            required_valid = False
            issues.append({
                "type": "required_field_missing",
                "field": "content_hash",
                "record_index": idx,
                "severity": "critical",
                "message": f"Record #{idx} missing or invalid SHA-256 'content_hash'."
            })

        # 4. Published Date (Optional but if present must be valid)
        pub_date = rec.get("published_date")
        if pub_date:
            try:
                if isinstance(pub_date, str):
                    datetime.fromisoformat(pub_date.replace("Z", "+00:00"))
            except ValueError:
                dates_valid = False
                issues.append({
                    "type": "invalid_date",
                    "field": "published_date",
                    "record_index": idx,
                    "severity": "medium",
                    "message": f"Record #{idx} contains unparseable date format: '{pub_date}'."
                })

    return required_valid, urls_valid, dates_valid, issues
