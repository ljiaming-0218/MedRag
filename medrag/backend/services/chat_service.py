from asyncio import to_thread
from services.agent_router_service import build_report_prompt
from services.report_service import route_task
from services.user_service import get_existing_user, ALLOWED_USER_TYPES
from services.query_rewrite_service import rewrite_query
from services.prompt_service import build_rag_prompt
from services.search_service import search_relevant_chunks
from stores.conversation_store import find_conversation_by_id
from services.llm_service import generate_answer
from services.message_service import get_recent_messages, create_message

NO_SOURCE_ANSWER = "当前文献未提供相关信息。"


async def prepare_ask_context(user_id: str, conversation_id: str, query: str, history_limit: int = 6, n_results: int = 3, user_type: str| None = None,) -> dict:
    if not user_id.strip():
        raise ValueError("user_id 不能为空")

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
    if conversation["user_id"] != user_id:
        raise ValueError("当前用户无权访问该会话")

    request_user_type = user_type.strip().lower() if user_type and user_type.strip() else None
    if request_user_type and request_user_type not in ALLOWED_USER_TYPES:
        raise ValueError("非法的 user_type")

    user = await get_existing_user(user_id)

    resolved_user_type = (
        request_user_type
        or conversation.get("user_type")
        or user.get("default_user_type")
        or "general"
    )


    history = await get_recent_messages(conversation_id, history_limit)
    user_message = await create_message(conversation_id, "user", query)
    rewritten_query = await to_thread(rewrite_query, history, query)
    sources = await to_thread(search_relevant_chunks, user_id, conversation["document_id"], rewritten_query, n_results)
    
    prompt= build_rag_prompt(query, sources, resolved_user_type, history)
    
    context = {
        "conversation_id": conversation["_id"],
        "document_id": conversation["document_id"],
        "user_id": conversation["user_id"],
        "history": history,
        "query": query,
        "user_type": resolved_user_type,
        "rewritten_query": rewritten_query,
        "user_message": user_message,
        "sources": sources,
        "sources_count": len(sources),
        "prompt": prompt,
    }
    
    return context

async def ask_conversation(user_id: str, conversation_id: str, query: str, history_limit: int = 6, n_results: int = 3, user_type: str | None = None) -> dict:
    context = await prepare_ask_context(user_id, conversation_id, query, history_limit, n_results, user_type)
    task_type = route_task(query)

    if not context["sources_count"]:
        answer = NO_SOURCE_ANSWER
    elif task_type == "report":
        prompt = build_report_prompt(
            context["rewritten_query"],
            context["sources"],
            context["user_type"],
            context["history"],
        )
        answer = await to_thread(generate_answer, prompt)
    else:
        answer = await to_thread(generate_answer, context["prompt"])
    assistant_message = await create_message(conversation_id, "assistant", answer, context["sources"], context["rewritten_query"])
    
    return {
        "conversation_id": context["conversation_id"],
        "user_type": context["user_type"],
        "answer": answer,
        "sources": context["sources"],
        "sources_count": context["sources_count"],        
        "rewritten_query": context["rewritten_query"],
        "assistant_message": assistant_message,
        "task_type": task_type
    }
