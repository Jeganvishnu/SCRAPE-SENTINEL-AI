# Scrape Sentinel AI

> **"An explainable self-healing web scraping platform powered by Bright Data Scraper Studio."**

---

## Value Statement
Scrape Sentinel AI transforms brittle web scraping into an observable, self-healing recovery system. It detects scraper failures, uses historical evidence and AI-assisted diagnosis to propose constrained repairs, executes approved repairs through a self-healing engine, and only declares recovery after independent validation succeeds.

---

## Problem & Solution Architecture

### The Problem
Traditional web data pipelines silently break when target websites change their layout or DOM structure. Selector changes and missing fields corrupt downstream analytics, machine learning datasets, and AI RAG pipelines. Manual scraper maintenance consumes engineering time and leads to undetected data loss.

### The Solution
Scrape Sentinel AI combines **Bright Data Scraper Studio** for web extraction, a deterministic **Validation Engine**, explainable **AI Root-Cause Diagnosis**, **Safety Gate** policy enforcement, automated **Phase 5 Healing Engine** execution, and real-time **Phase 6 Observability Telemetry**.

```
                 SCRAPE SENTINEL AI
                         │
                         ▼
            BRIGHT DATA SCRAPER STUDIO
               (c_mt46lngz2asqzj8tkj)
                         │
                         ▼
                RAW JSON EXTRACTION
                         │
                         ▼
                 VALIDATION ENGINE
                         │
            ┌────────────┴────────────┐
            │                         │
         HEALTHY                   FAILURE
            │                         │
            │                         ▼
            │                  AI DIAGNOSIS
            │                         │
            │                         ▼
            │                  ROOT CAUSE + EVIDENCE
            │                         │
            │                         ▼
            │                  REPAIR PLAN
            │                         │
            │                         ▼
            │                   SAFETY GATE
            │                         │
            │                         ▼
            │                  SELF-HEALING ENGINE
            │                         │
            │                         ▼
            │                  RECOVERY SCRAPE
            │                         │
            │                         ▼
            └────────────────►  VALIDATION ENGINE
                                      │
                             ┌────────┴────────┐
                             ▼                 ▼
                         VERIFIED            FAILED
                             │                 │
                             ▼                 ▼
                     HEALTH IMPROVES     MANUAL REVIEW
                             │
                             ▼
                     RELIABILITY DASHBOARD
```

---

## Key Features

- **Bright Data Scraper Studio Custom Collector**: Custom collector instance (`c_mt46lngz2asqzj8tkj`) created in Scraper Studio for scraping public technical changelogs.
- **Deterministic Validation Engine**: Validates required fields, schema structure, date formats, URL integrity, duplicates, and record count anomalies.
- **Explainable AI Root-Cause Analysis**: Builds compact failure context, calculates schema diffs, collects historical evidence, and determines root cause.
- **Safety Gate & Risk Policy**: Evaluates confidence thresholds ($\ge 0.85$ + LOW risk $\rightarrow$ Automatic Repair Approval; Medium/Low confidence $\rightarrow$ Manual Human Review).
- **Strict Repair Allowlist**: Restricts repairs to safe types (`selector_update`, `field_mapping_update`, `schema_mapping_update`, `normalization_update`). Destructive commands are **BLOCKED**.
- **Prompt Injection Defense**: Encapsulates scraped web payload data under `<UNTRUSTED_WEB_DATA>` to prevent prompt overrides or injection attacks.
- **Invariant Collector Lineage**: Recovery scrapes re-run using the **SAME** Collector ID (`c_mt46lngz2asqzj8tkj`), maintaining data lineage continuity.
- **Independent Verification**: Recovery is only declared `VERIFIED` when independent validation returns a passing score (`100/100`).
- **Reliability & Telemetry Dashboard**: Real-time System Health Score (0–100), MTTR in seconds, recovery rate %, activity feed timeline, and validation quality trends.

---

## Technology Stack

- **Scraping Engine**: Bright Data Scraper Studio (`@brightdata/cli`)
- **Backend API**: Python 3.14 + FastAPI + SQLAlchemy 2.0 + Pydantic v2
- **Frontend UI**: React + TypeScript + Vite + Tailwind CSS + Lucide Icons
- **Database**: PostgreSQL / Supabase
- **AI Providers**: Google Gemini REST API (`gemini-1.5-flash`), OpenAI (`gpt-4o-mini`), Mock Provider
- **Testing**: Pytest unit test suite (33 passing tests)

---

## Quick Start Setup

### 1. Prerequisites
- Python 3.10+ (Python 3.14 supported)
- Node.js 18+ & npm
- PostgreSQL database (or Supabase)

### 2. Environment Configuration
Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

### 3. Backend Setup & Database Migrations
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate      # Windows (.venv/bin/activate on Linux/macOS)
pip install -r requirements.txt
python app/core/run_migrations.py
uvicorn main:app --reload --port 8000
```

### 4. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

---

## Environment Variables

| Variable | Description | Example Placeholder |
| :--- | :--- | :--- |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@localhost:5432/postgres` |
| `BRIGHTDATA_API_KEY` | Bright Data API Key | `your_bright_data_api_key` |
| `BRIGHT_DATA_USERNAME` | Bright Data account email | `your_email@example.com` |
| `BRIGHT_DATA_COLLECTOR_ID` | Scraper Studio Collector ID | `c_mt46lngz2asqzj8tkj` |
| `AI_PROVIDER` | AI provider (`google`, `openai`, `mock`) | `google` |
| `AI_MODEL` | AI LLM model name | `gemini-1.5-flash` |
| `AI_API_KEY` | Google Gemini or OpenAI API Key | `your_ai_api_key` |
| `AI_ENABLED` | Enable/disable AI layer | `true` |
| `AI_TIMEOUT_SECONDS` | Timeout for AI requests | `15` |
| `AI_MAX_TOKENS` | Token limit for AI responses | `1000` |

---

## Bright Data Scraper Studio Role
Scrape Sentinel AI uses a **CUSTOM** collector built inside **Bright Data Scraper Studio** (`c_mt46lngz2asqzj8tkj`). The collector targets public developer release logs (`https://supabase.com/changelog`) and extracts structured JSON containing title, publication date, category, description, and direct link.

---

## Limitations
- **Structural Anomaly Limits**: Web page layout changes that remove content entirely require manual template re-authoring.
- **Anti-Bot Protections**: Target websites with aggressive anti-bot protections rely on Bright Data's proxy rotation and unlocking capabilities.
- **Safety Boundaries**: High-risk or low-confidence repair recommendations are intentionally withheld from auto-execution and flagged for manual review.

---

## AI Disclosure
AI coding tools (including Antigravity / Gemini) were utilized during project development for pair programming, test suite scaffolding, documentation, and architectural planning. All submitted code, scraper integrations, safety boundaries, and database schemas were reviewed, tested, modified, and understood by the project participant.

---

## License
This project is licensed under the [MIT License](LICENSE).
