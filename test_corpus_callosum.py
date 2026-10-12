from orchestrator import query_lamla
from corpus_callosum import CorpusCallosum


def test_orchestrator_routes_perimeter_request(monkeypatch):
    monkeypatch.delenv("CAMERA_RTSP_URL", raising=False)
    result = query_lamla("Check the North zone perimeter.")
    assert result["status"] == "unavailable"
    assert result["inference_status"] == "unavailable"
    assert result["zone"] == "North"


def test_perimeter_request_without_zone_uses_default_zone(monkeypatch):
    monkeypatch.delenv("CAMERA_RTSP_URL", raising=False)
    result = query_lamla("Check the perimeter.")
    assert result["zone"] == "North"
    assert result["inference_status"] == "unavailable"


def test_can_request_does_not_claim_secure_without_provider():
    result = CorpusCallosum().route_intent("Check vehicle CAN bus status.")
    assert result == {
        "status": "unavailable",
        "module": "CAN Bus & ECU Telemetry Interceptor",
        "message": "No CAN bus telemetry provider is configured.",
    }


def test_can_request_uses_registered_provider():
    bridge = CorpusCallosum()
    bridge.register_tool(
        "can_interceptor",
        lambda command: {"command": command},
    )
    assert bridge.route_intent("Check vehicle CAN bus status.") == {
        "command": "read_telemetry"
    }


def test_can_route_passes_explicit_command_context():
    bridge = CorpusCallosum()
    bridge.register_tool("can_interceptor", lambda command: {"command": command})
    assert bridge.route_intent(
        "Check vehicle CAN bus status.",
        context={"command": "invalid"},
    ) == {"command": "invalid"}


def test_rf_request_does_not_claim_clear_without_provider():
    result = CorpusCallosum().route_intent("Check RF spectrum for jamming.")
    assert result == {
        "status": "unavailable",
        "module": "RF Spectrum & Anti-Jamming Monitor",
        "message": "No RF spectrum monitoring provider is configured.",
    }


def test_agent_can_be_registered():
    bridge = CorpusCallosum()
    agent = lambda: "vision response"
    bridge.register_agent("yolo_vision", agent, {"version": "test"})
    assert bridge.agent_handlers["yolo_vision"] is agent
    assert bridge.active_agents["yolo_vision"] == {
        "status": "registered",
        "description": "YOLO Computer Vision & Gait Profiling Agent",
        "metadata": {"version": "test"},
    }


def test_status_reports_all_thirteen_pillars_as_json_serializable():
    import json

    bridge = CorpusCallosum()
    bridge.register_agent("yolo_vision", lambda: "vision response")
    result = bridge.route_intent("Show all agent status")
    assert len(result["pillars"]) == 13
    assert result["pillars"]["yolo_vision"]["status"] == "registered"
    assert result["pillars"]["can_ecu_interceptor"]["status"] == "unavailable"
    json.dumps(result)


def test_unmatched_prompt_reports_no_available_route():
    assert CorpusCallosum().route_intent("Give me a tactical summary.") == {
        "status": "error",
        "message": "No matching route or active agent handler available.",
    }


def test_unmatched_prompt_uses_configured_text_generation_client():
    class FakeClient:
        def generate(self, prompt):
            return {"status": "active", "response": prompt}

    result = CorpusCallosum(llm_client=FakeClient()).route_intent(
        "Give me a tactical summary."
    )

    assert result == {
        "status": "active",
        "response": "Give me a tactical summary.",
    }


def test_registering_tool_does_not_claim_mcp_server_is_connected():
    bridge = CorpusCallosum()
    bridge.register_tool("perimeter_camera", lambda zone: {"zone": zone})
    assert bridge.active_agents["yolo_vision"]["status"] == "configured"
    assert bridge.active_agents["mcp_bridges"]["status"] == "local_tools_registered"
    assert "MCP server connections are not configured" in bridge.active_agents[
        "mcp_bridges"
    ]["description"]


def test_registering_can_handler_updates_pillar_without_claiming_device_online():
    bridge = CorpusCallosum()
    bridge.register_tool("can_interceptor", lambda prompt: {"prompt": prompt})
    assert bridge.active_agents["can_ecu_interceptor"]["status"] == "configured"
    result = bridge.route_intent("Show all agent status")
    assert result["pillars"]["can_ecu_interceptor"]["status"] == "configured"


def test_forensic_request_routes_context_payload_to_registered_vault():
    bridge = CorpusCallosum()
    received = {}

    def store_evidence(*, payload):
        received["payload"] = payload
        return {"status": "recorded"}

    bridge.register_tool("forensic_vault", store_evidence)
    assert bridge.route_intent(
        "Store this incident evidence",
        context={"payload": {"event": "alarm"}},
    ) == {"status": "recorded"}
    assert received["payload"] == {"event": "alarm"}


def test_relay_request_uses_registered_handler_in_simulation_only():
    bridge = CorpusCallosum()
    bridge.register_tool(
        "relay_controller",
        lambda action: {
            "status": "simulation_only",
            "action": action,
            "hardware_actuated": False,
        },
    )

    result = bridge.route_intent(
        "Trigger perimeter siren",
        context={"action": "perimeter_siren"},
    )
    assert result == {
        "status": "simulation_only",
        "action": "perimeter_siren",
        "hardware_actuated": False,
    }


def test_relay_trigger_prompt_selects_matching_simulated_relay():
    bridge = CorpusCallosum()
    received = {}

    def handle_relay(*, action):
        received["action"] = action
        return {"status": "simulation_only", "action": action}

    bridge.register_tool("relay_controller", handle_relay)

    result = bridge.route_intent("Trigger perimeter siren")

    assert received["action"] == "perimeter_siren"
    assert result == {
        "status": "simulation_only",
        "action": "perimeter_siren",
    }
