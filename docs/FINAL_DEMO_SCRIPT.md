# Scrape Sentinel AI — Hackathon Final Video Demo Script

> **Target Duration:** 3.5 – 5 Minutes  
> **Key Message:** "Scrape Sentinel AI transforms brittle web scraping into an observable, explainable recovery system powered by Bright Data Scraper Studio."

---

## Storyboard & Timing Breakdown

### 0:00 – 0:30 | The Problem
- **Visual**: Show traditional web scraper breaking on a website layout change.
- **Narrator**: "Web scrapers silently break when websites update their layout. Selector changes and missing fields corrupt downstream pipelines, requiring manual engineering fixes."

### 0:30 – 1:00 | Architecture & Bright Data Scraper Studio
- **Visual**: Show architecture diagram and Bright Data Scraper Studio interface.
- **Narrator**: "Scrape Sentinel AI solves this. Powered by Bright Data Scraper Studio (Collector `c_mt46lngz2asqzj8tkj`), we collect structured public data from target websites."

### 1:00 – 1:45 | Normal Scrape & Observability Dashboard
- **Visual**: Open Dashboard (`http://localhost:5173`). Click "Run Scraper Now". Show 100/100 Health Score, success rate, validation score bar chart, and activity timeline.
- **Narrator**: "During normal operation, extracted payloads pass deterministic field and schema validation. The reliability dashboard tracks real-time telemetry, transparent health scores, and record counts."

### 1:45 – 2:30 | Failure Detection & AI Scraper Intelligence
- **Visual**: Trigger a controlled DOM failure (e.g. missing title field). Dashboard status shifts to `DEGRADED`. Open Insights AI Panel (`/insights`). Show AI Root Cause, Evidence list, and Safety Gate evaluation (`LOW RISK`, `88% Confidence`).
- **Narrator**: "When target layout changes, the Validation Engine detects missing required properties and logs a Failure Event. The AI Intelligence layer builds a compact failure context, identifies root causes with evidence, and evaluates repair safety."

### 2:30 – 3:30 | Safety Gate & Verified Self-Healing
- **Visual**: Open Healing tab (`/healing`). Click "Execute AI Guided Heal". Show recovery scrape re-running using the **SAME Collector ID**. Show Validation Engine re-evaluating output and marking recovery `VERIFIED`.
- **Narrator**: "AI proposes repairs, but deterministic validation is the final authority. The Phase 5 healing engine re-executes using the SAME Bright Data Collector ID. Scrape Sentinel AI only declares recovery when independent validation succeeds."

### 3:30 – 4:30 | Reliability Telemetry & Dashboard Recovery
- **Visual**: Return to Dashboard. Show System Health back to `HEALTHY`, Health Score updated, MTTR logged, and AI Repair History recorded.
- **Narrator**: "Dashboard health score and telemetry update in real-time. Every failure and recovery is observable, explainable, and fully audited."
