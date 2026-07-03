


from pathlib import Path


def load_prompt_template() -> str:
    file = Path(__file__).parent.parent / "prompts" / "medical_qa_prompt.txt"
    with open(file, "r", encoding="utf-8") as f:
        return f.read()

def build_context(retrieved_chunks: list[dict]) -> str:
    context = ""
    for chunk in retrieved_chunks:
        context += f"[第{chunk['元数据']['page_number']}页, distance {chunk['距离']}, chunk {chunk['元数据']['chunk_index']}]\n{chunk['文本块']}\n"
    return context

def build_rag_prompt(question: str, retrieved_chunks: list[dict], history: list[dict] | None = None) -> str:
    prompt_template = load_prompt_template()
    context = build_context(retrieved_chunks)
    history_context = build_history_context(history or [])
    # 这里可以使用模板引擎或简单的字符串替换来构建最终的提示
    return prompt_template.format(history=history_context, question=question, context=context)

def build_history_context(history: list[dict]) -> str:
    if not history:
        return "无历史对话"
    history_context = ""
    for message in history:
        role = message["role"]
        content = message["content"]
        history_context += f"{role}: {content}\n"
    return history_context
