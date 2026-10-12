import pytest

from llamafile_client import LlamafileClient


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def raise_for_status(self):
        pass

    def json(self):
        return self.payload


def test_generate_sends_openai_compatible_chat_request(monkeypatch):
    captured = {}

    def fake_post(url, json, timeout):
        captured.update(url=url, payload=json, timeout=timeout)
        return FakeResponse(
            {"choices": [{"message": {"content": "Local model response"}}]}
        )

    monkeypatch.setattr("llamafile_client.requests.post", fake_post)
    result = LlamafileClient().generate("Summarize the system.")

    assert result == {
        "status": "active",
        "model": "local-model",
        "response": "Local model response",
    }
    assert captured == {
        "url": "http://127.0.0.1:8080/v1/chat/completions",
        "payload": {
            "model": "local-model",
            "messages": [{"role": "user", "content": "Summarize the system."}],
            "stream": False,
        },
        "timeout": 120,
    }


def test_generate_reports_unavailable_server(monkeypatch):
    import requests

    def fail_post(*_args, **_kwargs):
        raise requests.ConnectionError("connection refused")

    monkeypatch.setattr("llamafile_client.requests.post", fail_post)
    result = LlamafileClient().generate("hello")

    assert result["status"] == "unavailable"
    assert "connection refused" in result["message"]


def test_generate_reports_invalid_response_shape(monkeypatch):
    monkeypatch.setattr(
        "llamafile_client.requests.post",
        lambda *_args, **_kwargs: FakeResponse({"choices": []}),
    )

    assert LlamafileClient().generate("hello") == {
        "status": "error",
        "message": "Local llamafile returned no completion choices.",
    }


def test_client_configuration_can_be_overridden(monkeypatch):
    monkeypatch.setenv("LLAMAFILE_BASE_URL", "http://localhost:9000/v1/")
    monkeypatch.setenv("LLAMAFILE_MODEL", "selected-local-model")

    client = LlamafileClient()

    assert client.base_url == "http://localhost:9000/v1"
    assert client.model == "selected-local-model"


def test_client_rejects_non_local_api_endpoint():
    with pytest.raises(ValueError, match="localhost or a loopback IP"):
        LlamafileClient(base_url="https://api.example.com/v1")
