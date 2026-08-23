import React, { useEffect, useState } from 'react';
import { getHealth } from '../services/api';
import { RefreshCw } from 'lucide-react';

export const Topbar: React.FC = () => {
  const [isOnline, setIsOnline] = useState<boolean | null>(null);
  const [isChecking, setIsChecking] = useState<boolean>(false);

  const checkApiHealth = async () => {
    setIsChecking(true);
    try {
      const data = await getHealth();
      if (data && (data.status === 'healthy' || data.status === 'ok')) {
        setIsOnline(true);
      } else {
        setIsOnline(false);
      }
    } catch {
      setIsOnline(false);
    } finally {
      setIsChecking(false);
    }
  };

  useEffect(() => {
    checkApiHealth();
    const interval = setInterval(checkApiHealth, 15000);
    return () => clearInterval(interval);
  }, []);

  return (
    <header className="h-16 bg-[#161b22] border-b border-[#30363d] px-6 flex items-center justify-between sticky top-0 z-10">
      <div>
        <h2 className="text-sm font-semibold text-gray-200">Public Technology Change Intelligence</h2>
      </div>

      <div className="flex items-center gap-4">
        {/* Status Indicator */}
        <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-[#0d1117] border border-[#30363d] text-xs">
          <span className="text-gray-400 font-medium">Bright Data Pipeline API</span>
          <div className="flex items-center gap-1.5 pl-1">
            {isOnline === null ? (
              <span className="inline-block w-2 h-2 rounded-full bg-yellow-500 animate-pulse" />
            ) : isOnline ? (
              <>
                <span className="inline-block w-2 h-2 rounded-full bg-emerald-500" />
                <span className="text-emerald-400 font-semibold">Online</span>
              </>
            ) : (
              <>
                <span className="inline-block w-2 h-2 rounded-full bg-red-500" />
                <span className="text-red-400 font-semibold">Offline</span>
              </>
            )}
          </div>
          <button
            onClick={checkApiHealth}
            disabled={isChecking}
            title="Refresh API Status"
            className="ml-1 text-gray-500 hover:text-gray-300 transition-colors disabled:opacity-50"
          >
            <RefreshCw className={`w-3 h-3 ${isChecking ? 'animate-spin' : ''}`} />
          </button>
        </div>
      </div>
    </header>
  );
};
