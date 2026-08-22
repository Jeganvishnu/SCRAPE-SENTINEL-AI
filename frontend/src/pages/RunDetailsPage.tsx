import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getRun, getRunValidation } from '../services/api';
import { ShieldCheck, ArrowLeft, CheckCircle2, XCircle, Clock } from 'lucide-react';

export const RunDetailsPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [run, setRun] = useState<any | null>(null);
  const [val, setVal] = useState<any | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!id) return;
    setLoading(true);
    Promise.all([
      getRun(id).catch(() => null),
      getRunValidation(id).catch(() => null)
    ]).then(([r, v]) => {
      setRun(r);
      setVal(v);
      setLoading(false);
    }).catch(err => {
      setError(err.message);
      setLoading(false);
    });
  }, [id]);

  if (loading) {
    return <div className="p-12 text-center text-xs text-gray-400">Loading run details from Supabase...</div>;
  }

  if (error || !run) {
    return (
      <div className="space-y-4">
        <Link to="/runs" className="text-xs text-emerald-400 flex items-center gap-1"><ArrowLeft className="w-4 h-4" /> Back to Runs</Link>
        <div className="bg-red-500/10 border border-red-500/30 p-4 rounded-xl text-xs text-red-400">
          Run details unavailable: {error || 'Not found'}
        </div>
      </div>
    );
  }

  const isSuccess = run.status === 'SUCCESS';
  const valPassed = val?.validation_status === 'passed';

  return (
    <div className="space-y-6">
      <Link to="/runs" className="text-xs text-emerald-400 hover:underline flex items-center gap-1">
        <ArrowLeft className="w-4 h-4" /> Back to Scrape Runs
      </Link>

      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-bold text-gray-100">Run Execution Lifecycle Details</h1>
          <p className="text-xs text-gray-400 font-mono">ID: {run.id}</p>
        </div>
        <span className={`px-3 py-1 rounded-md text-xs font-semibold ${isSuccess ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 'bg-red-500/10 text-red-400 border border-red-500/20'}`}>
          {run.status}
        </span>
      </div>

      {/* Lifecycle Steps Visualization */}
      <div className="bg-[#161b22] border border-[#30363d] rounded-xl p-5 space-y-3">
        <h3 className="font-semibold text-sm text-gray-200">Execution & Verification Lifecycle</h3>
        <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-6 gap-3 text-center">
          <div className="bg-[#21262d] border border-[#30363d] p-3 rounded-lg space-y-1">
            <CheckCircle2 className="w-5 h-5 text-emerald-400 mx-auto" />
            <span className="text-[11px] font-semibold text-gray-200">1. Scrape</span>
            <p className="text-[10px] text-gray-400">Triggered</p>
          </div>
          <div className="bg-[#21262d] border border-[#30363d] p-3 rounded-lg space-y-1">
            <CheckCircle2 className="w-5 h-5 text-emerald-400 mx-auto" />
            <span className="text-[11px] font-semibold text-gray-200">2. Collector Output</span>
            <p className="text-[10px] text-gray-400">{run.records_found} Records</p>
          </div>
          <div className="bg-[#21262d] border border-[#30363d] p-3 rounded-lg space-y-1">
            {valPassed ? <CheckCircle2 className="w-5 h-5 text-emerald-400 mx-auto" /> : <XCircle className="w-5 h-5 text-red-400 mx-auto" />}
            <span className="text-[11px] font-semibold text-gray-200">3. Validation</span>
            <p className="text-[10px] text-gray-400">Score: {val?.validation_score ?? 'N/A'}</p>
          </div>
          <div className="bg-[#21262d] border border-[#30363d] p-3 rounded-lg space-y-1">
            {!valPassed ? <CheckCircle2 className="w-5 h-5 text-amber-400 mx-auto" /> : <Clock className="w-5 h-5 text-gray-500 mx-auto" />}
            <span className="text-[11px] font-semibold text-gray-200">4. Failure Detect</span>
            <p className="text-[10px] text-gray-400">{!valPassed ? 'Logged' : 'None'}</p>
          </div>
          <div className="bg-[#21262d] border border-[#30363d] p-3 rounded-lg space-y-1">
            <Clock className="w-5 h-5 text-gray-500 mx-auto" />
            <span className="text-[11px] font-semibold text-gray-200">5. Healing</span>
            <p className="text-[10px] text-gray-400">Phase 5 Queue</p>
          </div>
          <div className="bg-[#21262d] border border-[#30363d] p-3 rounded-lg space-y-1">
            <CheckCircle2 className="w-5 h-5 text-emerald-400 mx-auto" />
            <span className="text-[11px] font-semibold text-gray-200">6. Verified</span>
            <p className="text-[10px] text-gray-400">{isSuccess ? 'Verified' : 'Pending'}</p>
          </div>
        </div>
      </div>

      {/* Metric Details */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="bg-[#161b22] border border-[#30363d] rounded-xl p-5 space-y-3">
          <h3 className="font-semibold text-sm text-gray-200">Run Execution Metadata</h3>
          <div className="space-y-2 text-xs">
            <div className="flex justify-between border-b border-[#30363d] pb-1">
              <span className="text-gray-400">Source ID:</span>
              <span className="font-mono text-gray-200">{run.source_id}</span>
            </div>
            <div className="flex justify-between border-b border-[#30363d] pb-1">
              <span className="text-gray-400">Collector ID:</span>
              <span className="font-mono text-emerald-400">{run.collector_id}</span>
            </div>
            <div className="flex justify-between border-b border-[#30363d] pb-1">
              <span className="text-gray-400">Started At:</span>
              <span className="text-gray-200">{new Date(run.started_at).toLocaleString()}</span>
            </div>
            <div className="flex justify-between border-b border-[#30363d] pb-1">
              <span className="text-gray-400">Duration:</span>
              <span className="text-gray-200">{run.duration_ms ? `${run.duration_ms} ms` : 'N/A'}</span>
            </div>
          </div>
        </div>

        <div className="bg-[#161b22] border border-[#30363d] rounded-xl p-5 space-y-3">
          <h3 className="font-semibold text-sm text-gray-200 flex items-center gap-1.5">
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
            Validation Results
          </h3>
          {val ? (
            <div className="space-y-2 text-xs">
              <div className="flex justify-between border-b border-[#30363d] pb-1">
                <span className="text-gray-400">Score:</span>
                <span className="font-bold text-emerald-400 text-sm">{val.validation_score}/100</span>
              </div>
              <div className="flex justify-between border-b border-[#30363d] pb-1">
                <span className="text-gray-400">Schema Valid:</span>
                <span className={val.schema_valid ? 'text-emerald-400' : 'text-red-400'}>{val.schema_valid ? 'PASS' : 'FAIL'}</span>
              </div>
              <div className="flex justify-between border-b border-[#30363d] pb-1">
                <span className="text-gray-400">Required Fields:</span>
                <span className={val.required_fields_valid ? 'text-emerald-400' : 'text-red-400'}>{val.required_fields_valid ? 'PASS' : 'FAIL'}</span>
              </div>
              <div className="flex justify-between border-b border-[#30363d] pb-1">
                <span className="text-gray-400">Schema Drift:</span>
                <span className={val.schema_change_detected ? 'text-amber-400' : 'text-emerald-400'}>{val.schema_change_detected ? 'DETECTED' : 'STABLE'}</span>
              </div>
            </div>
          ) : (
            <p className="text-xs text-gray-400">No validation result associated with run.</p>
          )}
        </div>
      </div>
    </div>
  );
};
