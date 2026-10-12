from ipaddress import ip_address
import os
from typing import Any
from urllib.parse import urlsplit

import requests


class LlamafileClient:
    """Send text-generation requests to a local llamafile OpenAI-compatible API."""

    def __init__(
        self,
        base_url: str | None = None,
        model: str | None = None,
        timeout: int = 120,
    ) -> None:
        configured_url = (
            base_url or os.getenv("LLAMAFILE_BASE_URL", "http://127.0.0.1:8080/v1")
        ).rstrip("/")
        parsed_url = urlsplit(configured_url)
        hostname = parsed_url.hostname
        try:
            is_loopback = hostname is not None and (
                hostname.lower() == "localhost" or ip_address(hostname).is_loopback
            )
        except ValueError:
            is_loopback = False
        if (
            parsed_url.scheme != "http"
            or parsed_url.username is not None
            or parsed_url.password is not None
            or not is_loopback
        ):
            raise ValueError(
                "LLAMAFILE_BASE_URL must be an HTTP URL on localhost or a loopback IP."
            )

        self.base_url = configured_url
        self.model = model or os.getenv("LLAMAFILE_MODEL", "local-model")
        self.timeout = timeout

    def generate(self, prompt: str) -> dict[str, Any]:
        """Generate a response, reporting server and protocol errors explicitly."""
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                json={
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "stream": False,
                },
                timeout=self.timeout,
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as error:
            return {
                "status": "unavailable",
                "message": f"Local llamafile request failed: {error}",
            }

        try:
            payload = response.json()
        except ValueError:
            return {
                "status": "error",
                "message": "Local llamafile returned an invalid JSON response.",
            }

        if not isinstance(payload, dict):
            return {
                "status": "error",
                "message": "Local llamafile returned an invalid completion response.",
            }

        choices = payload.get("choices")
        if not isinstance(choices, list) or not choices:
            return {
                "status": "error",
                "message": "Local llamafile returned no completion choices.",
            }

        first_choice = choices[0]
        message = first_choice.get("message") if isinstance(first_choice, dict) else None
        content = message.get("content") if isinstance(message, dict) else None
        if not isinstance(content, str):
            return {
                "status": "error",
                "message": "Local llamafile returned an invalid completion message.",
            }

        return {
            "status": "active",
            "model": self.model,
            "response": content,
        }
