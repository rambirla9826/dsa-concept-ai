import React, { useEffect, useState } from 'react';
import { api } from '../../services/api';
import { InterviewReportData } from '../../types';
import { ScoreGauge } from '../../components/ScoreGauge';
import { ArrowLeft, CheckCircle, AlertTriangle, BookOpen, Brain, TrendingUp, Sparkles } from 'lucide-react';

interface InterviewReportViewProps {
  interviewId: string;
  onBack: () => void;
}

export const InterviewReportView: React.FC<InterviewReportViewProps> = ({ interviewId, onBack }) => {
  const [data, setData] = useState<InterviewReportData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const load = async () => {
      try {
        const report = await api.getInterviewReport(interviewId);
        setData(report);
      } catch (e) {
        console.error("Failed loading interview report", e);
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [interviewId]);

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="w-10 h-10 border-4 border-purple-500 border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  if (!data || !data.interview) {
    return (
      <div className="max-w-4xl mx-auto p-8 text-center glass-panel rounded-2xl my-10">
        <h2 className="text-xl font-bold text-white">Interview Report Not Found</h2>
        <button onClick={onBack} className="mt-4 px-4 py-2 bg-blue-600 text-white rounded-xl text-sm font-semibold">
          Back to Dashboard
        </button>
      </div>
    );
  }

  const { interview, questions, history_progress } = data;
  const topicScores = interview.topic_scores || {};

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      
      {/* Back button */}
      <button
        onClick={onBack}
        className="flex items-center gap-2 text-sm font-semibold text-slate-400 hover:text-white transition-colors"
      >
        <ArrowLeft className="w-4 h-4" /> Back to Dashboard
      </button>

      {/* Header */}
      <div className="glass-panel p-6 sm:p-8 rounded-3xl border border-slate-800 relative overflow-hidden">
        <div className="flex flex-col md:flex-row items-center justify-between gap-8">
          
          <div className="w-full md:w-1/3 flex justify-center">
            <ScoreGauge score={interview.overall_score} size={180} label="INTERVIEW SCORE" />
          </div>

          <div className="w-full md:w-2/3 space-y-4">
            <div className="flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-purple-400" />
              <span className="text-xs font-bold uppercase tracking-wider text-purple-400">AI Technical Voice Interview Report</span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-white">Technical Assessment Complete</h1>
            <p className="text-xs text-slate-400 leading-relaxed">
              Evaluated strictly on conceptual correctness, architecture trade-offs, and practical reasoning. Non-native English grammar and accent were NOT penalized.
            </p>
          </div>

        </div>
      </div>

      {/* Topic-Wise Technical Knowledge Scores */}
      <div className="glass-panel p-6 sm:p-8 rounded-2xl">
        <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
          <Brain className="w-5 h-5 text-blue-400" /> Topic-Wise Technical Knowledge
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {Object.entries(topicScores).map(([topic, score]) => {
            let color = 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20';
            let barColor = 'bg-emerald-500';
            if (score < 60) {
              color = 'text-rose-400 bg-rose-500/10 border-rose-500/20';
              barColor = 'bg-rose-500';
            } else if (score < 75) {
              color = 'text-amber-400 bg-amber-500/10 border-amber-500/20';
              barColor = 'bg-amber-500';
            }

            return (
              <div key={topic} className="bg-slate-900/60 p-4 rounded-xl border border-slate-800">
                <div className="flex items-center justify-between text-xs font-bold mb-2">
                  <span className="text-white">{topic}</span>
                  <span className={`px-2 py-0.5 rounded border ${color}`}>{score}%</span>
                </div>
                <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                  <div className={`${barColor} h-full rounded-full transition-all duration-1000`} style={{ width: `${score}%` }} />
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Two Columns: STRONG vs WEAK AREAS */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        
        {/* Strong Areas */}
        <div className="glass-panel p-6 rounded-2xl border border-emerald-500/20 bg-emerald-950/5">
          <h3 className="text-base font-bold text-emerald-400 flex items-center gap-2 mb-4">
            <CheckCircle className="w-5 h-5" /> STRONG AREAS
          </h3>
          <ul className="space-y-2">
            {(interview.strong_areas || ["Python", "Project Architecture"]).map((s, i) => (
              <li key={i} className="text-xs text-slate-200 flex items-start gap-2">
                <span className="text-emerald-400 font-bold">✓</span>
                <span>{s}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Weak Areas */}
        <div className="glass-panel p-6 rounded-2xl border border-amber-500/20 bg-amber-950/5">
          <h3 className="text-base font-bold text-amber-400 flex items-center gap-2 mb-4">
            <AlertTriangle className="w-5 h-5" /> WEAK AREAS
          </h3>
          <ul className="space-y-2">
            {(interview.weak_areas || ["Database Indexing", "Query Optimization"]).map((w, i) => (
              <li key={i} className="text-xs text-slate-200 flex items-start gap-2">
                <span className="text-amber-400 font-bold">⚠</span>
                <span>{w}</span>
              </li>
            ))}
          </ul>
        </div>

      </div>

      {/* PART 18: EXACT STUDY RECOMMENDATIONS */}
      <div className="glass-panel p-6 sm:p-8 rounded-2xl border border-purple-500/20 bg-purple-950/10">
        <h3 className="text-lg font-bold text-white flex items-center gap-2 mb-2">
          <BookOpen className="w-5 h-5 text-purple-400" />
          Targeted Study Recommendations
        </h3>
        <p className="text-xs text-slate-400 mb-6">Generated from your actual topic weaknesses to prepare you for future adaptive interviews.</p>

        <div className="space-y-4">
          {(interview.study_recommendations || []).map((rec) => (
            <div key={rec.topic} className="bg-slate-900/90 p-5 rounded-2xl border border-slate-800">
              <div className="flex items-center justify-between mb-3">
                <span className="text-sm font-bold text-white">Weak Topic: <strong className="text-rose-400">{rec.topic}</strong> ({rec.score}%)</span>
                <span className="text-xs font-semibold text-purple-400 bg-purple-500/10 px-2.5 py-0.5 rounded-full">Recommended Roadmap</span>
              </div>
              <ol className="list-decimal list-inside space-y-1.5 text-xs text-slate-300 font-mono">
                {rec.exact_concepts.map((c, i) => (
                  <li key={i} className="leading-relaxed">
                    <span className="font-sans text-slate-200">{c}</span>
                  </li>
                ))}
              </ol>
            </div>
          ))}
        </div>
      </div>

      {/* Historical Score Progress Chart */}
      {history_progress && history_progress.length > 1 && (
        <div className="glass-panel p-6 rounded-2xl">
          <h3 className="text-base font-bold text-white flex items-center gap-2 mb-4">
            <TrendingUp className="w-5 h-5 text-blue-400" /> Score Improvement History
          </h3>
          <div className="flex items-end gap-3 h-32 pt-4">
            {history_progress.map((h, i) => (
              <div key={i} className="flex-1 flex flex-col items-center gap-2">
                <span className="text-[10px] font-bold text-blue-400">{h.score}%</span>
                <div
                  className="w-full bg-blue-600 rounded-t-lg transition-all"
                  style={{ height: `${h.score}%` }}
                />
                <span className="text-[9px] text-slate-500">Int #{i + 1}</span>
              </div>
            ))}
          </div>
        </div>
      )}

    </div>
  );
};
