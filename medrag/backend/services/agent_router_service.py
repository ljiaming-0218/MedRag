

from pathlib import Path

from services.prompt_service import build_context, build_history_context, build_user_type_instruction






def build_report_prompt(query, sources, user_type, history) -> str:
    prompt_template = load_report_prompt_template()
    context = build_context(sources)
    history_context = build_history_context(history or [])
    user_type_instruction = build_user_type_instruction(user_type)
    return prompt_template.format(history=history_context, query=query, context=context, user_type=user_type, user_type_instruction=user_type_instruction)


def load_report_prompt_template() -> str:
    file = Path(__file__).parent.parent / "prompts" / "report_prompt.txt"
    with open(file, "r", encoding="utf-8") as f:
        return f.read()