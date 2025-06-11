import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.user_store import email_to_user_id, user_store

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_storage():
    user_store.clear()
    email_to_user_id.clear()


@pytest.fixture
def sample_user_data():
    return {
        "email": "stephen.clark@anaconda.com",
        "password": "icantwaittoworkwithStephen",
    }


@pytest.fixture
def registered_user(sample_user_data):
    """Create and return a registered user for testing."""
    response = client.post("/registration", json=sample_user_data)
    assert response.status_code == 201
    return response.json()
