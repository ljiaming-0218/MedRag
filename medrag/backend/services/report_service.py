

def route_task(query: str) -> str:
    #if any(keyword in query for keyword in ["总结", "摘要", "概括"]):
    #    return "summary"
    #elif any(keyword in query for keyword in ["术语", "关键词", "概念"]):
    #    return "term"
    #el
    if any(keyword in query for keyword in ["阅读报告", "分析这篇文献"]):
        return "report"
    #elif any(keyword in query for keyword in ["依据", "来源", "引用"]):
    #    return "source_check"
    #else:
    return "qa"