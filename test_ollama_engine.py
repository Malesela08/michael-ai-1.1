import json

from ollama_engine import OllamaEngineHandler


class FakeResponse:
    def __init__(self, payload, status=200):
        self.status = status
        self.payload = json.dumps(payload).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return None

    def read(self):
        return self.payload


def test_connection_reports_daemon_and_configured_model(monkeypatch):
    captured = {}

    def fake_urlopen(request, timeout):
        captured["method"] = request.get_method()
        captured["timeout"] = timeout
        return FakeResponse({"models": [{"name": "llama3.2"}]})

    monkeypatch.setattr(
        "ollama_engine.urlopen",
        fake_urlopen,
    )
    handler = OllamaEngineHandler(endpoint="http://ollama.local/", model="llama3.2")

    result = handler.check_connection()

    assert result["status"] == "active"
    assert result["endpoint"] == "http://ollama.local"
    assert result["model"] == "llama3.2"
    assert captured == {"method": "GET", "timeout": 2}


def test_connection_accepts_ollama_default_latest_tag(monkeypatch):
    def fake_urlopen(request, timeout):
        assert request.get_method() == "GET"
        assert timeout == 2
        return FakeResponse({"models": [{"name": "llama3.2:latest"}]})

    monkeypatch.setattr(
        "ollama_engine.urlopen",
        fake_urlopen,
    )

    result = OllamaEngineHandler(model="llama3.2").check_connection()

    assert result["status"] == "active"
    assert result["available_models"] == ["llama3.2:latest"]


def test_connection_distinguishes_missing_model_from_unreachable_daemon(monkeypatch):
    monkeypatch.setattr(
        "ollama_engine.urlopen",
        lambda request, timeout: FakeResponse({"models": []})
        if request.get_method() == "GET" and timeout == 2
        else None,
    )
    result = OllamaEngineHandler(model="llama3.2").check_connection()
    assert result["status"] == "model_unavailable"
    assert result["available_models"] == []


def test_inference_posts_project_context_to_local_api(monkeypatch, tmp_path):
    (tmp_path / "main.py").write_text("print('project code')", encoding="utf-8")
    captured = {}

    def fake_urlopen(request, timeout):
        captured["url"] = request.full_url
        captured["body"] = json.loads(request.data)
        captured["timeout"] = timeout
        return FakeResponse({"response": "hello"})

    monkeypatch.setattr("ollama_engine.urlopen", fake_urlopen)
    result = OllamaEngineHandler(model="llama3.2", project_root=tmp_path).handle(
        {"action": "generate", "prompt": "say hello"}
    )
    assert result["status"] == "active"
    assert result["response"] == "hello"
    assert captured["url"] == "http://localhost:11434/api/generate"
    assert captured["body"]["model"] == "llama3.2"
    assert "--- main.py ---\nprint('project code')" in captured["body"]["prompt"]
    assert "say hello" in captured["body"]["prompt"]
    assert captured["body"]["stream"] is False
    assert captured["timeout"] == 10


def test_inference_failure_is_explicit_not_simulation_success(monkeypatch):
    from urllib.error import URLError

    def fail_urlopen(request, timeout):
        assert request.full_url.endswith("/api/generate")
        assert timeout == 10
        raise URLError("connection refused")

    monkeypatch.setattr("ollama_engine.urlopen", fail_urlopen)
    result = OllamaEngineHandler().handle(
        {"action": "generate", "prompt": "hello"}
    )
    assert result["status"] == "unavailable"
    assert "no response was generated" in result["message"]


def test_unsupported_action_is_rejected():
    result = OllamaEngineHandler().handle({"action": "restart"})
    assert result == {
        "status": "invalid_action",
        "action": "restart",
        "message": "Unsupported Ollama action 'restart'.",
    }
