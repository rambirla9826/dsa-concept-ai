import React from 'react';
import { useAuth } from '../context/AuthContext';
import { Brain, Flame, Shield, LogOut, User as UserIcon, LayoutDashboard, Code, BarChart3, Settings, Mic } from 'lucide-react';

interface NavbarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
}

export const Navbar: React.FC<NavbarProps> = ({ activeTab, setActiveTab }) => {
  const { user, logout, isAdmin } = useAuth();

  return (
    <header className="glass-panel sticky top-0 z-50 border-b border-slate-800 bg-slate-950/80 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        
        {/* Logo */}
        <div className="flex items-center gap-3 cursor-pointer" onClick={() => setActiveTab('dashboard')}>
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-600 to-purple-600 flex items-center justify-center shadow-lg shadow-blue-500/20">
            <Brain className="w-6 h-6 text-white" />
          </div>
          <div>
            <span className="font-extrabold text-xl tracking-tight text-white flex items-center gap-1.5 font-sans">
              AlgoConcept <span className="bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent text-xs font-semibold px-2 py-0.5 rounded-full border border-blue-500/30">AI</span>
            </span>
            <p className="text-[10px] text-slate-400 font-medium tracking-wider uppercase">Conceptual DSA Thinking</p>
          </div>
        </div>

        {/* Navigation Tabs */}
        {user && (
          <nav className="hidden md:flex items-center gap-1 bg-slate-900/90 p-1 rounded-xl border border-slate-800">
            <button
              onClick={() => setActiveTab('dashboard')}
              className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-sm font-medium transition-all ${
                activeTab === 'dashboard'
                  ? 'bg-blue-600 text-white shadow-md shadow-blue-600/30'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
              }`}
            >
              <LayoutDashboard className="w-4 h-4" />
              Student Dashboard
            </button>

            <button
              onClick={() => setActiveTab('problems')}
              className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-sm font-medium transition-all ${
                activeTab === 'problems' || activeTab.startsWith('problem-')
                  ? 'bg-blue-600 text-white shadow-md shadow-blue-600/30'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
              }`}
            >
              <Code className="w-4 h-4" />
              DSA Questions
            </button>

            <button
              onClick={() => setActiveTab('voice-interview')}
              className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-sm font-medium transition-all ${
                activeTab === 'voice-interview' || activeTab === 'interview-report'
                  ? 'bg-purple-600 text-white shadow-md shadow-purple-600/30'
                  : 'text-purple-400 hover:text-purple-300 hover:bg-purple-950/40'
              }`}
            >
              <Mic className="w-4 h-4" />
              Voice Interview
            </button>

            {isAdmin && (
              <button
                onClick={() => setActiveTab('admin-dashboard')}
                className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-sm font-medium transition-all ${
                  activeTab.startsWith('admin')
                    ? 'bg-purple-600 text-white shadow-md shadow-purple-600/30'
                    : 'text-purple-400 hover:text-purple-300 hover:bg-purple-950/40'
                }`}
              >
                <Shield className="w-4 h-4" />
                Admin Portal
              </button>
            )}
          </nav>
        )}

        {/* Right Section / User Info */}
        <div className="flex items-center gap-4">
          {user ? (
            <div className="flex items-center gap-3">
              {/* Streak Badge */}
              <div className="flex items-center gap-1.5 px-3 py-1 bg-amber-500/10 border border-amber-500/20 text-amber-400 rounded-full text-xs font-bold shadow-sm">
                <Flame className="w-4 h-4 fill-amber-400 text-amber-400 animate-bounce" />
                <span>{user.streak_count || 7} Day Streak</span>
              </div>

              {/* User Avatar & Logout */}
              <div className="flex items-center gap-2 bg-slate-900 border border-slate-800 pl-3 pr-1.5 py-1 rounded-full">
                <span className="text-xs font-semibold text-slate-300 flex items-center gap-1">
                  <UserIcon className="w-3.5 h-3.5 text-blue-400" />
                  {user.display_name}
                </span>
                <button
                  onClick={logout}
                  title="Sign Out"
                  className="p-1.5 hover:bg-rose-500/20 hover:text-rose-400 text-slate-400 rounded-full transition-colors"
                >
                  <LogOut className="w-4 h-4" />
                </button>
              </div>
            </div>
          ) : (
            <div className="flex items-center gap-2">
              <button
                onClick={() => setActiveTab('login')}
                className="px-5 py-2 text-sm font-bold text-white bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 rounded-xl shadow-lg shadow-blue-600/30 transition-all transform active:scale-95"
              >
                Sign In
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};
