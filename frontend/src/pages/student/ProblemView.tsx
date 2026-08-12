import React, { useEffect, useState } from 'react';
import { api } from '../../services/api';
import { QuestionDetail } from '../../types';
import { DifficultyBadge, CategoryBadge } from '../../components/Badge';
import { ArrowLeft, Lightbulb, Send, CheckCircle2, ShieldCheck, Sparkles, AlertCircle } from 'lucide-react';

interface ProblemViewProps {
  questionId: string;
  onBack: () => void;
  onSubmitSuccess: (submissionId: string) => void;
}

export const ProblemView: React.FC<ProblemViewProps> = ({ questionId, onBack, onSubmitSuccess }) => {
  const [question, setQuestion] = useState<QuestionDetail | null>(null);
  const [studentAnswer, setStudentAnswer] = useState<string>('');
  const [visibleHintsCount, setVisibleHintsCount] = useState<number>(0);
  const [submitting, setSubmitting] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const load = async () => {
      try {
        const q = await api.getQuestionDetail(questionId);
        setQuestion(q);
      } catch (e) {
        console.error("Error loading question", e);
        setError("Failed loading question details");
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [questionId]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!studentAnswer.trim() || studentAnswer.length < 10) {
      setError("Please provide a detailed explanation (minimum 10 characters).");
      return;
    }

    setSubmitting(true);
    setError(null);

    try {
      const res = await api.submitAnswer(questionId, studentAnswer);
      onSubmitSuccess(res.submission_id);
    } catch (err: any) {
      console.error("Submission failed", err);
      setError(err.message || "Evaluation failed. Please try again.");
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="w-10 h-10 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  if (!question) {
    return (
      <div className="max-w-4xl mx-auto p-8 text-center glass-panel rounded-2xl my-10">
        <AlertCircle className="w-12 h-12 text-rose-400 mx-auto mb-3" />
        <h2 className="text-xl font-bold text-white">Question not found</h2>
        <button onClick={onBack} className="mt-4 px-4 py-2 bg-blue-600 text-white rounded-xl text-sm font-semibold">
          Back to Questions
        </button>
      </div>
    );
  }

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      
      {/* Top Bar / Navigation */}
      <button
        onClick={onBack}
        className="flex items-center gap-2 text-sm font-semibold text-slate-400 hover:text-white transition-colors"
      >
        <ArrowLeft className="w-4 h-4" />
        Back to Question Bank
      </button>

      {/* Main Problem Header */}
      <div className="glass-panel p-6 sm:p-8 rounded-2xl border border-slate-800">
        <div className="flex flex-wrap items-center gap-3 mb-3">
          <CategoryBadge category={question.category} />
          <DifficultyBadge difficulty={question.difficulty} />
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-white">{question.title}</h1>

        {/* Problem Statement */}
        <div className="mt-6 text-slate-300 leading-relaxed text-sm sm:text-base whitespace-pre-line bg-slate-900/60 p-5 rounded-xl border border-slate-800">
          {question.problem_statement}
        </div>

        {/* Examples */}
        {question.examples && question.examples.length > 0 && (
          <div className="mt-6 space-y-4">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400">Examples</h3>
            {question.examples.map((ex, idx) => (
              <div key={idx} className="bg-slate-900/80 p-4 rounded-xl border border-slate-800 text-xs font-mono">
                <p className="text-blue-400"><strong className="text-slate-400">Input:</strong> {ex.input}</p>
                <p className="text-emerald-400 mt-1"><strong className="text-slate-400">Output:</strong> {ex.output}</p>
                {ex.explanation && (
                  <p className="text-slate-400 mt-1 font-sans"><strong className="text-slate-400 font-mono">Explanation:</strong> {ex.explanation}</p>
                )}
              </div>
            ))}
          </div>
        )}

        {/* Constraints */}
        {question.constraints && question.constraints.length > 0 && (
          <div className="mt-6">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">Constraints</h3>
            <ul className="list-disc list-inside text-xs text-slate-400 space-y-1 font-mono">
              {question.constraints.map((c, i) => (
                <li key={i}>{c}</li>
              ))}
            </ul>
          </div>
        )}

        {/* Progressive Hint System */}
        {question.hints && question.hints.length > 0 && (
          <div className="mt-6 pt-6 border-t border-slate-800/80">
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-xs font-bold uppercase tracking-wider text-amber-400 flex items-center gap-1.5">
                <Lightbulb className="w-4 h-4" />
                Progressive Hint System
              </h3>
              {visibleHintsCount < question.hints.length && (
                <button
                  type="button"
                  onClick={() => setVisibleHintsCount(prev => prev + 1)}
                  className="text-xs font-semibold text-amber-400 hover:text-amber-300 underline"
                >
                  Show Hint {visibleHintsCount + 1}
                </button>
              )}
            </div>

            <div className="space-y-2">
              {question.hints.slice(0, visibleHintsCount).map((hint, idx) => (
                <div key={idx} className="bg-amber-500/10 border border-amber-500/20 p-3 rounded-xl text-xs text-amber-300 animate-fadeIn">
                  <strong>Hint {idx + 1}:</strong> {hint}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Answer Submission Form */}
      <form onSubmit={handleSubmit} className="glass-panel p-6 sm:p-8 rounded-2xl space-y-6">
        <div>
          <div className="flex items-center justify-between mb-2">
            <label className="block text-base font-bold text-white">
              Explain How You Would Solve This Problem
            </label>
            <span className="text-xs text-slate-400 font-medium">Natural English Answer</span>
          </div>

          {/* Core Product Guarantee Notice */}
          <div className="mb-4 bg-blue-950/30 border border-blue-500/20 p-3.5 rounded-xl flex items-start gap-3">
            <ShieldCheck className="w-5 h-5 text-blue-400 shrink-0 mt-0.5" />
            <p className="text-xs text-blue-300 leading-relaxed">
              <strong>Technical Assessment Guarantee:</strong> Your answer is evaluated on conceptual algorithm correctness, data structure choices, complexity, and edge cases. <strong>Imperfect English grammar, typos, accent-based phrasing, or style will NOT penalize your score.</strong>
            </p>
          </div>

          <textarea
            rows={8}
            value={studentAnswer}
            onChange={(e) => setStudentAnswer(e.target.value)}
            placeholder="Describe your step-by-step algorithmic approach in plain English. For example:
- What data structures will you use?
- How will you iterate or divide the problem space?
- What are the time and space complexities?
- What edge cases will you handle?"
            className="w-full bg-slate-900 border border-slate-700 rounded-xl p-4 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all font-mono leading-relaxed"
          />
        </div>

        {error && (
          <div className="p-4 bg-rose-500/10 border border-rose-500/20 rounded-xl text-rose-400 text-xs font-semibold flex items-center gap-2">
            <AlertCircle className="w-4 h-4 shrink-0" />
            {error}
          </div>
        )}

        <div className="flex items-center justify-between pt-2">
          <p className="text-xs text-slate-500">
            Submission triggers Gemini AI Evaluation &amp; Backend Deterministic Scoring Engine.
          </p>

          <button
            type="submit"
            disabled={submitting || studentAnswer.length < 10}
            className="px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 text-white font-bold text-sm rounded-xl shadow-lg shadow-blue-500/20 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2 transition-all transform active:scale-95"
          >
            {submitting ? (
              <>
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                <span>Evaluating Concepts...</span>
              </>
            ) : (
              <>
                <Send className="w-4 h-4" />
                <span>Submit Concept Answer</span>
              </>
            )}
          </button>
        </div>
      </form>

    </div>
  );
};
