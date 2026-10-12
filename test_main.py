import numpy as np

from main import create_hub, main, query_water_meter, scan_perimeter_camera
from vision_agent import VisionAgent


def test_create_hub_registers_available_tools():
    hub = create_hub()
    assert {
        "water_meter",
        "perimeter_camera",
        "forensic_vault",
        "relay_controller",
        "can_interceptor",
    } <= hub.registered_tools.keys()
    assert "yolo_vision" in hub.agent_handlers
    assert hub.active_agents["forensic_vault"]["status"] == "configured"
    assert hub.active_agents["active_interception"]["status"] == "configured"
    assert hub.active_agents["can_ecu_interceptor"]["status"] == "configured"
    assert {
        "forensic_vault",
        "active_interception",
        "can_ecu_interceptor",
    } <= hub.agent_handlers.keys()
    assert len(hub.active_agents) == 13
    assert hub.llm_client is not None


def test_water_meter_does_not_claim_placeholder_reading_is_live():
    assert query_water_meter() == {
        "status": "unavailable",
        "message": "No municipal water-meter data provider is configured.",
    }


def test_hub_can_route_does_not_claim_live_vehicle_telemetry():
    result = create_hub().route_intent("Check vehicle CAN bus status.")

    assert result["status"] == "simulation_only"
    assert result["metrics"] is None
    assert result["hardware_read"] is False


def test_camera_tool_reports_missing_stream_configuration(monkeypatch):
    monkeypatch.delenv("CAMERA_RTSP_URL", raising=False)
    result = scan_perimeter_camera("North")
    assert result["status"] == "unavailable"
    assert result["inference_status"] == "unavailable"
    assert result["zone"] == "North"
    assert result["message"] == (
        "No active video stream, image path, or camera URL configured."
    )


def test_vision_agent_reports_processed_frame_without_claiming_inference(
    monkeypatch, tmp_path
):
    frame_path = tmp_path / "frame.jpg"
    frame_path.touch()
    monkeypatch.setattr(
        "vision_agent.cv2.imread",
        lambda _path: np.full((480, 640, 3), 128, dtype="uint8"),
    )
    result = VisionAgent().analyze_frame(frame_path)
    assert result == {
        "status": "frame_processed",
        "zone": "North",
        "camera_status": "not_applicable",
        "resolution": "640x480",
        "frame_brightness": 128.0,
        "model": "YOLOv8-Nano-Edge",
        "inference_status": "unavailable",
        "threat_detected": None,
        "gait_profile": "unavailable",
        "message": (
            "Frame captured and brightness measured; YOLO inference is not configured."
        ),
    }


def test_camera_stream_configuration_is_passed_to_camera_probe(monkeypatch):
    monkeypatch.setenv("CAMERA_RTSP_URL", "rtsp://camera.local:554/live")
    class FakeCapture:
        def isOpened(self):
            return True

        def read(self):
            return True, np.full((480, 640, 3), 64, dtype="uint8")

        def release(self):
            pass

    monkeypatch.setattr("vision_agent.cv2.VideoCapture", lambda _url: FakeCapture())

    result = scan_perimeter_camera("South")
    assert result["status"] == "frame_processed"
    assert result["inference_status"] == "unavailable"
    assert result["camera_status"] == "stream_captured"
    assert result["resolution"] == "640x480"
    assert result["frame_brightness"] == 64.0
    assert result["zone"] == "South"


def test_cli_routes_water_meter_request(monkeypatch):
    import sys

    monkeypatch.setattr(sys, "argv", ["main.py", "check", "water", "meter"])

    result = main()
    assert result == {
        "status": "unavailable",
        "message": "No municipal water-meter data provider is configured.",
    }
