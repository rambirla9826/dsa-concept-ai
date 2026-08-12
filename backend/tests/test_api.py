import pytest
from fastapi.testclient import TestClient
from main import app
from app.seed.seed_db import seed_database

@pytest.fixture(autouse=True)
def setup_seed():
    seed_database()

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"

def test_login_student():
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "student@example.com", "password": "StudentPass123!"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["user"]["role"] == "USER"

def test_login_admin():
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "admin@algoconcept.ai", "password": "AdminPass123!"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["user"]["role"] == "ADMIN"

def test_list_questions():
    # Login first
    login_res = client.post("/api/v1/auth/login", json={"email": "student@example.com", "password": "StudentPass123!"})
    token = login_res.json()["access_token"]
    
    res = client.get("/api/v1/questions", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    questions = res.json()
    assert len(questions) >= 20  # Verified 20 seed questions!

def test_rbac_admin_protection():
    # Login as student
    login_res = client.post("/api/v1/auth/login", json={"email": "student@example.com", "password": "StudentPass123!"})
    token = login_res.json()["access_token"]
    
    # Attempting to access admin endpoint as student must fail with 403 Forbidden
    res = client.get("/api/v1/admin/overview", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 403
