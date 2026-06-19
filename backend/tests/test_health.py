"""
Tests for Health Check endpoints.
"""

def test_basic_health_check(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_detailed_health_check(client):
    response = client.get("/api/v1/health/detailed")
    assert response.status_code == 200
    data = response.json()
    
    # Check that it's no longer just "not_configured"
    assert "components" in data
    assert data["components"]["database"]["status"] in ["connected", "failed: "] or data["components"]["database"]["status"].startswith("failed:")
    
    # If docker-compose database is up, it should be connected
    # (Since our E2E tests pass, we expect the DB to be connected)
    assert data["components"]["database"]["status"] == "connected"
    
    # LLM Gateway might be missing keys locally, but it shouldn't be "not_configured"
    assert data["components"]["llm_gateway"]["status"] in ["configured", "missing_api_keys"]
