# Scrape Sentinel AI — Controlled Demo Scenario Guide

This directory contains instructions for performing a repeatable live demo or video recording of **Scrape Sentinel AI**.

---

## Controlled Demo Walkthrough

### 1. Normal Extraction Run (Healthy Baseline)
1. Start backend: `uvicorn main:app --reload --port 8000` in `backend/`.
2. Start frontend: `npm run dev` in `frontend/`.
3. Open Dashboard at `http://localhost:5173`.
4. Click **"Run Scraper Now"** for `Supabase Changelog`.
5. Verify status is **`HEALTHY`**, score is **`100/100`**, and 2 records are extracted.

### 2. Controlled DOM Failure Injection
1. Execute controlled extraction failure simulation or invoke target with missing title selector.
2. Observe validation failure: status changes to **`DEGRADED`**, score drops.

### 3. AI Diagnosis & Safety Gate Evaluation
1. Open **Insights AI Panel** (`http://localhost:5173/insights`).
2. Review AI Diagnosis: Category `missing_field`, Confidence `88%`, Root cause, and Evidence bullet points.
3. Observe Safety Gate evaluation: `LOW RISK` + High Confidence $\rightarrow$ **`AUTOMATIC REPAIR APPROVED`**.

### 4. Verified Phase 5 Self-Healing
1. Open **Healing Queue** (`http://localhost:5173/healing`).
2. Click **"Execute AI Guided Heal"**.
3. Re-execution occurs using the **SAME** Bright Data Collector ID (`c_mt46lngz2asqzj8tkj`).
4. Validation Engine re-evaluates payload and marks recovery **`VERIFIED`**.
5. Return to Dashboard: status restores to **`HEALTHY`**, score restores to **`100/100`**, and MTTR is logged.
