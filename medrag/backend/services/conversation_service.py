from datetime import datetime, timezone
from uuid import uuid4

from services.conversation_store import (
    find_conversations,
    insert_conversation,
)


async def create_conversation(document_id: str, title: str = "新会话") -> dict:
    # 清理并检查 document_id
    document_id = document_id.strip()
    if not document_id:
        raise ValueError("document_id不能为空")
    # 清理标题，空标题改为“新会话”
    title = title.strip() or "新会话"
    # 生成 now 和 conversation_id
    now = datetime.now(timezone.utc)
    conversation_id = str(uuid4())
    conversation = {
        "_id": conversation_id, 
        "title": title,
        "document_id": document_id,
        "created_at": now,
        "updated_at": now,
    }

    # await 调用 insert_conversation()
    await insert_conversation(conversation)
    return {
        "conversation_id": conversation["_id"],
        "title": conversation["title"],
        "document_id": conversation["document_id"],
        "created_at": conversation["created_at"],
        "updated_at": conversation["updated_at"],
    }


async def list_conversations(limit: int = 50) -> list[dict]:
    if limit <= 0 or limit > 100:
        raise ValueError("limit 必须在 1 到 100 之间")
    
    conversations = await find_conversations(limit)
    results = []

    for conversation in conversations:
        results.append({
            "conversation_id": conversation["_id"],
            "title": conversation["title"],
            "document_id": conversation["document_id"],
            "created_at": conversation["created_at"],
            "updated_at": conversation["updated_at"],
        })

    return results
