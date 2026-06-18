from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch, AsyncMock

client = TestClient(app)

def test_list_prompts():
    response = client.get("/api/v1/llm/prompts")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "name" in data[0]
    assert "version" in data[0]
    assert "description" in data[0]

def test_get_configured_models():
    response = client.get("/api/v1/llm/models")
    assert response.status_code == 200
    data = response.json()
    assert "premium" in data
    assert "fast" in data
    assert "fallback" in data

def test_get_telemetry_stats():
    response = client.get("/api/v1/llm/telemetry/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_calls" in data
    assert "total_tokens" in data
    assert "total_cost_usd" in data
    assert "buffer_size" in data
    assert "avg_tokens_per_call" in data
    assert "avg_cost_per_call_usd" in data

@patch("app.api.llm_routes.llm_gateway.generate", new_callable=AsyncMock)
def test_test_generate(mock_generate):
    # Mocking the actual LLM call to verify the route functions correctly
    # when the LLM service succeeds without needing real API keys.
    mock_generate.return_value = {"content": "Mocked JD content", "model": "mock-model", "usage": {"total_tokens": 10}, "latency_ms": 100, "telemetry_id": "123"}

    response = client.post(
        "/api/v1/llm/generate",
        json={
            "prompt_name": "jd_generation",
            "tier": "fast",
            "variables": {
                "title": "SE",
                "department": "Engineering",
                "location": "Remote",
                "brief": "Python",
                "skills": "Python"
            }
        }
    )
    assert response.status_code == 200
    assert response.json()["success"] == True
    assert response.json()["data"]["content"] == "Mocked JD content"
