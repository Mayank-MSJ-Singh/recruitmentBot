"""
Pytest configuration and shared fixtures for RecruitBot tests.
"""
import pytest
from fastapi.testclient import TestClient
import uuid

# Import the FastAPI application
from app.main import app
from app.core.auth import create_access_token

@pytest.fixture
def client():
    """Returns a FastAPI TestClient."""
    with TestClient(app) as c:
        yield c

@pytest.fixture
def candidate_token():
    """Returns a valid JWT token for a candidate."""
    return create_access_token(
        user_id=str(uuid.uuid4()),
        email="candidate_test@example.com",
        role="candidate"
    )

@pytest.fixture
def hiring_manager_token():
    """Returns a valid JWT token for a hiring manager."""
    return create_access_token(
        user_id=str(uuid.uuid4()),
        email="manager_test@example.com",
        role="hiring_manager"
    )
