# Bright Data Scraper Studio Integration Architecture

## Overview
**Scrape Sentinel AI** utilizes **Bright Data Scraper Studio** as its primary web data extraction engine. The platform interacts with a real, custom-built collector instance created inside Bright Data Scraper Studio to scrape structured public web data.

---

## 1. Collector Details & Scraper Studio Role

- **Scraper Studio Collector ID**: `c_mt46lngz2asqzj8tkj`
- **Target Web Source**: Supabase Product Changelog (`https://supabase.com/changelog`)
- **Scraper Type**: Custom Scraper Studio Collector
- **Data Extracted**:
  - `title`: Post title (e.g. "PostgreSQL 17 Support", "Supabase Auth Updates")
  - `published_date`: ISO timestamp or formatted date string
  - `category`: Article topic (e.g. "Database", "Auth", "Storage")
  - `description`: Summary release notes
  - `url`: Direct link to changelog entry

---

## 2. Execution Architecture

```
BRIGHT DATA SCRAPER STUDIO (@brightdata/cli)
                  ↓
          CUSTOM COLLECTOR
       (c_mt46lngz2asqzj8tkj)
                  ↓
         RAW JSON DATA PAYLOAD
                  ↓
          SENTINEL BACKEND
       (FastAPI + Python 3.14)
                  ↓
         NORMALIZATION SERVICE
                  ↓
           VALIDATION ENGINE
                  ↓
     ┌────────────┴────────────┐
     ↓                         ↓
VALIDATED RECS            FAILURE EVENT
     ↓                         ↓
  SUPABASE DB            AI DIAGNOSIS + HEALING
```

---

## 3. API & CLI Integration Method

The backend invokes Bright Data Scraper Studio via official CLI execution (`@brightdata/cli`) or HTTP REST collector endpoints:

```bash
npx @brightdata/cli collector run c_mt46lngz2asqzj8tkj --url https://supabase.com/changelog --format json
```

### Authentication Approach
- Authentication is handled via API Key and credentials stored safely in local environment variables (`BRIGHTDATA_API_KEY`, `BRIGHT_DATA_USERNAME`).
- Secrets are loaded dynamically via `backend/app/core/brightdata_config.py` and are **never** hardcoded or exposed to the frontend browser interface.

---

## 4. Validation & Self-Healing Integration

- **Deterministic Validation**: Every raw JSON array returned by the custom collector passes through the **Validation Engine** (`backend/app/validators/engine.py`).
- **Failure Detection**: If required fields (e.g. `title`) are missing or schema drift occurs, a `FailureEvent` is recorded.
- **AI-Guided Scraper Repair**: The AI Intelligence layer generates a constrained repair plan (`selector_update`, `field_mapping_update`).
- **Invariant Collector Continuity**: Post-repair verification re-runs using the **SAME** Collector ID (`c_mt46lngz2asqzj8tkj`), maintaining data lineage continuity.
- **Independent Verification**: Recovery is only declared `VERIFIED` when independent validation returns a passing score (`100/100`).
