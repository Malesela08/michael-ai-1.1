from relay_controller import RelayControllerHandler


def test_relay_status_returns_initial_simulated_states_without_actuation():
    controller = RelayControllerHandler()

    result = controller.handle()

    assert result == {
        "status": "simulation_only",
        "relay_states": {
            "fuel_pump_immobilizer": "armed",
            "perimeter_siren": "standby",
            "electric_gate": "locked",
        },
        "hardware_actuated": False,
        "message": (
            "Simulated relay state inventory returned; no physical hardware "
            "is connected."
        ),
    }


def test_relay_action_only_changes_simulated_state():
    controller = RelayControllerHandler()

    result = controller.handle(action="perimeter_siren")

    assert result["status"] == "simulation_only"
    assert result["state"] == "simulated_triggered"
    assert result["hardware_actuated"] is False
    assert controller.states["perimeter_siren"] == "simulated_triggered"


def test_unknown_relay_action_is_rejected_without_actuation():
    controller = RelayControllerHandler()

    result = controller.handle(action="unknown_relay")

    assert result == {
        "status": "invalid_action",
        "action": "unknown_relay",
        "hardware_actuated": False,
        "message": "Unknown relay action 'unknown_relay'. No state was changed.",
    }


def test_status_request_does_not_change_relay_state():
    controller = RelayControllerHandler()
    result = controller.handle(action="status")

    assert result["status"] == "simulation_only"
    assert result["hardware_actuated"] is False
    assert result["relay_states"]["electric_gate"] == "locked"
