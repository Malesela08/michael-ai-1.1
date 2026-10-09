import requests

from src.core.config import DEFAULT_MODEL, OLLAMA_HOST

OLLAMA_URL = f"{OLLAMA_HOST}/api/generate"

def query_lamla(prompt_text):
    payload = {
        "model": DEFAULT_MODEL,
        "prompt": prompt_text,
        "stream": False
    }
    
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        return result.get("response", "No response generated.")
    except requests.exceptions.RequestException as e:
        return f"Error communicating with local Ollama server: {e}"

if __name__ == "__main__":
    print("Initializing Lamla Master Orchestrator...")
    test_prompt = "Check the vehicle status and report on the perimeter security cameras."
    print(f"\nPrompt: {test_prompt}\n")
    
    answer = query_lamla(test_prompt)
    print(f"Lamla Response:\n{answer}")
