-- Migration: 20260822000000_init_schema.sql
-- Description: Create Phase 4 Core Tables, Indexes, Constraints, and RLS for Scrape Sentinel AI

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. SOURCES TABLE
CREATE TABLE IF NOT EXISTS sources (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    url TEXT NOT NULL,
    collector_id TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'paused', 'failed', 'healing', 'warning')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_sources_collector_id ON sources(collector_id);

-- 2. SCRAPE RUNS TABLE
CREATE TABLE IF NOT EXISTS scrape_runs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_id UUID REFERENCES sources(id) ON DELETE CASCADE,
    collector_id TEXT NOT NULL,
    started_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    completed_at TIMESTAMPTZ,
    status TEXT NOT NULL DEFAULT 'running' CHECK (status IN ('running', 'success', 'partial', 'failed', 'invalid')),
    records_found INTEGER NOT NULL DEFAULT 0,
    records_valid INTEGER NOT NULL DEFAULT 0,
    records_invalid INTEGER NOT NULL DEFAULT 0,
    duration_ms BIGINT,
    error_code TEXT,
    error_message TEXT,
    raw_output_hash TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_scrape_runs_source_id ON scrape_runs(source_id);
CREATE INDEX IF NOT EXISTS idx_scrape_runs_started_at ON scrape_runs(started_at DESC);

-- 3. SCRAPED RECORDS TABLE
CREATE TABLE IF NOT EXISTS scraped_records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_id UUID REFERENCES sources(id) ON DELETE CASCADE,
    scrape_run_id UUID REFERENCES scrape_runs(id) ON DELETE CASCADE,
    title TEXT,
    published_date TIMESTAMPTZ,
    version TEXT,
    category TEXT,
    description TEXT,
    url TEXT,
    content_hash TEXT NOT NULL,
    scraped_at TIMESTAMPTZ NOT NULL,
    raw_data JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_scraped_records_source_id ON scraped_records(source_id);
CREATE INDEX IF NOT EXISTS idx_scraped_records_scrape_run_id ON scraped_records(scrape_run_id);
CREATE INDEX IF NOT EXISTS idx_scraped_records_content_hash ON scraped_records(content_hash);

-- 4. VALIDATION RESULTS TABLE
CREATE TABLE IF NOT EXISTS validation_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    scrape_run_id UUID REFERENCES scrape_runs(id) ON DELETE CASCADE,
    validation_status TEXT NOT NULL CHECK (validation_status IN ('passed', 'warning', 'failed')),
    schema_valid BOOLEAN NOT NULL,
    required_fields_valid BOOLEAN NOT NULL,
    url_valid BOOLEAN NOT NULL,
    date_valid BOOLEAN NOT NULL,
    duplicate_free BOOLEAN NOT NULL,
    record_count_valid BOOLEAN NOT NULL,
    schema_change_detected BOOLEAN NOT NULL DEFAULT false,
    validation_score NUMERIC(5,2),
    issues JSONB,
    validated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_validation_results_scrape_run_id ON validation_results(scrape_run_id);

-- 5. FAILURE EVENTS TABLE
CREATE TABLE IF NOT EXISTS failure_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_id UUID REFERENCES sources(id) ON DELETE CASCADE,
    scrape_run_id UUID REFERENCES scrape_runs(id) ON DELETE CASCADE,
    failure_type TEXT NOT NULL CHECK (failure_type IN ('authentication_failure', 'collector_failure', 'empty_result', 'record_count_drop', 'schema_change', 'required_field_missing', 'invalid_url', 'invalid_date', 'duplicate_records', 'malformed_output', 'timeout', 'unknown')),
    severity TEXT NOT NULL CHECK (severity IN ('low', 'medium', 'high', 'critical')),
    message TEXT NOT NULL,
    details JSONB,
    detected_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    status TEXT NOT NULL DEFAULT 'open' CHECK (status IN ('open', 'acknowledged', 'resolved'))
);

CREATE INDEX IF NOT EXISTS idx_failure_events_source_id ON failure_events(source_id);
CREATE INDEX IF NOT EXISTS idx_failure_events_scrape_run_id ON failure_events(scrape_run_id);
CREATE INDEX IF NOT EXISTS idx_failure_events_status ON failure_events(status);

-- ENABLE ROW LEVEL SECURITY
ALTER TABLE sources ENABLE ROW LEVEL SECURITY;
ALTER TABLE scrape_runs ENABLE ROW LEVEL SECURITY;
ALTER TABLE scraped_records ENABLE ROW LEVEL SECURITY;
ALTER TABLE validation_results ENABLE ROW LEVEL SECURITY;
ALTER TABLE failure_events ENABLE ROW LEVEL SECURITY;

-- CREATE RLS POLICIES FOR BACKEND / SERVICE ROLE ACCESS
DROP POLICY IF EXISTS "Allow all access to service role on sources" ON sources;
CREATE POLICY "Allow all access to service role on sources" ON sources FOR ALL USING (true);

DROP POLICY IF EXISTS "Allow all access to service role on scrape_runs" ON scrape_runs;
CREATE POLICY "Allow all access to service role on scrape_runs" ON scrape_runs FOR ALL USING (true);

DROP POLICY IF EXISTS "Allow all access to service role on scraped_records" ON scraped_records;
CREATE POLICY "Allow all access to service role on scraped_records" ON scraped_records FOR ALL USING (true);

DROP POLICY IF EXISTS "Allow all access to service role on validation_results" ON validation_results;
CREATE POLICY "Allow all access to service role on validation_results" ON validation_results FOR ALL USING (true);

DROP POLICY IF EXISTS "Allow all access to service role on failure_events" ON failure_events;
CREATE POLICY "Allow all access to service role on failure_events" ON failure_events FOR ALL USING (true);
