import requests

def query_ollama(prompt, model="llama3"):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": model, "prompt": prompt, "stream": False},
            timeout=30
        )
        response.raise_for_status()
        return response.json().get("response")
    except requests.exceptions.RequestException as e:
        print(f"Ollama connection error: {e}")
        return None

if __name__ == "__main__":
    print("Testing Ollama connection...")
    print(query_ollama("Hello! Are you working?"))
