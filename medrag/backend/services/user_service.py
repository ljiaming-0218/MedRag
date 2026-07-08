
from uuid import uuid4
from datetime import datetime, timezone
from services.user_store import find_user_by_username, insert_user
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
    

    now = datetime.now(timezone.utc)
    created = True
    user = {
        "_id": str(uuid4()),
        "username": username,
        "default_user_type": default_user_type,
        "created_at": now,
        "updated_at": now,
    }


    try:
        await insert_user(user)
    except DuplicateKeyError as e:
        if await find_user_by_username(username):
            created = False
            return {
                "user_id": user["_id"],
                "username": user["username"],
                "default_user_type": user["default_user_type"],
                "created_at": user["created_at"],
                "updated_at": user["updated_at"],
                "created": created,
            }
        else:
            raise ValueError(f"Failed to create user due to a duplicate key error: {str(e)}") from e
    
    return {
        "user_id": user["_id"],
        "username": user["username"],
        "default_user_type": user["default_user_type"],
        "created_at": user["created_at"],
        "updated_at": user["updated_at"],
        "created": created,
    }


