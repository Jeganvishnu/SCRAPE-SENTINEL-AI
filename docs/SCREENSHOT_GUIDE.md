# Scrape Sentinel AI — Screenshot Capture Guide

This guide details all required screenshots for submission documentation, README presentation, and judge review.

---

## Required Screenshots List

Save all captured images into `docs/screenshots/`:

| # | File Name | Route / View | Target UI Elements |
| :- | :--- | :--- | :--- |
| **1** | `01_dashboard_overview.png` | `http://localhost:5173/` | System Health Score (100/100), Status Pill (`HEALTHY`), Telemetry Cards (Success Rate 100%, Validation Quality 100%, MTTR), and Activity Feed Timeline. |
| **2** | `02_brightdata_collector.png` | Bright Data Scraper Studio UI or Terminal | Scraper Studio Collector ID `c_mt46lngz2asqzj8tkj`, target source (`https://supabase.com/changelog`), and output configuration. |
| **3** | `03_failure_detected.png` | `http://localhost:5173/` | System Health Score dropped to `DEGRADED`, Warning alert box, and recorded `REQUIRED_FIELD_MISSING` failure event. |
| **4** | `04_ai_insights_diagnosis.png` | `http://localhost:5173/insights` | AI Root-Cause Diagnosis panel, Confidence score (`88%`), Evidence bullet points, and Safety Gate decision (`LOW RISK`). |
| **5** | `05_healing_queue.png` | `http://localhost:5173/healing` | Phase 5 Healing Queue table, attempt numbers, and "Execute AI Guided Heal" button. |
| **6** | `06_recovery_verified.png` | `http://localhost:5173/` | Post-healing recovery verification state, System Health restored to `HEALTHY`, updated MTTR in seconds, and verified validation score. |

---

## Capture Procedure

1. Open `http://localhost:5173` in Google Chrome or Microsoft Edge.
2. Set browser resolution to **1920 x 1080** (Full HD).
3. Use `F12` Developer Tools $\rightarrow$ Command Palette (`Ctrl+Shift+P`) $\rightarrow$ type `Capture full size screenshot` (or press `Alt + Print Screen`).
4. Move saved PNGs into `docs/screenshots/`.
