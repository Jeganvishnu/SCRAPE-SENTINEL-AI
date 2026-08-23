# Scrape Sentinel AI — Hackathon Official Submission Form

> **Instructions**: Copy and paste the text below into the official hackathon submission portal fields.

---

## 1. Basic Project Information

- **Project Name**: SCRAPE SENTINEL AI
- **Short Description**: Scrape Sentinel AI is an explainable self-healing web scraping platform that uses a custom Bright Data Scraper Studio scraper, AI-assisted failure diagnosis, safe repair planning, recovery verification, and real-time reliability observability.
- **Repository URL**: `https://github.com/Jeganvishnu/SCRAPE-SENTINEL-AI`
- **Demo Video URL**: `[ADD DEMO VIDEO URL]`

---

## 2. Long Description

### Problem Statement
Traditional web data pipelines silently break when target websites update their HTML structure or CSS selectors. Missing fields or structural drift corrupt downstream machine learning datasets, analytics, and AI RAG applications. Manual scraper maintenance consumes engineering time and leads to undetected data loss.

### Solution & Innovation
Scrape Sentinel AI combines **Bright Data Scraper Studio** for web extraction, deterministic **Validation**, explainable **AI Root-Cause Diagnosis**, **Safety Gate** risk policy enforcement, automated **Phase 5 Healing Engine** execution, and real-time **Phase 6 Observability Telemetry**.

### Architectural Flow
1. **Extraction**: Custom Bright Data Scraper Studio Collector (`c_mt46lngz2asqzj8tkj`) extracts public technical changelogs.
2. **Validation**: Deterministic Validation Engine checks required fields, date formats, URL integrity, duplicates, and record count anomalies.
3. **Failure Detection**: Missing required fields trigger a `FailureEvent` and drop System Health to `DEGRADED`.
4. **AI Diagnosis**: AI constructs sanitized failure context, calculates schema diffs, collects historical evidence, and determines root cause.
5. **Safety Gate Policy**: AI proposals are restricted to a safe repair allowlist (`selector_update`, `field_mapping_update`). Unsafe or destructive commands are **BLOCKED**.
6. **Phase 5 Healing**: Approved repairs re-execute using the **SAME** Bright Data Collector ID, maintaining data lineage.
7. **Independent Verification**: Recovery is only declared `VERIFIED` when independent validation returns a passing score (`100/100`).
8. **Observability**: Live React dashboard displays Health Score (0–100), MTTR in seconds, recovery rate %, and activity feed timelines.

---

## 3. Technology Stack
- **Scraping Engine**: Bright Data Scraper Studio (`@brightdata/cli`)
- **Backend API**: Python 3.14 + FastAPI + SQLAlchemy 2.0 + Pydantic v2
- **Frontend UI**: React + TypeScript + Vite + Tailwind CSS + Lucide Icons
- **Database**: PostgreSQL / Supabase
- **AI Providers**: Google Gemini REST API (`gemini-1.5-flash`), OpenAI (`gpt-4o-mini`), Mock Provider
- **Testing**: Pytest unit test suite (33 passing tests)

---

## 4. Bright Data Scraper Studio Usage
The project relies on a **CUSTOM** collector built inside **Bright Data Scraper Studio** (`c_mt46lngz2asqzj8tkj`). The collector targets public developer release logs (`https://supabase.com/changelog`) and extracts structured JSON containing title, publication date, category, description, and direct link.

---

## 5. AI Usage Disclosure
AI coding tools (including Antigravity / Gemini) were utilized during project development for pair programming, test suite scaffolding, documentation, and architectural planning. All submitted code, scraper integrations, safety boundaries, and database schemas were reviewed, tested, modified, and understood by the project participant.
