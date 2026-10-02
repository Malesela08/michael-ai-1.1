def evaluate_threat():
    print("[NODE_7_EVALUATOR]: Analyzing vector telemetry...")
    print("[NODE_8_DISPATCHER]: Alert channels armed. Shift status updated to active watch.")

if __name__ == "__main__":
    evaluate_threat()
import requests
import json

class OllamaEngine:
    def __init__(self, model: str = "llama3.2", host: str = "http://localhost:11434"):
        self.model = model
        self.host = host
        self.endpoint = f"{self.host}/api/generate"

    def generate_response(self, prompt: str, system_prompt: str = "") -> str:
        """Sends a prompt to the local Ollama instance and returns the generated response."""
        payload = {
            "model": self.model,
            "prompt": prompt,
            "system": system_prompt,
            "stream": False
        }
        
        try:
            response = requests.post(self.endpoint, json=payload)
            response.raise_for_status()
            data = response.json()
            return data.get("response", "")
        except requests.exceptions.RequestException as e:
            print(f"[OLLAMA_ENGINE_ERROR]: Failed to connect to Ollama: {e}")
            return ""

# Basic test execution
if __name__ == "__main__":
    engine = OllamaEngine()
    result = engine.generate_response(
        prompt="Analyze telemetry status: Normal baseline detected.",
        system_prompt="You are Michael AI Threat Evaluator Core."
    )
    print("Engine Output:", result)