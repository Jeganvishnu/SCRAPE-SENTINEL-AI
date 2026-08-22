# Scrape Sentinel AI — Backend API Specification Plan

> **Phase:** 1 — REST API Blueprint Specification  
> **Framework:** FastAPI (Python 3.11+)

---

## 1. OpenAPI System Overview

The **Scrape Sentinel AI** backend provides REST API endpoints to manage target sources, trigger Bright Data Scraper Studio runs, inspect validation results, manage automated self-healing events, fetch AI change insights, and query the dataset via natural language Q&A.

---

## 2. Endpoint Definitions

### System Health

#### `GET /health`
- **Purpose:** Service health check and database connectivity verification.
- **Method:** `GET`
- **Request:** None
- **Response (200 OK):**
  ```json
  {
    "status": "healthy",
    "timestamp": "2026-08-22T14:38:26Z",
    "version": "1.0.0",
    "database": "connected"
  }
  ```
- **Error Cases:** `503 Service Unavailable` if DB connection fails.

---

### Target Source Management

#### `POST /sources`
- **Purpose:** Register a new public web scraping source and bind its Bright Data Collector ID.
- **Method:** `POST`
- **Request Body:**
  ```json
  {
    "id": "supabase_changelog",
    "name": "Supabase Changelog",
    "url": "https://supabase.com/changelog",
    "collector_id": "c_m1abc123xyz"
  }
  ```
- **Response (201 Created):**
  ```json
  {
    "id": "supabase_changelog",
    "name": "Supabase Changelog",
    "url": "https://supabase.com/changelog",
    "collector_id": "c_m1abc123xyz",
    "status": "HEALTHY",
    "created_at": "2026-08-22T14:38:26Z"
  }
  ```
- **Error Cases:** `400 Bad Request` if `id` already exists or URL format is invalid.

#### `GET /sources`
- **Purpose:** List all configured data sources and their current health status.
- **Method:** `GET`
- **Request Params:** `status` (optional filter, e.g. `HEALTHY`, `FAILED`)
- **Response (200 OK):**
  ```json
  [
    {
      "id": "supabase_changelog",
      "name": "Supabase Changelog",
      "url": "https://supabase.com/changelog",
      "collector_id": "c_m1abc123xyz",
      "status": "HEALTHY",
      "updated_at": "2026-08-22T14:38:26Z"
    }
  ]
  ```

#### `GET /sources/{id}`
- **Purpose:** Retrieve specific source details and configuration.
- **Method:** `GET`
- **Response (200 OK):** Source detail object.
- **Error Cases:** `404 Not Found` if source `id` does not exist.

---

### Scraping & Run Execution

#### `POST /sources/{id}/scrape`
- **Purpose:** Trigger a scraping run for a specific target source via Bright Data Scraper Studio.
- **Method:** `POST`
- **Response (202 Accepted):**
  ```json
  {
    "run_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
    "source_id": "supabase_changelog",
    "status": "RUNNING",
    "started_at": "2026-08-22T14:38:26Z"
  }
  ```
- **Error Cases:** `404 Not Found` if source missing; `409 Conflict` if run already in progress.

#### `GET /sources/{id}/runs`
- **Purpose:** List history of execution runs for a source.
- **Method:** `GET`
- **Request Params:** `limit` (default 20), `offset` (default 0)
- **Response (200 OK):** Array of `scrape_runs` summary objects.

---

### Self-Healing & Recovery

#### `POST /sources/{id}/heal`
- **Purpose:** Dispatch a healing request to Bright Data Scraper Studio for a broken collector.
- **Method:** `POST`
- **Request Body:**
  ```json
  {
    "failure_type": "REQUIRED_FIELD_MISSING",
    "heal_prompt": "The element selector for post title changed from 'h3.title' to 'h3.text-foreground'. Extract title from 'h3.text-foreground'.",
    "require_approval": true
  }
  ```
- **Response (200 OK):**
  ```json
  {
    "healing_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
    "source_id": "supabase_changelog",
    "heal_status": "PENDING_APPROVAL",
    "collector_id": "c_m1abc123xyz"
  }
  ```

#### `POST /healing/{id}/approve`
- **Purpose:** Approve a pending healing prompt and authorize Bright Data scraper rerun with the SAME Collector ID.
- **Method:** `POST`
- **Response (200 OK):**
  ```json
  {
    "healing_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
    "approval_status": "APPROVED",
    "rerun_status": "PASSED",
    "collector_id": "c_m1abc123xyz"
  }
  ```

#### `GET /healing/history/{source_id}`
- **Purpose:** Retrieve full self-healing history and audit logs for a source.
- **Method:** `GET`
- **Response (200 OK):** List of `healing_events` objects.

---

### Health Metrics & Status Monitoring

#### `GET /health/sources`
- **Purpose:** Aggregate health metrics for the dashboard summary view.
- **Method:** `GET`
- **Response (200 OK):**
  ```json
  {
    "total_sources": 1,
    "healthy_sources": 1,
    "warning_sources": 0,
    "failed_sources": 0,
    "total_records_collected": 42
  }
  ```

#### `GET /health/sources/{id}`
- **Purpose:** Detailed validation metrics, error rates, and failure signals for a source.
- **Method:** `GET`

---

### AI Insights & Change Intelligence

#### `GET /insights`
- **Purpose:** Retrieve list of AI-analyzed change records with breaking change warnings and impact scores.
- **Method:** `GET`
- **Request Params:** `impact_min` (e.g. 7), `category` (optional)
- **Response (200 OK):** List of `ai_insights` records with linked record details.

#### `POST /insights/analyze/{run_id}`
- **Purpose:** Trigger LLM analysis on records extracted in a completed run.
- **Method:** `POST`
- **Response (200 OK):** Summary count of analyzed records and generated insights.

#### `POST /ask`
- **Purpose:** Interactive natural language Q&A ("Ask Sentinel") querying scraped product changelogs.
- **Method:** `POST`
- **Request Body:**
  ```json
  {
    "question": "What breaking changes were released for Supabase database read replicas recently?"
  }
  ```
- **Response (200 OK):**
  ```json
  {
    "answer": "Supabase moved Read Replica management from Database -> Replication to Project Settings -> Infrastructure on Aug 21, 2026.",
    "citations": [
      {
        "title": "Read replicas moved to Project Settings → Infrastructure",
        "url": "https://supabase.com/changelog/read-replicas-moved-to-infrastructure",
        "published_date": "2026-08-21"
      }
    ]
  }
  ```
