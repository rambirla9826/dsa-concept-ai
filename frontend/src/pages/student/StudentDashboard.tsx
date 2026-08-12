import React, { useEffect, useState } from 'react';
import { api } from '../../services/api';
import { StudentDashboardData, ResumeData } from '../../types';
import { ScoreGauge } from '../../components/ScoreGauge';
import { DifficultyBadge } from '../../components/Badge';
import { Flame, CheckCircle, Brain, ArrowRight, TrendingUp, AlertCircle, Sparkles, Mic, FileText, Upload, Shield } from 'lucide-react';
import { ResumeUploadModal } from '../../components/ResumeUploadModal';

interface StudentDashboardProps {
  onSelectQuestion: (id: string) => void;
  onViewResult: (subId: string) => void;
  onStartVoiceInterview: (interviewId: string) => void;
  onViewInterviewReport: (interviewId: string) => void;
}

export const StudentDashboard: React.FC<StudentDashboardProps> = ({
  onSelectQuestion,
  onViewResult,
  onStartVoiceInterview,
  onViewInterviewReport
}) => {
  const [data, setData] = useState<StudentDashboardData | null>(null);
  const [resume, setResume] = useState<ResumeData | null>(null);
  const [interviewHistory, setInterviewHistory] = useState<any[]>([]);
  const [isResumeModalOpen, setIsResumeModalOpen] = useState(false);
  const [loading, setLoading] = useState<boolean>(true);
  const [startingInterview, setStartingInterview] = useState(false);
  const [interviewError, setInterviewError] = useState<string | null>(null);

  const loadData = async () => {
    try {
      const [dashRes, resumeRes, historyRes] = await Promise.all([
        api.getStudentDashboard(),
        api.getLatestResume().catch(() => null),
        api.getInterviewHistory().catch(() => [])
      ]);
      setData(dashRes);
      setResume(resumeRes);
      setInterviewHistory(historyRes);
    } catch (e) {
      console.error("Failed loading student dashboard", e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleStartInterview = async () => {
    if (!resume) {
      setIsResumeModalOpen(true);
      return;
    }

    setStartingInterview(true);
    setInterviewError(null);

    try {
      const session = await api.startInterview();
      onStartVoiceInterview(session.interview_id);
    } catch (e: any) {
      console.error(e);
      setInterviewError(e.message || "Failed starting interview session.");
    } finally {
      setStartingInterview(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="flex flex-col items-center gap-3">
          <div className="w-10 h-10 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
          <p className="text-sm font-medium text-slate-400">Loading your conceptual progress...</p>
        </div>
      </div>
    );
  }

  if (!data) return null;

  const completedInterviews = interviewHistory.filter(i => i.status === 'COMPLETED');
  const lastInterview = completedInterviews[0];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      
      {/* Welcome Banner */}
      <div className="glass-panel p-6 sm:p-8 rounded-2xl relative overflow-hidden gradient-subtle border border-slate-800">
        <div className="absolute top-0 right-0 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl -z-10 pointer-events-none" />
        
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div>
            <div className="flex items-center gap-2 mb-2">
              <Sparkles className="w-5 h-5 text-amber-400" />
              <span className="text-xs font-bold uppercase tracking-wider text-blue-400">Conceptual Assessment Hub</span>
            </div>
            <h1 className="text-3xl sm:text-4xl font-extrabold text-white">
              Welcome back, {data.user_info.display_name}!
            </h1>
            <p className="mt-2 text-slate-400 text-sm sm:text-base max-w-2xl">
              Focus on algorithm thinking, complexity trade-offs, and conceptual mastery.
            </p>
          </div>

          {/* Streak Counter */}
          <div className="glass-panel p-4 rounded-xl flex items-center gap-3 self-start md:self-auto border border-amber-500/20 bg-amber-500/5">
            <div className="w-10 h-10 rounded-lg bg-amber-500/10 flex items-center justify-center text-amber-400">
              <Flame className="w-6 h-6 animate-pulse" />
            </div>
            <div>
              <p className="text-[10px] font-bold uppercase tracking-wider text-slate-400">Daily Streak</p>
              <p className="text-xl font-extrabold text-white">{data.stats.current_streak} Days</p>
            </div>
          </div>
        </div>
      </div>

      {/* PART 39: AI TECHNICAL VOICE INTERVIEW PROMINENT HERO CARD */}
      <div className="glass-panel p-6 sm:p-8 rounded-3xl border border-purple-500/30 bg-gradient-to-r from-purple-950/30 via-slate-900 to-blue-950/30 relative overflow-hidden shadow-2xl">
        <div className="absolute -top-12 -right-12 w-64 h-64 bg-purple-500/10 rounded-full blur-3xl pointer-events-none" />

        <div className="flex flex-col lg:flex-row items-center justify-between gap-8 relative">
          
          <div className="space-y-4 max-w-2xl">
            <div className="flex flex-wrap items-center gap-2">
              <span className="px-3 py-1 bg-purple-500/20 text-purple-300 border border-purple-500/30 rounded-full text-xs font-extrabold uppercase tracking-wider flex items-center gap-1.5">
                <Mic className="w-3.5 h-3.5 text-purple-400" /> AI VOICE TECHNICAL INTERVIEW
              </span>
              {resume && (
                <span className="px-2.5 py-0.5 bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded-full text-xs font-bold flex items-center gap-1">
                  <CheckCircle className="w-3 h-3" /> Resume Analyzed
                </span>
              )}
            </div>

            <h2 className="text-2xl sm:text-3xl font-extrabold text-white">
              Adaptive Two-Way Voice Technical Assessment
            </h2>

            <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
              AI speaks technical questions tailored specifically to your resume skills and projects. Speak your answers in natural voice — evaluated strictly on technical depth and reasoning.
            </p>

            {resume ? (
              <div className="bg-slate-900/80 p-3.5 rounded-xl border border-slate-800 flex items-center justify-between gap-4">
                <div className="flex items-center gap-2 text-xs text-slate-300 truncate">
                  <FileText className="w-4 h-4 text-purple-400 shrink-0" />
                  <span className="font-bold text-white truncate">{resume.filename}</span>
                  <span className="text-slate-500 hidden sm:inline">• {resume.skills.slice(0, 4).join(', ')}</span>
                </div>
                <button
                  onClick={() => setIsResumeModalOpen(true)}
                  className="text-xs font-bold text-purple-400 hover:text-purple-300 underline shrink-0"
                >
                  Update PDF
                </button>
              </div>
            ) : (
              <div className="bg-amber-500/10 p-3.5 rounded-xl border border-amber-500/20 text-xs text-amber-300 flex items-center justify-between gap-4">
                <span>Upload your PDF resume to unlock personalized voice questions.</span>
                <button
                  onClick={() => setIsResumeModalOpen(true)}
                  className="px-3 py-1.5 bg-amber-500 text-slate-950 font-bold rounded-lg shrink-0 flex items-center gap-1"
                >
                  <Upload className="w-3.5 h-3.5" /> Upload Resume
                </button>
              </div>
            )}

            {interviewError && (
              <div className="p-3 bg-rose-500/10 border border-rose-500/20 rounded-xl text-rose-400 text-xs font-semibold flex items-center gap-2">
                <AlertCircle className="w-4 h-4 shrink-0" />
                {interviewError}
              </div>
            )}
          </div>

          {/* Action Trigger Card */}
          <div className="w-full lg:w-72 glass-panel p-6 rounded-2xl border border-slate-800 text-center space-y-4 shrink-0 bg-slate-900/90">
            <div>
              <p className="text-[10px] font-bold uppercase tracking-wider text-slate-400">Student Attempts</p>
              <p className="text-3xl font-extrabold text-white mt-1">
                {interviewHistory.length} / 5 <span className="text-xs text-slate-400 font-normal">USED</span>
              </p>
            </div>

            {lastInterview && (
              <div className="pt-2 border-t border-slate-800">
                <p className="text-[10px] font-bold uppercase tracking-wider text-slate-400">Last Interview Score</p>
                <p className="text-2xl font-extrabold text-emerald-400">{lastInterview.overall_score}%</p>
              </div>
            )}

            <button
              onClick={handleStartInterview}
              disabled={startingInterview}
              className="w-full py-3.5 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-500 hover:to-blue-500 text-white font-extrabold text-sm rounded-xl shadow-lg shadow-purple-500/30 transition-all active:scale-95 flex items-center justify-center gap-2 disabled:opacity-50"
            >
              {startingInterview ? (
                <>
                  <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  <span>Reserving Session...</span>
                </>
              ) : (
                <>
                  <Mic className="w-4 h-4" />
                  <span>{resume ? 'START INTERVIEW' : 'UPLOAD RESUME'}</span>
                </>
              )}
            </button>
          </div>

        </div>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        
        {/* Conceptual Score Gauge */}
        <div className="glass-panel p-6 rounded-2xl flex flex-col items-center justify-center text-center">
          <ScoreGauge score={data.stats.average_concept_score} size={150} label="CONCEPT SCORE" />
          <p className="mt-3 text-xs text-slate-400 font-medium">Overall algorithm &amp; data structure reasoning</p>
        </div>

        {/* Attempted Problems */}
        <div className="glass-panel p-6 rounded-2xl flex flex-col justify-between">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-400">Problem Submissions</span>
            <Brain className="w-5 h-5 text-blue-400" />
          </div>
          <div>
            <p className="text-4xl font-extrabold text-white">{data.stats.total_attempted}</p>
            <p className="text-xs text-slate-400 mt-1">{data.stats.total_completed} successfully evaluated</p>
          </div>
          <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden mt-4">
            <div 
              className="bg-blue-500 h-full rounded-full transition-all duration-1000"
              style={{ width: `${Math.min(100, (data.stats.total_completed / Math.max(1, data.stats.total_attempted)) * 100)}%` }}
            />
          </div>
        </div>

        {/* Strong vs Weak Breakdown */}
        <div className="glass-panel p-6 rounded-2xl flex flex-col justify-between space-y-4">
          <div>
            <p className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">Strong Concepts</p>
            <div className="flex flex-wrap gap-1.5">
              {data.strong_topics.map(t => (
                <span key={t.category} className="px-2.5 py-1 bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-bold rounded-lg">
                  {t.category} ({t.score}%)
                </span>
              ))}
            </div>
          </div>

          <div>
            <p className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">Concepts To Improve</p>
            <div className="flex flex-wrap gap-1.5">
              {data.weak_topics.map(t => (
                <span key={t.category} className="px-2.5 py-1 bg-rose-500/10 border border-rose-500/20 text-rose-400 text-xs font-bold rounded-lg">
                  {t.category} ({t.score}%)
                </span>
              ))}
            </div>
          </div>
        </div>

      </div>

      {/* Past Voice Interview History List */}
      {completedInterviews.length > 0 && (
        <div className="glass-panel p-6 rounded-2xl space-y-4">
          <h3 className="text-base font-bold text-white flex items-center gap-2">
            <Mic className="w-5 h-5 text-purple-400" /> AI Technical Voice Interview History
          </h3>
          <div className="divide-y divide-slate-800">
            {completedInterviews.map((int: any) => (
              <div key={int.id} className="py-3 flex items-center justify-between text-xs">
                <div>
                  <p className="font-bold text-white">Interview #{int.id.slice(-4)}</p>
                  <p className="text-slate-400 text-[10px]">{new Date(int.completed_at || int.created_at).toLocaleDateString()}</p>
                </div>
                <div className="flex items-center gap-4">
                  <span className="font-bold text-purple-400 text-sm">{int.overall_score}%</span>
                  <button
                    onClick={() => onViewInterviewReport(int.id)}
                    className="px-3 py-1 bg-purple-600/20 text-purple-300 border border-purple-500/30 hover:bg-purple-600/30 rounded-lg font-bold"
                  >
                    View Report
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Resume Upload Modal */}
      <ResumeUploadModal
        isOpen={isResumeModalOpen}
        onClose={() => setIsResumeModalOpen(false)}
        onSuccess={(parsedResume) => {
          setResume(parsedResume);
        }}
      />

    </div>
  );
};
