import requests
import json
from typing import Optional, Dict, Any

class OllamaClient:
    def __init__(self, base_url: str = "http://localhost:11434", default_model: str = "llama3.2"):
        self.base_url = base_url.rstrip("/")
        self.default_model = default_model

    def generate(self, prompt: str, model: Optional[str] = None, timeout: int = 120) -> Dict[str, Any]:
        """Send a generation request to the local Ollama daemon."""
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": model or self.default_model,
            "prompt": prompt,
            "stream": False
        }
        
        try:
            response = requests.post(url, json=payload, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e), "response": None}

if __name__ == "__main__":
    client = OllamaClient()
    print("Testing local Ollama connection...")
    res = client.generate("System check: Confirm local sovereignty.")
    if res.get("response"):
        print(f"\n[Ollama Success]: {res['response']}")
    else:
        print(f"\n[Ollama Error]: {res.get('error')}")
