# Phase 6 — Observability, Monitoring & Reliability Architecture

## Overview
Phase 6 establishes a production monitoring and observability layer for **Scrape Sentinel AI**. Every extraction attempt becomes a transparent lifecycle:

```
SCRAPE STARTED
      ↓
SCRAPER EXECUTED
      ↓
OUTPUT RECEIVED
      ↓
VALIDATED
      ↓
FAILURE DETECTED
      ↓
HEALING ATTEMPT
      ↓
HEALING RESULT
      ↓
RECOVERY SCRAPE
      ↓
RECOVERY VALIDATION
      ↓
HEALTHY / FAILED
```

---

## 1. Health State Thresholds & Definitions

| Health State | Condition |
| :--- | :--- |
| **HEALTHY** | Success rate `≥ 85%`, average validation score `≥ 85/100`, zero active critical/high failures. |
| **WARNING** | Success rate `75–84%`, average validation score `70–84/100`, or unresolved low/medium warnings. |
| **DEGRADED** | Success rate `< 75%`, validation score `< 70/100`, or active unresolved high-severity failures. |
| **CRITICAL** | Success rate `< 50%` with active unresolved critical failures. |

---

## 2. Health Score Algorithm (0–100)

The health score is computed deterministically using real historical database metrics:

$$\text{Health Score} = (0.25 \times \text{SR}) + (0.20 \times \text{VQ}) + (0.15 \times \text{FS}) + (0.15 \times \text{RR}) + (0.10 \times \text{CS}) + (0.10 \times \text{SS}) + (0.05 \times \text{ER})$$

Where:
- **SR (Success Rate)**: Percentage of successful scrape runs.
- **VQ (Validation Quality)**: Average validation score (0–100).
- **FS (Failure Stability)**: 100 if zero open failures; 70 if low/medium failures; 0 if critical/high open failures.
- **RR (Recovery Rate)**: `(Verified Healing Attempts / Total Healing Attempts) * 100`. Defaults to 100% if no healing attempts exist.
- **CS (Record-Count Stability)**: Penalizes sudden drops in record count.
- **SS (Schema Stability)**: Penalizes structural schema drift.
- **ER (Execution Reliability)**: Subprocess execution baseline (100).

---

## 3. Reliability Metrics Definitions

- **Mean Time To Recovery (MTTR)**: Measured in seconds from `failure_event.detected_at` to `healing_attempt.completed_at` for verified recoveries:
  $$\text{MTTR} = \frac{\sum (\text{completed\_at} - \text{started\_at})}{\text{Verified Recoveries}}$$
  *(Returns `null` if 0 verified recoveries exist).*
- **Recovery Rate**: Percentage of healing attempts resulting in verified recovery. *(Returns `null` if 0 healing attempts exist).*

---

## 4. API Endpoints

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `GET /metrics/overview` | `GET` | Period overview (`24h`, `7d`, `30d`, `all`). |
| `GET /metrics/sources/{id}` | `GET` | Detailed source metrics and health header. |
| `GET /metrics/timeline` | `GET` | Chronological activity feed events. |
| `GET /metrics/validation` | `GET` | Historical validation quality trend points. |
| `GET /metrics/schema/{id}` | `GET` | Historical schema fingerprints and drift events. |
| `GET /metrics/healing` | `GET` | Recovery rate and MTTR metrics. |
| `GET /ready` | `GET` | Dependency readiness check. |
| `GET /system/status` | `GET` | System health badge and score. |
