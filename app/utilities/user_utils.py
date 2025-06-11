import uuid

from app.user_store import email_to_user_id, user_store
from app.models.user import UserResponse
from app.utilities.password_utils import hash_password


def create_user(email: str, password: str) -> str:
    # Generate UUID for user
    user_id = str(uuid.uuid4())

    # Hash password
    hashed_password = hash_password(password)

    user_record = {
        "id": user_id,
        "email": email,
        "password_hash": hashed_password,
    }

    user_store[user_id] = user_record
    email_to_user_id[email] = user_id

    return user_id


def get_user_by_id(user_id: str) -> dict | None:
    return user_store.get(user_id)


def get_user_by_email(email: str) -> dict | None:
    user_id = email_to_user_id.get(email)

    if not user_id:
        return None

    return get_user_by_id(user_id)


def update_user(user_id: str, updated_email: str = None, updated_password: str = None) -> dict | None:
    user = get_user_by_id(user_id)

    if not user:
        return None

    if updated_email:
        user["email"] = updated_email

    if updated_password:
        user["password"] = hash_password(updated_password)

    return user


def delete_user_by_id(user_id: str) -> str:
    user_email = user_store[user_id]["email"]

    del user_store[user_id]
    del email_to_user_id[user_email]
