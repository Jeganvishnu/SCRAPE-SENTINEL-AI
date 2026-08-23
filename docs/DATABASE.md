# Scrape Sentinel AI — Database Schema & Architecture

## Overview
Scrape Sentinel AI uses **Supabase PostgreSQL** for robust relational persistence. The database consists of 7 core tables linked by strict foreign key constraints and indexed for fast observability queries.

---

## Relational Schema Diagram

```
sources (id)
   ├──> scrape_runs (source_id)
   │       ├──> scraped_records (scrape_run_id)
   │       └──> validation_results (scrape_run_id)
   │
   ├──> failure_events (source_id)
   │       └──> healing_attempts (failure_event_id)
   │               └──> verification_run (scrape_runs.id)
   │
   └──> ai_diagnoses (source_id, failure_event_id, healing_attempt_id)
```

---

## Core Tables

### 1. `sources`
- `id` (UUID, Primary Key)
- `name` (TEXT)
- `url` (TEXT)
- `collector_id` (TEXT)
- `status` (TEXT: `HEALTHY`, `WARNING`, `DEGRADED`, `CRITICAL`)
- `created_at`, `updated_at` (TIMESTAMPTZ)

### 2. `scrape_runs`
- `id` (UUID, Primary Key)
- `source_id` (UUID, Foreign Key `sources.id`)
- `collector_id` (TEXT)
- `started_at`, `completed_at` (TIMESTAMPTZ)
- `status` (TEXT: `success`, `failed`)
- `records_found`, `records_valid`, `records_invalid` (INTEGER)
- `duration_ms` (INTEGER)
- `raw_output_hash` (TEXT)

### 3. `scraped_records`
- `id` (UUID, Primary Key)
- `source_id` (UUID, Foreign Key `sources.id`)
- `scrape_run_id` (UUID, Foreign Key `scrape_runs.id`)
- `title`, `published_date`, `version`, `category`, `description`, `url` (TEXT)
- `content_hash` (TEXT)
- `scraped_at` (TIMESTAMPTZ)

### 4. `validation_results`
- `id` (UUID, Primary Key)
- `scrape_run_id` (UUID, Foreign Key `scrape_runs.id`)
- `validation_status` (TEXT: `passed`, `failed`, `anomaly`)
- `schema_valid`, `required_fields_valid`, `url_valid`, `date_valid`, `duplicate_free`, `record_count_valid`, `schema_change_detected` (BOOLEAN)
- `validation_score` (NUMERIC(5,2))
- `issues` (JSONB)

### 5. `failure_events`
- `id` (UUID, Primary Key)
- `source_id` (UUID, Foreign Key `sources.id`)
- `scrape_run_id` (UUID, Foreign Key `scrape_runs.id`)
- `failure_type` (TEXT)
- `severity` (TEXT)
- `message` (TEXT)
- `status` (TEXT: `open`, `resolving`, `resolved`, `ignored`)

### 6. `healing_attempts`
- `id` (UUID, Primary Key)
- `source_id` (UUID, Foreign Key `sources.id`)
- `scrape_run_id` (UUID, Foreign Key `scrape_runs.id`)
- `failure_event_id` (UUID, Foreign Key `failure_events.id`)
- `collector_id` (TEXT)
- `attempt_number` (INTEGER)
- `started_at`, `completed_at` (TIMESTAMPTZ)
- `status` (TEXT: `executing`, `verified`, `failed`)
- `verification_run_id` (UUID, Foreign Key `scrape_runs.id`)

### 7. `ai_diagnoses`
- `id` (UUID, Primary Key)
- `source_id` (UUID, Foreign Key `sources.id`)
- `failure_event_id` (UUID, Foreign Key `failure_events.id`)
- `healing_attempt_id` (UUID, Foreign Key `healing_attempts.id`)
- `model` (TEXT)
- `prompt_version` (TEXT)
- `failure_category` (TEXT)
- `confidence` (NUMERIC(4,2))
- `root_cause` (TEXT)
- `evidence` (JSONB)
- `repair_type` (TEXT)
- `repair_plan` (JSONB)
- `risk` (TEXT)
- `approved` (BOOLEAN)
- `requires_manual_review` (BOOLEAN)
- `verification_status` (TEXT: `pending`, `verified`, `failed`)
