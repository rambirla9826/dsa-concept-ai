from datetime import datetime, timezone
from app.core.db import db
from app.core.security import hash_password
from app.seed.questions_data import SEED_QUESTIONS

def seed_database():
    """
    Populates database with 20 seed questions, version entries, concept blueprints,
    and a single master admin account. All temporary test/demo student accounts are removed.
    """
    print("[Seed] Initializing clean production database...")
    
    # 1. Create Master Admin User
    admin_user = {
        "uid": "admin_master_001",
        "email": "admin@algoconcept.ai",
        "password": hash_password("AdminPass123!"),
        "display_name": "Master Admin",
        "role": "ADMIN",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "last_login": datetime.now(timezone.utc).isoformat(),
        "streak_count": 1,
        "is_disabled": False,
        "metrics": {"total_attempted": 0, "total_completed": 0, "average_score": 0.0, "topic_scores": {}}
    }
    db.set_document("users", "admin_master_001", admin_user)

    # 2. Seed Questions & Concept Blueprints
    for q in SEED_QUESTIONS:
        q_id = q["id"]
        v_id = f"{q_id}_v1"
        b_id = f"{q_id}_bp1"

        # Question Record
        q_doc = {
            "id": q_id,
            "title": q["title"],
            "slug": q["title"].lower().replace(" ", "-").replace("'", "").replace("(", "").replace(")", ""),
            "category": q["category"],
            "difficulty": q["difficulty"],
            "problem_statement": q["problem_statement"],
            "examples": q["examples"],
            "constraints": q["constraints"],
            "hints": q["hints"],
            "is_published": True,
            "current_version_id": v_id,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat()
        }
        db.set_document("questions", q_id, q_doc)

        # Question Version Record
        v_doc = {
            "id": v_id,
            "question_id": q_id,
            "version_number": 1,
            "title": q["title"],
            "problem_statement": q["problem_statement"],
            "blueprint_id": b_id,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        db.set_document("question_versions", v_id, v_doc)

        # Concept Blueprint Record
        b_doc = {
            "id": b_id,
            "question_version_id": v_id,
            "concepts": q["concepts"],
            "expected_time_complexity": q["expected_time_complexity"],
            "expected_space_complexity": q["expected_space_complexity"],
            "expected_edge_cases": q["expected_edge_cases"]
        }
        db.set_document("concept_blueprints", b_id, b_doc)

    print(f"[Seed] Clean database initialized with {len(SEED_QUESTIONS)} published questions and Master Admin account!")

if __name__ == "__main__":
    seed_database()
