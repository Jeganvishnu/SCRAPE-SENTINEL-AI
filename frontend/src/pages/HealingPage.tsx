import React, { useEffect, useState } from 'react';
import { getFailures, triggerHeal, getAIHistory } from '../services/api';
import { HealingEvent } from '../types';
import { RefreshCw, PlayCircle, ShieldCheck, AlertTriangle, Cpu, CheckCircle2 } from 'lucide-react';

export const HealingPage: React.FC = () => {
  const [failures, setFailures] = useState<HealingEvent[]>([]);
  const [aiHistory, setAiHistory] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [healingId, setHealingId] = useState<string | null>(null);
  const [healSuccess, setHealSuccess] = useState<string | null>(null);
  const [healError, setHealError] = useState<string | null>(null);

  const loadData = async () => {
    setLoading(true);
    try {
      const [fData, aiData] = await Promise.all([
        getFailures().catch(() => []),
        getAIHistory().catch(() => [])
      ]);
      setFailures(fData);
      setAiHistory(aiData);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleExecuteHeal = async (failureId: string) => {
    setHealingId(failureId);
    setHealSuccess(null);
    setHealError(null);
    try {
      const res = await triggerHeal(failureId);
      setHealSuccess(`Phase 5 Repair & Verification Result: ${res.status.toUpperCase()}. ${res.message}`);
      await loadData();
    } catch (err: any) {
      setHealError(err.message || 'Healing execution failed');
    } finally {
      setHealingId(null);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-bold text-gray-100 flex items-center gap-2">
            <Cpu className="w-5 h-5 text-emerald-400" />
            AI-Guided Self-Healing Engine
          </h1>
          <p className="text-xs text-gray-400">
            Autonomous failure detection, AI root-cause analysis, safety gate evaluation & verified recovery.
          </p>
        </div>
        <button
          onClick={loadData}
          disabled={loading}
          className="px-3 py-1.5 rounded-lg bg-[#161b22] border border-[#30363d] text-xs text-gray-300 hover:text-white flex items-center gap-1.5 transition-colors"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
          <span>Refresh</span>
        </button>
      </div>

      {healSuccess && (
        <div className="bg-emerald-500/10 border border-emerald-500/30 rounded-xl p-4 text-xs text-emerald-400 flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4 shrink-0" />
          <span>{healSuccess}</span>
        </div>
      )}

      {healError && (
        <div className="bg-red-500/10 border border-red-500/30 rounded-xl p-4 text-xs text-red-400 flex items-center gap-2">
          <AlertTriangle className="w-4 h-4 shrink-0" />
          <span>{healError}</span>
        </div>
      )}

      {/* Failure Events & AI Diagnosis Table */}
      <div className="bg-[#161b22] border border-[#30363d] rounded-xl overflow-hidden">
        <div className="px-5 py-3 border-b border-[#30363d] font-semibold text-sm text-gray-300">
          Extraction Failures & Automated Healing Queue ({failures.length})
        </div>

        {failures.length === 0 ? (
          <div className="p-8 text-center space-y-1">
            <ShieldCheck className="w-8 h-8 text-emerald-400 mx-auto" />
            <p className="text-xs text-gray-300 font-semibold">Zero Unresolved Extraction Failures</p>
            <p className="text-[11px] text-gray-400">All target scrapers are passing validation with 100% field compliance.</p>
          </div>
        ) : (
          <div className="divide-y divide-[#30363d]">
            {failures.map((f) => {
              const diag = aiHistory.find(h => h.failure_event_id === f.id);
              const isHealing = healingId === f.id;

              return (
                <div key={f.id} className="p-5 space-y-4">
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                    <div className="space-y-1">
                      <div className="flex items-center gap-2">
                        <span className="px-2.5 py-0.5 rounded text-xs font-semibold bg-red-500/10 text-red-400 border border-red-500/20">
                          {f.failureType}
                        </span>
                        <span className="text-xs text-gray-400 font-mono">ID: {f.id.slice(0, 8)}...</span>
                      </div>
                      <p className="text-xs text-gray-300 font-medium">{f.healPrompt}</p>
                    </div>

                    <button
                      onClick={() => handleExecuteHeal(f.id)}
                      disabled={isHealing}
                      className="px-4 py-2 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-medium text-xs flex items-center gap-1.5 shrink-0 transition-colors disabled:opacity-50"
                    >
                      <PlayCircle className={`w-4 h-4 ${isHealing ? 'animate-spin' : ''}`} />
                      <span>{isHealing ? 'Executing Phase 5 Heal...' : 'Execute AI Guided Heal'}</span>
                    </button>
                  </div>

                  {/* AI Diagnosis Box if present */}
                  {diag && (
                    <div className="bg-[#21262d] border border-[#30363d] rounded-lg p-4 space-y-2 text-xs">
                      <div className="flex items-center justify-between">
                        <span className="font-semibold text-emerald-400 flex items-center gap-1.5">
                          <Cpu className="w-3.5 h-3.5" /> AI Diagnosis Summary:
                        </span>
                        <span className="text-gray-400 font-mono">Confidence: {Math.round(diag.confidence * 100)}%</span>
                      </div>
                      <p className="text-gray-300">{diag.root_cause}</p>
                      {diag.evidence && diag.evidence.length > 0 && (
                        <div className="text-[11px] text-gray-400">
                          <span className="font-semibold text-gray-300">Evidence:</span> {diag.evidence.join(' | ')}
                        </div>
                      )}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
};
