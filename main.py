import json
import sys
from typing import Any

from corpus_callosum import CorpusCallosum
from ollama_client import OllamaClient
from vision_agent import VisionAgent


def query_water_meter() -> dict[str, str]:
    """Return an unavailable status until a municipal data provider is configured."""
    return {
        "status": "unavailable",
        "message": "No municipal water-meter data provider is configured.",
    }


def scan_perimeter_camera(zone: str = "North") -> dict[str, Any]:
    """Capture a perimeter frame and report vision inference availability."""
    return VisionAgent().analyze_frame(zone=zone)


def create_hub() -> CorpusCallosum:
    """Create the central router and register the currently implemented tools."""
    callosum = CorpusCallosum(
        ollama_client=OllamaClient(default_model="llama3.2"),
        model="llama3.2",
    )
    vision_agent = VisionAgent()
    callosum.register_tool("water_meter", query_water_meter)
    callosum.register_agent(
        "yolo_vision",
        vision_agent.analyze_frame,
        {"requested_model": vision_agent.requested_model},
    )
    callosum.register_tool(
        "perimeter_camera",
        lambda zone: vision_agent.analyze_frame(zone=zone),
    )
    return callosum


def main() -> dict[str, Any]:
    print("Initializing Michael AI - Sovereign Core...")
    callosum = create_hub()

    prompt = (
        "Check the water meter status for the household."
        if len(sys.argv) == 1
        else " ".join(sys.argv[1:])
    )
    print(f"\n[Dispatching Agent Prompt]: '{prompt}'")
    result = callosum.route_intent(prompt)
    print("\n[Execution Result]:")
    print(json.dumps(result, indent=2))
    return result


if __name__ == "__main__":
    main()
