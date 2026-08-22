import React from 'react';
import { NavLink } from 'react-router-dom';
import { 
  LayoutDashboard, 
  Database, 
  PlayCircle, 
  Wrench, 
  Sparkles, 
  HelpCircle, 
  Settings, 
  ShieldAlert 
} from 'lucide-react';

interface NavItem {
  name: string;
  path: string;
  icon: React.ElementType;
}

const navItems: NavItem[] = [
  { name: 'Dashboard', path: '/', icon: LayoutDashboard },
  { name: 'Sources', path: '/sources', icon: Database },
  { name: 'Runs', path: '/runs', icon: PlayCircle },
  { name: 'Healing', path: '/healing', icon: Wrench },
  { name: 'Insights', path: '/insights', icon: Sparkles },
  { name: 'Ask Sentinel', path: '/ask', icon: HelpCircle },
  { name: 'Settings', path: '/settings', icon: Settings },
];

export const Sidebar: React.FC = () => {
  return (
    <aside className="w-64 bg-[#161b22] border-r border-[#30363d] flex flex-col justify-between h-screen sticky top-0">
      <div>
        {/* Logo / Brand */}
        <div className="p-4 border-b border-[#30363d] flex items-center gap-3">
          <div className="bg-emerald-500/10 p-2 rounded-lg border border-emerald-500/20">
            <ShieldAlert className="w-6 h-6 text-emerald-400" />
          </div>
          <div>
            <h1 className="font-bold text-gray-100 leading-tight">Scrape Sentinel</h1>
            <p className="text-xs text-gray-400 font-mono">AI Self-Healing Pipeline</p>
          </div>
        </div>

        {/* Navigation */}
        <nav className="p-3 space-y-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={item.path}
                to={item.path}
                end={item.path === '/'}
                className={({ isActive }) =>
                  `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                    isActive
                      ? 'bg-emerald-500/15 text-emerald-400 border border-emerald-500/30'
                      : 'text-gray-400 hover:text-gray-200 hover:bg-[#21262d]'
                  }`
                }
              >
                <Icon className="w-4 h-4 shrink-0" />
                <span>{item.name}</span>
              </NavLink>
            );
          })}
        </nav>
      </div>

      {/* Footer Info */}
      <div className="p-4 border-t border-[#30363d] text-xs text-gray-500">
        <p className="font-semibold text-gray-400">Bright Data Scraper Studio</p>
        <p>Phase 2 — Scaffold v0.1.0</p>
      </div>
    </aside>
  );
};
