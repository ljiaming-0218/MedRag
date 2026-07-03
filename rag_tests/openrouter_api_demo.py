from pathlib import Path
from openai import OpenAI


import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1] / "medrag"
sys.path.insert(0, str(PROJECT_ROOT))

from backend.config import (
    OPENROUTER_API_KEY,
    OPENROUTER_BASE_URL,
    OPENROUTER_MODEL,
)

def get_openrouter_client() -> OpenAI:


    client = OpenAI(
        api_key=OPENROUTER_API_KEY,
        base_url=OPENROUTER_BASE_URL,
    )
    return client

def create_client() -> OpenAI:
    """
    创建并返回一个 OpenRouter 客户端实例。
    """
    
    return get_openrouter_client()


def main():
    """
    测试 OpenRouter 客户端的功能。
    """
    client = create_client()
    response = client.chat.completions.create(
        model=OPENROUTER_MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "ok"}
        ]
    )
    print(response.choices[0].message.content)

if __name__ == "__main__":    main()