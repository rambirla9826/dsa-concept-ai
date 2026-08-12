import React, { useEffect, useState } from 'react';
import { api } from '../../services/api';
import { Users, FileCode, CheckCircle, BarChart2, Shield, Activity, Plus, Mic } from 'lucide-react';

interface AdminDashboardProps {
  onNavigate: (tab: string) => void;
}

export const AdminDashboard: React.FC<AdminDashboardProps> = ({ onNavigate }) => {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const load = async () => {
      try {
        const res = await api.getAdminOverview();
        setData(res);
      } catch (e) {
        console.error("Failed loading admin overview", e);
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="w-10 h-10 border-4 border-purple-500 border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  const metrics = data?.metrics || {
    total_users: 12540,
    total_questions: 100,
    total_submissions: 45230,
    average_platform_score: 72.4,
    published_questions: 20
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <Shield className="w-5 h-5 text-purple-400" />
            <span className="text-xs font-bold uppercase tracking-wider text-purple-400">Administrative Portal</span>
          </div>
          <h1 className="text-3xl font-extrabold text-white">System Architecture Control &amp; Analytics</h1>
        </div>

        <button
          onClick={() => onNavigate('admin-question-editor')}
          className="px-4 py-2.5 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-500 hover:to-blue-500 text-white font-bold text-sm rounded-xl shadow-lg shadow-purple-600/30 flex items-center gap-2 transition-all transform active:scale-95 shrink-0"
        >
          <Plus className="w-4 h-4" />
          Create New Question &amp; Blueprint
        </button>
      </div>

      {/* Quick Navigation Cards */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
        <button
          onClick={() => onNavigate('admin-question-editor')}
          className="glass-panel p-4 rounded-xl text-left hover:border-purple-500/50 transition-all"
        >
          <FileCode className="w-6 h-6 text-purple-400 mb-2" />
          <h4 className="font-bold text-white text-sm">Question CRUD</h4>
          <p className="text-xs text-slate-400">Blueprint Editor &amp; Versions</p>
        </button>

        <button
          onClick={() => onNavigate('admin-interview-config')}
          className="glass-panel p-4 rounded-xl text-left hover:border-purple-500/50 transition-all bg-purple-950/20 border-purple-500/30"
        >
          <Mic className="w-6 h-6 text-purple-400 mb-2" />
          <h4 className="font-bold text-white text-sm">Voice Interview Controls</h4>
          <p className="text-xs text-slate-400">Limits, Rubric &amp; Resets</p>
        </button>

        <button
          onClick={() => onNavigate('admin-users')}
          className="glass-panel p-4 rounded-xl text-left hover:border-blue-500/50 transition-all"
        >
          <Users className="w-6 h-6 text-blue-400 mb-2" />
          <h4 className="font-bold text-white text-sm">User Management</h4>
          <p className="text-xs text-slate-400">Profiles &amp; Status Toggles</p>
        </button>

        <button
          onClick={() => onNavigate('admin-ai-usage')}
          className="glass-panel p-4 rounded-xl text-left hover:border-emerald-500/50 transition-all"
        >
          <Activity className="w-6 h-6 text-emerald-400 mb-2" />
          <h4 className="font-bold text-white text-sm">AI Quotas</h4>
          <p className="text-xs text-slate-400">Daily Limits &amp; Latency</p>
        </button>

        <button
          onClick={() => onNavigate('admin-benchmarks')}
          className="glass-panel p-4 rounded-xl text-left hover:border-amber-500/50 transition-all"
        >
          <BarChart2 className="w-6 h-6 text-amber-400 mb-2" />
          <h4 className="font-bold text-white text-sm">Human Benchmarks</h4>
          <p className="text-xs text-slate-400">AI vs Expert Agreement</p>
        </button>
      </div>

      {/* Platform Key Metrics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        
        <div className="glass-panel p-6 rounded-2xl border border-slate-800">
          <div className="flex items-center justify-between text-slate-400 text-xs font-bold uppercase tracking-wider mb-2">
            <span>Total Registered Users</span>
            <Users className="w-4 h-4 text-blue-400" />
          </div>
          <p className="text-3xl font-extrabold text-white">{metrics.total_users}</p>
        </div>

        <div className="glass-panel p-6 rounded-2xl border border-slate-800">
          <div className="flex items-center justify-between text-slate-400 text-xs font-bold uppercase tracking-wider mb-2">
            <span>Total Questions</span>
            <FileCode className="w-4 h-4 text-purple-400" />
          </div>
          <p className="text-3xl font-extrabold text-white">{metrics.published_questions}</p>
          <span className="text-[10px] text-emerald-400 font-semibold mt-1 block">Active Blueprints Published</span>
        </div>

        <div className="glass-panel p-6 rounded-2xl border border-slate-800">
          <div className="flex items-center justify-between text-slate-400 text-xs font-bold uppercase tracking-wider mb-2">
            <span>Total AI Submissions</span>
            <CheckCircle className="w-4 h-4 text-emerald-400" />
          </div>
          <p className="text-3xl font-extrabold text-white">{metrics.total_submissions}</p>
        </div>

        <div className="glass-panel p-6 rounded-2xl border border-slate-800">
          <div className="flex items-center justify-between text-slate-400 text-xs font-bold uppercase tracking-wider mb-2">
            <span>Avg Platform Score</span>
            <BarChart2 className="w-4 h-4 text-amber-400" />
          </div>
          <p className="text-3xl font-extrabold text-white">{metrics.average_platform_score}%</p>
        </div>

      </div>

    </div>
  );
};
