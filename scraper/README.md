# Scrape Sentinel AI — Bright Data Scraper Studio Directory

> **Phase:** 2 — Configuration & Scraper Workspace Placeholder

This directory is reserved for Bright Data Scraper Studio configuration files, custom collector definitions, scraper execution scripts (`create.py`, `run.py`, `heal.py`), and local testing harnesses.

## Key Rules & Guidelines
- **Primary Scraper:** Bright Data Scraper Studio is the exclusive primary scraping engine for Scrape Sentinel AI.
- **Collector ID Persistence:** All iterations (initial execution, DOM failure detection, self-healing reruns) preserve the exact same `Collector ID`.
- **No Direct Scraper Execution in Phase 2:** Collector creation, scraping runs, and automated healing commands will be implemented in Phase 3 and Phase 5.
