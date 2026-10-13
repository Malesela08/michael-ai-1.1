import re
from collections.abc import Callable
from typing import Any, Protocol


class TextGenerationClient(Protocol):
    def generate(self, prompt: str) -> dict[str, Any]: ...


class CorpusCallosum:
    """Central decision engine and registry for Michael AI tools and agents."""

    def __init__(self, llm_client: TextGenerationClient | None = None) -> None:
        self.llm_client = llm_client
        self.registered_tools: dict[str, Callable[..., Any]] = {}
        self.active_agents: dict[str, dict[str, Any]] = {}
        self.agent_handlers: dict[str, Callable[..., Any]] = {}
        self._init_pillar_registry()

    def _init_pillar_registry(self) -> None:
        """Initialize the known pillars without claiming unconnected services are live."""
        self.active_agents = {
            "corpus_callosum": {
                "status": "active",
                "type": "central_engine",
            },
            "yolo_vision": {
                "status": "unavailable",
                "description": "YOLO Computer Vision & Gait Profiling Agent",
            },
            "mcp_bridges": {
                "status": "unavailable",
                "description": "Model Context Protocol Edge Data Bridges",
            },
            "active_interception": {
                "status": "unavailable",
                "description": "Automated Active Interception & Relay Controller",
            },
            "can_ecu_interceptor": {
                "status": "unavailable",
                "description": "CAN Bus & ECU Telemetry Interceptor",
            },
            "rf_spectrum_monitor": {
                "status": "unavailable",
                "description": "RF Spectrum & Anti-Jamming Monitor",
            },
            "sensor_fusion": {
                "status": "unavailable",
                "description": "Multi-Camera Sensor Fusion Module",
            },
            "forensic_vault": {
                "status": "unavailable",
                "description": "Local forensic evidence vault with SHA-256 checksums",
            },
            "iot_m2m_sim": {
                "status": "unavailable",
                "description": "IoT-M2M SIM & Dual-Redundant Communication Module",
            },
            "emergency_dispatch": {
                "status": "unavailable",
                "description": "Law Enforcement & Emergency Dispatch Bridge",
            },
            "power_manager": {
                "status": "unavailable",
                "description": "Edge Power & Grid Stability Manager",
            },
            "audit_sentinel": {
                "status": "unavailable",
                "description": "System Audit & Integrity Sentinel",
            },
            "dashboard_agent": {
                "status": "unavailable",
                "description": "Local User Interface & Dashboard Agent",
            },
        }

    def register_agent(
        self,
        agent_name: str,
        handler_func: Callable[..., Any],
        metadata: dict[str, Any] | None = None,
        *,
        include_in_pillars: bool = True,
    ) -> None:
        """Register an agent handler without exposing callables in status data."""
        self.agent_handlers[agent_name] = handler_func
        if include_in_pillars:
            entry = self.active_agents.setdefault(agent_name, {})
            entry.update(status="registered", metadata=metadata or {})

    def register_tool(self, name: str, func: Callable[..., Any]) -> None:
        """Register a local tool or MCP-backed endpoint."""
        self.registered_tools[name] = func
        pillar_for_tool = {
            "perimeter_camera": "yolo_vision",
            "can_interceptor": "can_ecu_interceptor",
            "rf_monitor": "rf_spectrum_monitor",
            "forensic_vault": "forensic_vault",
            "relay_controller": "active_interception",
        }.get(name)
        if pillar_for_tool:
            self.active_agents[pillar_for_tool]["status"] = "configured"

        if name in {
            "water_meter",
            "perimeter_camera",
            "can_interceptor",
            "rf_monitor",
            "forensic_vault",
            "relay_controller",
        }:
            self.active_agents["mcp_bridges"] = {
                "status": "local_tools_registered",
                "description": (
                    "Local tool handlers are registered; MCP server connections "
                    "are not configured."
                ),
            }

    def route_intent(
        self, prompt: str, context: dict[str, Any] | None = None
    ) -> Any:
        """Route recognized edge requests to registered local tools."""
        prompt_lower = prompt.lower().strip()

        if "water" in prompt_lower and "meter" in prompt_lower:
            if "water_meter" in self.registered_tools:
                return self.registered_tools["water_meter"]()
            return {
                "status": "unavailable",
                "message": "No municipal water-meter data provider is configured.",
            }

        if re.search(r"\b(can|ecu|vehicle)\b", prompt_lower):
            if "can_interceptor" in self.registered_tools:
                command = (
                    context.get("command", "read_telemetry")
                    if context
                    else "read_telemetry"
                )
                return self.registered_tools["can_interceptor"](command=command)
            return {
                "status": "unavailable",
                "module": "CAN Bus & ECU Telemetry Interceptor",
                "message": "No CAN bus telemetry provider is configured.",
            }

        if re.search(r"\b(rf|jamming|spectrum)\b", prompt_lower):
            if "rf_monitor" in self.registered_tools:
                return self.registered_tools["rf_monitor"]()
            return {
                "status": "unavailable",
                "module": "RF Spectrum & Anti-Jamming Monitor",
                "message": "No RF spectrum monitoring provider is configured.",
            }

        if re.search(r"\b(relay|immobilizer|siren|gate|ignition)\b", prompt_lower):
            if "relay_controller" in self.registered_tools:
                action = context.get("action") if context else None
                if action is None:
                    action = "status"
                    action_requested = re.search(
                        r"\b(trigger|activate|engage|open|close|lock|unlock|arm|disarm)\b",
                        prompt_lower,
                    )
                    if action_requested:
                        if re.search(r"\b(immobilizer|fuel pump|ignition)\b", prompt_lower):
                            action = "fuel_pump_immobilizer"
                        elif "siren" in prompt_lower:
                            action = "perimeter_siren"
                        elif "gate" in prompt_lower:
                            action = "electric_gate"
                return self.registered_tools["relay_controller"](action=action)
            return {
                "status": "unavailable",
                "module": "Relay Controller",
                "message": "No relay simulation handler is configured.",
            }

        if re.search(r"\b(forensic|evidence|incident)\b", prompt_lower):
            if "forensic_vault" in self.registered_tools:
                payload = context.get("payload") if context else None
                if payload is None:
                    payload = {"prompt": prompt}
                return self.registered_tools["forensic_vault"](payload=payload)
            return {
                "status": "unavailable",
                "module": "Forensic Evidence Vault",
                "message": "No forensic evidence storage handler is configured.",
            }

        if re.search(r"\b(camera|cameras|perimeter|scan|security)\b", prompt_lower):
            zone_match = re.search(
                r"\b(north|south|east|west)\b", prompt_lower, re.IGNORECASE
            )
            zone = (
                context.get("zone")
                if context and "zone" in context
                else zone_match.group(1).title() if zone_match else "North"
            )
            if "perimeter_camera" in self.registered_tools:
                source = context.get("source") if context else None
                if source is not None:
                    return self.registered_tools["perimeter_camera"](
                        zone, source=source
                    )
                return self.registered_tools["perimeter_camera"](zone)
            return {
                "camera_status": "unavailable",
                "zone": zone,
                "message": (
                    "Set CAMERA_SOURCE to a local image/video or online stream; "
                    "CAMERA_RTSP_URL also works for RTSP."
                ),
            }

        if (
            re.search(r"\b(status|agents|pillars)\b", prompt_lower)
        ):
            status = {
                "corpus_callosum_status": "operational",
                "pillars": self.active_agents,
            }
            return status

        if self.llm_client:
            return self.llm_client.generate(prompt)

        return {
            "status": "error",
            "message": "No matching route or active agent handler available.",
        }
