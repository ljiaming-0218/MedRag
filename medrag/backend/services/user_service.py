
from uuid import uuid4
from datetime import datetime, timezone
from stores.user_store import find_user_by_id, find_user_by_username, insert_user
from pymongo.errors import DuplicateKeyError



ALLOWED_USER_TYPES = {
    "undergraduate",
    "graduate_student",
    "researcher",
    "developer",
    "teacher",
    "general",
}


async def create_or_get_user(username: str, default_user_type: str = "general",) -> dict:
    username = username.strip()
    if username == "":
        raise ValueError("Username cannot be empty.")
    if len(username) > 30:
        raise ValueError("username 长度不能超过 30")
    default_user_type = default_user_type.strip().lower()
    if default_user_type not in ALLOWED_USER_TYPES:
        raise ValueError(f"Invalid user type: {default_user_type}. Allowed types: {ALLOWED_USER_TYPES}")
    
    existing_user = await find_user_by_username(username)

    if existing_user:
        return format_user_response(existing_user, False)

    now = datetime.now(timezone.utc)
    user = {
        "_id": str(uuid4()),
        "username": username,
        "default_user_type": default_user_type,
        "created_at": now,
        "updated_at": now,
    }
    try:
        await insert_user(user)
    except DuplicateKeyError:
        existing_user = await find_user_by_username(username)
        if existing_user:
            return format_user_response(existing_user, False)
        raise 

    
    return format_user_response(user, True)

async def get_existing_user(user_id: str) -> dict:
    user_id = user_id.strip()
    if user_id == "":
        raise ValueError("User ID cannot be empty.")
    user = await find_user_by_id(user_id)
    if not user:
        raise ValueError(f"User with ID {user_id} does not exist.")
    return format_user_response(user, False)

def format_user_response(user: dict, created: bool) -> dict:
    return {
        "user_id": user["_id"],
        "username": user["username"],
        "default_user_type": user["default_user_type"],
        "created_at": user["created_at"],
        "updated_at": user["updated_at"],
        "created": created,
    }