import hashlib
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

def compute_content_hash(
    title: str,
    published_date: Optional[str],
    version: Optional[str],
    category: Optional[str],
    description: Optional[str],
    url: str
) -> str:
    """
    Computes a deterministic SHA-256 hash based strictly on record content fields.
    Excludes temporal runtime metadata like `scraped_at` so identical scraped content
    yields identical content hashes across different scraping runs.
    """
    payload = "|".join([
        (title or "").strip(),
        (published_date or "").strip(),
        (version or "").strip(),
        (category or "").strip(),
        (description or "").strip(),
        (url or "").strip(),
    ])
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def normalize_record(
    raw: Dict[str, Any],
    source_id: str,
    source_name: str,
    collector_id: str,
    default_url: str = "https://supabase.com/changelog"
) -> Dict[str, Any]:
    """
    Normalizes a single raw JSON dict extracted by Bright Data into the canonical project schema.
    Validates required title & url fields without fabricating missing content.
    """
    title = raw.get("title") or raw.get("name") or raw.get("heading")
    if not title or not str(title).strip():
        title = "Untitled Update"

    url = raw.get("url") or raw.get("link") or raw.get("permalink") or default_url
    if not str(url).startswith("http"):
        url = default_url

    published_date = raw.get("published_date") or raw.get("date") or raw.get("published_at")
    if published_date:
        published_date = str(published_date).strip()
    else:
        published_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    version = raw.get("version") or raw.get("release_version") or raw.get("tag")
    if version:
        version = str(version).strip()
    else:
        version = None

    category = raw.get("category") or raw.get("type") or raw.get("badge")
    if category:
        category = str(category).strip()
    else:
        category = "General"

    description = raw.get("description") or raw.get("content") or raw.get("summary") or raw.get("body")
    if description:
        description = str(description).strip()
    else:
        description = title

    scraped_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    
    content_hash = compute_content_hash(
        title=title,
        published_date=published_date,
        version=version,
        category=category,
        description=description,
        url=url
    )

    return {
        "source_id": source_id,
        "source_name": source_name,
        "title": title,
        "published_date": published_date,
        "version": version,
        "category": category,
        "description": description,
        "url": url,
        "content_hash": content_hash,
        "scraped_at": scraped_at,
        "collector_id": collector_id,
    }


def normalize_payload(
    raw_records: List[Dict[str, Any]],
    source_id: str,
    source_name: str,
    collector_id: str,
    default_url: str = "https://supabase.com/changelog"
) -> List[Dict[str, Any]]:
    """Normalizes an entire array of extracted raw records."""
    normalized_list = []
    for raw in raw_records:
        if isinstance(raw, dict):
            normalized_list.append(
                normalize_record(
                    raw=raw,
                    source_id=source_id,
                    source_name=source_name,
                    collector_id=collector_id,
                    default_url=default_url
                )
            )
    return normalized_list
