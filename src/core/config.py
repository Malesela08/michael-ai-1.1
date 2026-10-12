import os

import requests

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
DEFAULT_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")


def is_ollama_available(model_name: str | None = None, timeout: float = 3.0) -> bool:
    try:
        response = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=timeout)
        response.raise_for_status()
        payload = response.json()
        if model_name is None:
            return True
        models = payload.get("models", [])
        return any(model.get("name", "").startswith(model_name) for model in models)
    except (requests.RequestException, ValueError):
        return False
