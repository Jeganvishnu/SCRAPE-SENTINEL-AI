import React, { useEffect, useState } from 'react';
import { getRuns, getRunValidation } from '../services/api';
import { ScrapeRun } from '../types';
import { RefreshCw, ShieldCheck } from 'lucide-react';

export const RunsPage: React.FC = () => {
  const [runs, setRuns] = useState<ScrapeRun[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedRunVal, setSelectedRunVal] = useState<any | null>(null);

  const loadRuns = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await getRuns();
      setRuns(data);
    } catch (err: any) {
      setError(err.message || 'Failed to load scrape runs');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadRuns();
  }, []);

  const handleInspectValidation = async (runId: string) => {
    try {
      const val = await getRunValidation(runId);
      setSelectedRunVal(val);
    } catch (err: any) {
      alert(`Validation details unavailable for run ${runId}`);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-bold text-gray-100">Scrape Run History</h1>
          <p className="text-sm text-gray-400">
            Historical execution logs and validation engine evaluation scores.
          </p>
        </div>
        <button
          onClick={loadRuns}
          disabled={loading}
          className="px-3 py-1.5 rounded-lg bg-[#161b22] border border-[#30363d] text-xs text-gray-300 hover:text-white flex items-center gap-1.5 transition-colors"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
          <span>Refresh</span>
        </button>
      </div>

      {error && (
        <div className="bg-red-500/10 border border-red-500/30 rounded-xl p-4 text-xs text-red-400">
          {error}
        </div>
      )}

      {loading ? (
        <div className="bg-[#161b22] border border-[#30363d] rounded-xl p-12 text-center text-xs text-gray-400">
          Loading scrape run history from Supabase...
        </div>
      ) : runs.length === 0 ? (
        <div className="bg-[#161b22] border border-[#30363d] rounded-xl p-12 text-center text-xs text-gray-400 space-y-2">
          <p className="font-semibold text-gray-200 text-sm">No scrape runs recorded yet.</p>
          <p>Scrape execution logs will appear here after triggering runs.</p>
        </div>
      ) : (
        <div className="bg-[#161b22] border border-[#30363d] rounded-xl overflow-hidden">
          <table className="w-full text-left text-sm text-gray-300">
            <thead className="bg-[#0d1117] border-b border-[#30363d] text-xs font-semibold text-gray-400 uppercase tracking-wider">
              <tr>
                <th className="px-6 py-3">Run ID</th>
                <th className="px-6 py-3">Started At</th>
                <th className="px-6 py-3">Records Found</th>
                <th className="px-6 py-3">Status</th>
                <th className="px-6 py-3">Validation Engine</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#30363d]">
              {runs.map((r) => (
                <tr key={r.id}>
                  <td className="px-6 py-4 font-mono text-xs text-gray-200">{r.id}</td>
                  <td className="px-6 py-4 text-xs text-gray-400">{new Date(r.startedAt).toLocaleString()}</td>
                  <td className="px-6 py-4 font-mono text-xs">{r.recordsCount}</td>
                  <td className="px-6 py-4">
                    <span className={`px-2 py-0.5 rounded text-xs font-medium ${
                      r.status === 'SUCCESS' ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 'bg-red-500/10 text-red-400 border border-red-500/20'
                    }`}>
                      {r.status}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <button
                      onClick={() => handleInspectValidation(r.id)}
                      className="px-2.5 py-1 rounded bg-[#21262d] hover:bg-[#30363d] border border-[#30363d] text-xs text-emerald-400 flex items-center gap-1"
                    >
                      <ShieldCheck className="w-3.5 h-3.5" /> Inspect Score
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {selectedRunVal && (
        <div className="bg-[#161b22] border border-emerald-500/30 rounded-xl p-5 space-y-3">
          <div className="flex items-center justify-between border-b border-[#30363d] pb-2">
            <h3 className="font-semibold text-sm text-gray-200">Validation Engine Evaluation</h3>
            <button onClick={() => setSelectedRunVal(null)} className="text-xs text-gray-400 hover:text-white">Close</button>
          </div>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
            <div>
              <span className="text-gray-400">Score:</span>
              <p className="font-bold text-emerald-400 text-sm">{selectedRunVal.validation_score}/100</p>
            </div>
            <div>
              <span className="text-gray-400">Status:</span>
              <p className="font-semibold text-gray-200 uppercase">{selectedRunVal.validation_status}</p>
            </div>
            <div>
              <span className="text-gray-400">Required Fields:</span>
              <p className="text-gray-200">{selectedRunVal.required_fields_valid ? 'PASS' : 'FAIL'}</p>
            </div>
            <div>
              <span className="text-gray-400">Schema Change:</span>
              <p className={selectedRunVal.schema_change_detected ? 'text-amber-400 font-semibold' : 'text-emerald-400'}>
                {selectedRunVal.schema_change_detected ? 'DETECTED' : 'STABLE'}
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
