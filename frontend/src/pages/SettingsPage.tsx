import React from 'react';
import { Shield } from 'lucide-react';

export const SettingsPage: React.FC = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-bold text-gray-100">System Settings & Configuration</h1>
        <p className="text-sm text-gray-400">
          Environment configuration, Bright Data Scraper Studio bindings, and retry policies.
        </p>
      </div>

      <div className="bg-[#161b22] border border-[#30363d] rounded-xl p-5 space-y-4">
        <h2 className="text-sm font-semibold text-gray-300 border-b border-[#30363d] pb-2 flex items-center gap-2">
          <Shield className="w-4 h-4 text-emerald-400" />
          Scraper Sentinel Environment Config
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
          <div>
            <span className="text-gray-500 block">Scraper Provider</span>
            <span className="text-gray-200 font-medium">Bright Data Scraper Studio</span>
          </div>
          <div>
            <span className="text-gray-500 block">Default Primary Target</span>
            <span className="text-gray-200 font-mono">https://supabase.com/changelog</span>
          </div>
          <div>
            <span className="text-gray-500 block">Backend API URL</span>
            <span className="text-gray-200 font-mono">http://localhost:8000</span>
          </div>
          <div>
            <span className="text-gray-500 block">Deterministic Validation Engine</span>
            <span className="text-emerald-400 font-semibold">Active (Pydantic)</span>
          </div>
        </div>
      </div>
    </div>
  );
};
