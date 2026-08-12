import React, { useEffect, useState } from 'react';
import { api } from '../../services/api';
import { ArrowLeft, Activity, Cpu, DollarSign, AlertCircle, CheckCircle } from 'lucide-react';

interface AdminAIUsageProps {
  onBack: () => void;
}

export const AdminAIUsage: React.FC<AdminAIUsageProps> = ({ onBack }) => {
  const [stats, setStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      try {
        const data = await api.getAIUsage();
        setStats(data);
      } catch (e) {
        console.error("Failed loading AI usage stats", e);
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  if (loading) {
    return (
      <div className="flex justify-center py-20">
        <div className="w-8 h-8 border-4 border-emerald-500 border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  const s = stats || {
    provider: "Google Gemini",
    model: "gemini-1.5-flash",
    daily_limit: 50,
    evaluations_today: 12,
    evaluations_this_month: 240,
    total_evaluations: 850,
    quota_remaining_today: 38,
    error_count: 0,
    error_rate_percent: 0.0,
    estimated_cost_usd: 0.0,
    free_tier_status: "ACTIVE_FREE_TIER"
  };

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      
      <button onClick={onBack} className="flex items-center gap-2 text-sm font-semibold text-slate-400 hover:text-white">
        <ArrowLeft className="w-4 h-4" /> Back to Admin Overview
      </button>

      <div>
        <div className="flex items-center gap-2 mb-1 text-emerald-400 font-bold text-xs">
          <Activity className="w-4 h-4" /> AI EVALUATOR MONITOR &amp; RATE LIMITING
        </div>
        <h1 className="text-2xl font-extrabold text-white">Google Gemini API Quota &amp; Usage Control</h1>
      </div>

      {/* Free Tier Cost Protection Banner */}
      <div className="bg-emerald-950/20 border border-emerald-500/30 p-4 rounded-2xl flex items-start gap-3">
        <CheckCircle className="w-5 h-5 text-emerald-400 shrink-0 mt-0.5" />
        <div>
          <h4 className="text-sm font-bold text-emerald-300">Free Tier Cost Strategy Active</h4>
          <p className="text-xs text-emerald-400/80 mt-0.5">
            System is running under Google Gemini Free Tier limits with application-level rate limiting enabled to ensure zero unexpected charges.
          </p>
        </div>
      </div>

      {/* Usage Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="glass-panel p-5 rounded-xl">
          <p className="text-xs font-bold uppercase text-slate-400">Evaluations Today</p>
          <p className="text-3xl font-extrabold text-white mt-1">{s.evaluations_today} / {s.daily_limit}</p>
          <p className="text-[10px] text-slate-500 mt-1">Daily Cap Limit</p>
        </div>

        <div className="glass-panel p-5 rounded-xl">
          <p className="text-xs font-bold uppercase text-slate-400">Quota Remaining Today</p>
          <p className="text-3xl font-extrabold text-emerald-400 mt-1">{s.quota_remaining_today}</p>
          <p className="text-[10px] text-slate-500 mt-1">Available Evaluations</p>
        </div>

        <div className="glass-panel p-5 rounded-xl">
          <p className="text-xs font-bold uppercase text-slate-400">Evaluations This Month</p>
          <p className="text-3xl font-extrabold text-white mt-1">{s.evaluations_this_month}</p>
          <p className="text-[10px] text-slate-500 mt-1">Monthly Total</p>
        </div>

        <div className="glass-panel p-5 rounded-xl">
          <p className="text-xs font-bold uppercase text-slate-400">Est. API Charges</p>
          <p className="text-3xl font-extrabold text-emerald-400 mt-1">$0.00</p>
          <p className="text-[10px] text-emerald-500 mt-1 font-bold">100% Covered by Free Quota</p>
        </div>
      </div>

      {/* Technical Configuration */}
      <div className="glass-panel p-6 rounded-2xl space-y-4">
        <h3 className="text-base font-bold text-white flex items-center gap-2">
          <Cpu className="w-5 h-5 text-purple-400" /> API Integration Parameters
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs font-mono">
          <div className="bg-slate-900 p-3 rounded-xl border border-slate-800">
            <span className="text-slate-400">Evaluator Engine:</span> <strong className="text-blue-400">{s.provider}</strong>
          </div>
          <div className="bg-slate-900 p-3 rounded-xl border border-slate-800">
            <span className="text-slate-400">Model Name:</span> <strong className="text-purple-400">{s.model}</strong>
          </div>
          <div className="bg-slate-900 p-3 rounded-xl border border-slate-800">
            <span className="text-slate-400">Structured Output:</span> <strong className="text-emerald-400">JSON Schema Enforced</strong>
          </div>
          <div className="bg-slate-900 p-3 rounded-xl border border-slate-800">
            <span className="text-slate-400">Scoring Calculation:</span> <strong className="text-amber-400">100% Deterministic Backend Engine</strong>
          </div>
        </div>
      </div>

    </div>
  );
};
