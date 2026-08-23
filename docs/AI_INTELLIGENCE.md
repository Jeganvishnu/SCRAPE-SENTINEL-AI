# Phase 7 — AI Scraper Intelligence Architecture

## Overview
Phase 7 introduces an explainable **AI Scraper Intelligence** layer into **Scrape Sentinel AI**. The AI layer operates as a diagnostic and planning engine that proposes structured repairs. The existing Phase 5 recovery and Phase 6 validation engines remain the final authority for verification.

```
                  SCRAPE
                    ↓
               VALIDATION
                    ↓
                FAILURE
                    ↓
          ┌─────────────────┐
          │ AI INTELLIGENCE │
          ├─────────────────┤
          │ Context Builder │
          │ Diagnose        │
          │ Find evidence   │
          │ Plan repair     │
          │ Safety Gate     │
          └────────┬────────┘
                   ↓
              SAFETY GATE
                   ↓
          EXISTING PHASE 5
             HEALING ENGINE
                   ↓
             RECOVERY SCRAPE
                   ↓
              VALIDATION
                   ↓
          ┌────────┴────────┐
          ↓                 ↓
       VERIFIED           FAILED
          ↓                 ↓
       PHASE 6          Manual review
       METRICS
```

---

## 1. Provider Abstraction
The AI layer is decoupled from specific vendors via `BaseAIProvider` (`backend/app/ai/provider.py`):
- `MockAIProvider`: Deterministic rule-based provider for offline mode, testing, and fallback.
- `OpenAIProvider`: LLM provider supporting structured JSON mode and prompt injection defense.

---

## 2. Safety Gate & Confidence Policy

| Confidence Level | Risk Level | Safety Gate Decision | Verification Policy |
| :--- | :--- | :--- | :--- |
| **$\ge$ 0.85 (High)** | **LOW** | `AUTOMATIC REPAIR APPROVED` | Phase 5 Execution + Phase 6 Independent Validation Required |
| **0.65 – 0.8499 (Medium)** | **MEDIUM** | `MANUAL HUMAN REVIEW REQUIRED` | User Approval via Sentinel UI before Phase 5 Execution |
| **< 0.65 (Low)** | **HIGH / BLOCKED** | `BLOCKED` | Manual Inspection Required |

---

## 3. Repair Type Allowlist
The AI is restricted to a safe, deterministic repair allowlist:
- `selector_update`: Allowed
- `field_mapping_update`: Allowed
- `schema_mapping_update`: Allowed
- `pagination_adjustment`: Allowed
- `normalization_update`: Allowed
- `retry_adjustment`: Allowed
- `no_repair`: Allowed
- `manual_review`: Allowed
- *Destructive commands (`execute_shell`, `delete_database`)*: **BLOCKED & REJECTED**

---

## 4. Prompt Injection Defense
Scraped web pages are untrusted third-party inputs. Scrape Sentinel AI encapsulates scraped web payload samples under `<UNTRUSTED_WEB_DATA>` delimiters with strict system instructions:
- Prompt overrides inside web data are ignored.
- Page content is treated strictly as passive data, never as system instructions.

---

## 5. Failure Classification Categories
The AI classifies scraper failures into strict categories:
- `selector_changed`
- `schema_changed`
- `missing_field`
- `renamed_field`
- `pagination_changed`
- `empty_result`
- `record_count_anomaly`
- `content_format_changed`
- `timeout`
- `validation_error`
- `unknown`

---

## 6. Repair Loop Protection & Fallback
- **Max Attempts Limit**: A maximum of 3 repair attempts is enforced per failure event. Exceeding this limit automatically sets status to `requires_manual_review`.
- **Offline / Failure Fallback**: If the AI API is unavailable or disabled (`AI_ENABLED=false`), the system logs the event and seamlessly falls back to Phase 5 deterministic healing without crashing.
