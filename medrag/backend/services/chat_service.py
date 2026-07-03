from asyncio import to_thread
from services.prompt_service import build_rag_prompt
from services.search_service import search_relevant_chunks
from services.conversation_store import find_conversation_by_id
from services.llm_service import generate_answer
from services.message_service import get_recent_messages, create_message


async def prepare_ask_context(conversation_id: str, query: str, history_limit: int = 6, n_results: int = 3) -> dict:
    if history_limit < 1 or history_limit > 20:
        raise ValueError("history_limit 必须在 1 到 20 之间")
    if n_results < 1 or n_results > 10:
        raise ValueError("n_results 必须在 1 到 10 之间")
    conversation_id = conversation_id.strip()
    if not conversation_id:
        raise ValueError("conversation_id 不能为空")
    query = query.strip()
    if not query:
        raise ValueError("query 不能为空")
    conversation = await find_conversation_by_id(conversation_id)

    if conversation is None:
        raise ValueError("会话不存在")

    history = await get_recent_messages(conversation_id, history_limit)
    user_message = await create_message(conversation_id, "user", query)
    sources = await to_thread(search_relevant_chunks,conversation["document_id"], query, n_results)
    prompt= build_rag_prompt(query, sources, history)
    context = {
        "conversation_id": conversation["_id"],
        "document_id": conversation["document_id"],
        "history": history,
        "query": query,
        "user_message": user_message,
        "sources": sources,
        "sources_count": len(sources),
        "prompt": prompt,
    }

    return context

async def ask_conversation(conversation_id: str, query: str, history_limit: int = 6, n_results: int = 3,) -> dict:
    context = await prepare_ask_context(conversation_id, query, history_limit, n_results)
    answer = await to_thread(generate_answer, context["prompt"])
    assistant_message = await create_message(conversation_id, "assistant", answer, context["sources"])
    return {
        "conversation_id": context["conversation_id"],
        "answer": answer,
        "sources": context["sources"],
        "assistant_message": assistant_message,
    }