import requests

from src.core.config import DEFAULT_MODEL, OLLAMA_HOST


def query_ollama(prompt, model=DEFAULT_MODEL):
    try:
        response = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json={"model": model, "prompt": prompt, "stream": False},
            timeout=30,
        )
        response.raise_for_status()
        return response.json().get("response")
    except requests.exceptions.RequestException as error:
        print(f"Ollama connection error: {error}")
        return None
