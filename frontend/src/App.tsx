import React, { useState } from 'react';
import { AuthProvider, useAuth } from './context/AuthContext';
import { Navbar } from './components/Navbar';
import { StudentDashboard } from './pages/student/StudentDashboard';
import { ProblemList } from './pages/student/ProblemList';
import { ProblemView } from './pages/student/ProblemView';
import { ResultView } from './pages/student/ResultView';
import { VoiceInterviewView } from './pages/student/VoiceInterviewView';
import { InterviewReportView } from './pages/student/InterviewReportView';
import { AdminDashboard } from './pages/admin/AdminDashboard';
import { AdminQuestionEditor } from './pages/admin/AdminQuestionEditor';
import { AdminUsers } from './pages/admin/AdminUsers';
import { AdminAIUsage } from './pages/admin/AdminAIUsage';
import { AdminBenchmarks } from './pages/admin/AdminBenchmarks';
import { AdminInterviewConfig } from './pages/admin/AdminInterviewConfig';
import { Login } from './pages/Login';

const MainContent: React.FC = () => {
  const { user, loading } = useAuth();
  const [activeTab, setActiveTab] = useState<string>('dashboard');
  const [selectedQuestionId, setSelectedQuestionId] = useState<string | null>(null);
  const [selectedSubmissionId, setSelectedSubmissionId] = useState<string | null>(null);
  const [activeInterviewId, setActiveInterviewId] = useState<string | null>(null);

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="flex flex-col items-center gap-3">
          <div className="w-10 h-10 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
          <p className="text-sm text-slate-400 font-medium">Restoring session...</p>
        </div>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="min-h-screen bg-slate-950">
        <Navbar activeTab="login" setActiveTab={() => {}} />
        <Login onSuccess={() => setActiveTab('dashboard')} />
      </div>
    );
  }

  const handleSelectQuestion = (qId: string) => {
    setSelectedQuestionId(qId);
    setActiveTab(`problem-${qId}`);
  };

  const handleViewResult = (subId: string) => {
    setSelectedSubmissionId(subId);
    setActiveTab(`result-${subId}`);
  };

  const handleStartVoiceInterview = (interviewId: string) => {
    setActiveInterviewId(interviewId);
    setActiveTab('voice-interview');
  };

  const handleViewInterviewReport = (interviewId: string) => {
    setActiveInterviewId(interviewId);
    setActiveTab('interview-report');
  };

  return (
    <div className="min-h-screen bg-slate-950 flex flex-col selection:bg-blue-500 selection:text-white">
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} />
      
      <main className="flex-1">
        {activeTab === 'dashboard' && (
          <StudentDashboard
            onSelectQuestion={handleSelectQuestion}
            onViewResult={handleViewResult}
            onStartVoiceInterview={handleStartVoiceInterview}
            onViewInterviewReport={handleViewInterviewReport}
          />
        )}

        {activeTab === 'problems' && (
          <ProblemList onSelectQuestion={handleSelectQuestion} />
        )}

        {activeTab === 'voice-interview' && activeInterviewId && (
          <VoiceInterviewView
            interviewId={activeInterviewId}
            onFinish={() => setActiveTab('interview-report')}
          />
        )}

        {activeTab === 'interview-report' && activeInterviewId && (
          <InterviewReportView
            interviewId={activeInterviewId}
            onBack={() => setActiveTab('dashboard')}
          />
        )}

        {activeTab.startsWith('problem-') && selectedQuestionId && (
          <ProblemView
            questionId={selectedQuestionId}
            onBack={() => setActiveTab('problems')}
            onSubmitSuccess={(subId) => {
              setSelectedSubmissionId(subId);
              setActiveTab(`result-${subId}`);
            }}
          />
        )}

        {activeTab.startsWith('result-') && selectedSubmissionId && (
          <ResultView
            submissionId={selectedSubmissionId}
            onBackToDashboard={() => setActiveTab('dashboard')}
            onSelectQuestion={handleSelectQuestion}
          />
        )}

        {/* ADMIN PORTAL TAB VIEWS */}
        {activeTab === 'admin-dashboard' && (
          <AdminDashboard onNavigate={(tab) => setActiveTab(tab)} />
        )}

        {activeTab === 'admin-question-editor' && (
          <AdminQuestionEditor onBack={() => setActiveTab('admin-dashboard')} />
        )}

        {activeTab === 'admin-users' && (
          <AdminUsers onBack={() => setActiveTab('admin-dashboard')} />
        )}

        {activeTab === 'admin-interview-config' && (
          <AdminInterviewConfig onBack={() => setActiveTab('admin-dashboard')} />
        )}

        {activeTab === 'admin-ai-usage' && (
          <AdminAIUsage onBack={() => setActiveTab('admin-dashboard')} />
        )}

        {activeTab === 'admin-benchmarks' && (
          <AdminBenchmarks onBack={() => setActiveTab('admin-dashboard')} />
        )}
      </main>
    </div>
  );
};

export default function App() {
  return (
    <AuthProvider>
      <MainContent />
    </AuthProvider>
  );
}
