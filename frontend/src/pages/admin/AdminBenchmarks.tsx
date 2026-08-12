import React, { useEffect, useState } from 'react';
import { api } from '../../services/api';
import { ArrowLeft, BarChart2, Plus, CheckCircle, Calculator } from 'lucide-react';

interface AdminBenchmarksProps {
  onBack: () => void;
}

export const AdminBenchmarks: React.FC<AdminBenchmarksProps> = ({ onBack }) => {
  const [benchmarks, setBenchmarks] = useState<any>(null);
  const [submissions, setSubmissions] = useState<any[]>([]);
  const [selectedSubId, setSelectedSubId] = useState('');
  const [humanScore, setHumanScore] = useState<number>(85);
  const [notes, setNotes] = useState('');
  const [loading, setLoading] = useState(true);
  const [recording, setRecording] = useState(false);

  const loadData = async () => {
    try {
      const [bData, sData] = await Promise.all([
        api.getBenchmarks(),
        api.getUserSubmissions()
      ]);
      setBenchmarks(bData);
      setSubmissions(sData);
      if (sData.length > 0) {
        setSelectedSubId(sData[0].id);
      }
    } catch (e) {
      console.error("Failed loading benchmarks", e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleRecord = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedSubId) return;
    setRecording(true);
    try {
      await api.addBenchmark(selectedSubId, humanScore, notes);
      setNotes('');
      loadData();
    } catch (err: any) {
      alert(err.message || "Failed recording benchmark");
    } finally {
      setRecording(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center py-20">
        <div className="w-8 h-8 border-4 border-amber-500 border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  const b = benchmarks || {
    total_benchmarks: 0,
    mean_absolute_error: 0.0,
    agreement_rate_pct: 100.0,
    correlation: 1.0,
    entries: []
  };

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      
      <button onClick={onBack} className="flex items-center gap-2 text-sm font-semibold text-slate-400 hover:text-white">
        <ArrowLeft className="w-4 h-4" /> Back to Admin Overview
      </button>

      <div>
        <div className="flex items-center gap-2 mb-1 text-amber-400 font-bold text-xs">
          <BarChart2 className="w-4 h-4" /> HUMAN BENCHMARK &amp; EVALUATION ACCURACY SYSTEM
        </div>
        <h1 className="text-2xl font-extrabold text-white">AI Evaluator vs. Human Expert Agreement</h1>
      </div>

      {/* Analytics Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="glass-panel p-5 rounded-xl">
          <p className="text-xs font-bold uppercase text-slate-400">Total Benchmarks</p>
          <p className="text-3xl font-extrabold text-white mt-1">{b.total_benchmarks}</p>
          <p className="text-[10px] text-slate-500 mt-1">Evaluated Submissions</p>
        </div>

        <div className="glass-panel p-5 rounded-xl">
          <p className="text-xs font-bold uppercase text-slate-400">Mean Absolute Error (MAE)</p>
          <p className="text-3xl font-extrabold text-amber-400 mt-1">{b.mean_absolute_error}</p>
          <p className="text-[10px] text-slate-500 mt-1">Lower is better (&lt; 5.0 optimal)</p>
        </div>

        <div className="glass-panel p-5 rounded-xl">
          <p className="text-xs font-bold uppercase text-slate-400">Agreement Rate (&lt;=10 pts)</p>
          <p className="text-3xl font-extrabold text-emerald-400 mt-1">{b.agreement_rate_pct}%</p>
          <p className="text-[10px] text-slate-500 mt-1">Within 10 point score variance</p>
        </div>

        <div className="glass-panel p-5 rounded-xl">
          <p className="text-xs font-bold uppercase text-slate-400">Pearson Correlation</p>
          <p className="text-3xl font-extrabold text-purple-400 mt-1">{b.correlation}</p>
          <p className="text-[10px] text-slate-500 mt-1">1.0 = Perfect Positive Correlation</p>
        </div>
      </div>

      {/* Add Expert Benchmark Score Form */}
      <form onSubmit={handleRecord} className="glass-panel p-6 rounded-2xl space-y-4">
        <h3 className="text-base font-bold text-white flex items-center gap-2">
          <Plus className="w-5 h-5 text-amber-400" /> Record Expert Human Benchmark
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-xs font-bold text-slate-400 uppercase mb-1">Select Student Submission</label>
            <select
              value={selectedSubId}
              onChange={(e) => setSelectedSubId(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded-xl p-2.5 text-xs text-white"
            >
              {submissions.map(s => (
                <option key={s.id} value={s.id}>
                  {s.question_title} - AI Score: {s.final_score}% (ID: {s.id})
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-xs font-bold text-slate-400 uppercase mb-1">Expert Human Score (0-100)</label>
            <input
              type="number"
              min="0"
              max="100"
              value={humanScore}
              onChange={(e) => setHumanScore(parseFloat(e.target.value))}
              className="w-full bg-slate-900 border border-slate-700 rounded-xl p-2.5 text-xs text-white"
            />
          </div>

          <div>
            <label className="block text-xs font-bold text-slate-400 uppercase mb-1">Expert Reviewer Notes</label>
            <input
              type="text"
              placeholder="e.g. Validated time complexity logic"
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded-xl p-2.5 text-xs text-white"
            />
          </div>
        </div>

        <div className="flex justify-end pt-2">
          <button
            type="submit"
            disabled={recording || !selectedSubId}
            className="px-5 py-2 bg-amber-600 hover:bg-amber-500 text-white font-bold text-xs rounded-xl flex items-center gap-2"
          >
            <Calculator className="w-4 h-4" /> Save Benchmark Data
          </button>
        </div>
      </form>

      {/* Benchmark Entries Table */}
      <div className="glass-panel rounded-2xl overflow-hidden">
        <div className="p-4 border-b border-slate-800 text-sm font-bold text-white">
          Recorded Benchmark Dataset ({b.entries.length} Entries)
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm text-slate-300">
            <thead className="bg-slate-900/80 text-xs font-bold uppercase tracking-wider text-slate-400 border-b border-slate-800">
              <tr>
                <th className="py-3 px-4">Submission ID</th>
                <th className="py-3 px-4">AI Score</th>
                <th className="py-3 px-4">Human Score</th>
                <th className="py-3 px-4">Difference</th>
                <th className="py-3 px-4">Notes</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 text-xs">
              {b.entries.map((item: any) => {
                const diff = Math.abs(item.ai_score - item.human_score);
                return (
                  <tr key={item.id} className="hover:bg-slate-900/40">
                    <td className="py-3 px-4 font-mono text-slate-400">{item.submission_id}</td>
                    <td className="py-3 px-4 font-bold text-blue-400">{item.ai_score}%</td>
                    <td className="py-3 px-4 font-bold text-purple-400">{item.human_score}%</td>
                    <td className={`py-3 px-4 font-bold ${diff <= 5 ? 'text-emerald-400' : diff <= 10 ? 'text-amber-400' : 'text-rose-400'}`}>
                      {diff.toFixed(1)} pts
                    </td>
                    <td className="py-3 px-4 text-slate-400">{item.notes || 'N/A'}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>

    </div>
  );
};
