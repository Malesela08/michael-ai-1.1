from can_ecu_agent import CanEcuInterceptorHandler


def test_can_handler_does_not_claim_live_telemetry_without_bus_access():
    result = CanEcuInterceptorHandler().handle()

    assert result == {
        "status": "simulation_only",
        "interface": "vcan0",
        "metrics": None,
        "hardware_read": False,
        "message": (
            "No CAN telemetry was read. This handler does not connect to "
            "vcan0 or a vehicle bus."
        ),
    }


def test_can_handler_rejects_unsupported_command():
    result = CanEcuInterceptorHandler().handle("immobilize")

    assert result["status"] == "invalid_command"
    assert result["hardware_read"] is False
    assert result["command"] == "immobilize"
