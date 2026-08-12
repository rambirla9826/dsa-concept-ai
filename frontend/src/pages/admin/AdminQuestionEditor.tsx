import React, { useState } from 'react';
import { api } from '../../services/api';
import { ConceptItem } from '../../types';
import { Plus, Trash2, Save, ArrowLeft, CheckCircle2 } from 'lucide-react';

interface AdminQuestionEditorProps {
  onBack: () => void;
}

export const AdminQuestionEditor: React.FC<AdminQuestionEditorProps> = ({ onBack }) => {
  const [title, setTitle] = useState('');
  const [category, setCategory] = useState('Arrays');
  const [difficulty, setDifficulty] = useState('Medium');
  const [problemStatement, setProblemStatement] = useState('');
  const [expectedTime, setExpectedTime] = useState('O(n)');
  const [expectedSpace, setExpectedSpace] = useState('O(1)');
  const [constraintsText, setConstraintsText] = useState('1 <= N <= 10^5');
  const [hintsText, setHintsText] = useState('Think about using two pointers');
  
  // Concept Blueprint items
  const [concepts, setConcepts] = useState<ConceptItem[]>([
    {
      concept_id: 'C1',
      concept_name: 'Core Data Structure Selection',
      description: 'Student identifies appropriate data structure (e.g. HashMap or Array)',
      importance: 'high',
      weight: 40,
      is_mandatory: true,
      expected_keywords: ['hashmap', 'array']
    },
    {
      concept_id: 'C2',
      concept_name: 'Single Pass Traversal',
      description: 'Student explains iterating elements in linear time',
      importance: 'high',
      weight: 60,
      is_mandatory: true,
      expected_keywords: ['single pass', 'loop']
    }
  ]);

  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState<string | null>(null);

  const addConcept = () => {
    const nextId = `C${concepts.length + 1}`;
    setConcepts([
      ...concepts,
      {
        concept_id: nextId,
        concept_name: '',
        description: '',
        importance: 'medium',
        weight: 20,
        is_mandatory: true,
        expected_keywords: []
      }
    ]);
  };

  const removeConcept = (index: number) => {
    setConcepts(concepts.filter((_, i) => i !== index));
  };

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setMessage(null);

    const payload = {
      title,
      category,
      difficulty,
      problem_statement: problemStatement,
      examples: [{ input: 'Sample Input', output: 'Sample Output', explanation: 'Sample Explanation' }],
      constraints: constraintsText.split('\n').filter(c => c.trim()),
      hints: hintsText.split('\n').filter(h => h.trim()),
      concepts,
      expected_time_complexity: expectedTime,
      expected_space_complexity: expectedSpace,
      expected_edge_cases: ['Empty array', 'Single element']
    };

    try {
      await api.createQuestion(payload);
      setMessage("Question and Concept Blueprint published successfully!");
      setTimeout(() => onBack(), 1500);
    } catch (err: any) {
      console.error(err);
      setMessage(`Error: ${err.message || 'Save failed'}`);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      
      <button onClick={onBack} className="flex items-center gap-2 text-sm font-semibold text-slate-400 hover:text-white">
        <ArrowLeft className="w-4 h-4" /> Back to Admin Overview
      </button>

      <div className="glass-panel p-6 sm:p-8 rounded-2xl">
        <h1 className="text-2xl font-extrabold text-white mb-6">Create New DSA Question &amp; Concept Blueprint</h1>

        <form onSubmit={handleSave} className="space-y-6">
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-xs font-bold text-slate-300 uppercase mb-1">Question Title</label>
              <input
                type="text"
                required
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="e.g. Detect Cycle in Graph"
                className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-sm text-white focus:border-purple-500 focus:outline-none"
              />
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-300 uppercase mb-1">Category</label>
              <select
                value={category}
                onChange={(e) => setCategory(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-sm text-white focus:border-purple-500 focus:outline-none"
              >
                {['Arrays', 'Strings', 'Hashing', 'Binary Search', 'Linked List', 'Trees', 'Graphs', 'Greedy', 'Dynamic Programming', 'SQL'].map(cat => (
                  <option key={cat} value={cat}>{cat}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-300 uppercase mb-1">Difficulty</label>
              <select
                value={difficulty}
                onChange={(e) => setDifficulty(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-sm text-white focus:border-purple-500 focus:outline-none"
              >
                <option value="Easy">Easy</option>
                <option value="Medium">Medium</option>
                <option value="Hard">Hard</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block text-xs font-bold text-slate-300 uppercase mb-1">Problem Statement</label>
            <textarea
              rows={4}
              required
              value={problemStatement}
              onChange={(e) => setProblemStatement(e.target.value)}
              placeholder="Full problem text..."
              className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-sm text-white focus:border-purple-500 focus:outline-none"
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-bold text-slate-300 uppercase mb-1">Optimal Time Complexity</label>
              <input
                type="text"
                value={expectedTime}
                onChange={(e) => setExpectedTime(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-sm text-white"
              />
            </div>
            <div>
              <label className="block text-xs font-bold text-slate-300 uppercase mb-1">Optimal Space Complexity</label>
              <input
                type="text"
                value={expectedSpace}
                onChange={(e) => setExpectedSpace(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-sm text-white"
              />
            </div>
          </div>

          {/* CONCEPT BLUEPRINT EDITOR SECTION */}
          <div className="pt-6 border-t border-slate-800">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="text-lg font-bold text-purple-400">Admin-Defined Concept Blueprint</h3>
                <p className="text-xs text-slate-400">Define the granular concepts student explanations must hit.</p>
              </div>
              <button
                type="button"
                onClick={addConcept}
                className="px-3 py-1.5 bg-purple-600/20 text-purple-300 border border-purple-500/30 rounded-xl text-xs font-semibold flex items-center gap-1.5 hover:bg-purple-600/30"
              >
                <Plus className="w-4 h-4" /> Add Concept Item
              </button>
            </div>

            <div className="space-y-4">
              {concepts.map((c, idx) => (
                <div key={idx} className="bg-slate-900/80 p-4 rounded-xl border border-slate-800 space-y-3">
                  <div className="flex items-center justify-between gap-3">
                    <span className="font-bold text-purple-400 text-sm">{c.concept_id}</span>
                    <button
                      type="button"
                      onClick={() => removeConcept(idx)}
                      className="text-slate-500 hover:text-rose-400 p-1"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                    <input
                      type="text"
                      placeholder="Concept Name (e.g. Two Pointers)"
                      value={c.concept_name}
                      onChange={(e) => {
                        const updated = [...concepts];
                        updated[idx].concept_name = e.target.value;
                        setConcepts(updated);
                      }}
                      className="bg-slate-950 border border-slate-800 rounded-lg p-2 text-xs text-white"
                    />

                    <input
                      type="text"
                      placeholder="Description"
                      value={c.description}
                      onChange={(e) => {
                        const updated = [...concepts];
                        updated[idx].description = e.target.value;
                        setConcepts(updated);
                      }}
                      className="bg-slate-950 border border-slate-800 rounded-lg p-2 text-xs text-white"
                    />

                    <input
                      type="number"
                      placeholder="Scoring Weight %"
                      value={c.weight}
                      onChange={(e) => {
                        const updated = [...concepts];
                        updated[idx].weight = parseFloat(e.target.value) || 10;
                        setConcepts(updated);
                      }}
                      className="bg-slate-950 border border-slate-800 rounded-lg p-2 text-xs text-white"
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>

          {message && (
            <div className="p-4 rounded-xl bg-purple-500/10 border border-purple-500/20 text-purple-300 text-xs font-bold flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4" />
              {message}
            </div>
          )}

          <div className="pt-4 flex justify-end">
            <button
              type="submit"
              disabled={saving}
              className="px-6 py-3 bg-purple-600 hover:bg-purple-500 text-white font-bold text-sm rounded-xl flex items-center gap-2"
            >
              <Save className="w-4 h-4" />
              {saving ? 'Publishing...' : 'Publish Question & Blueprint'}
            </button>
          </div>

        </form>
      </div>

    </div>
  );
};
