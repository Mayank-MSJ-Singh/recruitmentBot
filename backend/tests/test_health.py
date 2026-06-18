from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "RecruitBot API"
    assert "timestamp" in data

def test_detailed_health_check():
    response = client.get("/api/v1/health/detailed")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "RecruitBot API"
    assert "components" in data
    assert "database" in data["components"]
    assert "llm_gateway" in data["components"]
    assert "redis" in data["components"]
