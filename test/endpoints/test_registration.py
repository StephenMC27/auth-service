import uuid

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.user_store import email_to_user_id, user_store
from app.utilities.password_utils import verify_password

client = TestClient(app)


class TestUserRegistration:
    """Test user registration endpoint."""

    def test_register_user_success(self, sample_user_data):
        """Test successful user registration."""
        response = client.post("/registration", json=sample_user_data)

        assert response.status_code == 201

        data = response.json()
        assert "id" in data
        assert data["email"] == sample_user_data["email"]
        assert "password" not in data  # Password should not be in response

        # Verify UUID format
        try:
            uuid.UUID(data["id"])
        except ValueError:
            pytest.fail("User ID is not a valid UUID")

        # Verify user is stored in database
        assert data["id"] in user_store
        assert sample_user_data["email"] in email_to_user_id

        # Verify password is hashed
        stored_user = user_store[data["id"]]
        assert "password_hash" in stored_user
        assert stored_user["password_hash"] != sample_user_data["password"]
        assert verify_password(
            sample_user_data["password"], stored_user["password_hash"]
        )

    def test_register_duplicate_email(self, sample_user_data):
        """Test registration with duplicate email address."""
        # First registration should succeed
        response1 = client.post("/registration", json=sample_user_data)
        assert response1.status_code == 201

        # Second registration with same email should fail
        response2 = client.post("/registration", json=sample_user_data)
        assert response2.status_code == 409
        assert "Email already registered" in response2.json()["detail"]

    def test_register_invalid_email(self):
        """Test registration with invalid email format."""
        invalid_data = {
            "email": "invalid-email",
            "password": "testpassword123",
        }

        response = client.post("/registration", json=invalid_data)
        assert response.status_code == 422

    def test_register_missing_fields(self):
        """Test registration with missing required fields."""
        # Missing password
        incomplete_data = {"email": "test@example.com"}

        response = client.post("/registration", json=incomplete_data)
        assert response.status_code == 422

        # Missing email
        incomplete_data = {"password": "testpassword123"}

        response = client.post("/registration", json=incomplete_data)
        assert response.status_code == 422

    def test_register_empty_fields(self):
        """Test registration with empty field values."""
        empty_data = {"email": "", "password": ""}

        response = client.post("/registration", json=empty_data)
        assert response.status_code == 422

    def test_register_case_sensitive_password(self):
        """Test that email addresses are treated case-sensitively."""
        user_data_1 = {"email": "test@example.com", "password": "password123"}

        user_data_2 = {"email": "test@example.com", "password": "PASSWORD123"}

        response1 = client.post("/registration", json=user_data_1)
        assert response1.status_code == 201

        response2 = client.post("/registration", json=user_data_2)
        # Should succeed as passwords are different case
        assert response2.status_code == 201
