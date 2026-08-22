# Validation Engine & Failure Detection Architecture

## Overview
Scrape Sentinel AI introduces a real-time **Validation Engine** that evaluates structured outputs from Bright Data Scraper Studio custom collectors before persisting data or triggering downstream tasks.

```
REAL BRIGHT DATA SCRAPER
          ↓
RAW OUTPUT
          ↓
NORMALIZATION
          ↓
VALIDATION ENGINE
          ↓
VALIDATION RESULT
          ↓
       ┌──┴──┐
       ↓     ↓
     VALID  FAILED
       ↓     ↓
   DATABASE  FAILURE EVENT
                ↓
          HEALING QUEUE
                ↓
        PHASE 5 WILL HEAL
```

---

## 1. Validation Rules & Criteria

### A. Required Field Validation
For every extracted record, the following fields are strictly mandatory:
- `title`: Must be a non-empty string.
- `url`: Must be a syntactically valid HTTP/HTTPS URL.
- `content_hash`: Must be a valid 64-character SHA-256 string.
- `scraped_at`: Must be present as a ISO-8601 timestamp.

If any required field is missing or invalid:
- `required_fields_valid = false`
- Validation issue logged with severity `high` or `critical`.

### B. URL Syntax Rules
URLs are validated for syntax (`http://` or `https://` scheme, valid domain/hostname format) without incurring live network requests during evaluation.

### C. Date Validation
If `published_date` is present, it is validated for ISO-8601 format and normalized to UTC. Absence of an optional date field does not trigger total run failure.

### D. Duplicate Detection
Duplicate records within a single scrape run are identified by matching deterministic `content_hash` strings:
- Issue type: `duplicate_records`
- Severity: `medium`

### E. Empty Result Detection
An extraction payload returning `0` records triggers:
- Issue type: `empty_result`
- Severity: `critical`
- Validation status: `failed`

### F. Record-Count Anomaly Algorithm
The engine maintains a historical baseline of recent healthy runs for each source:
- If current record count drops by `> 50%` compared to the historical average baseline:
  - Issue type: `record_count_drop`
  - Severity: `high`
  - `record_count_valid = false`

### G. Schema Fingerprinting & Drift Detection
A deterministic 16-character SHA-256 fingerprint is calculated over the set of observed JSON keys:
- `compute_schema_fingerprint(fields)`
- If expected keys are missing or unexpected keys appear:
  - `schema_change_detected = true`
  - Issue details record `removed_fields` and `added_fields`.

---

## 2. Transparent Validation Score (0–100)

The validation score is calculated using the following transparent formula:

| Component | Max Points |
| :--- | :--- |
| **Required Fields Valid** | 30.0 pts |
| **URL Validity** | 15.0 pts |
| **Date Validity** | 10.0 pts |
| **Duplicate-Free** | 15.0 pts |
| **Record Count Valid** | 15.0 pts |
| **Schema Stability** | 15.0 pts |
| **Total Maximum Score** | **100.0 pts** |

---

## 3. Decision Matrix (PASS / WARNING / FAILED)

- **PASSED**: Validation Score `≥ 85.0` AND no `critical` or `high` severity issues.
- **WARNING**: Validation Score `70.0–84.9` OR minor optional field anomalies (no critical/high issues).
- **FAILED**: Validation Score `< 70.0` OR presence of `critical`/`high` severity issues (e.g. empty result, missing title, schema drift).

> **Note on Healing:** Automatic self-healing reruns are intentionally **not** triggered in Phase 4. Detected failures are logged to `failure_events` and queued for Phase 5 self-healing.
