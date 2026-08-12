from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, Depends
from app.core.db import db
from app.core.security import get_current_user
from app.models.question import QuestionSummary, QuestionDetail

router = APIRouter(prefix="/questions", tags=["Questions"])

@router.get("", response_model=List[dict])
def list_questions(
    category: Optional[str] = Query(None),
    difficulty: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    current_user: dict = Depends(get_current_user)
):
    questions = db.list_collection("questions")
    published = [q for q in questions if q.get("is_published", True)]
    
    if category:
        published = [q for q in published if q.get("category", "").lower() == category.lower()]
        
    if difficulty:
        published = [q for q in published if q.get("difficulty", "").lower() == difficulty.lower()]
        
    if search:
        search_lower = search.lower()
        published = [
            q for q in published 
            if search_lower in q.get("title", "").lower() or search_lower in q.get("problem_statement", "").lower()
        ]
        
    result = []
    for q in published:
        result.append({
            "id": q["id"],
            "title": q["title"],
            "category": q["category"],
            "difficulty": q["difficulty"],
            "created_at": q.get("created_at", "")
        })
    return result

@router.get("/categories", response_model=List[str])
def get_categories(current_user: dict = Depends(get_current_user)):
    questions = db.list_collection("questions")
    categories = set(q.get("category") for q in questions if q.get("category"))
    default_categories = [
        "Arrays", "Strings", "Hashing", "Two Pointers", "Sliding Window",
        "Binary Search", "Linked List", "Stack", "Queue", "Trees",
        "Binary Trees", "BST", "Heap", "Graphs", "BFS", "DFS",
        "Greedy", "Dynamic Programming", "Recursion", "Backtracking", "SQL"
    ]
    return sorted(list(categories.union(default_categories)))

@router.get("/{id}", response_model=dict)
def get_question_detail(id: str, current_user: dict = Depends(get_current_user)):
    question = db.get_document("questions", id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
        
    version_id = question.get("current_version_id")
    blueprint = None
    
    # Locate blueprint
    blueprints = db.list_collection("concept_blueprints")
    for bp in blueprints:
        if bp.get("question_version_id") == version_id:
            blueprint = bp
            break
            
    return {
        "id": question["id"],
        "title": question["title"],
        "category": question["category"],
        "difficulty": question["difficulty"],
        "problem_statement": question["problem_statement"],
        "examples": question.get("examples", []),
        "constraints": question.get("constraints", []),
        "hints": question.get("hints", []),
        "current_version_id": version_id,
        "blueprint": blueprint
    }
