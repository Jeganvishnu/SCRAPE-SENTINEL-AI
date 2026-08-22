import React, { useEffect, useState } from 'react';
import { getOverviewMetrics, getTimeline, getValidationTrends, getSources, triggerScrape } from '../services/api';
import { PlayCircle, ShieldCheck, AlertTriangle, RefreshCw, Activity, Heart, Clock, Layers } from 'lucide-react';

export const DashboardPage: React.FC = () => {
  const [period, setPeriod] = useState<string>('7d');
  const [overview, setOverview] = useState<any | null>(null);
  const [timeline, setTimeline] = useState<any[]>([]);
  const [trends, setTrends] = useState<any[]>([]);
  const [sources, setSources] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [scraping, setScraping] = useState<boolean>(false);
  const [scrapeError, setScrapeError] = useState<string | null>(null);

  const loadMetrics = async () => {
    setLoading(true);
    try {
      const [ov, tm, tr, src] = await Promise.all([
        getOverviewMetrics(period).catch(() => null),
        getTimeline().catch(() => []),
        getValidationTrends().catch(() => []),
        getSources().catch(() => [])
      ]);
      setOverview(ov);
      setTimeline(tm);
      setTrends(tr);
      setSources(src);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadMetrics();
    // 30-second live polling refresh
    const interval = setInterval(loadMetrics, 30000);
    return () => clearInterval(interval);
  }, [period]);

  const handleRunScraper = async () => {
    if (sources.length === 0) return;
    setScraping(true);
    setScrapeError(null);
    try {
      await triggerScrape(sources[0].id);
      await loadMetrics();
    } catch (err: any) {
      setScrapeError(err.message || 'Scrape execution failed');
    } finally {
      setScraping(false);
    }
  };

  const primarySource = sources[0];

  const getHealthBadge = (state: string) => {
    switch (state?.toLowerCase()) {
      case 'healthy':
        return <span className="px-2.5 py-1 rounded-md text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">HEALTHY</span>;
      case 'warning':
        return <span className="px-2.5 py-1 rounded-md text-xs font-semibold bg-amber-500/10 text-amber-400 border border-amber-500/20">WARNING</span>;
      case 'degraded':
        return <span className="px-2.5 py-1 rounded-md text-xs font-semibold bg-orange-500/10 text-orange-400 border border-orange-500/20">DEGRADED</span>;
      case 'critical':
        return <span className="px-2.5 py-1 rounded-md text-xs font-semibold bg-red-500/10 text-red-400 border border-red-500/20">CRITICAL</span>;
      default:
        return <span className="px-2.5 py-1 rounded-md text-xs font-semibold bg-gray-500/10 text-gray-400 border border-gray-500/20">UNKNOWN</span>;
    }
  };

  return (
    <div className="space-y-6">
      {/* Top Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold text-gray-100 flex items-center gap-2">
            <Activity className="w-5 h-5 text-emerald-400" />
            Reliability & Observability Dashboard
          </h1>
          <p className="text-xs text-gray-400">
            Real-time telemetry, transparent health scores, validation quality trends & recovery metrics.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <select
            value={period}
            onChange={(e) => setPeriod(e.target.value)}
            className="bg-[#161b22] border border-[#30363d] text-xs text-gray-300 rounded-lg px-3 py-1.5 focus:outline-none"
          >
            <option value="24h">Last 24 Hours</option>
            <option value="7d">Last 7 Days</option>
            <option value="30d">Last 30 Days</option>
            <option value="all">All Time</option>
          </select>
          <button
            onClick={loadMetrics}
            disabled={loading}
            className="px-3 py-1.5 rounded-lg bg-[#161b22] border border-[#30363d] text-xs text-gray-300 hover:text-white flex items-center gap-1.5 transition-colors"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
            <span>Refresh</span>
          </button>
        </div>
      </div>

      {/* Target Info Banner */}
      <div className="bg-[#161b22] border border-[#30363d] rounded-xl p-5 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <span className="px-2 py-0.5 rounded text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              Bright Data Scraper Studio
            </span>
            <span className="text-xs text-gray-400 font-mono">
              Collector ID: {primarySource?.collectorId || 'c_mt46lngz2asqzj8tkj'}
            </span>
          </div>
          <h2 className="text-base font-semibold text-gray-200">
            {primarySource?.name || 'Supabase Product Changelog'}
          </h2>
          <p className="text-xs text-gray-400 font-mono">
            {primarySource?.url || 'https://supabase.com/changelog'}
          </p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={handleRunScraper}
            disabled={scraping || !primarySource}
            className="px-4 py-2 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-medium text-xs flex items-center gap-2 transition-colors disabled:opacity-50"
          >
            <PlayCircle className={`w-4 h-4 ${scraping ? 'animate-spin' : ''}`} />
            <span>{scraping ? 'Executing Collector...' : 'Run Scraper Now'}</span>
          </button>
        </div>
      </div>

      {scrapeError && (
        <div className="bg-red-500/10 border border-red-500/30 rounded-xl p-4 text-xs text-red-400 flex items-center gap-2">
          <AlertTriangle className="w-4 h-4 shrink-0" />
          <span>{scrapeError}</span>
        </div>
      )}

      {/* Real Summary Observability Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-[#161b22] border border-[#30363d] rounded-xl p-4 space-y-2">
          <div className="flex items-center justify-between text-xs text-gray-400">
            <span>System Health</span>
            <Heart className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="flex items-center justify-between">
            <span className="text-2xl font-bold text-gray-100">{overview?.health_score ?? 100}/100</span>
            {getHealthBadge(overview?.system_health)}
          </div>
          <p className="text-[11px] text-gray-400 truncate">{overview?.explanation || 'All components healthy.'}</p>
        </div>

        <div className="bg-[#161b22] border border-[#30363d] rounded-xl p-4 space-y-2">
          <div className="flex items-center justify-between text-xs text-gray-400">
            <span>Success Rate ({period})</span>
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
          </div>
          <p className="text-2xl font-bold text-emerald-400">{overview?.success_rate ?? 100}%</p>
          <p className="text-[11px] text-gray-400">{overview?.successful_runs ?? 0} / {overview?.total_runs ?? 0} runs passed</p>
        </div>

        <div className="bg-[#161b22] border border-[#30363d] rounded-xl p-4 space-y-2">
          <div className="flex items-center justify-between text-xs text-gray-400">
            <span>Avg Validation Quality</span>
            <Layers className="w-4 h-4 text-blue-400" />
          </div>
          <p className="text-2xl font-bold text-gray-100">{overview?.average_validation_score ?? 100}/100</p>
          <p className="text-[11px] text-gray-400">Transparent engine score</p>
        </div>

        <div className="bg-[#161b22] border border-[#30363d] rounded-xl p-4 space-y-2">
          <div className="flex items-center justify-between text-xs text-gray-400">
            <span>Healing Recovery Rate</span>
            <Clock className="w-4 h-4 text-amber-400" />
          </div>
          <p className="text-2xl font-bold text-amber-400">
            {overview?.recovery_rate !== null && overview?.recovery_rate !== undefined ? `${overview.recovery_rate}%` : 'N/A'}
          </p>
          <p className="text-[11px] text-gray-400">
            {overview?.recovery_rate === null ? 'No healing attempts yet' : `MTTR: ${overview?.mttr_seconds ?? 0}s`}
          </p>
        </div>
      </div>

      {/* Validation Score Trends */}
      <div className="bg-[#161b22] border border-[#30363d] rounded-xl p-5 space-y-4">
        <h3 className="font-semibold text-sm text-gray-200">Validation Quality Trend ({trends.length} Recent Runs)</h3>
        {trends.length === 0 ? (
          <p className="text-xs text-gray-400 text-center py-6">No historical validation trends recorded yet.</p>
        ) : (
          <div className="space-y-2">
            {trends.map((t, idx) => (
              <div key={idx} className="flex items-center gap-3 text-xs">
                <span className="text-gray-400 font-mono w-32 truncate">{new Date(t.timestamp).toLocaleTimeString()}</span>
                <div className="flex-1 bg-[#21262d] rounded-full h-3 overflow-hidden">
                  <div
                    className={`h-full ${t.validation_score >= 85 ? 'bg-emerald-500' : (t.validation_score >= 70 ? 'bg-amber-500' : 'bg-red-500')}`}
                    style={{ width: `${t.validation_score}%` }}
                  />
                </div>
                <span className="font-mono text-gray-200 w-12 text-right">{t.validation_score}</span>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Activity Timeline */}
      <div className="bg-[#161b22] border border-[#30363d] rounded-xl overflow-hidden">
        <div className="px-5 py-3 border-b border-[#30363d] font-semibold text-sm text-gray-300">
          System Activity Lifecycle Timeline
        </div>
        {timeline.length === 0 ? (
          <p className="text-xs text-gray-400 text-center py-8">No system activity logged yet.</p>
        ) : (
          <div className="divide-y divide-[#30363d]">
            {timeline.slice(0, 10).map((item, idx) => (
              <div key={idx} className="px-5 py-3 flex items-center justify-between text-xs">
                <div className="space-y-0.5">
                  <span className="font-mono text-emerald-400 uppercase">{item.type}</span>
                  <p className="text-gray-300">{item.message}</p>
                </div>
                <span className="text-gray-400 font-mono">{new Date(item.timestamp).toLocaleString()}</span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
