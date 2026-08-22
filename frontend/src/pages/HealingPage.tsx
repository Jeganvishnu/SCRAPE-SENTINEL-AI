import React, { useEffect, useState } from 'react';
import { getFailures } from '../services/api';
import { HealingEvent } from '../types';
import { AlertOctagon, RefreshCw, ShieldAlert } from 'lucide-react';

export const HealingPage: React.FC = () => {
  const [failures, setFailures] = useState<HealingEvent[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  const loadFailures = async () => {
    setLoading(true);
    try {
      const data = await getFailures();
      setFailures(data);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadFailures();
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-bold text-gray-100">Failure Events & Healing Queue</h1>
          <p className="text-sm text-gray-400">
            Detected structural breakages, schema drift, and empty result signals awaiting Phase 5 autonomous healing.
          </p>
        </div>
        <button
          onClick={loadFailures}
          disabled={loading}
          className="px-3 py-1.5 rounded-lg bg-[#161b22] border border-[#30363d] text-xs text-gray-300 hover:text-white flex items-center gap-1.5 transition-colors"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
          <span>Refresh</span>
        </button>
      </div>

      <div className="bg-amber-500/10 border border-amber-500/30 rounded-xl p-4 text-xs text-amber-300 flex items-center gap-2">
        <ShieldAlert className="w-4 h-4 shrink-0 text-amber-400" />
        <span>
          <strong>Phase 4 Status:</strong> Failure detection & Supabase event logging active. 
          <em> Automatic self-healing reruns will be enabled in Phase 5.</em>
        </span>
      </div>

      {loading ? (
        <div className="bg-[#161b22] border border-[#30363d] rounded-xl p-12 text-center text-xs text-gray-400">
          Loading failure events from Supabase...
        </div>
      ) : failures.length === 0 ? (
        <div className="bg-[#161b22] border border-[#30363d] rounded-xl p-12 text-center text-xs text-gray-400 space-y-2">
          <AlertOctagon className="w-8 h-8 text-emerald-400 mx-auto" />
          <p className="font-semibold text-gray-200 text-sm">No active failure events detected.</p>
          <p>Scrapers are healthy and passing structural validation.</p>
        </div>
      ) : (
        <div className="bg-[#161b22] border border-[#30363d] rounded-xl overflow-hidden">
          <table className="w-full text-left text-sm text-gray-300">
            <thead className="bg-[#0d1117] border-b border-[#30363d] text-xs font-semibold text-gray-400 uppercase tracking-wider">
              <tr>
                <th className="px-6 py-3">Event ID</th>
                <th className="px-6 py-3">Failure Type</th>
                <th className="px-6 py-3">Detected Time</th>
                <th className="px-6 py-3">Message</th>
                <th className="px-6 py-3">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#30363d]">
              {failures.map((f) => (
                <tr key={f.id}>
                  <td className="px-6 py-4 font-mono text-xs text-gray-200">{f.id.slice(0, 8)}...</td>
                  <td className="px-6 py-4 font-mono text-xs text-amber-400">{f.failureType}</td>
                  <td className="px-6 py-4 text-xs text-gray-400">{new Date(f.recoveryTimestamp || Date.now()).toLocaleString()}</td>
                  <td className="px-6 py-4 text-xs text-gray-300 max-w-xs truncate">{f.healPrompt}</td>
                  <td className="px-6 py-4">
                    <span className="px-2 py-0.5 rounded text-xs font-medium bg-amber-500/10 text-amber-400 border border-amber-500/20">
                      Detected failure — Awaiting healing
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};
