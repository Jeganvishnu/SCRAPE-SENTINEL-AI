# Scrape Sentinel AI — Hackathon Demonstration Plan

> **Phase:** 6 — Observability, Monitoring & Self-Healing Demo Flow  
> **Target:** Bright Data Scraper Studio Hackathon Submission Video & Live Demo

---

## 1. Demo Storyboard Overview

The goal of the demonstration is to prove that **Scrape Sentinel AI** handles the core problem of brittle web scrapers: when a target website changes its structure, the system detects validation failure, sends an automated DOM healing prompt to **Bright Data Scraper Studio**, obtains human approval (if required), reruns using the **SAME Collector ID**, passes validation, and restores normal downstream AI analysis without pipeline breakage.

---

## 2. Step-by-Step 15-Point Demonstration Script

| Step # | Demo Action | User Interface / Terminal State | Technical Verification Point |
| :--- | :--- | :--- | :--- |
| **1** | **Show Observability Dashboard** | Open Dashboard. Show System Health (`HEALTHY`), Health Score (`94/100`), Success Rate %, and Active Failures count. | Real DB metrics from `GET /metrics/overview`. |
| **2** | **Run Custom Bright Data Scraper** | Click "Run Scraper Now" button on Dashboard for `Supabase Changelog`. | API calls `POST /sources/{id}/scrape`. |
| **3** | **Show Collector ID** | Highlight the active Bright Data Scraper Studio `Collector ID` (`c_mt46lngz2asqzj8tkj`). | Collector ID persists in database and UI. |
| **4** | **Show Structured JSON** | Display extracted raw JSON payload array returned from Bright Data. | Payload includes `title`, `published_date`, `category`, `description`, `url`. |
| **5** | **Show Validation Score & Trends** | Display Validation Engine score (`100/100`), status `PASS`, and historical trend bar chart. | `validation_results.validation_score == 100.0`. |
| **6** | **Introduce Extraction Failure** | Simulate DOM structure change (e.g. inject selector mismatch or mock target DOM modification where `title` class changes). | Trigger extraction run against modified structure. |
| **7** | **Show Failure Detection** | Validation engine detects missing required `title` field across records. System Health drops to `DEGRADED`. | `failure_events` generated with `REQUIRED_FIELD_MISSING`. |
| **8** | **Show Failure Details & Timeline** | Open Failure Details page. Show failure type, severity, detected time, and activity feed event (`failure_detected`). | Real event logged in activity feed. |
| **9** | **Show Healing Queue** | Open Healing tab in UI. Display `Detected failure — Awaiting healing` label and MTTR metrics. | Healing attempt queued for Phase 5 engine. |
| **10** | **Approve When Required** | System flags `NEEDS_APPROVAL`. Click "Approve Healing" button in Sentinel UI. | API calls `POST /healing/{id}/approve`. |
| **11** | **Rerun SAME Collector ID** | Trigger automatic post-heal execution run. Highlight that the **SAME Collector ID** (`c_mt46lngz2asqzj8tkj`) is reused. | Invariant `collector_id` verified. |
| **12** | **Show Recovered Output** | Display new structured JSON returned post-healing with correctly extracted titles and fields. | Extraction payload restored. |
| **13** | **Show Validation Passing** | Validation engine re-evaluates payload: status returns to `PASS`. | `scrape_runs.status == 'SUCCESS'`. |
| **14** | **Show DB & Dashboard Recovery** | Refresh Dashboard. Show source status back to `HEALTHY`, score back to `100/100`, total record counts incremented. | `sources.status == 'HEALTHY'`. |
| **15** | **Show AI Insight** | Navigate to Insights tab. Show AI-generated summary and impact score for the newly recovered records. | `ai_insights` populated for recovered records. |

---

## 3. Demo Video Requirements & Hackathon Verification

- **Video Length:** 3–5 minutes.
- **Key Visual Callouts:**
  1. Highlight Bright Data Scraper Studio interface / CLI integration.
  2. Clearly highlight the `Collector ID` before and after healing to prove continuity.
  3. Show live transition from `HEALTHY` -> `DEGRADED` -> `HEALING` -> `VERIFIED` -> `HEALTHY`.
