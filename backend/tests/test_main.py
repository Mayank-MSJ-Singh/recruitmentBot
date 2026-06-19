"""
Tests for main.py configurations, metadata, CORS and security behaviors.
"""

def test_app_metadata(client):
    """Verify that FastAPI application properties are correctly registered."""
    from app.main import app
    from app.core.config import get_settings
    
    settings = get_settings()
    assert app.title == settings.APP_NAME
    assert app.version == settings.APP_VERSION

def test_root_endpoint(client):
    """Verify the root endpoint redirects/provides API info."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "service" in data
    assert "version" in data
    assert "docs" in data
    assert "health" in data

def test_cors_preflight(client):
    """Verify CORS preflight OPTIONS requests return correct headers."""
    headers = {
        "Origin": "http://localhost:5173",
        "Access-Control-Request-Method": "POST",
        "Access-Control-Request-Headers": "Content-Type, Authorization",
    }
    # Preflight request to a sample route
    response = client.options("/api/v1/auth/login", headers=headers)
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == "http://localhost:5173"
    assert "POST" in response.headers.get("access-control-allow-methods", "")

def test_not_found_route(client):
    """Verify requesting an invalid path returns a 404 response."""
    response = client.get("/api/v1/nonexistent-route-for-testing")
    assert response.status_code == 404
    assert response.json()["detail"] == "Not Found"
