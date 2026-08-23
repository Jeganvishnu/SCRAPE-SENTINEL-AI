# Scrape Sentinel AI — REST API Specification

## System & Health Endpoints

### `GET /health`
Returns the status of backend dependencies.
- **Response**:
  ```json
  {
    "status": "healthy",
    "database": "connected",
    "bright_data": "configured",
    "version": "1.0.0",
    "timestamp": "2026-08-23T07:00:00Z"
  }
  ```

### `GET /ready`
Readiness check for load balancers and deployment orchestrators.

### `GET /system/status`
Returns weighted health score (0–100) and human-readable explanation.

---

## Sources Endpoints

### `GET /sources`
Lists registered target web sources.

### `GET /sources/{source_id}`
Returns details for a single target source.

### `POST /sources/{source_id}/scrape`
Triggers extraction via Bright Data Scraper Studio.

---

## Observability & Metrics Endpoints

### `GET /metrics/overview`
Query parameter: `period` (`24h`, `7d`, `30d`, `all`). Returns overview telemetry, success rate, validation score, MTTR, and recovery rate.

### `GET /metrics/sources/{source_id}`
Returns source health header, success rate, and historical metrics.

### `GET /metrics/timeline`
Returns chronological activity feed timeline events (`scrape_completed`, `failure_detected`, `recovery_verified`).

### `GET /metrics/validation`
Returns historical validation quality trend data points.

### `GET /metrics/schema/{source_id}`
Returns schema fingerprints and structural drift history.

### `GET /metrics/healing`
Returns healing recovery metrics and MTTR in seconds.

---

## AI Scraper Intelligence Endpoints

### `GET /ai/status`
Returns AI configuration status, active provider, model, total diagnoses, and verification rate.

### `POST /ai/diagnose/{failure_id}`
Triggers AI root cause analysis and evidence collection for a failure event.

### `POST /ai/repair-plan/{failure_id}`
Generates structured repair plan and Safety Gate evaluation.

### `GET /ai/history`
Query parameter: `source_id`. Returns historical AI diagnoses and verification results.

---

## Failures & Healing Endpoints

### `GET /failures`
Lists all extraction failure events.

### `GET /failures/{failure_id}`
Returns details for a failure event including AI diagnosis.

### `POST /failures/{failure_id}/heal`
Triggers the Phase 5 self-healing pipeline, executes recovery scrape, and re-validates output.
