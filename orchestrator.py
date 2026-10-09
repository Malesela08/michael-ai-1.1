import json
from typing import Any

from corpus_callosum import CorpusCallosum


def query_lamla(prompt_text: str) -> dict[str, Any]:
    """Route a user request through the Corpus Callosum and its registered tools."""
    bridge = CorpusCallosum()
    return bridge.route_intent(prompt_text)

if __name__ == "__main__":
    print("Initializing Lamla Master Orchestrator...")
    test_prompt = "Check the vehicle status and report on the perimeter security cameras."
    print(f"\nPrompt: {test_prompt}\n")
    
    answer = query_lamla(test_prompt)
    print(f"Lamla Response:\n{json.dumps(answer, indent=2)}")
