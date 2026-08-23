# Scrape Sentinel AI — Hackathon Demonstration Plan

> **Phase:** 7 — AI-Powered Scraper Intelligence & Self-Healing Demo Flow  
> **Target:** Bright Data Scraper Studio Hackathon Submission Video & Live Demo

---

## 1. Demo Storyboard Overview

The goal of the demonstration is to prove that **Scrape Sentinel AI** handles brittle web scrapers: when target site structure changes, the system detects validation failure, triggers explainable **AI Failure Diagnosis**, extracts evidence, passes through a **Safety Gate**, executes repair instructions via **Bright Data Scraper Studio**, verifies recovery independently using Phase 6 validation, and updates observability metrics.

---

## 2. Step-by-Step 17-Point Demonstration Script

| Step # | Demo Action | User Interface / Terminal State | Technical Verification Point |
| :--- | :--- | :--- | :--- |
| **1** | **Show Observability Dashboard** | Open Dashboard. Show System Health (`HEALTHY`), Health Score (`94/100`), Success Rate %, and Active Failures count. | Real DB metrics from `GET /metrics/overview`. |
| **2** | **Run Custom Bright Data Scraper** | Click "Run Scraper Now" button on Dashboard for `Supabase Changelog`. | API calls `POST /sources/{id}/scrape`. |
| **3** | **Show Collector ID** | Highlight the active Bright Data Scraper Studio `Collector ID` (`c_mt46lngz2asqzj8tkj`). | Collector ID persists in database and UI. |
| **4** | **Show Structured JSON** | Display extracted raw JSON payload array returned from Bright Data. | Payload includes `title`, `published_date`, `category`, `description`, `url`. |
| **5** | **Show Validation Score & Trends** | Display Validation Engine score (`100/100`), status `PASS`, and historical trend bar chart. | `validation_results.validation_score == 100.0`. |
| **6** | **Introduce Extraction Failure** | Simulate DOM structure change (e.g. inject selector mismatch where `title` class changes). | Trigger extraction run against modified structure. |
| **7** | **Show Failure Detection** | Validation engine detects missing required `title` field across records. Status drops to `DEGRADED`. | `failure_events` generated with `REQUIRED_FIELD_MISSING`. |
| **8** | **Open AI Intelligence Panel** | Navigate to Insights / AI Intelligence page (`/insights`). | Displays AI Engine Active, Provider (`mock`/`openai`), Model (`gpt-4o-mini`). |
| **9** | **Show AI Root Cause & Evidence** | Display AI Diagnosis: Category `missing_field`, Confidence `88%`, Root Cause, Evidence list. | Real record in `ai_diagnoses` DB table. |
| **10** | **Show Safety Gate Evaluation** | Show Safety Gate decision: `LOW RISK` + High Confidence $\rightarrow$ `AUTOMATIC REPAIR APPROVED`. | SafetyGate policy evaluated. |
| **11** | **Execute AI-Guided Heal** | Open Healing tab. Click "Execute AI Guided Heal". | API calls `POST /failures/{id}/heal`. |
| **12** | **Rerun SAME Collector ID** | Trigger automatic post-heal execution run. Highlight that the **SAME Collector ID** (`c_mt46lngz2asqzj8tkj`) is reused. | Invariant `collector_id` verified. |
| **13** | **Show Recovered Output** | Display new structured JSON returned post-healing with correctly extracted titles and fields. | Extraction payload restored. |
| **14** | **Show Independent Validation** | Validation engine re-evaluates payload: status returns to `PASS`. | `scrape_runs.status == 'SUCCESS'`. |
| **15** | **Show DB & Dashboard Recovery** | Refresh Dashboard. Show source status back to `HEALTHY`, score back to `100/100`, total record counts incremented. | `sources.status == 'HEALTHY'`. |
| **16** | **Show AI Repair History** | Open Insights tab. Show AI Repair History table with `VERIFIED` status. | `ai_diagnoses.verification_status == 'verified'`. |
| **17** | **Verify AI Fallback** | Temporarily set `AI_ENABLED=false`. Execute scrape failure. Verify system falls back to Phase 5 deterministic healing seamlessly. | Safe fallback verified. |

---

## 3. Key Video Callouts

1. Highlight Bright Data Scraper Studio interface / CLI integration.
2. Highlight invariant `Collector ID` continuity before and after healing.
3. Show live transition: `HEALTHY` $\rightarrow$ `DEGRADED` $\rightarrow$ `AI DIAGNOSIS` $\rightarrow$ `SAFETY GATE APPROVED` $\rightarrow$ `VERIFIED RECOVERY` $\rightarrow$ `HEALTHY`.
