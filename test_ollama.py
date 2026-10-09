import requests

from src.core.config import DEFAULT_MODEL, OLLAMA_HOST

def test_ollama_inference():
    url = f"{OLLAMA_HOST}/api/generate"
    payload = {
        "model": DEFAULT_MODEL,
        "prompt": "System test online. Reply with OK.",
        "stream": False
    }
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        print(f"Status: {response.status_code} OK")
        print("Model Response:", result.get("response", "").strip())
    except requests.exceptions.RequestException as error:
        print(f"Error communicating with Ollama: {error}")

if __name__ == "__main__":
    test_ollama_inference()
