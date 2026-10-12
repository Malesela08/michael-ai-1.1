from ollama_client import OllamaClient


def test_generate_sends_project_context_to_configured_local_model(monkeypatch, tmp_path):
    (tmp_path / "main.py").write_text("print('project code')", encoding="utf-8")
    captured = {}

    class FakeResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {"response": "answer"}

    def fake_post(url, json, timeout):
        captured.update(url=url, payload=json, timeout=timeout)
        return FakeResponse()

    monkeypatch.setattr("ollama_client.requests.post", fake_post)
    client = OllamaClient(project_root=tmp_path)

    result = client.generate("Explain this project")

    assert result == {"response": "answer"}
    assert captured["url"] == "http://localhost:11434/api/generate"
    assert captured["payload"]["model"] == "llama3.2"
    assert "--- main.py ---\nprint('project code')" in captured["payload"]["prompt"]
    assert "Explain this project" in captured["payload"]["prompt"]
