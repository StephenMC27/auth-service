from .fixtures import client


class TestUserLogin:
    """Test user login endpoint."""

    def test_login_success(self, sample_user_data, registered_user):
        """Test successful user login."""
        login_data = {
            "email": sample_user_data["email"],
            "password": sample_user_data["password"],
        }

        response = client.post("/login", json=login_data)
        assert response.status_code == 200

        data = response.json()
        assert data["message"] == "Login successful"
        assert data["user_id"] == registered_user["id"]

    def test_login_invalid_email(self):
        """Test login with non-existent email."""
        login_data = {"email": "nonexistent@example.com", "password": "anypassword"}

        response = client.post("/login", json=login_data)
        assert response.status_code == 401
        assert "Invalid email or password" in response.json()["detail"]

    def test_login_invalid_password(self, sample_user_data, registered_user):
        """Test login with incorrect password."""
        login_data = {"email": sample_user_data["email"], "password": "wrongpassword"}

        response = client.post("/login", json=login_data)
        assert response.status_code == 401
        assert "Invalid email or password" in response.json()["detail"]

    def test_login_missing_fields(self):
        """Test login with missing required fields."""
        # Missing password
        incomplete_data = {"email": "test@example.com"}
        response = client.post("/login", json=incomplete_data)
        assert response.status_code == 422

        # Missing email
        incomplete_data = {"password": "testpassword"}
        response = client.post("/login", json=incomplete_data)
        assert response.status_code == 422

    def test_login_invalid_email_format(self):
        """Test login with invalid email format."""
        login_data = {"email": "invalid-email", "password": "testpassword"}

        response = client.post("/login", json=login_data)
        assert response.status_code == 422

    def test_login_empty_credentials(self):
        """Test login with empty credentials."""
        login_data = {"email": "", "password": ""}

        response = client.post("/login", json=login_data)
        assert response.status_code == 422
