from typing import Any


class RelayControllerHandler:
    """Simulate relay state transitions without controlling physical hardware."""

    def __init__(self) -> None:
        self.states = {
            "fuel_pump_immobilizer": "armed",
            "perimeter_siren": "standby",
            "electric_gate": "locked",
        }

    def handle(self, action: str = "status") -> dict[str, Any]:
        """Return simulated state only; no hardware interface is used."""
        if action == "status":
            return {
                "status": "simulation_only",
                "relay_states": self.states.copy(),
                "hardware_actuated": False,
                "message": (
                    "Simulated relay state inventory returned; no physical hardware "
                    "is connected."
                ),
            }

        if action in self.states:
            self.states[action] = "simulated_triggered"
            return {
                "status": "simulation_only",
                "action": action,
                "state": self.states[action],
                "hardware_actuated": False,
                "message": (
                    f"Relay action '{action}' was simulated; no physical hardware "
                    "was actuated."
                ),
            }

        return {
            "status": "invalid_action",
            "action": action,
            "hardware_actuated": False,
            "message": f"Unknown relay action '{action}'. No state was changed.",
        }
