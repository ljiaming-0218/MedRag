


from pathlib import Path


def build_rag_prompt(question: str, retrieved_chunks: list[dict], user_type: str = "general", history: list[dict] | None = None) -> str:
    prompt_template = load_prompt_template()
    context = build_context(retrieved_chunks)
    history_context = build_history_context(history or [])
    user_type_instruction = build_user_type_instruction(user_type)
    # 这里可以使用模板引擎或简单的字符串替换来构建最终的提示
    return prompt_template.format(history=history_context, question=question, context=context, user_type=user_type, user_type_instruction=user_type_instruction)


def load_prompt_template() -> str:
    file = Path(__file__).parent.parent / "prompts" / "medical_qa_prompt.txt"
    with open(file, "r", encoding="utf-8") as f:
        return f.read()

def build_context(retrieved_chunks: list[dict]) -> str:
    context = ""
    for chunk in retrieved_chunks:
        context += f"[第{chunk['元数据']['page_number']}页, distance {chunk['距离']}, chunk {chunk['元数据']['chunk_index']}]\n{chunk['文本块']}\n"
    return context

def build_history_context(history: list[dict]) -> str:
    if not history:
        return "无历史对话"
    history_context = ""
    for message in history:
        role = message["role"]
        content = message["content"]
        history_context += f"{role}: {content}\n"
    return history_context


def build_user_type_instruction(user_type) -> str:
    if user_type == "undergraduate":
        return "少术语，多解释基础概念"
    elif user_type == "graduate_student":
        return "强调研究问题、方法、创新点、局限"
    elif user_type == "researcher":
        return "强调相关工作、贡献、实验设置、可复现性"
    elif user_type == "developer":
        return "强调实现流程、技术路线、工程落地"
    elif user_type == "teacher":
        return "强调知识结构、教学讲解"
    else:
        return "简洁概括"
    
    