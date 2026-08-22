import React from 'react';
import { Sparkles } from 'lucide-react';

export const InsightsPage: React.FC = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-bold text-gray-100">AI Change Intelligence</h1>
        <p className="text-sm text-gray-400">
          Automated LLM change categorization, impact scoring, and release note summaries.
        </p>
      </div>

      <div className="bg-[#161b22] border border-[#30363d] rounded-xl p-12 text-center space-y-3">
        <Sparkles className="w-8 h-8 text-gray-500 mx-auto" />
        <h2 className="text-base font-semibold text-gray-200">No AI insights generated yet</h2>
        <p className="text-xs text-gray-400 max-w-md mx-auto">
          Downstream AI change analysis and breaking release scoring will be integrated in Phase 7.
        </p>
      </div>
    </div>
  );
};
