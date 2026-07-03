from datetime import datetime, timezone
from uuid import uuid4

from services.conversation_store import find_conversation_by_id, update_conversation_updated_at
from services.message_store import find_recent_messages_by_conversation, insert_message, find_messages_by_conversation


async def create_message(conversation_id: str, role: str, content: str, sources: list[dict] | None = None) -> dict:
    conversation_id = conversation_id.strip()
    if not conversation_id:
        raise ValueError("conversation_id 不能为空")

    conversation = await find_conversation_by_id(conversation_id)
    if conversation is None:
        raise ValueError("会话不存在")
    role = role.strip().lower()
    if role not in {"user", "assistant"}:
        raise ValueError("role 只能是 user 或 assistant")

    content = content.strip()
    if not content:
        raise ValueError("content 不能为空")

    if sources is None:
        sources = []

    if not isinstance(sources, list):
        raise ValueError("sources 必须是列表")
    now = datetime.now(timezone.utc)
    message_id = str(uuid4())

    message = {
        "_id": message_id, 
        "conversation_id": conversation_id,
        "role": role,
        "content": content,
        "sources": sources,
        "created_at": now,
        
    }

    await insert_message(message)
    await update_conversation_updated_at(conversation_id, now)
    return {
        "message_id": message["_id"],
        "conversation_id": message["conversation_id"],
        "role": message["role"],
        "content": message["content"],
        "sources": message["sources"],
        "created_at": message["created_at"],
        
    }

async def list_messages(conversation_id: str,) -> list[dict]:
    conversation_id = conversation_id.strip()
    if not conversation_id:
        raise ValueError("conversation_id 不能为空")

    conversation = await find_conversation_by_id(conversation_id)

    if conversation is None:
        raise ValueError("会话不存在")
    messages = await find_messages_by_conversation(conversation_id)

    results = []

    for message in messages:
        results.append({
            "message_id": message["_id"],
            "conversation_id": message["conversation_id"],
            "role": message["role"],
            "content": message["content"],
            "sources": message["sources"],
            "created_at": message["created_at"],
        })

    return results


async def get_recent_messages(conversation_id: str, limit: int=6) -> list[dict]:
    if limit < 1 or limit > 20:
        raise ValueError("limit 必须在 1 到 20 之间")
    conversation_id = conversation_id.strip()
    if not conversation_id:
        raise ValueError("conversation_id 不能为空")

    conversation = await find_conversation_by_id(conversation_id)

    if conversation is None:
        raise ValueError("会话不存在")
    messages = await find_recent_messages_by_conversation(conversation_id, limit)

    results = []

    for message in messages:
        results.append({
            "message_id": message["_id"],
            "conversation_id": message["conversation_id"],
            "role": message["role"],
            "content": message["content"],
            "sources": message["sources"],
            "created_at": message["created_at"],
        })

    return results