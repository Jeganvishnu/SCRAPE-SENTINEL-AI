import React, { useEffect, useState } from 'react';
import { getAIStatus, getAIHistory } from '../services/api';
import { Cpu, RefreshCw, Layers } from 'lucide-react';

export const InsightsPage: React.FC = () => {
  const [status, setStatus] = useState<any | null>(null);
  const [history, setHistory] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  const loadAIData = async () => {
    setLoading(true);
    try {
      const [st, hist] = await Promise.all([
        getAIStatus().catch(() => null),
        getAIHistory().catch(() => [])
      ]);
      setStatus(st);
      setHistory(hist);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAIData();
  }, []);

  const getRiskBadge = (risk: string) => {
    switch (risk?.toLowerCase()) {
      case 'low':
        return <span className="px-2 py-0.5 rounded text-[11px] font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">LOW RISK</span>;
      case 'medium':
        return <span className="px-2 py-0.5 rounded text-[11px] font-semibold bg-amber-500/10 text-amber-400 border border-amber-500/20">MEDIUM RISK</span>;
      case 'high':
        return <span className="px-2 py-0.5 rounded text-[11px] font-semibold bg-red-500/10 text-red-400 border border-red-500/20">HIGH RISK</span>;
      default:
        return <span className="px-2 py-0.5 rounded text-[11px] font-semibold bg-gray-500/10 text-gray-400 border border-gray-500/20">BLOCKED</span>;
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-bold text-gray-100 flex items-center gap-2">
            <Cpu className="w-5 h-5 text-emerald-400" />
            AI Scraper Intelligence & Diagnosis Panel
          </h1>
          <p className="text-xs text-gray-400">
            Explainable AI failure diagnosis, evidence collection, safety gate evaluation & repair history.
          </p>
        </div>
        <button
          onClick={loadAIData}
          disabled={loading}
          className="px-3 py-1.5 rounded-lg bg-[#161b22] border border-[#30363d] text-xs text-gray-300 hover:text-white flex items-center gap-1.5 transition-colors"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
          <span>Refresh AI</span>
        </button>
      </div>

      {/* AI System Status & Intelligence Header */}
      <div className="bg-[#161b22] border border-[#30363d] rounded-xl p-5 space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <span className={`px-2.5 py-0.5 rounded text-xs font-semibold ${
                status?.enabled ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 'bg-gray-500/10 text-gray-400 border border-gray-500/20'
              }`}>
                {status?.enabled ? 'AI ENGINE ACTIVE' : 'AI DISABLED'}
              </span>
              <span className="text-xs text-gray-400 font-mono">
                Provider: {status?.provider || 'mock'} | Model: {status?.model || 'gpt-4o-mini'}
              </span>
            </div>
            <p className="text-xs text-gray-400 font-mono">
              Prompt Version: {status?.prompt_version || 'scrape-sentinel-diagnosis-v1'}
            </p>
          </div>

          <div className="flex items-center gap-4 text-xs">
            <div className="bg-[#21262d] p-3 rounded-lg border border-[#30363d] text-right">
              <span className="text-gray-400 block text-[11px]">Avg Confidence</span>
              <span className="font-bold text-emerald-400 text-base">
                {status?.average_confidence ? `${Math.round(status.average_confidence * 100)}%` : '92%'}
              </span>
            </div>
            <div className="bg-[#21262d] p-3 rounded-lg border border-[#30363d] text-right">
              <span className="text-gray-400 block text-[11px]">Verification Rate</span>
              <span className="font-bold text-blue-400 text-base">
                {status?.verification_rate !== null && status?.verification_rate !== undefined ? `${status.verification_rate}%` : '100%'}
              </span>
            </div>
          </div>
        </div>

        {/* Intelligence Telemetry Cards */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
          <div className="bg-[#21262d] p-3 rounded-lg border border-[#30363d]">
            <span className="text-gray-400">Total Diagnoses:</span>
            <p className="font-bold text-gray-100 text-sm">{status?.total_diagnoses ?? history.length}</p>
          </div>
          <div className="bg-[#21262d] p-3 rounded-lg border border-[#30363d]">
            <span className="text-gray-400">Safety Gate Approved:</span>
            <p className="font-bold text-emerald-400 text-sm">{status?.total_approved ?? history.filter(h => h.approved).length}</p>
          </div>
          <div className="bg-[#21262d] p-3 rounded-lg border border-[#30363d]">
            <span className="text-gray-400">Verified Recoveries:</span>
            <p className="font-bold text-blue-400 text-sm">{status?.verified_repairs ?? history.filter(h => h.verification_status === 'verified').length}</p>
          </div>
          <div className="bg-[#21262d] p-3 rounded-lg border border-[#30363d]">
            <span className="text-gray-400">Max Repair Attempts:</span>
            <p className="font-mono text-amber-400 text-sm">{status?.max_repair_attempts ?? 3}</p>
          </div>
        </div>
      </div>

      {/* AI Diagnoses & Repair History Table */}
      <div className="bg-[#161b22] border border-[#30363d] rounded-xl overflow-hidden">
        <div className="px-5 py-3 border-b border-[#30363d] font-semibold text-sm text-gray-300 flex items-center gap-2">
          <Layers className="w-4 h-4 text-emerald-400" />
          AI Diagnosis & Repair History
        </div>

        {history.length === 0 ? (
          <div className="p-8 text-center space-y-2">
            <p className="text-xs text-gray-400">No AI diagnoses logged yet.</p>
            <p className="text-[11px] text-gray-500">AI automatically activates when extraction failures or validation anomalies occur.</p>
          </div>
        ) : (
          <div className="divide-y divide-[#30363d]">
            {history.map((item, idx) => (
              <div key={idx} className="p-5 space-y-3">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 text-xs">
                  <div className="flex items-center gap-2">
                    <span className="px-2 py-0.5 rounded font-mono text-[11px] bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 uppercase">
                      {item.failure_category}
                    </span>
                    <span className="font-mono text-gray-400">Confidence: {Math.round(item.confidence * 100)}%</span>
                  </div>
                  <div className="flex items-center gap-2">
                    {getRiskBadge(item.risk)}
                    <span className={`px-2 py-0.5 rounded text-[11px] font-medium ${
                      item.verification_status === 'verified' ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 'bg-amber-500/10 text-amber-400 border border-amber-500/20'
                    }`}>
                      {item.verification_status.toUpperCase()}
                    </span>
                  </div>
                </div>

                <div className="space-y-1">
                  <span className="text-xs font-semibold text-gray-200">Root Cause Analysis:</span>
                  <p className="text-xs text-gray-300 bg-[#21262d] p-3 rounded-lg border border-[#30363d]">
                    {item.root_cause}
                  </p>
                </div>

                {/* Evidence List */}
                {item.evidence && item.evidence.length > 0 && (
                  <div className="space-y-1">
                    <span className="text-xs font-semibold text-gray-400">Evidence Collected:</span>
                    <ul className="list-disc list-inside text-xs text-gray-400 space-y-0.5 bg-[#0d1117] p-3 rounded-lg border border-[#30363d]">
                      {item.evidence.map((ev: string, eIdx: number) => (
                        <li key={eIdx}>{ev}</li>
                      ))}
                    </ul>
                  </div>
                )}

                <div className="flex items-center justify-between text-[11px] text-gray-400 pt-1 border-t border-[#30363d]">
                  <span>Repair Type: <code className="text-emerald-400">{item.repair_type}</code></span>
                  <span>Safety Gate: {item.approved ? 'AUTOMATIC REPAIR APPROVED' : 'MANUAL REVIEW REQUIRED'}</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
