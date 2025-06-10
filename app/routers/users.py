from fastapi import APIRouter, HTTPException, status

from app.models.user import UserDelete
from app.user_store import email_to_user_id, user_store

router = APIRouter(prefix="/users", tags=["users"])


@router.delete("/{user_id}", response_model=UserDelete)
async def delete_user(user_id: str):
    """
    Removes a user from both the user_store dictionary and the
    email_to_user_id dictionary

    Args:
        user_id (str): UUID of the user to delete

    Returns:
        UserDelete: Success message confirming deletion

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

    return UserDelete(message="User deleted successfully", user_id=user_id)
