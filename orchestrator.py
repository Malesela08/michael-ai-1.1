import json
from typing import Any

from corpus_callosum import CorpusCallosum
from main import query_water_meter, scan_perimeter_camera
from ollama_client import OllamaClient


def query_lamla(prompt_text: str) -> Any:
    """Route a user request through the Corpus Callosum and its registered tools."""
    bridge = CorpusCallosum(ollama_client=OllamaClient(default_model="llama3.2"))
    bridge.register_tool("water_meter", query_water_meter)
    bridge.register_tool("perimeter_camera", scan_perimeter_camera)
    return bridge.route_intent(prompt_text)

if __name__ == "__main__":
    print("Initializing Lamla Master Orchestrator...")
    test_prompt = "Check the vehicle status and report on the perimeter security cameras."
    print(f"\nPrompt: {test_prompt}\n")
    
    answer = query_lamla(test_prompt)
    print(f"Lamla Response:\n{json.dumps(answer, indent=2)}")
