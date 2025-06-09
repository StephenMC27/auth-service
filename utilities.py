import hashlib


def hash_password(password: str) -> str:
    """
    Hash password using SHA-256.

    Args:
        password (str): Plain text password

    Returns:
        str: hash of the password in hexadecimal format
    """
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.

    Args:
        password (str): Plain text password
        hashed_password (str): Previously hashed password to compare against

    Returns:
        bool: True if password matches the hash, False otherwise
    """
    return hash_password(password) == hashed_password
