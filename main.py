import argparse
import json
import os
import sys
from os import PathLike
from typing import Any

from can_ecu_agent import CanEcuInterceptorHandler
from corpus_callosum import CorpusCallosum
from forensic_vault import ForensicVaultHandler
from llamafile_client import LlamafileClient
from relay_controller import RelayControllerHandler
from vision_agent import VisionAgent


def query_water_meter() -> dict[str, str]:
    """Return an unavailable status until a municipal data provider is configured."""
    return {
        "status": "unavailable",
        "message": "No municipal water-meter data provider is configured.",
    }


def scan_perimeter_camera(
    zone: str = "North",
    source: str | PathLike[str] | int | None = None,
) -> dict[str, Any]:
    """Capture a perimeter frame and report vision inference availability."""
    return VisionAgent(source=source).analyze_frame(zone=zone)


def create_hub() -> CorpusCallosum:
    """Create the central router and register the currently implemented tools."""
    callosum = CorpusCallosum(llm_client=LlamafileClient())
    vision_agent = VisionAgent()
    vault_handler = ForensicVaultHandler()
    relay_handler = RelayControllerHandler()
    can_handler = CanEcuInterceptorHandler()
    callosum.register_tool("water_meter", query_water_meter)
    callosum.register_agent(
        "yolo_vision",
        vision_agent.analyze_frame,
        {"requested_model": vision_agent.requested_model},
    )
    callosum.register_tool(
        "perimeter_camera",
        lambda zone, source=None: vision_agent.analyze_frame(source, zone=zone),
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
    return callosum


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Michael AI - Sovereign Edge Security & Telemetry Platform"
    )
    parser.add_argument(
        "--all-nodes",
        action="store_true",
        help="Report registered nodes and their configured status; does not activate them",
    )
    parser.add_argument(
        "--camera-source",
        default=os.getenv("CAMERA_SOURCE"),
        help="Camera device index, local image/video, or authorized stream URL",
    )
    parser.add_argument(
        "prompt",
        nargs="*",
        help="Optional prompt or task command for the orchestrator",
    )
    return parser.parse_args(argv)


def main() -> dict[str, Any]:
    args = parse_args()
    callosum = create_hub()
    if args.all_nodes:
        prompt = "Show system status"
    else:
        prompt = (
            "Check the water meter status for the household."
            if not args.prompt
            else " ".join(args.prompt)
        )

    context = {"source": args.camera_source} if args.camera_source is not None else None
    print("Initializing Michael AI - Sovereign Core...")
    print(f"\n[Dispatching Agent Prompt]: '{prompt}'")
    result = callosum.route_intent(prompt, context=context)
    print("\n[Execution Result]:")
    print(json.dumps(result, indent=2))
    return result


if __name__ == "__main__":
    main()
