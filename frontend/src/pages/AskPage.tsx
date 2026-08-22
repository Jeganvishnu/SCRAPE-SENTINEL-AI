import React from 'react';
import { HelpCircle } from 'lucide-react';

export const AskPage: React.FC = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-bold text-gray-100">Ask Sentinel Q&A</h1>
        <p className="text-sm text-gray-400">
          Query scraped public product changelogs using natural language.
        </p>
      </div>

      <div className="bg-[#161b22] border border-[#30363d] rounded-xl p-12 text-center space-y-3">
        <HelpCircle className="w-8 h-8 text-gray-500 mx-auto" />
        <h2 className="text-base font-semibold text-gray-200">Natural Language Q&A Ready</h2>
        <p className="text-xs text-gray-400 max-w-md mx-auto">
          Ask Sentinel RAG search over extracted tech product updates will be activated in Phase 7.
        </p>
      </div>
    </div>
  );
};
