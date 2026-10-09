from orchestrator import query_lamla


def fail_if_ollama_is_called(*args, **kwargs):
    raise AssertionError("Perimeter tool routing should not require Ollama.")


def test_orchestrator_routes_perimeter_request_without_ollama(monkeypatch):
    monkeypatch.setattr("ollama_client.OllamaClient.generate", fail_if_ollama_is_called)
    assert query_lamla("Check the North zone perimeter.") == {
        "status": "success",
        "routed": True,
        "tool": "check_perimeter",
        "output": {
            "status": "unavailable",
            "zone": "North",
            "cameras_active": None,
            "alerts": None,
            "message": "No live perimeter camera or sensor provider is configured.",
        },
    }


def test_perimeter_request_without_zone_does_not_guess_one(monkeypatch):
    monkeypatch.setattr("ollama_client.OllamaClient.generate", fail_if_ollama_is_called)
    result = query_lamla("Check the perimeter.")
    assert result["output"]["zone"] == "unspecified"
    assert result["output"]["status"] == "unavailable"
