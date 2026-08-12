import React, { useState } from 'react';
import { api } from '../services/api';
import { ResumeData } from '../types';
import { Upload, FileText, CheckCircle2, AlertCircle, X, Sparkles } from 'lucide-react';

interface ResumeUploadModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: (resume: ResumeData) => void;
}

export const ResumeUploadModal: React.FC<ResumeUploadModalProps> = ({ isOpen, onClose, onSuccess }) => {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  if (!isOpen) return null;

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const selected = e.target.files[0];
      if (!selected.name.toLowerCase().endsWith('.pdf')) {
        setError('Only PDF resumes are supported.');
        return;
      }
      setFile(selected);
      setError(null);
    }
  };

  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;

    setUploading(true);
    setError(null);

    try {
      const data = await api.uploadResume(file);
      onSuccess(data);
      onClose();
    } catch (err: any) {
      console.error(err);
      setError(err.message || 'Failed analyzing resume.');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md">
      <div className="w-full max-w-lg glass-panel p-6 sm:p-8 rounded-3xl border border-slate-800 shadow-2xl relative">
        
        <button
          onClick={onClose}
          className="absolute top-4 right-4 p-2 text-slate-400 hover:text-white rounded-full hover:bg-slate-800/60 transition-colors"
        >
          <X className="w-5 h-5" />
        </button>

        <div className="text-center mb-6">
          <div className="w-12 h-12 rounded-2xl bg-gradient-to-tr from-blue-600 to-purple-600 flex items-center justify-center mx-auto mb-3 shadow-lg shadow-purple-500/20">
            <FileText className="w-6 h-6 text-white" />
          </div>
          <h2 className="text-2xl font-extrabold text-white">Upload Your Resume</h2>
          <p className="text-xs text-slate-400 mt-1">
            AI will analyze your skills and projects to build a personalized voice technical interview.
          </p>
        </div>

        <form onSubmit={handleUpload} className="space-y-6">
          
          <div className="border-2 border-dashed border-slate-700 hover:border-purple-500/50 rounded-2xl p-6 text-center transition-colors cursor-pointer relative bg-slate-900/50">
            <input
              type="file"
              accept=".pdf"
              onChange={handleFileChange}
              className="absolute inset-0 opacity-0 cursor-pointer w-full h-full"
            />
            <Upload className="w-8 h-8 text-purple-400 mx-auto mb-2" />
            {file ? (
              <div className="text-sm font-bold text-emerald-400 flex items-center justify-center gap-1.5">
                <CheckCircle2 className="w-4 h-4" />
                {file.name}
              </div>
            ) : (
              <div>
                <p className="text-sm font-bold text-white">Click or drag &amp; drop PDF resume</p>
                <p className="text-xs text-slate-500 mt-1">Maximum size 10MB (.pdf)</p>
              </div>
            )}
          </div>

          {error && (
            <div className="p-3 bg-rose-500/10 border border-rose-500/20 rounded-xl text-rose-400 text-xs font-semibold flex items-center gap-2">
              <AlertCircle className="w-4 h-4 shrink-0" />
              {error}
            </div>
          )}

          <div className="flex justify-end gap-3 pt-2">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-sm font-semibold text-slate-400 hover:text-white"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={!file || uploading}
              className="px-6 py-2.5 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 text-white font-bold text-sm rounded-xl shadow-lg shadow-purple-500/20 disabled:opacity-50 flex items-center gap-2"
            >
              {uploading ? (
                <>
                  <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  <span>Analyzing Resume Skills...</span>
                </>
              ) : (
                <>
                  <Sparkles className="w-4 h-4" />
                  <span>Analyze &amp; Extract Topics</span>
                </>
              )}
            </button>
          </div>

        </form>

      </div>
    </div>
  );
};
