# Scrape Sentinel AI — Database Schema Specification

> **Phase:** 1 — Database Data Model Specification  
> **Target RDBMS:** PostgreSQL / Supabase

---

## 1. Relational Entity Relationship Diagram (ERD)

```
┌───────────────────────────┐
│          sources          │
├───────────────────────────┤
│ PK  id (VARCHAR)          │◄─────┐
│     name (VARCHAR)        │      │
│     url (VARCHAR)         │      │
│     collector_id (VARCHAR)│      │
│     status (VARCHAR)      │      │
│     created_at (TIMESTAMPTZ)     │
│     updated_at (TIMESTAMPTZ)     │
└─────────────┬─────────────┘      │
              │ 1                  │ 1
              │                    │
              │ N                  │ N
┌─────────────▼─────────────┐ ┌────┴──────────────────────┐
│        scrape_runs        │ │      healing_events      │
├───────────────────────────┤ ├───────────────────────────┤
│ PK  id (UUID)             │ │ PK  id (UUID)             │
│ FK  source_id (VARCHAR)   │ │ FK  source_id (VARCHAR)   │
│     started_at (TIMESTAMPTZ)│ │     failure_type (VARCHAR)│
│     completed_at (TSTZ)   │ │     failure_rate (FLOAT)  │
│     status (VARCHAR)      │ │     heal_prompt (TEXT)    │
│     records_count (INT)   │ │     heal_status (VARCHAR) │
│     error_message (TEXT)  │ │     approval_status (VARCHAR)│
└───────────────────────────┘ │     rerun_status (VARCHAR)│
                              │     recovery_timestamp (TSTZ)│
                              └───────────────────────────┘
              │ 1
              │
              │ N
┌─────────────▼─────────────┐
│      scraped_records      │
├───────────────────────────┤
│ PK  id (UUID)             │◄───────────┐
│ FK  source_id (VARCHAR)   │            │
│     title (TEXT)          │            │
│     published_date (DATE) │            │ 1
│     version (VARCHAR)     │            │
│     category (VARCHAR)    │            │
│     description (TEXT)    │            │ N
│     url (TEXT)            │ ┌──────────┴────────────────┐
│     content_hash (VARCHAR)│ │        ai_insights        │
│     scraped_at (TIMESTAMPTZ)├─┤ PK  id (UUID)             │
│     collector_id (VARCHAR)│ │ FK  record_id (UUID)      │
└───────────────────────────┘ │     change_type (VARCHAR) │
                              │     impact_score (INT)    │
                              │     summary (TEXT)        │
                              │     reason (TEXT)         │
                              │     recommendation (TEXT) │
                              │     created_at (TSTZ)     │
                              └───────────────────────────┘
```

---

## 2. SQL DDL Specifications

### Table 1: `sources`
Stores configured web scraping target definitions and their associated Bright Data Scraper Studio Collector IDs.

```sql
CREATE TABLE sources (
    id VARCHAR(64) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    url TEXT NOT NULL,
    collector_id VARCHAR(128) NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'HEALTHY', -- HEALTHY, WARNING, FAILED, HEALING, NEEDS_APPROVAL
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

### Table 2: `scrape_runs`
Tracks execution attempts, run durations, record counts, and run statuses.

```sql
CREATE TABLE scrape_runs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_id VARCHAR(64) NOT NULL REFERENCES sources(id) ON DELETE CASCADE,
    started_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMPTZ,
    status VARCHAR(32) NOT NULL DEFAULT 'RUNNING', -- RUNNING, SUCCESS, FAILED, WARNING
    records_count INT NOT NULL DEFAULT 0,
    error_message TEXT
);

CREATE INDEX idx_scrape_runs_source_started ON scrape_runs(source_id, started_at DESC);
```

### Table 3: `scraped_records`
Stores normalized extracted data payloads collected from targets.

```sql
CREATE TABLE scraped_records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_id VARCHAR(64) NOT NULL REFERENCES sources(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    published_date DATE NOT NULL,
    version VARCHAR(64) DEFAULT 'N/A',
    category VARCHAR(64) NOT NULL DEFAULT 'General',
    description TEXT NOT NULL,
    url TEXT NOT NULL,
    content_hash VARCHAR(64) NOT NULL UNIQUE,
    scraped_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    collector_id VARCHAR(128) NOT NULL
);

CREATE INDEX idx_scraped_records_source ON scraped_records(source_id);
CREATE INDEX idx_scraped_records_pubdate ON scraped_records(published_date DESC);
CREATE INDEX idx_scraped_records_hash ON scraped_records(content_hash);
```

### Table 4: `healing_events`
Audit trail log of failure detections, generated healing prompts, approval statuses, and recovery timestamps.

```sql
CREATE TABLE healing_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_id VARCHAR(64) NOT NULL REFERENCES sources(id) ON DELETE CASCADE,
    failure_type VARCHAR(64) NOT NULL, -- REQUIRED_FIELD_MISSING, RECORD_COUNT_DROP, ZERO_RECORDS, SCHEMA_MISMATCH
    failure_rate DOUBLE PRECISION NOT NULL DEFAULT 0.0,
    heal_prompt TEXT NOT NULL,
    heal_status VARCHAR(32) NOT NULL DEFAULT 'INITIATED', -- INITIATED, PENDING_APPROVAL, SENT_TO_BRIGHT_DATA, HEALED, FAILED
    approval_status VARCHAR(32) NOT NULL DEFAULT 'NOT_REQUIRED', -- NOT_REQUIRED, PENDING, APPROVED, REJECTED
    rerun_status VARCHAR(32) NOT NULL DEFAULT 'PENDING', -- PENDING, RERUNNING, PASSED, FAILED
    recovery_timestamp TIMESTAMPTZ
);

CREATE INDEX idx_healing_events_source ON healing_events(source_id);
```

### Table 5: `ai_insights`
Stores AI-generated intelligence, severity/impact ratings, summaries, and developer recommendations.

```sql
CREATE TABLE ai_insights (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    record_id UUID NOT NULL REFERENCES scraped_records(id) ON DELETE CASCADE,
    change_type VARCHAR(64) NOT NULL, -- BREAKING_CHANGE, DEPRECATION, NEW_FEATURE, BUG_FIX, PERFORMANCE
    impact_score INT NOT NULL CHECK (impact_score >= 1 AND impact_score <= 10),
    summary TEXT NOT NULL,
    reason TEXT NOT NULL,
    recommendation TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_ai_insights_record ON ai_insights(record_id);
CREATE INDEX idx_ai_insights_impact ON ai_insights(impact_score DESC);
```

---

## 3. Table Relationships & Key Constraints

1. **`sources` ──< `scrape_runs` (1-to-Many):** One data source has many execution runs. Deleting a source cascade-deletes its runs.
2. **`sources` ──< `scraped_records` (1-to-Many):** One source yields many scraped payload records. Unique constraint on `content_hash` prevents duplicate record insertion.
3. **`sources` ──< `healing_events` (1-to-Many):** One source records multiple self-healing audit events over time.
4. **`scraped_records` ──< `ai_insights` (1-to-Many / 1-to-1):** Each extracted record can be analyzed by the AI module to generate structured intelligence.
