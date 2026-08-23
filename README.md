# Scrape Sentinel AI

## Tagline

"When the web changes, your data pipeline should not stop."

## Current Status

**Phase 7 — AI-Powered Scraper Intelligence (Completed)**

## Problem

Traditional web-data pipelines silently break when website structure changes, causing data corruption or missing records without clear telemetry or explainable root-cause diagnosis.

## Solution Architecture

Scrape Sentinel AI combines Bright Data Scraper Studio for web data collection, deterministic schema validation, explainable AI failure diagnosis with Safety Gate enforcement, automatic Phase 5 healing execution, and real-time observability telemetry.

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
     ┌──────────────────┐
     │ AI INTELLIGENCE  │
     ├──────────────────┤
     │ Context Builder  │
     │ Root Cause       │
     │ Evidence         │
     │ Safety Gate      │
     └────────┬─────────┘
              ↓
        HEALING QUEUE
              ↓
      RECOVERY SCRAPE
              ↓
     INDEPENDENT VALIDATION
              ↓
  ┌───────────┴───────────┐
  ↓                       ↓
VERIFIED              FAILED
  ↓                       ↓
PHASE 6 METRICS       MANUAL REVIEW
```

## Phase 7 AI Features

- **Provider Abstraction**: Pluggable provider interface (`BaseAIProvider`) supporting `MockAIProvider` (offline/testing) and `OpenAIProvider` (`gpt-4o-mini`).
- **Explainable Diagnosis**: Generates structured JSON root cause analysis with evidence bullet points and affected field lists.
- **Safety Gate & Risk Policy**: Evaluates confidence ($\ge 0.85$ + LOW risk $\rightarrow$ Automatic Approval; Medium/Low confidence $\rightarrow$ Manual Human Review).
- **Repair Allowlist**: Enforces strict repair type allowlist (`selector_update`, `field_mapping_update`, `schema_mapping_update`, `normalization_update`, `retry_adjustment`). Destructive operations are **BLOCKED**.
- **Prompt Injection Defense**: Encapsulates scraped web payload data under `<UNTRUSTED_WEB_DATA>` to prevent prompt overrides or injection attacks.
- **Repair Loop Protection**: Enforces maximum 3 repair attempts per failure event before forcing manual review.
- **AI Fallback**: If AI is disabled or unavailable, seamlessly falls back to Phase 5 deterministic healing without application crash.
- **AI Endpoints**:
  - `GET /ai/status`
  - `POST /ai/diagnose/{failure_id}`
  - `POST /ai/repair-plan/{failure_id}`
  - `GET /ai/history`

## Technology Stack

- **Frontend**: React + TypeScript + Vite + Tailwind CSS + Lucide Icons
- **Backend**: Python + FastAPI + SQLAlchemy 2.0 + psycopg2-binary
- **Scraping Engine**: Bright Data Scraper Studio (`@brightdata/cli`)
- **Database**: PostgreSQL / Supabase
- **Testing**: Pytest unit test suite (32 passing tests)

## Development Phases

- [x] Phase 1: Architecture and target selection
- [x] Phase 2: Project scaffold and configuration
- [x] Phase 3: Bright Data custom scraper integration
- [x] Phase 4: Validation, failure detection & Supabase database
- [x] Phase 5: Self-healing scraper engine foundation & `healing_attempts`
- [x] Phase 6: Observability, monitoring & reliability dashboard
- [x] Phase 7: AI-powered scraper intelligence & safety gate
- [ ] Phase 8: Automation & webhooks
- [ ] Phase 9: Testing & security audit
- [ ] Phase 10: Final submission & demo

## Local Run Commands

### Backend Migration & Server
```bash
cd backend
.venv\Scripts\python app/core/run_migrations.py
.venv\Scripts\uvicorn main:app --reload --port 8000
```

### Frontend Development
```bash
cd frontend
npm run dev
```

### Access Points
- **Frontend Dashboard**: http://localhost:5173
- **Backend API Docs**: http://localhost:8000/docs
- **Backend Health Check**: http://localhost:8000/health
- **AI Status API**: http://localhost:8000/ai/status

## AI Disclosure

This project utilizes AI coding assistance (including Antigravity / Gemini) during development for architectural planning, code scaffolding, documentation generation, and pair programming. All generated code is reviewed, tested, modified, and fully understood by the project participant.
