# Scrape Sentinel AI

## Tagline

"When the web changes, your data pipeline should not stop."

## Current Status

**Phase 6 — Observability, Monitoring & Reliability Dashboard (Completed)**

## Problem

Traditional web-data pipelines silently break when website structure changes, causing data corruption or missing records without clear telemetry.

## Solution Architecture

Scrape Sentinel AI uses Bright Data Scraper Studio to collect public web data, normalizes raw payloads, executes a deterministic Validation Engine, logs failure events and healing attempts, persists structured records to Supabase PostgreSQL, calculates transparent health scores (0–100), and visualizes the complete extraction lifecycle in real-time.

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
┌─────────────────────────────────┐
│ PHASE 6                         │
│ Monitoring + Reliability        │
│ Metrics + Timeline + Dashboard  │
└─────────────────────────────────┘
```

## Phase 6 Features

- **Observability & Monitoring Endpoints**:
  - `GET /metrics/overview` (Period: `24h`, `7d`, `30d`, `all`)
  - `GET /metrics/sources/{source_id}`
  - `GET /metrics/timeline`
  - `GET /metrics/validation`
  - `GET /metrics/schema/{source_id}`
  - `GET /metrics/healing` (Recovery rate & MTTR calculation in seconds)
  - `GET /ready` & `GET /system/status`
- **Transparent Health Score (0–100)**: Weighted calculation based on success rate (25%), validation quality (20%), failure stability (15%), recovery rate (15%), record-count stability (10%), schema stability (10%), and execution reliability (5%).
- **Health Badges**: Dynamic `HEALTHY`, `WARNING`, `DEGRADED`, and `CRITICAL` status badges with human-readable explanations.
- **Run Lifecycle Visualization**: Visual step progression (`Scrape → Output → Validation → Failure → Healing → Recovery → Verified`) on `/runs/:id`.
- **Live 30s Refresh**: Lightweight frontend polling refresh without full page reloads.
- **Explicit Exclusions**: *Phase 7 AI/RAG intelligence features are intentionally not implemented until Phase 7.*

## Technology Stack

- **Frontend**: React + TypeScript + Vite + Tailwind CSS + Lucide Icons
- **Backend**: Python + FastAPI + SQLAlchemy 2.0 + psycopg2-binary
- **Scraping Engine**: Bright Data Scraper Studio (`@brightdata/cli`)
- **Database**: PostgreSQL / Supabase
- **Testing**: Pytest unit test suite (27 passing tests)

## Development Phases

- [x] Phase 1: Architecture and target selection
- [x] Phase 2: Project scaffold and configuration
- [x] Phase 3: Bright Data custom scraper integration
- [x] Phase 4: Validation, failure detection & Supabase database
- [x] Phase 5: Self-healing scraper engine foundation & `healing_attempts`
- [x] Phase 6: Observability, monitoring & reliability dashboard
- [ ] Phase 7: AI/RAG intelligence
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
- **System Status**: http://localhost:8000/system/status

## AI Disclosure

This project utilizes AI coding assistance (including Antigravity / Gemini) during development for architectural planning, code scaffolding, documentation generation, and pair programming. All generated code is reviewed, tested, modified, and fully understood by the project participant.
