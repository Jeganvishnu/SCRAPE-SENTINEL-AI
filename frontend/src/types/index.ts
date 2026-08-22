export type SourceStatus = 'HEALTHY' | 'WARNING' | 'FAILED' | 'HEALING' | 'NEEDS_APPROVAL';

export interface Source {
  id: string;
  name: string;
  url: string;
  collectorId: string;
  status: SourceStatus;
  createdAt: string;
  updatedAt: string;
}

export type RunStatus = 'RUNNING' | 'SUCCESS' | 'FAILED' | 'WARNING';

export interface ScrapeRun {
  id: string;
  sourceId: string;
  startedAt: string;
  completedAt?: string;
  status: RunStatus;
  recordsCount: number;
  errorMessage?: string;
}

export interface ScrapedRecord {
  id: string;
  sourceId: string;
  title: string;
  publishedDate: string;
  version?: string;
  category: string;
  description: string;
  url: string;
  contentHash: string;
  scrapedAt: string;
  collectorId: string;
}

export type FailureType = 'REQUIRED_FIELD_MISSING' | 'RECORD_COUNT_DROP' | 'ZERO_RECORDS' | 'SCHEMA_MISMATCH';
export type HealStatus = 'INITIATED' | 'PENDING_APPROVAL' | 'SENT_TO_BRIGHT_DATA' | 'HEALED' | 'FAILED';
export type ApprovalStatus = 'NOT_REQUIRED' | 'PENDING' | 'APPROVED' | 'REJECTED';
export type RerunStatus = 'PENDING' | 'RERUNNING' | 'PASSED' | 'FAILED';

export interface HealingEvent {
  id: string;
  sourceId: string;
  failureType: FailureType;
  failureRate: number;
  healPrompt: string;
  healStatus: HealStatus;
  approvalStatus: ApprovalStatus;
  rerunStatus: RerunStatus;
  recoveryTimestamp?: string;
}

export type ChangeType = 'BREAKING_CHANGE' | 'DEPRECATION' | 'NEW_FEATURE' | 'BUG_FIX' | 'PERFORMANCE';

export interface AIInsight {
  id: string;
  recordId: string;
  changeType: ChangeType;
  impactScore: number;
  summary: string;
  reason: string;
  recommendation: string;
  createdAt: string;
}

export interface HealthStatus {
  status: string;
  service: string;
  version: string;
}
