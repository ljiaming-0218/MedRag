
from pathlib import Path

from services.llm_service import generate_answer


def load_query_rewrite_template() -> str:
    file = Path(__file__).parent.parent / "prompts" / "query_rewrite_prompt.txt"
    with open(file, "r", encoding="utf-8") as f:
        return f.read()

def build_history_text(history: list[dict]) -> str:
    if not history:
        return "无历史对话"

    lines = []
    for message in history:
        role = message.get("role", "")
        content = message.get("content", "")

        if role == "user":
            role_name = "用户"
        elif role == "assistant":
            role_name = "助手"
        else:
            role_name = role or "未知角色"

        if content:
            lines.append(f"{role_name}: {content}")

    return "\n".join(lines) if lines else "无历史对话"


def build_query_rewrite_prompt(history: list[dict], query: str) -> str:
    template = load_query_rewrite_template()
    history_text = build_history_text(history)

    return template.format(
        history=history_text,
        query=query,
    )



def rewrite_query(history: list[dict], query: str) -> str:
    query = query.strip()
    if not query:
        raise ValueError("query 不能为空")

    if not history:
        return query

    try:
        prompt = build_query_rewrite_prompt(history, query)
        rewritten_query = generate_answer(prompt).strip()
    except Exception as e:
        print(f"Query rewrite failed: {e}")
        return query

    if not rewritten_query:
        return query

    return rewritten_query