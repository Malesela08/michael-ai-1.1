from unittest.mock import patch

from src.core.config import DEFAULT_MODEL, OLLAMA_HOST
from src.core.ollama_client import query_ollama


@patch("src.core.ollama_client.requests.post")
def test_twin_inference_mock(mock_post):
    mock_response = mock_post.return_value
    mock_response.json.return_value = {"response": "Mocked AI response"}

    result = query_ollama("test")

    assert result == "Mocked AI response"
    mock_post.assert_called_once_with(
        f"{OLLAMA_HOST}/api/generate",
        json={"model": DEFAULT_MODEL, "prompt": "test", "stream": False},
        timeout=30,
    )
