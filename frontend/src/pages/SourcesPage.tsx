import React, { useEffect, useState } from 'react';
import { getSources } from '../services/api';
import { Source } from '../types';
import { Globe, RefreshCw } from 'lucide-react';

export const SourcesPage: React.FC = () => {
  const [sources, setSources] = useState<Source[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  const loadSources = async () => {
    setLoading(true);
    try {
      const data = await getSources();
      setSources(data);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadSources();
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-bold text-gray-100">Target Data Sources</h1>
          <p className="text-sm text-gray-400">
            Registered web targets bound to Bright Data Scraper Studio custom collectors.
          </p>
        </div>
        <button
          onClick={loadSources}
          disabled={loading}
          className="px-3 py-1.5 rounded-lg bg-[#161b22] border border-[#30363d] text-xs text-gray-300 hover:text-white flex items-center gap-1.5 transition-colors"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
          <span>Refresh</span>
        </button>
      </div>

      {loading ? (
        <div className="bg-[#161b22] border border-[#30363d] rounded-xl p-12 text-center text-xs text-gray-400">
          Loading target sources...
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {sources.map((src) => (
            <div key={src.id} className="bg-[#161b22] border border-[#30363d] rounded-xl p-5 space-y-4">
              <div className="flex items-start justify-between">
                <div className="space-y-1">
                  <span className="px-2 py-0.5 rounded text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                    {src.status}
                  </span>
                  <h3 className="text-base font-semibold text-gray-200">{src.name}</h3>
                </div>
                <Globe className="w-5 h-5 text-gray-400" />
              </div>

              <div className="space-y-2 text-xs">
                <div>
                  <span className="text-gray-400">Target URL:</span>
                  <p className="font-mono text-gray-200 truncate">{src.url}</p>
                </div>
                <div>
                  <span className="text-gray-400">Bright Data Collector ID:</span>
                  <p className="font-mono text-emerald-400">{src.collectorId}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
