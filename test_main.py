from main import main, query_water_meter, scan_perimeter_camera


def test_water_meter_does_not_claim_placeholder_reading_is_live():
    assert query_water_meter() == {
        "status": "unavailable",
        "message": "No municipal water-meter data provider is configured.",
    }


def test_camera_tool_reports_missing_stream_configuration(monkeypatch):
    monkeypatch.delenv("CAMERA_RTSP_URL", raising=False)
    assert scan_perimeter_camera("North") == {
        "camera_status": "unavailable",
        "zone": "North",
        "message": "Set CAMERA_RTSP_URL to a camera stream to enable live checks.",
    }


def test_camera_stream_configuration_is_passed_to_camera_probe(monkeypatch):
    monkeypatch.setenv("CAMERA_RTSP_URL", "rtsp://camera.local:554/live")
    monkeypatch.setattr(
        "main.check_live_camera_stream",
        lambda url: {"camera_status": "online_and_streaming", "host": "camera.local"},
    )

    assert scan_perimeter_camera("South") == {
        "camera_status": "online_and_streaming",
        "host": "camera.local",
        "zone": "South",
    }


def test_cli_routes_water_meter_request_without_ollama(monkeypatch):
    monkeypatch.setattr("sys.argv", ["main.py", "check", "water", "meter"])
    monkeypatch.setattr(
        "ollama_client.OllamaClient.generate",
        lambda *args, **kwargs: (_ for _ in ()).throw(
            AssertionError("Water meter routing should not require Ollama.")
        ),
    )

    result = main()
    assert result["tool"] == "check_water_meter"
    assert result["output"]["status"] == "unavailable"
