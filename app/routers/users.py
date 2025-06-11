from fastapi import APIRouter, HTTPException, status

from app.models.user import UserDelete
from app.utilities.user_utils import get_user_by_id, delete_user_by_id

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

    if not get_user_by_id(user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    delete_user_by_id(user_id)

    return UserDelete(message="User deleted successfully", user_id=user_id)
