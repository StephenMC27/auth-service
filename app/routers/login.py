from fastapi import APIRouter, HTTPException, status

from app.models.login import LoginResponse
from app.models.user import User
from app.user_store import email_to_user_id, user_store
from app.utilities.password_utils import verify_password

router = APIRouter(prefix="/login", tags=["login"])


@router.post("/", response_model=LoginResponse)
async def login_user(login_data: User):
    """
    Validates user credentials against stored user data and returns
    a success message with user ID if authentication is successful.

    Args:
        login_data (User): Login credentials containing email and password

    Returns:
        LoginResponse: Success message and user ID

    Raises:
        HTTPException: 401 Unauthorized for invalid email or password
        HTTPException: 422 Unprocessable Entity for validation errors
    """

    # Check if email exists
    if login_data.email not in email_to_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
        )

    user_id = email_to_user_id[login_data.email]
    user_record = user_store[user_id]

    # Verify password
    if not verify_password(login_data.password, user_record["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
        )

    return LoginResponse(message="Login successful", user_id=user_id)
