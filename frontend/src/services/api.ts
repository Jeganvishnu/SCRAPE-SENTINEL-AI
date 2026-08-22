import { Source, ScrapeRun, HealingEvent } from '../types';

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000';

export async function getHealth(): Promise<any> {
  const response = await fetch(`${BACKEND_URL}/health`, {
    headers: { 'Accept': 'application/json' },
  });
  if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
  return response.json();
}

export async function getOverviewMetrics(period: string = '7d'): Promise<any> {
  const response = await fetch(`${BACKEND_URL}/metrics/overview?period=${period}`);
  if (!response.ok) throw new Error('Failed to fetch overview metrics');
  return response.json();
}

export async function getSourceMetrics(sourceId: string, period: string = '7d'): Promise<any> {
  const response = await fetch(`${BACKEND_URL}/metrics/sources/${sourceId}?period=${period}`);
  if (!response.ok) throw new Error(`Failed to fetch metrics for source ${sourceId}`);
  return response.json();
}

export async function getTimeline(): Promise<any[]> {
  const response = await fetch(`${BACKEND_URL}/metrics/timeline`);
  if (!response.ok) throw new Error('Failed to fetch timeline');
  return response.json();
}

export async function getValidationTrends(sourceId?: string): Promise<any[]> {
  const url = sourceId ? `${BACKEND_URL}/metrics/validation?source_id=${sourceId}` : `${BACKEND_URL}/metrics/validation`;
  const response = await fetch(url);
  if (!response.ok) throw new Error('Failed to fetch validation trends');
  return response.json();
}

export async function getSchemaHistory(sourceId: string): Promise<any[]> {
  const response = await fetch(`${BACKEND_URL}/metrics/schema/${sourceId}`);
  if (!response.ok) throw new Error(`Failed to fetch schema history for ${sourceId}`);
  return response.json();
}

export async function getHealingMetrics(period: string = '7d'): Promise<any> {
  const response = await fetch(`${BACKEND_URL}/metrics/healing?period=${period}`);
  if (!response.ok) throw new Error('Failed to fetch healing metrics');
  return response.json();
}

export async function getSources(): Promise<Source[]> {
  const response = await fetch(`${BACKEND_URL}/sources`);
  if (!response.ok) throw new Error('Failed to fetch sources');
  const data = await response.json();
  return data.map((item: any) => ({
    id: item.id,
    name: item.name,
    url: item.url,
    collectorId: item.collector_id,
    status: item.status.toUpperCase(),
    createdAt: item.created_at,
    updatedAt: item.updated_at
  }));
}

export async function getSource(id: string): Promise<Source> {
  const response = await fetch(`${BACKEND_URL}/sources/${id}`);
  if (!response.ok) throw new Error(`Failed to fetch source ${id}`);
  const item = await response.json();
  return {
    id: item.id,
    name: item.name,
    url: item.url,
    collectorId: item.collector_id,
    status: item.status.toUpperCase(),
    createdAt: item.created_at,
    updatedAt: item.updated_at
  };
}

export async function triggerScrape(sourceId: string): Promise<any> {
  const response = await fetch(`${BACKEND_URL}/sources/${sourceId}/scrape`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' }
  });
  if (!response.ok) {
    const err = await response.json();
    throw new Error(err.detail || 'Scrape execution failed');
  }
  return response.json();
}

export async function getRuns(): Promise<ScrapeRun[]> {
  const response = await fetch(`${BACKEND_URL}/runs`);
  if (!response.ok) throw new Error('Failed to fetch runs');
  const data = await response.json();
  return data.map((item: any) => ({
    id: item.id,
    sourceId: item.source_id,
    startedAt: item.started_at,
    completedAt: item.completed_at,
    status: item.status.toUpperCase(),
    recordsCount: item.records_found,
    errorMessage: item.error_message
  }));
}

export async function getRun(runId: string): Promise<any> {
  const response = await fetch(`${BACKEND_URL}/runs/${runId}`);
  if (!response.ok) throw new Error(`Failed to fetch run ${runId}`);
  return response.json();
}

export async function getRunValidation(runId: string): Promise<any> {
  const response = await fetch(`${BACKEND_URL}/runs/${runId}/validation`);
  if (!response.ok) throw new Error(`Failed to fetch validation for run ${runId}`);
  return response.json();
}

export async function getFailures(): Promise<HealingEvent[]> {
  const response = await fetch(`${BACKEND_URL}/failures`);
  if (!response.ok) throw new Error('Failed to fetch failures');
  const data = await response.json();
  return data.map((item: any) => ({
    id: item.id,
    sourceId: item.source_id,
    failureType: item.failure_type.toUpperCase(),
    failureRate: 0,
    healPrompt: item.message,
    healStatus: 'INITIATED',
    approvalStatus: 'PENDING',
    rerunStatus: 'PENDING',
    recoveryTimestamp: item.detected_at
  }));
}
