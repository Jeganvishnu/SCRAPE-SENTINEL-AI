# Scrape Sentinel AI — Judge Q&A & Defense Guide

### Q1: Why did you choose this problem?
**Answer**: Web scraping pipelines are notoriously brittle. Website DOM updates silently corrupt downstream analytics or AI RAG apps. Manual scraper maintenance consumes engineering time. Scrape Sentinel AI turns scraper failure into an observable, self-healing lifecycle.

### Q2: What makes this different from a normal web scraper?
**Answer**: Traditional scrapers blindly retry or fail silently. Scrape Sentinel AI adds deterministic field/schema validation, explainable AI root-cause analysis, safety-gated repair planning, and independent verification before declaring recovery.

### Q3: What role does Bright Data Scraper Studio play?
**Answer**: Bright Data Scraper Studio is our core extraction engine. We created and deployed a custom collector (`c_mt46lngz2asqzj8tkj`) to extract structured public data. The backend triggers the collector via `@brightdata/cli` and HTTP APIs.

### Q4: Can AI execute arbitrary shell commands or code?
**Answer**: Absolutely not. AI is restricted to a strict repair allowlist (`selector_update`, `field_mapping_update`, `schema_mapping_update`). Destructive commands like `execute_shell` or `delete_database` are blocked by the Safety Gate.

### Q5: How do you prevent endless repair loops?
**Answer**: We enforce a hard limit of 3 repair attempts per failure event. Exceeding 3 attempts automatically flags the failure for manual human review.

### Q6: How do you handle prompt injection from scraped web data?
**Answer**: Scraped content is treated as untrusted input and encapsulated under `<UNTRUSTED_WEB_DATA>` delimiters. System instructions explicitly command the AI to ignore any prompt overrides inside web content.

### Q7: What happens if the AI service fails or is disabled?
**Answer**: The system safely falls back to Phase 5 deterministic healing without crashing. AI is optional and non-blocking.

### Q8: What is your MTTR metric?
**Answer**: MTTR (Mean Time To Recovery) measures the exact duration in seconds from failure detection (`detected_at`) to verified recovery completion (`completed_at`).
