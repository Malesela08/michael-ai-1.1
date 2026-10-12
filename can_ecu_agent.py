from typing import Any


class CanEcuInterceptorHandler:
    """Provide clearly labeled CAN telemetry simulation without bus access."""

    def __init__(self, interface: str = "vcan0") -> None:
        self.interface = interface

    def handle(self, command: str = "read_telemetry") -> dict[str, Any]:
        """Return simulation metadata; this handler does not read a CAN interface."""
        if command != "read_telemetry":
            return {
                "status": "invalid_command",
                "command": command,
                "interface": self.interface,
                "hardware_read": False,
                "message": f"Unsupported CAN command '{command}'.",
            }

        return {
            "status": "simulation_only",
            "interface": self.interface,
            "metrics": None,
            "hardware_read": False,
            "message": (
                "No CAN telemetry was read. This handler does not connect to "
                "vcan0 or a vehicle bus."
            ),
        }
