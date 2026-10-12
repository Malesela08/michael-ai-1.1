from ollama_context import build_project_prompt


def test_prompt_includes_readable_project_files_and_excludes_generated_or_secret_files(
    tmp_path,
):
    (tmp_path / "src").mkdir()
    (tmp_path / "vendor" / "lib").mkdir(parents=True)
    (tmp_path / ".venv" / "lib").mkdir(parents=True)
    (tmp_path / "node_modules" / "pkg").mkdir(parents=True)
    (tmp_path / "src" / "agent.py").write_text("agent implementation", encoding="utf-8")
    (tmp_path / "vendor" / "lib" / "helper.py").write_text(
        "project dependency", encoding="utf-8"
    )
    (tmp_path / "README.md").write_text("project overview", encoding="utf-8")
    (tmp_path / ".env").write_text("TOKEN=do-not-send", encoding="utf-8")
    (tmp_path / "signing.pem").write_text("private key", encoding="utf-8")
    (tmp_path / ".venv" / "lib" / "package.py").write_text("installed code", encoding="utf-8")
    (tmp_path / "node_modules" / "pkg" / "index.js").write_text(
        "installed code", encoding="utf-8"
    )
    (tmp_path / "image.bin").write_bytes(b"\x00\xff")

    result = build_project_prompt("What does the agent do?", tmp_path)

    assert "--- README.md ---\nproject overview" in result
    assert "--- src/agent.py ---\nagent implementation" in result
    assert "--- vendor/lib/helper.py ---\nproject dependency" in result
    assert "<user_request>\nWhat does the agent do?\n</user_request>" in result
    assert "do-not-send" not in result
    assert "private key" not in result
    assert "installed code" not in result


def test_prompt_without_readable_project_files_is_unchanged(tmp_path):
    (tmp_path / "binary.dat").write_bytes(b"\x00\xff")

    assert build_project_prompt("hello", tmp_path) == "hello"
