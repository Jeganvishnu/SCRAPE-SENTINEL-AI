# Scrape Sentinel AI — Final Hackathon Submission Pitches

> **Project Name:** SCRAPE SENTINEL AI  
> **Repository:** https://github.com/Jeganvishnu/SCRAPE-SENTINEL-AI  
> **Tagline:** "An explainable self-healing web scraping platform powered by Bright Data Scraper Studio."

---

## 1. 30-Second Elevator Pitch
"Web scrapers break silently whenever target websites update their DOM layout, corrupting downstream analytics and AI pipelines. Scrape Sentinel AI solves this. Powered by Bright Data Scraper Studio (Collector `c_mt46lngz2asqzj8tkj`), our platform detects missing fields through deterministic validation, uses AI to diagnose structural DOM changes with evidence, evaluates safe repairs through a Safety Gate, executes approved fixes through a Phase 5 self-healing engine, and only declares recovery after independent Phase 6 validation succeeds."

---

## 2. 60-Second Hackathon Pitch
"Every web data pipeline faces a fundamental flaw: when target websites alter their HTML structure or CSS selectors, traditional scrapers fail silently or crash without telemetry.

Scrape Sentinel AI turns scraper failure into an observable, self-healing lifecycle. Built on Bright Data Scraper Studio, our custom collector collects structured public data. When layout shifts occur, our Validation Engine detects missing required properties and records a failure event.

Instead of letting AI blindly modify code, AI proposes explainable repairs backed by evidence from historical runs. Our Safety Gate evaluates risk policy—allowing low-risk repairs while flagging ambiguous changes for human review.

The Phase 5 self-healing engine re-runs extraction using the SAME Bright Data Collector ID, and recovery is only declared verified when independent validation passes 100%. All telemetry, MTTR, and health scores are tracked live on our observability dashboard."

---

## 3. 3-Minute Technical Explanation
"Scrape Sentinel AI is engineered around a closed-loop extraction reliability lifecycle:

1. **Extraction**: Custom Bright Data Scraper Studio collector (`c_mt46lngz2asqzj8tkj`) extracts public developer release notes from `https://supabase.com/changelog`.
2. **Validation**: The backend Validation Engine (`backend/app/validators/engine.py`) checks required fields, date formats, URL integrity, duplicates, and record count anomalies.
3. **Failure Detection**: If required properties (e.g. `title`) are missing, a `FailureEvent` is persisted to Supabase PostgreSQL, and System Health drops to `DEGRADED`.
4. **AI Diagnosis & Safety Gate**: The AI Intelligence layer builds a compact failure context comparing the failed payload with previous successful sample records and historical schema diffs.
   - **Explainable Diagnosis**: AI classifies the failure (`missing_field`, `schema_changed`) and produces root cause analysis backed by bullet-point evidence.
   - **Safety Gate**: AI is restricted to a strict repair allowlist (`selector_update`, `field_mapping_update`). Destructive commands are **BLOCKED**. Confidence $\ge 0.85$ + LOW risk allows automated execution.
5. **Phase 5 Self-Healing**: Approved repairs re-execute using the **SAME** Bright Data Collector ID, maintaining data lineage continuity.
6. **Recovery Verification**: AI cannot claim success. The re-scraped payload must independently pass the Phase 6 Validation Engine before `HealingAttempt.status` becomes `VERIFIED`.
7. **Phase 6 Observability**: All telemetry, MTTR in seconds, health scores (0–100), and activity feed timelines update live on the React dashboard."
