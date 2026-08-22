# Scrape Sentinel AI — System Architecture & Design Specification

> **Tagline:** *"When the web changes, your data pipeline should not stop."*  
> **Phase:** 1 — Architecture & Blueprint (Hackathon Specification)

---

## 1. System Overview & Core Concept

**Scrape Sentinel AI** is an autonomous, self-healing web data extraction and change intelligence platform. Modern data pipelines silently break when target websites modify their DOM structure, class names, or content layouts. Scrape Sentinel AI solves this by continuously validating incoming scraped data, detecting structural and content extraction failures deterministically, automatically healing custom scrapers via **Bright Data Scraper Studio**, and maintaining uninterrupted downstream AI analysis.

### High-Level End-to-End Pipeline Concept

```
PUBLIC TECH CHANGELOG / WEBSITE
            │
            ▼
BRIGHT DATA SCRAPER STUDIO CUSTOM SCRAPER (Collector ID)
            │
            ▼
    STRUCTURED JSON OUTPUT
            │
            ▼
   DATA NORMALIZATION LAYER
            │
            ▼
 DETERMINISTIC VALIDATION ENGINE
            │
            ├──► [PASS] ──► POSTGRESQL DB ──► LLM AI ANALYSIS ──► DASHBOARD & ALERTS
            │
            └──► [FAIL] ──► FAILURE DETECTOR ──► HEALING CONTROLLER
                                                       │
                                                       ▼
                                            BRIGHT DATA HEAL API
                                                       │
                                                       ▼
                                          HUMAN APPROVAL (IF REQUIRED)
                                                       │
                                                       ▼
                                        RERUN SAME COLLECTOR ID
                                                       │
                                                       ▼
                                            PIPELINE RECOVERED
```

---

## 2. Technology Stack

| Layer | Technology | Selection Rationale |
| :--- | :--- | :--- |
| **Frontend UI** | React 18, TypeScript, Vite, Tailwind CSS, Recharts | High performance, strict typing, responsive components, rich visualization charts for data health. |
| **Backend API** | Python 3.11+, FastAPI, Pydantic v2 | Asynchronous request processing, native data validation with Pydantic, fast OpenAPI generation. |
| **Scraper Studio** | Bright Data Scraper Studio & Bright Data CLI | Custom IDE-managed Scraper with dedicated `Collector ID`, supporting automated AI healing requests. |
| **Database** | PostgreSQL / Supabase | Relational integrity for data runs, structured scraped records, healing logs, and AI insights. |
| **AI Analysis** | OpenAI / Gemini API (LLM) | Categorization, summary generation, and breaking change impact scoring on collected records. |
| **Automation** | GitHub Actions / Cron Task Runner | Scheduled periodic scraping runs and validation triggering. |

---

## 3. Subsystem Boundaries & Architecture Layers

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                     USER INTERFACE                                      │
│ React + TypeScript + Vite Dashboard (Sources, Runs, Healing Controls, Insights, Ask AI)│
└──────────────────────────────────────────┬──────────────────────────────────────────────┘
                                           │ HTTP REST / JSON API
┌──────────────────────────────────────────▼──────────────────────────────────────────────┐
│                                   FASTAPI BACKEND                                       │
│ ┌──────────────────────┐  ┌──────────────────────┐  ┌─────────────────────────────────┐ │
│ │ Source Manager       │  │ Scraper Runner       │  │ Validation Engine               │ │
│ └──────────────────────┘  └──────────────────────┘  └─────────────────────────────────┘ │
│ ┌──────────────────────┐  ┌──────────────────────┐  ┌─────────────────────────────────┐ │
│ │ Failure Detector     │  │ Healing Controller   │  │ AI Analysis Engine              │ │
│ └──────────────────────┘  └──────────────────────┘  └─────────────────────────────────┘ │
└────────┬───────────────────────────┬─────────────────────────────────┬──────────────────┘
         │ Scraper Studio API/CLI    │ SQL Queries                     │ API Prompt/Completion
┌────────▼────────────────┐ ┌────────▼──────────────────────┐ ┌────────▼──────────────────┐
│   BRIGHT DATA BOUNDARY  │ │     DATABASE BOUNDARY        │ │       AI BOUNDARY        │
│ Bright Data Scraper     │ │ PostgreSQL / Supabase        │ │ LLM Service (OpenAI/     │
│ Studio Custom Collector │ │ (sources, scrape_runs,       │ │ Gemini)                  │
│ (Collector ID)          │ │  scraped_records, healing,   │ │ (Impact score, summary,   │
│ Scraper Heal & Rerun    │ │  ai_insights)                │ │  NL Q&A)                 │
└─────────────────────────┘ └──────────────────────────────┘ └──────────────────────────┘
```

### 3.1 Bright Data Boundary
- Manages the execution of the custom scraper via standard Bright Data Web Scraper API / CLI.
- Maintains the unique, persistent `Collector ID` across initial creation, normal execution, and post-healing reruns.
- Receives healing prompts generated by the backend Healing Controller when extraction failure is detected.

### 3.2 Database Boundary
- Stores state persistence: source metadata, run history, normalized scraped payload records, structured healing audit logs, and AI-generated change intelligence.
- Acts as the immutable truth for baseline schemas and historical data integrity.

### 3.3 AI Boundary
- Operates exclusively downstream of the deterministic validation layer.
- Performs semantic change analysis, change severity indexing (1-10 impact score), category tagging, and interactive RAG / Ask Sentinel queries.
- **Rule:** AI is never used for basic schema validation; validation is 100% deterministic.

---

## 4. End-to-End Data & Execution Flow

1. **Trigger:** User or Cron scheduler invokes `POST /sources/{id}/scrape`.
2. **Execution:** Backend calls Bright Data Scraper Studio API using the configured `collector_id`.
3. **Extraction & Raw Payload:** Bright Data returns structured JSON array from the target public URL.
4. **Normalization:** Backend normalizes raw JSON attributes into standard `ScrapedRecord` schema.
5. **Deterministic Validation:** Backend runs rule-based validation checks:
   - Check required fields (`title`, `published_date`, `url`).
   - Check empty payload / record count drop.
   - Check extraction error percentage.
6. **Branch A (Validation Success):**
   - Save records to `scraped_records` table.
   - Update `scrape_runs` status to `SUCCESS`.
   - Trigger background AI analysis task (`POST /insights/analyze/{run_id}`).
7. **Branch B (Validation Failure):**
   - Mark `scrape_runs` status as `FAILED` or `WARNING`.
   - Failure Detector analyzes failure signals and generates structured `ValidationReport`.
   - Healing Controller formats precise DOM/field healing prompt for Bright Data Scraper Studio.
   - Dispatches `POST /sources/{id}/heal` to Bright Data.
   - If manual approval flag is set, status transitions to `NEEDS_APPROVAL`.
   - Once healed/approved, system reruns scraper using the **SAME Collector ID**.
   - Validation re-evaluates healed output.

---

## 5. Detailed Self-Healing System Architecture

### 5.1 Failure Detection Signals (Deterministic Rules)

| Signal ID | Signal Name | Trigger Condition | Severity |
| :--- | :--- | :--- | :--- |
| `SIG_REQ_EMPTY` | Required Field Missing | > 10% of records have null/empty `title`, `url`, or `published_date`. | HIGH |
| `SIG_COUNT_DROP` | Record Count Drop | Total records extracted drops by > 75% compared to historical baseline. | HIGH |
| `SIG_ZERO_RECORDS` | Zero Extraction | Extracted records count == 0. | CRITICAL |
| `SIG_SCHEMA_INVALID` | Schema Mismatch | Field types fail Pydantic parsing (e.g. invalid date format). | MEDIUM |
| `SIG_DUPLICATE_SPIKE` | Duplicate Spike | Duplicate `content_hash` rate > 90% unexpectedly. | LOW |

### 5.2 Healing Control Loop & Safety Boundaries

```
[VALIDATION FAILURE DETECTED]
            │
            ▼
   CHECK MAX_HEAL_ATTEMPTS (Limit = 2)
   ├── Attempt Count > 2 ──► ABORT HEALING ──► Set Status `HEAL_FAILED` & Alert Admin
   └── Attempt Count <= 2
            │
            ▼
   CONSTRUCT HEAL PROMPT (Specify broken field & expected schema)
            │
            ▼
   DISPATCH TO BRIGHT DATA SCRAPER STUDIO (API / CLI)
            │
            ▼
   APPROVAL CHECK: Requires Human Approval?
   ├── YES ──► Pause, Set Status `NEEDS_APPROVAL`, Wait for `POST /healing/{id}/approve`
   └── NO  ──► Proceed Immediately
            │
            ▼
   RERUN SCRAPER WITH SAME COLLECTOR ID
            │
            ▼
   RE-VALIDATE SCRAPED payload
   ├── PASS ──► Log Recovery, Set Status `HEALTHY`, Resume Pipeline
   └── FAIL ──► Increment Attempt Counter, Loop Back
```

---

## 6. Verification & System Quality Controls

- **Deterministic Primacy:** Deterministic Pydantic & python validation engines evaluate every record before DB insertion or LLM invocation.
- **Collector ID Integrity:** The system strict-checks that `collector_id` remains invariant throughout the healing lifecycle.
- **Non-blocking Operations:** All scraping and AI enrichment tasks execute asynchronously via background workers.
