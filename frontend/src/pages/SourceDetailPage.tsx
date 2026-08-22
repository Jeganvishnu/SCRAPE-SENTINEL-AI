import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getSourceMetrics, getSchemaHistory } from '../services/api';
import { ArrowLeft, Globe, Layers } from 'lucide-react';

export const SourceDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [metrics, setMetrics] = useState<any | null>(null);
  const [schemaHist, setSchemaHist] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!id) return;
    setLoading(true);
    Promise.all([
      getSourceMetrics(id).catch(() => null),
      getSchemaHistory(id).catch(() => [])
    ]).then(([m, s]) => {
      setMetrics(m);
      setSchemaHist(s);
      setLoading(false);
    }).catch(err => {
      setError(err.message);
      setLoading(false);
    });
  }, [id]);

  if (loading) return <div className="p-12 text-center text-xs text-gray-400">Loading source metrics from Supabase...</div>;

  if (error || !metrics) {
    return (
      <div className="space-y-4">
        <Link to="/sources" className="text-xs text-emerald-400 flex items-center gap-1"><ArrowLeft className="w-4 h-4" /> Back to Sources</Link>
        <div className="bg-red-500/10 border border-red-500/30 p-4 rounded-xl text-xs text-red-400">
          Source details unavailable: {error || 'Not found'}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <Link to="/sources" className="text-xs text-emerald-400 hover:underline flex items-center gap-1">
        <ArrowLeft className="w-4 h-4" /> Back to Target Sources
      </Link>

      {/* Source Health Header */}
      <div className="bg-[#161b22] border border-[#30363d] rounded-xl p-5 space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div className="space-y-1">
            <span className="px-2.5 py-0.5 rounded text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 uppercase">
              {metrics.health}
            </span>
            <h1 className="text-xl font-bold text-gray-100 flex items-center gap-2">
              <Globe className="w-5 h-5 text-gray-400" />
              {metrics.name}
            </h1>
            <p className="text-xs text-gray-400 font-mono">{metrics.url}</p>
          </div>

          <div className="bg-[#21262d] border border-[#30363d] px-4 py-3 rounded-lg text-right">
            <span className="text-[11px] text-gray-400 block">Health Score</span>
            <span className="text-2xl font-bold text-emerald-400">{metrics.health_score}/100</span>
          </div>
        </div>

        <p className="text-xs text-gray-300 bg-[#21262d] p-3 rounded-lg border border-[#30363d]">
          {metrics.explanation}
        </p>

        {/* Source Telemetry Cards */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
          <div className="bg-[#21262d] p-3 rounded-lg border border-[#30363d]">
            <span className="text-gray-400">Success Rate:</span>
            <p className="font-bold text-emerald-400 text-sm">{metrics.success_rate}%</p>
          </div>
          <div className="bg-[#21262d] p-3 rounded-lg border border-[#30363d]">
            <span className="text-gray-400">Avg Validation Score:</span>
            <p className="font-bold text-gray-200 text-sm">{metrics.average_validation_score}/100</p>
          </div>
          <div className="bg-[#21262d] p-3 rounded-lg border border-[#30363d]">
            <span className="text-gray-400">Collector ID:</span>
            <p className="font-mono text-emerald-400 truncate">{metrics.collector_id}</p>
          </div>
          <div className="bg-[#21262d] p-3 rounded-lg border border-[#30363d]">
            <span className="text-gray-400">Active Failures:</span>
            <p className="font-bold text-amber-400 text-sm">{metrics.active_failures}</p>
          </div>
        </div>
      </div>

      {/* Schema Fingerprint History */}
      <div className="bg-[#161b22] border border-[#30363d] rounded-xl overflow-hidden">
        <div className="px-5 py-3 border-b border-[#30363d] font-semibold text-sm text-gray-300 flex items-center gap-2">
          <Layers className="w-4 h-4 text-emerald-400" />
          Schema Fingerprint History
        </div>
        {schemaHist.length === 0 ? (
          <p className="text-xs text-gray-400 text-center py-6">No historical schema fingerprint entries.</p>
        ) : (
          <table className="w-full text-left text-sm text-gray-300">
            <thead className="bg-[#0d1117] border-b border-[#30363d] text-xs font-semibold text-gray-400 uppercase tracking-wider">
              <tr>
                <th className="px-6 py-3">Timestamp</th>
                <th className="px-6 py-3">Run ID</th>
                <th className="px-6 py-3">Schema Fingerprint</th>
                <th className="px-6 py-3">Schema Drift</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#30363d]">
              {schemaHist.map((h, idx) => (
                <tr key={idx}>
                  <td className="px-6 py-4 text-xs text-gray-400">{new Date(h.timestamp).toLocaleString()}</td>
                  <td className="px-6 py-4 font-mono text-xs text-gray-200">{h.run_id.slice(0, 8)}...</td>
                  <td className="px-6 py-4 font-mono text-xs text-emerald-400">{h.schema_fingerprint}</td>
                  <td className="px-6 py-4">
                    <span className={`px-2 py-0.5 rounded text-xs font-medium ${
                      h.schema_change_detected ? 'bg-amber-500/10 text-amber-400 border border-amber-500/20' : 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                    }`}>
                      {h.schema_change_detected ? 'DRIFT DETECTED' : 'STABLE'}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
};
