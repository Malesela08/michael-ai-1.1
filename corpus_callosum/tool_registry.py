"""Secure local tool registry (cameras, CAN bus, sensors)."""
import logging

logger = logging.getLogger("ToolRegistry")

class ToolRegistry:
    def __init__(self):
        logger.info("🛠️ [Tool Registry] Initializing secure edge tool registry.")
        self.tools = {
            "camera": {"status": "available", "protocol": "RTSP/ONVIF"},
            "can_bus": {"status": "available", "protocol": "ECU/Telemetry"},
            "relay_controller": {"status": "available", "protocol": "GPIO"}
        }

    def get_tool(self, tool_name: str):
        return self.tools.get(tool_name, {"status": "unavailable"})
