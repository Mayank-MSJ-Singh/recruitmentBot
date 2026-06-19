"""
End-to-End API tests for the Requisition flow.
"""
import pytest
import uuid

@pytest.fixture
def registered_hm_token(client):
    """Registers a temporary Hiring Manager and returns their token."""
    email = f"hm_{uuid.uuid4()}@company.com"
    payload = {
        "email": email,
        "password": "securepassword123",
        "first_name": "Test",
        "last_name": "Manager",
        "role": "hiring_manager"
    }
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 201
    return response.json()["access_token"]

def test_create_requisition_flow(client, registered_hm_token):
    """Tests that a Hiring Manager can create a job requisition."""
    payload = {
        "title": "Backend Python Developer",
        "department": "Engineering",
        "raw_brief": "We need a strong backend developer skilled in Python, FastAPI, and Postgres to build robust microservices.",
        "skills_required": ["Python", "FastAPI", "SQLAlchemy", "PostgreSQL"],
        "location": "Remote",
        "salary_range": "₹20-30 LPA"
    }
    
    response = client.post(
        "/api/v1/requisitions",
        json=payload,
        headers={"Authorization": f"Bearer {registered_hm_token}"}
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == payload["title"]
    assert data["department"] == payload["department"]
    assert data["status"] == "draft"
    
    # Verify it appears in the list
    list_response = client.get(
        "/api/v1/requisitions",
        headers={"Authorization": f"Bearer {registered_hm_token}"}
    )
    assert list_response.status_code == 200
    
    # Check that our newly created requisition is in the list
    reqs = list_response.json()["requisitions"]
    assert any(r["id"] == data["id"] for r in reqs)
