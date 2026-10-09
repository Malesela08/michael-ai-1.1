import pytest
import requests

from src.core.config import DEFAULT_MODEL, OLLAMA_HOST, is_ollama_available


@pytest.mark.skipif(
    not is_ollama_available(DEFAULT_MODEL),
    reason="Ollama server is not running or the configured model is not available.",
)
def test_ollama_inference():
    url = f"{OLLAMA_HOST}/api/generate"
    payload = {
        "model": DEFAULT_MODEL,
        "prompt": "System test online. Reply with OK.",
        "stream": False,
    }

    response = requests.post(url, json=payload, timeout=30)
    response.raise_for_status()
    result = response.json()
    print(f"Status: {response.status_code} OK")
    print("Model Response:", result.get("response", "").strip())
    assert result.get("response", "").strip()


if __name__ == "__main__":
    test_ollama_inference()
