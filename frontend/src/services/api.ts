import { 
  User, 
  QuestionSummary, 
  QuestionDetail, 
  StudentDashboardData, 
  FullEvaluationResult,
  SubmissionRecord,
  ResumeData,
  InterviewStartData,
  InterviewQuestionData,
  InterviewReportData,
  UserInterviewLimit
} from '../types';

const API_BASE = import.meta.env.VITE_API_BASE_URL || '/api/v1';

class ApiService {
  private token: string | null = localStorage.getItem('algo_token');

  setToken(token: string | null) {
    this.token = token;
    if (token) {
      localStorage.setItem('algo_token', token);
    } else {
      localStorage.removeItem('algo_token');
    }
  }

  getToken(): string | null {
    return this.token || localStorage.getItem('algo_token');
  }

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const token = this.getToken();
    const headers: Record<string, string> = {
      ...(options.headers as Record<string, string> || {}),
    };

    // Auto set Content-Type unless FormData is used for file upload
    if (!(options.body instanceof FormData) && !headers['Content-Type']) {
      headers['Content-Type'] = 'application/json';
    }

    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const res = await fetch(`${API_BASE}${endpoint}`, {
      ...options,
      headers
    });

    if (!res.ok) {
      const errorData = await res.json().catch(() => ({ detail: 'Network response was not ok' }));
      throw new Error(errorData.detail || `HTTP Error ${res.status}`);
    }

    return res.json();
  }

  // --- AUTH ---
  async login(email: string, password: string) {
    const data = await this.request<{ access_token: string; user: User }>('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password })
    });
    this.setToken(data.access_token);
    return data;
  }

  async register(email: string, password: string, display_name: string, role: string = 'USER') {
    const data = await this.request<{ access_token: string; user: User }>('/auth/register', {
      method: 'POST',
      body: JSON.stringify({ email, password, display_name, role })
    });
    this.setToken(data.access_token);
    return data;
  }

  async getMe() {
    return this.request<User>('/auth/me');
  }

  logout() {
    this.setToken(null);
  }

  // --- QUESTIONS ---
  async getQuestions(category?: string, difficulty?: string, search?: string) {
    const params = new URLSearchParams();
    if (category) params.append('category', category);
    if (difficulty) params.append('difficulty', difficulty);
    if (search) params.append('search', search);
    
    const query = params.toString() ? `?${params.toString()}` : '';
    return this.request<QuestionSummary[]>(`/questions${query}`);
  }

  async getCategories() {
    return this.request<string[]>('/questions/categories');
  }

  async getQuestionDetail(id: string) {
    return this.request<QuestionDetail>(`/questions/${id}`);
  }

  // --- SUBMISSIONS & EVALUATION ---
  async submitAnswer(questionId: string, studentAnswer: string) {
    return this.request<{ submission_id: string; evaluation_id: string; final_score: number; evaluation: FullEvaluationResult }>(
      `/submissions/question/${questionId}`,
      {
        method: 'POST',
        body: JSON.stringify({ student_answer: studentAnswer })
      }
    );
  }

  async getSubmissionResult(id: string) {
    return this.request<{ submission: SubmissionRecord; evaluation: FullEvaluationResult; question: QuestionDetail }>(
      `/submissions/${id}`
    );
  }

  async getUserSubmissions() {
    return this.request<SubmissionRecord[]>('/submissions');
  }

  // --- STUDENT DASHBOARD ---
  async getStudentDashboard() {
    return this.request<StudentDashboardData>('/users/me/dashboard');
  }

  // --- RESUME API ---
  async uploadResume(file: File) {
    const formData = new FormData();
    formData.append('file', file);
    return this.request<ResumeData>('/resumes/upload', {
      method: 'POST',
      body: formData
    });
  }

  async getLatestResume() {
    return this.request<ResumeData>('/resumes/latest');
  }

  // --- AI VOICE TECHNICAL INTERVIEW API ---
  async startInterview() {
    return this.request<InterviewStartData>('/interviews/start', {
      method: 'POST'
    });
  }

  async getNextQuestion(interviewId: string) {
    return this.request<InterviewQuestionData>(`/interviews/${interviewId}/next-question`);
  }

  async submitInterviewAnswer(interviewId: string, answer: string) {
    return this.request<any>(`/interviews/${interviewId}/submit-answer`, {
      method: 'POST',
      body: JSON.stringify({ student_answer: answer })
    });
  }

  async finishInterview(interviewId: string) {
    return this.request<any>(`/interviews/${interviewId}/finish`, {
      method: 'POST'
    });
  }

  async getInterviewReport(interviewId: string) {
    return this.request<InterviewReportData>(`/interviews/${interviewId}/report`);
  }

  async getInterviewHistory() {
    return this.request<any[]>('/interviews/history');
  }

  // --- ADMIN PORTAL ---
  async getAdminOverview() {
    return this.request<any>('/admin/overview');
  }

  async createQuestion(questionData: any) {
    return this.request<any>('/admin/questions', {
      method: 'POST',
      body: JSON.stringify(questionData)
    });
  }

  async updateQuestion(id: string, questionData: any) {
    return this.request<any>(`/admin/questions/${id}`, {
      method: 'PUT',
      body: JSON.stringify(questionData)
    });
  }

  async archiveQuestion(id: string) {
    return this.request<any>(`/admin/questions/${id}`, {
      method: 'DELETE'
    });
  }

  async getAdminUsers() {
    return this.request<any[]>('/admin/users');
  }

  async toggleUserStatus(uid: string, isDisabled: boolean) {
    return this.request<any>(`/admin/users/${uid}/status?is_disabled=${isDisabled}`, {
      method: 'PUT'
    });
  }

  async updateUserRole(uid: string, newRole: string) {
    return this.request<any>(`/admin/users/${uid}/role?new_role=${newRole}`, {
      method: 'PUT'
    });
  }

  async deleteUser(uid: string) {
    return this.request<any>(`/admin/users/${uid}`, {
      method: 'DELETE'
    });
  }

  async getAIUsage() {
    return this.request<any>('/admin/ai-usage');
  }

  async getBenchmarks() {
    return this.request<any>('/admin/benchmarks');
  }

  async addBenchmark(submission_id: string, human_score: number, notes: string) {
    return this.request<any>('/admin/benchmarks', {
      method: 'POST',
      body: JSON.stringify({ submission_id, human_score, notes })
    });
  }

  // --- ADMIN INTERVIEW CONTROLS ---
  async getAdminInterviewAnalytics() {
    return this.request<any>('/admin/interviews/analytics');
  }

  async getAdminInterviewLimits() {
    return this.request<UserInterviewLimit[]>('/admin/interviews/limits');
  }

  async updateUserInterviewLimit(uid: string, allowed: number, isUnlimited: boolean, isDisabled: boolean) {
    return this.request<any>(`/admin/interviews/limits/${uid}?allowed_interviews=${allowed}&is_unlimited=${isUnlimited}&is_disabled=${isDisabled}`, {
      method: 'PUT'
    });
  }

  async resetUserInterviewAttempts(uid: string) {
    return this.request<any>(`/admin/interviews/limits/${uid}/reset`, {
      method: 'POST'
    });
  }
}

export const api = new ApiService();
