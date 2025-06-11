from app.utilities.password_utils import hash_password, verify_password


class TestPasswordUtilities:
    """Test password hashing and verification utilities."""

    def test_hash_password(self):
        """Test password hashing functionality."""
        password = "testpassword123"
        hashed = hash_password(password)

        # Should return a string
        assert isinstance(hashed, str)

        # Should be SHA-256 hex (64 characters)
        assert len(hashed) == 64

        # Should be consistent
        assert hash_password(password) == hashed

        # Different passwords should produce different hashes
        assert hash_password("different") != hashed

    def test_verify_password(self):
        """Test password verification functionality."""
        password = "testpassword123"
        hashed = hash_password(password)

        # Correct password should verify
        assert verify_password(password, hashed) is True

        # Incorrect password should not verify
        assert verify_password("wrongpassword", hashed) is False

        # Empty password should not verify
        assert verify_password("", hashed) is False
