from orchestrator import query_lamla
from corpus_callosum import CorpusCallosum


def fail_if_ollama_is_called(*args, **kwargs):
    raise AssertionError("Perimeter tool routing should not require Ollama.")


def test_orchestrator_routes_perimeter_request_without_ollama(monkeypatch):
    monkeypatch.delenv("CAMERA_RTSP_URL", raising=False)
    monkeypatch.setattr("main.OllamaClient.generate", fail_if_ollama_is_called)
    result = query_lamla("Check the North zone perimeter.")
    assert result["status"] == "unavailable"
    assert result["inference_status"] == "unavailable"
    assert result["zone"] == "North"


def test_perimeter_request_without_zone_uses_default_zone(monkeypatch):
    monkeypatch.delenv("CAMERA_RTSP_URL", raising=False)
    monkeypatch.setattr("main.OllamaClient.generate", fail_if_ollama_is_called)
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
    bridge.register_tool("can_interceptor", lambda prompt: {"prompt": prompt})
    assert bridge.route_intent("Check vehicle CAN bus status.") == {
        "prompt": "check vehicle can bus status."
    }


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
