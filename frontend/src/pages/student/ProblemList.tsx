import React, { useEffect, useState } from 'react';
import { api } from '../../services/api';
import { QuestionSummary } from '../../types';
import { DifficultyBadge, CategoryBadge } from '../../components/Badge';
import { Search, Filter, ArrowRight, Code } from 'lucide-react';

interface ProblemListProps {
  onSelectQuestion: (id: string) => void;
}

export const ProblemList: React.FC<ProblemListProps> = ({ onSelectQuestion }) => {
  const [questions, setQuestions] = useState<QuestionSummary[]>([]);
  const [categories, setCategories] = useState<string[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string>('');
  const [selectedDifficulty, setSelectedDifficulty] = useState<string>('');
  const [searchTerm, setSearchTerm] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      try {
        const [qRes, cRes] = await Promise.all([
          api.getQuestions(selectedCategory, selectedDifficulty, searchTerm),
          api.getCategories()
        ]);
        setQuestions(qRes);
        setCategories(cRes);
      } catch (e) {
        console.error("Failed loading questions", e);
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [selectedCategory, selectedDifficulty, searchTerm]);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-extrabold text-white flex items-center gap-2">
            <Code className="w-8 h-8 text-blue-500" />
            DSA Conceptual Problem Bank
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Explain your algorithmic logic, time complexity, and edge cases in plain English.
          </p>
        </div>

        {/* Filter Controls */}
        <div className="flex flex-wrap items-center gap-3">
          {/* Search */}
          <div className="relative">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              placeholder="Search problem title..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="bg-slate-900 border border-slate-800 rounded-xl pl-9 pr-4 py-2 text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:border-blue-500"
            />
          </div>

          {/* Difficulty Dropdown */}
          <select
            value={selectedDifficulty}
            onChange={(e) => setSelectedDifficulty(e.target.value)}
            className="bg-slate-900 border border-slate-800 rounded-xl px-3 py-2 text-sm text-slate-200 focus:outline-none focus:border-blue-500"
          >
            <option value="">All Difficulties</option>
            <option value="Easy">Easy</option>
            <option value="Medium">Medium</option>
            <option value="Hard">Hard</option>
          </select>
        </div>
      </div>

      {/* Category Filter Pills */}
      <div className="flex items-center gap-2 overflow-x-auto pb-2 scrollbar-none">
        <button
          onClick={() => setSelectedCategory('')}
          className={`px-3 py-1.5 rounded-full text-xs font-semibold whitespace-nowrap transition-all ${
            selectedCategory === ''
              ? 'bg-blue-600 text-white shadow-md shadow-blue-600/30'
              : 'bg-slate-900 text-slate-400 border border-slate-800 hover:text-white'
          }`}
        >
          All Categories
        </button>
        {categories.map((cat) => (
          <button
            key={cat}
            onClick={() => setSelectedCategory(cat)}
            className={`px-3 py-1.5 rounded-full text-xs font-semibold whitespace-nowrap transition-all ${
              selectedCategory === cat
                ? 'bg-blue-600 text-white shadow-md shadow-blue-600/30'
                : 'bg-slate-900 text-slate-400 border border-slate-800 hover:text-white'
            }`}
          >
            {cat}
          </button>
        ))}
      </div>

      {/* Question Table Grid */}
      {loading ? (
        <div className="flex items-center justify-center py-16">
          <div className="w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
        </div>
      ) : questions.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {questions.map((q) => (
            <div
              key={q.id}
              onClick={() => onSelectQuestion(q.id)}
              className="glass-panel glass-panel-hover p-5 rounded-2xl cursor-pointer flex flex-col justify-between group"
            >
              <div>
                <div className="flex items-center justify-between mb-3">
                  <CategoryBadge category={q.category} />
                  <DifficultyBadge difficulty={q.difficulty} />
                </div>
                <h3 className="font-bold text-white text-lg group-hover:text-blue-400 transition-colors">
                  {q.title}
                </h3>
              </div>

              <div className="mt-6 pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs font-bold text-blue-400">
                <span>Solve Conceptual Blueprint</span>
                <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="text-center py-16 glass-panel rounded-2xl">
          <Filter className="w-10 h-10 text-slate-500 mx-auto mb-3" />
          <h3 className="text-lg font-bold text-white">No questions match filters</h3>
          <p className="text-slate-400 text-sm mt-1">Try selecting a different category or search term.</p>
        </div>
      )}

    </div>
  );
};
