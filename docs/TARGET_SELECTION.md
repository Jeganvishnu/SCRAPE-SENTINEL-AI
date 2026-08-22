# Scrape Sentinel AI — Target Website Selection & Schema Specification

> **Phase:** 1 — Target Selection & Scraped Data Schema  
> **Use Case:** Public Technology / Product Change Intelligence

---

## 1. Candidate Website Evaluations

### Candidate 1: Supabase Product Changelog (PRIMARY TARGET)

- **Name:** Supabase Product Changelog
- **URL:** `https://supabase.com/changelog`
- **What public information is available:** Detailed product update titles, release dates, categories/tags (Database, Auth, Storage, Realtime, Studio, Edge Functions, Platform), release notes text, breaking change markers, and direct permalinks (`/changelog/<slug>`).
- **Why it is useful:** High-impact developer infrastructure changelog. Enables automated intelligence on database improvements, breaking API changes, and feature additions for developer operations teams.
- **Expected fields:** `title`, `published_date`, `version`, `category`, `description`, `url`, `source_id`, `source_name`, `content_hash`, `scraped_at`, `collector_id`
- **Publicly accessible:** YES
- **Login required:** NO
- **Paywall:** NO
- **Government website:** NO
- **Personal/private data required:** NO
- **Suitable for custom Scraper Studio scraper:** YES
- **Likely already covered by Bright Data pre-built scraper:** UNKNOWN *(Must be marked UNKNOWN as library coverage cannot be verified from local sandbox)*
- **Reason:** Clean, semantic HTML layout with structured RSS feeds, distinct category badges, and deep link anchors. Ideal for demonstrating deterministic extraction validation and layout change failure detection.
- **Risk level:** LOW

---

### Candidate 2: Vercel Platform Changelog (BACKUP TARGET)

- **Name:** Vercel Platform Changelog
- **URL:** `https://vercel.com/changelog`
- **What public information is available:** Cloud platform product updates, Next.js feature announcements, deployment optimization notes, publish dates, and feature categories.
- **Why it is useful:** Excellent public source for tracking cloud deployment platform evolution and frontend stack improvements.
- **Expected fields:** `title`, `published_date`, `version`, `category`, `description`, `url`, `source_id`, `source_name`, `content_hash`, `scraped_at`, `collector_id`
- **Publicly accessible:** YES
- **Login required:** NO
- **Paywall:** NO
- **Government website:** NO
- **Personal/private data required:** NO
- **Suitable for custom Scraper Studio scraper:** YES
- **Likely already covered by Bright Data pre-built scraper:** UNKNOWN
- **Reason:** Modern Next.js rendered HTML structure with highly consistent update cards, providing an excellent backup target.
- **Risk level:** LOW

---

### Candidate 3: GitHub Product Changelog

- **Name:** GitHub Product Changelog
- **URL:** `https://github.blog/changelog/`
- **What public information is available:** Product release announcements across GitHub Enterprise, Actions, Security, and Copilot. Includes publish dates, tags, and summary articles.
- **Why it is useful:** Broad coverage of core developer tooling updates.
- **Expected fields:** `title`, `published_date`, `version`, `category`, `description`, `url`, `source_id`, `source_name`, `content_hash`, `scraped_at`, `collector_id`
- **Publicly accessible:** YES
- **Login required:** NO
- **Paywall:** NO
- **Government website:** NO
- **Personal/private data required:** NO
- **Suitable for custom Scraper Studio scraper:** YES
- **Likely already covered by Bright Data pre-built scraper:** UNKNOWN
- **Reason:** WordPress structured blog/changelog format with predictable HTML semantic tags.
- **Risk level:** LOW

---

### Candidate 4: Stripe Developer API Changelog

- **Name:** Stripe Developer API Changelog
- **URL:** `https://docs.stripe.com/changelog`
- **What public information is available:** API version upgrades, endpoint deprecation notices, parameter additions, and implementation guides.
- **Why it is useful:** Highly critical API breaking change tracking.
- **Expected fields:** `title`, `published_date`, `version`, `category`, `description`, `url`, `source_id`, `source_name`, `content_hash`, `scraped_at`, `collector_id`
- **Publicly accessible:** YES
- **Login required:** NO
- **Paywall:** NO
- **Government website:** NO
- **Personal/private data required:** NO
- **Suitable for custom Scraper Studio scraper:** YES
- **Likely already covered by Bright Data pre-built scraper:** UNKNOWN
- **Reason:** Structured documentation site with detailed breaking change tags.
- **Risk level:** LOW

---

## 2. Target Selection Summary

### PRIMARY TARGET
- **Name:** Supabase Product Changelog
- **URL:** `https://supabase.com/changelog`
- **Reason for Selection:** Provides the strongest combination of clear structured fields (`title`, `date`, `category`, `article_body`, `permalink`), stable public accessibility, high relevance to developer change intelligence, and clear DOM selectors suitable for a custom Bright Data Scraper Studio collector and controlled self-healing demonstration.
- **Compliance Assessment:** **100% COMPLIANT**. Fully public website, no login required, no paywall, non-government, contains zero PII/private data.

### BACKUP TARGET
- **Name:** Vercel Platform Changelog
- **URL:** `https://vercel.com/changelog`
- **Reason for Selection:** Reliable secondary source with identical field structure, ensuring pipeline fallback flexibility if needed.
- **Compliance Assessment:** **100% COMPLIANT**. Fully public, non-government, no authentication or personal data.

---

## 3. Normalized Scraped Data Schema

For the selected primary target (Supabase Changelog), every extracted record must normalize to the following schema:

```json
{
  "source_id": "supabase_changelog",
  "source_name": "Supabase Changelog",
  "title": "Read replicas moved to Project Settings → Infrastructure",
  "published_date": "2026-08-21",
  "version": "v1.2026.08",
  "category": "Improvement",
  "description": "Read replica management now lives on Project Settings → Infrastructure, next to compute and disk.",
  "url": "https://supabase.com/changelog/read-replicas-moved-to-infrastructure",
  "content_hash": "a4f8b2c1d9e3f7a5b1c9d8e2f4a6b0c3d5e7f9a1b3c5d7e9f1a3b5c7d9e1f3a5",
  "scraped_at": "2026-08-22T14:38:26Z",
  "collector_id": "c_m1abc123xyz"
}
```

### Detailed Field Definitions & Validation Rules

| Field Name | Data Type | Required / Optional | Field Description | Deterministic Validation Rule | Observed Example |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `source_id` | String | **Required** | Unique internal slug of data source | Must match regex `^[a-z0-9_]+$` and match active `sources.id`. | `"supabase_changelog"` |
| `source_name` | String | **Required** | Human-readable name of target site | Non-empty string, length 3..100 characters. | `"Supabase Changelog"` |
| `title` | String | **Required** | Title of the product release or changelog entry | Non-empty string, length 5..300 characters. | `"Read replicas moved to Project Settings → Infrastructure"` |
| `published_date` | String (ISO Date) | **Required** | Date the entry was published on the target site | Valid ISO 8601 date string (`YYYY-MM-DD`). | `"2026-08-21"` |
| `version` | String | Optional | Software version identifier if present | String or null. Default fallback `"N/A"`. | `"v1.2026.08"` |
| `category` | String | **Required** | Feature tag or update classification | Must be one of `["Improvement", "Bug Fix", "Breaking Change", "Feature", "Security", "General"]`. | `"Improvement"` |
| `description` | String | **Required** | Text content summary of the release note | Non-empty string, min length 10 characters. | `"Read replica management now lives on Project Settings..."` |
| `url` | String (URL) | **Required** | Permalink to the specific entry or source page | Must be valid HTTP/HTTPS URL starting with `https://`. | `"https://supabase.com/changelog/read-replicas-moved-to-infrastructure"` |
| `content_hash` | String (SHA-256) | **Required** | Hex hash of `title + published_date + description` | Exact 64-character hexadecimal SHA-256 string. | `"a4f8b2c1d9e3f7a5b1c9d8e2f4a6b0c3d5e7f9a1b3c5d7e9f1a3b5c7d9e1f3a5"` |
| `scraped_at` | String (ISO Datetime) | **Required** | UTC timestamp when record was extracted | Valid ISO 8601 UTC timestamp (`YYYY-MM-DDTHH:MM:SSZ`). | `"2026-08-22T14:38:26Z"` |
| `collector_id` | String | **Required** | Bright Data Scraper Studio Collector ID | Non-empty string starting with `c_` or matching Bright Data format. | `"c_m1abc123xyz"` |
