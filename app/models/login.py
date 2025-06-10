from pydantic import BaseModel


class LoginResponse(BaseModel):
    """
    Pydantic model for user login response.

    Attributes:
        message (str): Success message
        user_id (str): User's UUID for identification
    """

    message: str
    user_id: str
