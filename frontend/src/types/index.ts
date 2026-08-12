export type Role = 'USER' | 'ADMIN';

export interface User {
  uid: string;
  email: string;
  display_name: string;
  role: Role;
  streak_count?: number;
  metrics?: {
    total_attempted: number;
    total_completed: number;
    average_score: number;
    topic_scores: Record<string, number>;
  };
}

export interface ConceptItem {
  concept_id: string;
  concept_name: string;
  description: string;
  importance: 'high' | 'medium' | 'low';
  weight: number;
  is_mandatory: boolean;
  expected_keywords?: string[];
}

export interface ConceptBlueprint {
  id: string;
  question_version_id: string;
  concepts: ConceptItem[];
  expected_time_complexity: string;
  expected_space_complexity: string;
  expected_edge_cases: string[];
}

export interface ExampleCase {
  input: string;
  output: string;
  explanation?: string;
}

export interface QuestionSummary {
  id: string;
  title: string;
  category: string;
  difficulty: 'Easy' | 'Medium' | 'Hard';
  created_at: string;
}

export interface QuestionDetail extends QuestionSummary {
  problem_statement: string;
  examples: ExampleCase[];
  constraints: string[];
  hints: string[];
  current_version_id: string;
  blueprint?: ConceptBlueprint;
}

export interface ConceptStatusEvaluation {
  concept_id: string;
  status: 'correct' | 'partial' | 'incorrect';
  score: number;
  evidence: string;
  feedback?: string;
}

export interface ComplexityEvaluation {
  student_answer: string;
  expected: string;
  score: number;
  feedback?: string;
}

export interface FullEvaluationResult {
  id: string;
  submission_id: string;
  user_id: string;
  question_id: string;
  final_score: number;
  blueprint_score: number;
  dimension_scores: {
    concept_blueprint: number;
    algorithm_correctness: number;
    reasoning: number;
    time_complexity: number;
    space_complexity: number;
    edge_cases: number;
  };
  concept_evaluations: ConceptStatusEvaluation[];
  algorithm_correctness: number;
  reasoning: number;
  time_complexity: ComplexityEvaluation;
  space_complexity: ComplexityEvaluation;
  edge_cases: number;
  technical_feedback: string;
  misconceptions: string[];
  strengths: string[];
  improvements: string[];
  evaluated_at: string;
}

export interface SubmissionRecord {
  id: string;
  user_id: string;
  question_id: string;
  question_title: string;
  student_answer?: string;
  final_score: number;
  status: string;
  created_at: string;
}

export interface StudentDashboardData {
  user_info: {
    uid: string;
    display_name: string;
    email: string;
    streak_count: number;
  };
  stats: {
    total_attempted: number;
    total_completed: number;
    average_concept_score: number;
    current_streak: number;
  };
  topic_performance: Record<string, number>;
  weak_topics: { category: string; score: number }[];
  strong_topics: { category: string; score: number }[];
  recommended_questions: { id: string; title: string; category: string; difficulty: string }[];
  recent_submissions: SubmissionRecord[];
}

// --- AI VOICE TECHNICAL INTERVIEW TYPES ---

export interface ResumeData {
  id: string;
  user_id: string;
  filename: string;
  skills: string[];
  languages?: string[];
  frameworks?: string[];
  databases?: string[];
  cloud?: string[];
  projects: { name: string; technologies: string[]; topics: string[] }[];
  compact_context: string;
  created_at: string;
}

export interface InterviewStartData {
  interview_id: string;
  allowed_interviews: number;
  used_interviews: number;
  remaining_interviews: number;
  resume_topics: string[];
}

export interface InterviewQuestionData {
  question_id: string;
  question_number: number;
  question_text: string;
  topic: string;
  difficulty: string;
  question_type: string;
}

export interface StudyRecommendation {
  topic: string;
  score: number;
  exact_concepts: string[];
}

export interface InterviewReportData {
  interview: {
    id: string;
    user_id: string;
    overall_score: number;
    topic_scores: Record<string, number>;
    strong_areas: string[];
    weak_areas: string[];
    study_recommendations: StudyRecommendation[];
    completed_at: string;
  };
  questions: {
    id: string;
    question_number: number;
    question_text: string;
    topic: string;
    difficulty: string;
    question_type: string;
    student_answer_raw: string;
    eval_score: number;
  }[];
  history_progress: { interview_id: string; score: number; date: string }[];
}

export interface UserInterviewLimit {
  user_id: string;
  display_name: string;
  email: string;
  allowed_interviews: number;
  used_interviews: number;
  is_unlimited: boolean;
  is_disabled: boolean;
  updated_at: string;
}
