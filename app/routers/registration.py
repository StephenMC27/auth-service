import uuid

from fastapi import APIRouter, HTTPException, status

from app.models.user import User, UserResponse
from app.user_store import email_to_user_id, user_store
from app.utilities import hash_password

router = APIRouter(prefix="/registration", tags=["registration"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user: User):
    """
    Creates a new user account with email validation, password hashing,
    and UUID generation. Ensures email uniqueness.

    Args:
        user_data (User): User registration data containing
            email and password

    Returns:
        UserResponse: Created user data (without password)

    Raises:
        HTTPException: 409 Conflict if email already exists
        HTTPException: 422 Unprocessable Entity for validation errors
    """

    # Check if email already exists
    if user.email in email_to_user_id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already registered"
        )

    # Generate UUID for user
    user_id = str(uuid.uuid4())

    # Hash password
    hashed_password = hash_password(user.password)

    user_record = {
        "id": user_id,
        "email": user.email,
        "password_hash": hashed_password,
    }

    user_store[user_id] = user_record
    email_to_user_id[user.email] = user_id

    return UserResponse(id=user_id, email=user.email)
