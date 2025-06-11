import uuid

import pytest

from app.main import app
from app.user_store import email_to_user_id, user_store

from .fixtures import client


class TestUserDeletion:
    """Test user deletion endpoint."""

    def test_delete_user_success(self, registered_user, sample_user_data):
        """Test successful user deletion."""
        user_id = registered_user["id"]

        # Verify user exists before deletion
        assert user_id in user_store
        assert sample_user_data["email"] in email_to_user_id

        response = client.delete(f"/users/{user_id}")
        assert response.status_code == 200

        data = response.json()
        assert data["message"] == "User deleted successfully"

        # Verify user is removed from both databases
        assert user_id not in user_store
        assert sample_user_data["email"] not in email_to_user_id

    def test_delete_nonexistent_user(self):
        """Test deletion of non-existent user."""
        fake_user_id = str(uuid.uuid4())

        response = client.delete(f"/users/{fake_user_id}")
        assert response.status_code == 404
        assert "User not found" in response.json()["detail"]

    def test_delete_invalid_uuid_format(self):
        """Test deletion with invalid UUID format."""
        invalid_id = "invalid-uuid"

        response = client.delete(f"/users/{invalid_id}")
        assert response.status_code == 404
        assert "User not found" in response.json()["detail"]

    def test_delete_empty_user_id(self):
        """Test deletion with empty user ID."""
        # This should result in a 404 or 405 depending on FastAPI routing
        response = client.delete("/users/")
        assert response.status_code in [404, 405]
