import pytest
from app.services.interview_engine import InterviewEngine
from app.services.interview_evaluator import InterviewEvaluator
from app.services.resume_analyzer import ResumeAnalyzer

def test_resume_parser_fallback():
    sample_text = "Experience with Python, FastAPI, PostgreSQL, RAG systems, and Qdrant vector database."
    result = ResumeAnalyzer._rule_based_fallback_extraction(sample_text)
    
    assert "Python" in result.skills
    assert "FastAPI" in result.skills
    assert "PostgreSQL" in result.skills
    assert len(result.projects) > 0

def test_question_deduplication_detection():
    past_questions = [
        "What is hybrid search?",
        "Explain how B-tree indexes work in DBMS."
    ]
    # Exact duplicate
    assert InterviewEngine.is_duplicate_question("What is hybrid search?", past_questions) == True
    # Semantically close / word overlap duplicate
    assert InterviewEngine.is_duplicate_question("What is hybrid search in RAG?", past_questions) == True
    # Completely distinct question
    assert InterviewEngine.is_duplicate_question("How does garbage collection work in Python?", past_questions) == False

def test_deterministic_question_scoring():
    dims = {
        "technical_correctness": 1.0,
        "concept_understanding": 1.0,
        "reasoning": 1.0,
        "completeness": 1.0,
        "practical_understanding": 1.0
    }
    score = InterviewEvaluator.calculate_question_score(dims)
    assert score == 100.0

def test_study_recommendation_generation():
    topic_scores = {
        "Python": 92.0,
        "RAG": 88.0,
        "DBMS Indexing": 45.0,
        "System Design": 55.0
    }
    recs = InterviewEvaluator.generate_exact_study_recommendations(topic_scores)
    assert len(recs) == 2
    weak_topics = [r.topic for r in recs]
    assert "DBMS Indexing" in weak_topics
    assert "System Design" in weak_topics
    assert len(recs[0].exact_concepts) == 5
