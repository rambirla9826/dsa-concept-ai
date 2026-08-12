import React, { useEffect, useState } from 'react';
import { api } from '../../services/api';
import { FullEvaluationResult, SubmissionRecord, QuestionDetail } from '../../types';
import { ScoreGauge } from '../../components/ScoreGauge';
import { ConceptBreakdownCard } from '../../components/ConceptBreakdownCard';
import { ArrowLeft, CheckCircle, AlertTriangle, Brain, ArrowRight, Clock, HardDrive, FileText } from 'lucide-react';

interface ResultViewProps {
  submissionId: string;
  onBackToDashboard: () => void;
  onSelectQuestion: (id: string) => void;
}

export const ResultView: React.FC<ResultViewProps> = ({ submissionId, onBackToDashboard, onSelectQuestion }) => {
  const [submission, setSubmission] = useState<SubmissionRecord | null>(null);
  const [evaluation, setEvaluation] = useState<FullEvaluationResult | null>(null);
  const [question, setQuestion] = useState<QuestionDetail | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const load = async () => {
      try {
        const data = await api.getSubmissionResult(submissionId);
        setSubmission(data.submission);
        setEvaluation(data.evaluation);
        setQuestion(data.question);
      } catch (e) {
        console.error("Failed loading submission result", e);
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [submissionId]);

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="w-10 h-10 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  if (!evaluation || !submission) {
    return (
      <div className="max-w-4xl mx-auto p-8 text-center glass-panel rounded-2xl my-10">
        <h2 className="text-xl font-bold text-white">Result Not Available</h2>
        <button onClick={onBackToDashboard} className="mt-4 px-4 py-2 bg-blue-600 text-white rounded-xl text-sm font-semibold">
          Back to Dashboard
        </button>
      </div>
    );
  }

  const dims = evaluation.dimension_scores || {
    concept_blueprint: 90,
    algorithm_correctness: 95,
    reasoning: 85,
    time_complexity: 60,
    space_complexity: 100,
    edge_cases: 80
  };

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      
      {/* Back Button */}
      <button
        onClick={onBackToDashboard}
        className="flex items-center gap-2 text-sm font-semibold text-slate-400 hover:text-white transition-colors"
      >
        <ArrowLeft className="w-4 h-4" />
        Back to Dashboard
      </button>

      {/* Hero Scorecard Panel */}
      <div className="glass-panel p-6 sm:p-8 rounded-3xl border border-slate-800 relative overflow-hidden">
        <div className="flex flex-col md:flex-row items-center justify-between gap-8">
          
          {/* Radial Score Gauge */}
          <div className="w-full md:w-1/3 flex justify-center">
            <ScoreGauge score={evaluation.final_score} size={180} />
          </div>

          {/* Dimension Score Progress Bars */}
          <div className="w-full md:w-2/3 space-y-3">
            <h3 className="text-sm font-bold text-slate-400 uppercase tracking-wider mb-2">Dimension Breakdown</h3>
            
            {/* Concept Blueprint */}
            <div>
              <div className="flex justify-between text-xs font-semibold mb-1">
                <span className="text-slate-300">Concept Blueprint Fulfillment (30%)</span>
                <span className="text-blue-400">{dims.concept_blueprint}%</span>
              </div>
              <div className="w-full bg-slate-900 h-2.5 rounded-full overflow-hidden">
                <div className="bg-blue-500 h-full rounded-full transition-all duration-1000" style={{ width: `${dims.concept_blueprint}%` }} />
              </div>
            </div>

            {/* Algorithm Correctness */}
            <div>
              <div className="flex justify-between text-xs font-semibold mb-1">
                <span className="text-slate-300">Algorithm / Approach Correctness (25%)</span>
                <span className="text-purple-400">{dims.algorithm_correctness}%</span>
              </div>
              <div className="w-full bg-slate-900 h-2.5 rounded-full overflow-hidden">
                <div className="bg-purple-500 h-full rounded-full transition-all duration-1000" style={{ width: `${dims.algorithm_correctness}%` }} />
              </div>
            </div>

            {/* Reasoning */}
            <div>
              <div className="flex justify-between text-xs font-semibold mb-1">
                <span className="text-slate-300">Technical Reasoning (15%)</span>
                <span className="text-emerald-400">{dims.reasoning}%</span>
              </div>
              <div className="w-full bg-slate-900 h-2.5 rounded-full overflow-hidden">
                <div className="bg-emerald-500 h-full rounded-full transition-all duration-1000" style={{ width: `${dims.reasoning}%` }} />
              </div>
            </div>

            {/* Time Complexity */}
            <div>
              <div className="flex justify-between text-xs font-semibold mb-1">
                <span className="text-slate-300">Time Complexity Correctness (15%)</span>
                <span className="text-amber-400">{dims.time_complexity}%</span>
              </div>
              <div className="w-full bg-slate-900 h-2.5 rounded-full overflow-hidden">
                <div className="bg-amber-500 h-full rounded-full transition-all duration-1000" style={{ width: `${dims.time_complexity}%` }} />
              </div>
            </div>

            {/* Space Complexity */}
            <div>
              <div className="flex justify-between text-xs font-semibold mb-1">
                <span className="text-slate-300">Space Complexity Correctness (10%)</span>
                <span className="text-indigo-400">{dims.space_complexity}%</span>
              </div>
              <div className="w-full bg-slate-900 h-2.5 rounded-full overflow-hidden">
                <div className="bg-indigo-500 h-full rounded-full transition-all duration-1000" style={{ width: `${dims.space_complexity}%` }} />
              </div>
            </div>

            {/* Edge Cases */}
            <div>
              <div className="flex justify-between text-xs font-semibold mb-1">
                <span className="text-slate-300">Edge Case Handling (5%)</span>
                <span className="text-rose-400">{dims.edge_cases}%</span>
              </div>
              <div className="w-full bg-slate-900 h-2.5 rounded-full overflow-hidden">
                <div className="bg-rose-500 h-full rounded-full transition-all duration-1000" style={{ width: `${dims.edge_cases}%` }} />
              </div>
            </div>

          </div>

        </div>
      </div>

      {/* Two Column Grid: WHAT YOU UNDERSTAND vs WHAT TO IMPROVE */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        
        {/* Strengths */}
        <div className="glass-panel p-6 rounded-2xl border border-emerald-500/20 bg-emerald-950/5">
          <h3 className="text-base font-bold text-emerald-400 flex items-center gap-2 mb-4">
            <CheckCircle className="w-5 h-5" />
            WHAT YOU UNDERSTAND
          </h3>
          <ul className="space-y-2">
            {(evaluation.strengths && evaluation.strengths.length > 0 ? evaluation.strengths : ["Algorithm structure is solid"]).map((s, i) => (
              <li key={i} className="text-xs text-slate-200 flex items-start gap-2">
                <span className="text-emerald-400 font-bold">✓</span>
                <span>{s}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Improvements */}
        <div className="glass-panel p-6 rounded-2xl border border-amber-500/20 bg-amber-950/5">
          <h3 className="text-base font-bold text-amber-400 flex items-center gap-2 mb-4">
            <AlertTriangle className="w-5 h-5" />
            WHAT TO IMPROVE
          </h3>
          <ul className="space-y-2">
            {(evaluation.improvements && evaluation.improvements.length > 0 ? evaluation.improvements : ["Add explicit edge case descriptions"]).map((imp, i) => (
              <li key={i} className="text-xs text-slate-200 flex items-start gap-2">
                <span className="text-amber-400 font-bold">⚠</span>
                <span>{imp}</span>
              </li>
            ))}
          </ul>
        </div>

      </div>

      {/* AI Technical Feedback */}
      <div className="glass-panel p-6 sm:p-8 rounded-2xl border border-blue-500/20 bg-blue-950/10">
        <h3 className="text-base font-bold text-white flex items-center gap-2 mb-3">
          <Brain className="w-5 h-5 text-blue-400" />
          AI Technical Feedback
        </h3>
        <p className="text-sm text-slate-300 leading-relaxed font-sans">
          "{evaluation.technical_feedback}"
        </p>

        {/* Complexity Analysis Cards */}
        <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="bg-slate-900/80 p-4 rounded-xl border border-slate-800">
            <div className="flex items-center gap-2 text-xs font-bold text-amber-400 mb-1">
              <Clock className="w-4 h-4" />
              Time Complexity Evaluation
            </div>
            <p className="text-xs text-slate-300">Stated: <strong className="text-white">{evaluation.time_complexity?.student_answer}</strong> | Expected: <strong className="text-emerald-400">{evaluation.time_complexity?.expected}</strong></p>
          </div>

          <div className="bg-slate-900/80 p-4 rounded-xl border border-slate-800">
            <div className="flex items-center gap-2 text-xs font-bold text-indigo-400 mb-1">
              <HardDrive className="w-4 h-4" />
              Space Complexity Evaluation
            </div>
            <p className="text-xs text-slate-300">Stated: <strong className="text-white">{evaluation.space_complexity?.student_answer}</strong> | Expected: <strong className="text-emerald-400">{evaluation.space_complexity?.expected}</strong></p>
          </div>
        </div>
      </div>

      {/* Detailed Concept Blueprint Breakdown */}
      <div className="glass-panel p-6 sm:p-8 rounded-2xl">
        <h3 className="text-lg font-bold text-white mb-4">Granular Concept Blueprint Breakdown</h3>
        <ConceptBreakdownCard evaluations={evaluation.concept_evaluations || []} />
      </div>

      {/* Student Original Answer */}
      <div className="glass-panel p-6 rounded-2xl">
        <h3 className="text-sm font-bold text-slate-400 uppercase tracking-wider mb-2 flex items-center gap-2">
          <FileText className="w-4 h-4 text-blue-400" />
          Your Submitted Explanation
        </h3>
        <div className="bg-slate-900/90 p-4 rounded-xl text-xs text-slate-300 font-mono leading-relaxed whitespace-pre-line border border-slate-800">
          {submission.student_answer}
        </div>
      </div>

    </div>
  );
};
