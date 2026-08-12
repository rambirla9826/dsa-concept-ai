import React, { useEffect, useState } from 'react';
import { api } from '../../services/api';
import { UserInterviewLimit } from '../../types';
import { ArrowLeft, Shield, RotateCcw, Plus, CheckCircle2, Sliders, Activity, Search } from 'lucide-react';

interface AdminInterviewConfigProps {
  onBack: () => void;
}

export const AdminInterviewConfig: React.FC<AdminInterviewConfigProps> = ({ onBack }) => {
  const [limits, setLimits] = useState<UserInterviewLimit[]>([]);
  const [analytics, setAnalytics] = useState<any>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(true);

  // Rubric weights
  const [techWeight, setTechWeight] = useState(40);
  const [conceptWeight, setConceptWeight] = useState(25);
  const [reasoningWeight, setReasoningWeight] = useState(15);
  const [completeWeight, setCompleteWeight] = useState(10);
  const [practicalWeight, setPracticalWeight] = useState(10);
  const [savingConfig, setSavingConfig] = useState(false);

  const loadData = async () => {
    try {
      const [lData, aData] = await Promise.all([
        api.getAdminInterviewLimits(),
        api.getAdminInterviewAnalytics()
      ]);
      setLimits(lData);
      setAnalytics(aData);
    } catch (e) {
      console.error("Failed loading interview controls", e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleGrantAttempts = async (user: UserInterviewLimit, additional: number) => {
    const newAllowed = user.allowed_interviews + additional;
    try {
      await api.updateUserInterviewLimit(user.user_id, newAllowed, user.is_unlimited, user.is_disabled);
      loadData();
    } catch (e: any) {
      alert(e.message || "Action failed");
    }
  };

  const handleResetAttempts = async (uid: string, email: string) => {
    if (window.confirm(`Reset used interview attempts to 0 for ${email}?`)) {
      try {
        await api.resetUserInterviewAttempts(uid);
        loadData();
      } catch (e: any) {
        alert(e.message || "Reset failed");
      }
    }
  };

  const handleToggleUnlimited = async (user: UserInterviewLimit) => {
    try {
      await api.updateUserInterviewLimit(user.user_id, user.allowed_interviews, !user.is_unlimited, user.is_disabled);
      loadData();
    } catch (e: any) {
      alert(e.message || "Action failed");
    }
  };

  const filteredLimits = limits.filter(l => 
    l.email.toLowerCase().includes(searchTerm.toLowerCase()) || 
    l.display_name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      
      <button onClick={onBack} className="flex items-center gap-2 text-sm font-semibold text-slate-400 hover:text-white">
        <ArrowLeft className="w-4 h-4" /> Back to Admin Overview
      </button>

      <div>
        <div className="flex items-center gap-2 mb-1 text-purple-400 font-bold text-xs">
          <Shield className="w-4 h-4" /> ADMIN INTERVIEW LIMITS &amp; RUBRIC CONTROL
        </div>
        <h1 className="text-2xl font-extrabold text-white">AI Voice Technical Interview Control Panel</h1>
      </div>

      {/* Analytics Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="glass-panel p-5 rounded-xl">
          <p className="text-xs font-bold uppercase text-slate-400">Total Interviews Conducted</p>
          <p className="text-3xl font-extrabold text-white mt-1">{analytics?.total_interviews || 0}</p>
        </div>

        <div className="glass-panel p-5 rounded-xl">
          <p className="text-xs font-bold uppercase text-slate-400">Completed Sessions</p>
          <p className="text-3xl font-extrabold text-emerald-400 mt-1">{analytics?.completed_interviews || 0}</p>
        </div>

        <div className="glass-panel p-5 rounded-xl">
          <p className="text-xs font-bold uppercase text-slate-400">Avg Interview Score</p>
          <p className="text-3xl font-extrabold text-purple-400 mt-1">{analytics?.average_interview_score || 0}%</p>
        </div>

        <div className="glass-panel p-5 rounded-xl">
          <p className="text-xs font-bold uppercase text-slate-400">Default Limit / Student</p>
          <p className="text-3xl font-extrabold text-amber-400 mt-1">5 Sessions</p>
        </div>
      </div>

      {/* Rubric Weight Configurator */}
      <div className="glass-panel p-6 rounded-2xl space-y-4">
        <h3 className="text-base font-bold text-white flex items-center gap-2">
          <Sliders className="w-5 h-5 text-purple-400" /> Interview Rubric Dimension Weight Configurator
        </h3>
        
        <div className="grid grid-cols-2 md:grid-cols-5 gap-3 text-xs font-semibold">
          <div>
            <label className="text-slate-400 block mb-1">Tech Correctness</label>
            <input type="number" value={techWeight} onChange={(e) => setTechWeight(parseInt(e.target.value))} className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2 text-white" />
          </div>
          <div>
            <label className="text-slate-400 block mb-1">Concept Understanding</label>
            <input type="number" value={conceptWeight} onChange={(e) => setConceptWeight(parseInt(e.target.value))} className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2 text-white" />
          </div>
          <div>
            <label className="text-slate-400 block mb-1">Reasoning</label>
            <input type="number" value={reasoningWeight} onChange={(e) => setReasoningWeight(parseInt(e.target.value))} className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2 text-white" />
          </div>
          <div>
            <label className="text-slate-400 block mb-1">Completeness</label>
            <input type="number" value={completeWeight} onChange={(e) => setCompleteWeight(parseInt(e.target.value))} className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2 text-white" />
          </div>
          <div>
            <label className="text-slate-400 block mb-1">Practical</label>
            <input type="number" value={practicalWeight} onChange={(e) => setPracticalWeight(parseInt(e.target.value))} className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2 text-white" />
          </div>
        </div>
      </div>

      {/* Student Interview Attempt Limits Table */}
      <div className="glass-panel rounded-2xl overflow-hidden">
        <div className="p-4 border-b border-slate-800 flex items-center justify-between">
          <h3 className="text-sm font-bold text-white">Student Interview Attempt Limits &amp; Resets</h3>
          <div className="relative">
            <Search className="w-3.5 h-3.5 text-slate-400 absolute left-2.5 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              placeholder="Search student..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="bg-slate-900 border border-slate-800 rounded-xl pl-8 pr-3 py-1.5 text-xs text-slate-200"
            />
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm text-slate-300">
            <thead className="bg-slate-900/80 text-xs font-bold uppercase tracking-wider text-slate-400 border-b border-slate-800">
              <tr>
                <th className="py-3 px-4">Student</th>
                <th className="py-3 px-4">Interviews Used</th>
                <th className="py-3 px-4">Allowed Limit</th>
                <th className="py-3 px-4">Access Type</th>
                <th className="py-3 px-4 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 text-xs">
              {filteredLimits.map((l) => (
                <tr key={l.user_id} className="hover:bg-slate-900/40">
                  <td className="py-3 px-4 font-bold text-white">
                    {l.display_name}
                    <span className="block text-[10px] text-slate-400 font-normal">{l.email}</span>
                  </td>
                  <td className="py-3 px-4 font-bold text-amber-400">
                    {l.used_interviews}
                  </td>
                  <td className="py-3 px-4 font-bold text-white">
                    {l.is_unlimited ? '∞ Unlimited' : l.allowed_interviews}
                  </td>
                  <td className="py-3 px-4">
                    {l.is_unlimited ? (
                      <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-purple-500/10 text-purple-400 border border-purple-500/20">Unlimited</span>
                    ) : (
                      <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-blue-500/10 text-blue-400 border border-blue-500/20">Standard ({l.allowed_interviews})</span>
                    )}
                  </td>
                  <td className="py-3 px-4 text-right">
                    <div className="flex items-center justify-end gap-2">
                      <button
                        onClick={() => handleGrantAttempts(l, 5)}
                        className="px-2 py-1 bg-blue-600/20 text-blue-300 border border-blue-500/30 hover:bg-blue-600/30 rounded text-[10px] font-bold flex items-center gap-1"
                      >
                        <Plus className="w-3 h-3" /> +5 Attempts
                      </button>

                      <button
                        onClick={() => handleResetAttempts(l.user_id, l.email)}
                        className="px-2 py-1 bg-amber-600/20 text-amber-300 border border-amber-500/30 hover:bg-amber-600/30 rounded text-[10px] font-bold flex items-center gap-1"
                      >
                        <RotateCcw className="w-3 h-3" /> Reset 0
                      </button>

                      <button
                        onClick={() => handleToggleUnlimited(l)}
                        className="px-2 py-1 bg-purple-600/20 text-purple-300 border border-purple-500/30 hover:bg-purple-600/30 rounded text-[10px] font-bold"
                      >
                        {l.is_unlimited ? 'Set Limited' : 'Set Unlimited'}
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

    </div>
  );
};
