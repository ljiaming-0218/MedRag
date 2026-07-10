from services.db import get_database


from datetime import datetime


async def insert_conversation(conversation: dict) -> None:
    database = get_database()
    conversation_collection = database["conversations"]

    await conversation_collection.insert_one(conversation)
    

async def find_conversation_by_id(conversation_id: str) -> dict | None:
    database = get_database()
    conversation_collection = database["conversations"]

    conversation = await conversation_collection.find_one({"_id":conversation_id})
    return conversation

async def find_conversations(user_id: str, limit: int = 50) -> list[dict]:
    database = get_database()
    conversation_collection = database["conversations"]

    cursor = conversation_collection.find({"user_id": user_id})
    cursor = cursor.sort("updated_at", -1)
    cursor = cursor.limit(limit)

    conversations = []

    async for conversation in cursor:
        conversations.append(conversation)

    return conversations

async def create_conversation_indexes() -> None:
    database = get_database()
    conversation_collection = database["conversations"]

    await conversation_collection.create_index(
        [("updated_at", -1)],
        name="updated_at_desc_idx",
    )

async def update_conversation_updated_at(conversation_id: str, updated_at: datetime,) -> None:
    database = get_database()
    conversation_collection = database["conversations"]

    await conversation_collection.update_one(
        {"_id": conversation_id},
        {"$set": {"updated_at": updated_at}},
    )