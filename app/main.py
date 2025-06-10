import uuid

from fastapi import FastAPI, HTTPException, status

from models import DeleteResponse, LoginResponse, User, UserResponse
from user_store import email_to_user_id, user_store
from utilities import hash_password, verify_password

app = FastAPI(title="User Authentication Service")


# API Endpoints
@app.post("/registration", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
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


@app.post("/login", response_model=LoginResponse)
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


@app.delete("/users/{user_id}", response_model=DeleteResponse)
async def delete_user(user_id: str):
    """
    Removes a user from both the user_store dictionary and the
    email_to_user_id dictionary

    Args:
        user_id (str): UUID of the user to delete

    Returns:
        DeleteResponse: Success message confirming deletion

    Raises:
        HTTPException: 404 Not Found if user does not exist
    """

    if user_id not in user_store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    user_email = user_store[user_id]["email"]

    del user_store[user_id]
    del email_to_user_id[user_email]

    return DeleteResponse(message="User deleted successfully", user_id=user_id)
