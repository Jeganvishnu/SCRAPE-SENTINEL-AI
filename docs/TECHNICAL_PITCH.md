# Scrape Sentinel AI — 3-Minute Technical Deep Dive for Judges

## 1. Core Problem Statement (0:00 – 0:30)
Web data pipelines suffer from DOM fragility. A simple class rename on a target website breaks CSS selectors, causing missing fields or zero records. Traditional systems either fail silently or require manual developer intervention.

---

## 2. Bright Data Scraper Studio Integration (0:30 – 1:00)
Scrape Sentinel AI uses **Bright Data Scraper Studio** as its primary extraction engine. We built and deployed a custom collector (`c_mt46lngz2asqzj8tkj`) targeting public technical changelogs (`https://supabase.com/changelog`). The backend invokes the collector using `@brightdata/cli` and REST APIs, returning structured JSON payloads containing titles, release dates, categories, descriptions, and URLs.

---

## 3. Validation & Failure Detection Engine (1:00 – 1:30)
Extracted payloads pass through a deterministic **Validation Engine** (`backend/app/validators/engine.py`). It evaluates required fields, schema fingerprints, date formats, URL validity, duplicates, and record count anomalies. If required properties are missing, a `FailureEvent` is recorded in Supabase PostgreSQL, and System Health drops to `DEGRADED`.

---

## 4. AI Scraper Intelligence & Safety Gate (1:30 – 2:15)
When a failure occurs, the AI Intelligence layer builds a sanitized failure context comparing the failed payload with previous successful sample records and historical schema diffs.
- **Explainable Diagnosis**: AI classifies the failure (e.g. `missing_field`, `schema_changed`) and produces root cause analysis backed by bullet-point evidence.
- **Safety Gate Enforcement**: AI is restricted to a strict repair allowlist (`selector_update`, `field_mapping_update`). Destructive commands are **BLOCKED**. Confidence $\ge 0.85$ + LOW risk allows automated execution; lower confidence forces manual human review.
- **Prompt Injection Defense**: Untrusted scraped web content is strictly isolated under `<UNTRUSTED_WEB_DATA>` tags.

---

## 5. Phase 5 Self-Healing & Independent Verification (2:15 – 2:45)
Approved repairs pass to the Phase 5 Self-Healing Engine. Re-execution occurs using the **SAME** Bright Data Collector ID (`c_mt46lngz2asqzj8tkj`), maintaining data lineage continuity.
- **Final Verification Authority**: AI cannot claim success. The re-scraped payload must independently pass the Phase 6 Validation Engine (100% field compliance) before `HealingAttempt.status` becomes `VERIFIED`.

---

## 6. Phase 6 Observability & Reliability Telemetry (2:45 – 3:00)
All telemetry is tracked live on the frontend React dashboard:
- **System Health Score (0–100)**: Calculated from success rate (25%), validation quality (20%), failure stability (15%), recovery rate (15%), and count stability (10%).
- **MTTR**: Mean Time To Recovery in seconds.
- **Audit Lineage**: Complete history from Scrape $\rightarrow$ Validation $\rightarrow$ AI Diagnosis $\rightarrow$ Safety Gate $\rightarrow$ Recovery Scrape $\rightarrow$ Verified Health.
