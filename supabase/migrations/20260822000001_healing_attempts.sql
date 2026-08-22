-- Migration: 20260822000001_healing_attempts.sql
-- Description: Create Phase 6 Healing Attempts Table, Indexes, and RLS for Observability and Recovery Lifecycle

CREATE TABLE IF NOT EXISTS healing_attempts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_id UUID REFERENCES sources(id) ON DELETE CASCADE,
    scrape_run_id UUID REFERENCES scrape_runs(id) ON DELETE CASCADE,
    failure_event_id UUID REFERENCES failure_events(id) ON DELETE CASCADE,
    collector_id TEXT NOT NULL,
    attempt_number INTEGER NOT NULL DEFAULT 1,
    started_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    completed_at TIMESTAMPTZ,
    status TEXT NOT NULL DEFAULT 'queued' CHECK (status IN ('queued', 'running', 'success', 'failed', 'verified')),
    failure_type TEXT,
    previous_schema_fingerprint TEXT,
    new_schema_fingerprint TEXT,
    old_instruction_hash TEXT,
    new_instruction_hash TEXT,
    verification_run_id UUID REFERENCES scrape_runs(id) ON DELETE SET NULL,
    error_code TEXT,
    error_message TEXT,
    details JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_healing_attempts_source_id ON healing_attempts(source_id);
CREATE INDEX IF NOT EXISTS idx_healing_attempts_scrape_run_id ON healing_attempts(scrape_run_id);
CREATE INDEX IF NOT EXISTS idx_healing_attempts_failure_event_id ON healing_attempts(failure_event_id);
CREATE INDEX IF NOT EXISTS idx_healing_attempts_status ON healing_attempts(status);

ALTER TABLE healing_attempts ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "Allow all access to service role on healing_attempts" ON healing_attempts;
CREATE POLICY "Allow all access to service role on healing_attempts" ON healing_attempts FOR ALL USING (true);
