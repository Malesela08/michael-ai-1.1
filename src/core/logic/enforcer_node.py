import os
import sys

import ollama

from src.core.config import DEFAULT_MODEL

# Ensure current directory is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from system_persona import get_system_prompt


def secure_query(model_name, user_input):
    print(f"Enforcing with {model_name}...")
    response = ollama.chat(
        model=model_name,
        messages=[
            {"role": "system", "content": get_system_prompt()},
            {"role": "user", "content": user_input},
        ],
    )
    return response["message"]["content"]


if __name__ == "__main__":
    answer = secure_query(
        DEFAULT_MODEL, "Immediate status report on perimeter security."
    )
    print(answer)
