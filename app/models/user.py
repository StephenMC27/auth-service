from pydantic import BaseModel, EmailStr


class User(BaseModel):
    """
    Pydantic model for user registration request data.

    Attributes:
        email (EmailStr): User's email address, must be valid email format
        password (str): User's password in plain text (will be hashed)
        name (str): User's display name
    """

    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """
    Pydantic model for user data response.

    Attributes:
        id (str): User's UUID
        email (str): User's email address
    """

    id: str
    email: EmailStr


class UserDelete(BaseModel):
    """
    Pydantic model for user deletion response.

    Attributes:
        msg (str): Success message confirming deletion
    """

    message: str
    user_id: str
