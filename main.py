import json
import sys
from typing import Any

from can_ecu_agent import CanEcuInterceptorHandler
from corpus_callosum import CorpusCallosum
from forensic_vault import ForensicVaultHandler
from ollama_engine import OllamaEngineHandler
from ollama_client import OllamaClient
from relay_controller import RelayControllerHandler
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
    vault_handler = ForensicVaultHandler()
    relay_handler = RelayControllerHandler()
    can_handler = CanEcuInterceptorHandler()
    ollama_engine = OllamaEngineHandler(model="llama3.2")
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
    callosum.register_agent(
        "forensic_vault",
        vault_handler.handle,
        {"storage": "local_json", "encrypted": False},
    )
    callosum.register_tool("forensic_vault", vault_handler.handle)
    callosum.register_agent(
        "active_interception",
        relay_handler.handle,
        {"hardware_actuated": False, "mode": "simulation_only"},
    )
    callosum.register_tool("relay_controller", relay_handler.handle)
    callosum.register_agent(
        "can_ecu_interceptor",
        can_handler.handle,
        {"interface": can_handler.interface, "mode": "simulation_only"},
    )
    callosum.register_tool("can_interceptor", can_handler.handle)
    callosum.register_tool("ollama_engine", ollama_engine.handle)
    callosum.register_agent(
        "ollama_engine",
        ollama_engine.handle,
        {"provider": "local_ollama", "model": ollama_engine.model},
        include_in_pillars=False,
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
