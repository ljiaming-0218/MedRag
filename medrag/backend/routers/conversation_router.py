from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from services.message_service import list_messages
from services.conversation_service import create_conversation,list_conversations
from services.chat_service import ask_conversation
router = APIRouter(
    prefix="/conversations",
    tags=["conversations"],
)

class CreateConversationRequest(BaseModel):
    document_id: str
    title: str = "新会话"

class AskConversationRequest(BaseModel):
    query: str = Field(min_length=1)
    history_limit: int = Field(default=6, ge=1, le=20)
    n_results: int = Field(default=3, ge=1, le=10)

@router.post("", status_code=201)
async def create_conversation_endpoint(request: CreateConversationRequest,) -> dict:
    try:
        conversation = await create_conversation(request.document_id, request.title)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return conversation

@router.get("")
async def list_conversations_endpoint(limit: int = Query(default=50, ge=1, le=100),) -> list[dict]:
    return await list_conversations(limit)

@router.get("/{conversation_id}/messages")
async def list_messages_endpoint(conversation_id: str,) -> list[dict]:
    try:
        messages = await list_messages(conversation_id)
    except  ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    return messages


@router.post("/{conversation_id}/ask")
async def ask_conversation_endpoint(conversation_id: str, request: AskConversationRequest,) -> dict:
    try:
        result = await ask_conversation(conversation_id, request.query, request.history_limit, request.n_results)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return result