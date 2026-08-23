-- Migration: 20260823000000_ai_diagnoses.sql
-- Create ai_diagnoses table for Phase 7 AI Scraper Intelligence reasoning & audit

CREATE TABLE IF NOT EXISTS public.ai_diagnoses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_id UUID NOT NULL REFERENCES public.sources(id) ON DELETE CASCADE,
    failure_event_id UUID NOT NULL REFERENCES public.failure_events(id) ON DELETE CASCADE,
    healing_attempt_id UUID REFERENCES public.healing_attempts(id) ON DELETE SET NULL,
    model TEXT NOT NULL,
    prompt_version TEXT NOT NULL,
    failure_category TEXT NOT NULL,
    confidence NUMERIC(4,2) NOT NULL,
    root_cause TEXT NOT NULL,
    evidence JSONB NOT NULL DEFAULT '[]'::jsonb,
    repair_type TEXT NOT NULL,
    repair_plan JSONB NOT NULL DEFAULT '{}'::jsonb,
    risk TEXT NOT NULL,
    approved BOOLEAN NOT NULL DEFAULT FALSE,
    requires_manual_review BOOLEAN NOT NULL DEFAULT FALSE,
    verification_status TEXT NOT NULL DEFAULT 'pending',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexes for efficient query filtering
CREATE INDEX IF NOT EXISTS idx_ai_diagnoses_source_id ON public.ai_diagnoses(source_id);
CREATE INDEX IF NOT EXISTS idx_ai_diagnoses_failure_event_id ON public.ai_diagnoses(failure_event_id);
CREATE INDEX IF NOT EXISTS idx_ai_diagnoses_created_at ON public.ai_diagnoses(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_ai_diagnoses_verification_status ON public.ai_diagnoses(verification_status);

-- Enable RLS
ALTER TABLE public.ai_diagnoses ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Allow read access to ai_diagnoses" ON public.ai_diagnoses;
CREATE POLICY "Allow read access to ai_diagnoses" ON public.ai_diagnoses
    FOR SELECT USING (true);

DROP POLICY IF EXISTS "Allow write access to ai_diagnoses" ON public.ai_diagnoses;
CREATE POLICY "Allow write access to ai_diagnoses" ON public.ai_diagnoses
    FOR ALL USING (true);
