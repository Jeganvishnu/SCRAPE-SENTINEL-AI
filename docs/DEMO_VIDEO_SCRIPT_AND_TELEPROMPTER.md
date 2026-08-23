# Scrape Sentinel AI — Full Demo Video Script & Teleprompter

> **Target Duration:** 4.0 – 4.5 Minutes  
> **Speaker Role:** Hackathon Participant / Presenter  
> **Pre-recording Setup:** Run backend on port 8000, frontend on port 5173, microphone set to 1080p recording.

---

## Storyboard & Verbatim Spoken Script

### SECTION 1: Introduction & Problem Statement (0:00 – 0:35)

- **On Screen**: Show traditional web scraper breaking on HTML layout change / error console.
- **Spoken Script (Verbatim)**:
  > *"Hello everyone! Web scrapers are the lifeblood of modern data pipelines, AI models, and market intelligence. But they suffer from a fatal flaw: websites constantly change their HTML structure and CSS selectors.
  > When a website updates its DOM, traditional scrapers fail silently or crash, corrupting downstream analytics and AI RAG pipelines. Engineers waste hours manually inspecting logs and re-authoring code.
  > Today, I'm excited to present **Scrape Sentinel AI**—an explainable, self-healing web scraping platform powered by **Bright Data Scraper Studio**."*

---

### SECTION 2: Architecture & Bright Data Scraper Studio (0:35 – 1:15)

- **On Screen**: Switch to Architecture Diagram in `README.md`, then show Bright Data Scraper Studio Collector `c_mt46lngz2asqzj8tkj`.
- **Spoken Script (Verbatim)**:
  > *"Here is how Scrape Sentinel AI works. At its core, data extraction is handled by a custom collector instance built inside **Bright Data Scraper Studio** with ID `c_mt46lngz2asqzj8tkj`.
  > Our target source is a public developer changelog—specifically the Supabase technical updates log. The backend executes this collector via Bright Data's CLI and REST APIs, receiving clean, structured JSON arrays containing post titles, publication dates, categories, descriptions, and direct URLs."*

---

### SECTION 3: Normal Extraction & Reliability Dashboard (1:15 – 1:55)

- **On Screen**: Open Dashboard at `http://localhost:5173`. Click **"Run Scraper Now"**. Show 100/100 Health Score, green status, and record count.
- **Spoken Script (Verbatim)**:
  > *"Let's look at normal operation. When I trigger an extraction run from the dashboard, raw data flows into our Phase 6 Validation Engine.
  > The validation engine deterministically verifies required fields, date formats, URL integrity, duplicates, and record count stability. Because all items pass validation, our System Health Score is 100 out of 100, and telemetry cards update live."*

---

### SECTION 4: Controlled Failure & Failure Detection (1:55 – 2:35)

- **On Screen**: Trigger controlled layout failure (missing title field). Show dashboard updating status to `DEGRADED`.
- **Spoken Script (Verbatim)**:
  > *"Now, let's simulate what happens when the target website alters its layout and the `title` field selector breaks.
  > Instantly, the Validation Engine flags missing required properties across extracted records. A `FailureEvent` is recorded in our Supabase PostgreSQL database, and System Health drops to DEGRADED. Notice how nothing fails silently—every anomaly is logged and observable."*

---

### SECTION 5: AI Diagnosis & Safety Gate (2:35 – 3:20)

- **On Screen**: Navigate to Insights AI Panel (`/insights`). Highlight Root Cause, Evidence bullet points, and Safety Gate badge (`LOW RISK`).
- **Spoken Script (Verbatim)**:
  > *"Now, the Phase 7 AI Intelligence layer steps in. It constructs a sanitized failure context comparing the failed payload against historical successful runs and schema fingerprints.
  > Here on the Insights panel, the AI classifies the root cause as `missing_field` with 88% confidence. It provides clear, explainable evidence bullet points.
  > Crucially, AI is not given unrestricted execution power. It passes through our Safety Gate, which enforces a strict repair allowlist—only allowing safe selector and mapping updates. Unsafe or destructive commands are strictly BLOCKED."*

---

### SECTION 6: Phase 5 Healing & Recovery Verification (3:20 – 4:05)

- **On Screen**: Navigate to Healing Queue (`/healing`). Click **"Execute AI Guided Heal"**. Show recovery scrape re-running and health restoring to 100/100.
- **Spoken Script (Verbatim)**:
  > *"Because the proposed repair passed the Safety Gate with high confidence, the Phase 5 Self-Healing Engine executes the recovery run using the **SAME** Bright Data Collector ID, maintaining data lineage continuity.
  > But AI cannot declare its own success. The recovery payload undergoes independent validation by the Phase 6 Validation Engine. Only after passing 100% of field checks is recovery officially verified.
  > Returning to the dashboard, System Health is restored to 100/100, MTTR in seconds is logged, and the complete audit trail is preserved."*

---

### SECTION 7: Closing & Submission Summary (4:05 – 4:30)

- **On Screen**: Return to Dashboard main overview showing System Health 100/100.
- **Spoken Script (Verbatim)**:
  > *"Scrape Sentinel AI transforms brittle scrapers into an observable, explainable, self-healing pipeline—giving developers total confidence in their web data pipelines.
  > Thank you for reviewing Scrape Sentinel AI!"*
