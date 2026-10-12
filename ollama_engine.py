import json
import os
import socket
from pathlib import Path
from typing import Any
from urllib.error import URLError
from urllib.request import Request, urlopen

from ollama_context import build_project_prompt


class OllamaEngineHandler:
    """Check and invoke a local Ollama daemon over its HTTP API."""

    def __init__(
        self,
        endpoint: str | None = None,
        model: str | None = None,
        project_root: Path | None = None,
    ) -> None:
        self.endpoint = (
            endpoint or os.getenv("OLLAMA_HOST", "http://localhost:11434")
        ).rstrip("/")
        self.model = model or os.getenv("OLLAMA_MODEL", "llama3.2")
        self.project_root = project_root

    def check_connection(self) -> dict[str, Any]:
        """Report daemon reachability and whether the configured model is present."""
        request = Request(f"{self.endpoint}/api/tags", method="GET")
        try:
            with urlopen(request, timeout=2) as response:
                if response.status != 200:
                    return {
                        "status": "unavailable",
                        "endpoint": self.endpoint,
                        "message": f"Ollama returned HTTP {response.status}.",
                    }
                data = json.loads(response.read().decode("utf-8"))
        except (URLError, TimeoutError, socket.timeout) as error:
            return {
                "status": "unavailable",
                "endpoint": self.endpoint,
                "error": str(error),
                "message": "Ollama daemon offline or unreachable. Start via 'ollama serve'.",
            }
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            return {
                "status": "error",
                "endpoint": self.endpoint,
                "error": str(error),
                "message": "Ollama returned an invalid model-list response.",
            }

        if not isinstance(data, dict):
            return {
                "status": "error",
                "endpoint": self.endpoint,
                "message": "Ollama returned an invalid model-list response.",
            }

        models = [
            model.get("name")
            for model in data.get("models", [])
            if isinstance(model, dict) and isinstance(model.get("name"), str)
        ]
        configured_models = {self.model}
        if ":" not in self.model:
            configured_models.add(f"{self.model}:latest")
        if not configured_models.intersection(models):
            return {
                "status": "model_unavailable",
                "endpoint": self.endpoint,
                "model": self.model,
                "available_models": models,
                "message": "Ollama is reachable, but the configured model is not available.",
            }

        return {
            "status": "active",
            "endpoint": self.endpoint,
            "model": self.model,
            "available_models": models,
            "message": "Local Ollama engine connection and configured model verified.",
        }

    def handle(self, payload: dict[str, Any] | str | None = None) -> dict[str, Any]:
        """Check engine status or execute a real local inference request."""
        action = "status"
        prompt: str | None = None
        if isinstance(payload, dict):
            action = payload.get("action", "status")
            prompt = payload.get("prompt")
        elif isinstance(payload, str):
            prompt = payload
            action = "generate"

        if action != "generate":
            if action == "status":
                return self.check_connection()
            return {
                "status": "invalid_action",
                "action": action,
                "message": f"Unsupported Ollama action '{action}'.",
            }
        if not prompt:
            return self.check_connection()

        request_data = json.dumps(
            {
                "model": self.model,
                "prompt": build_project_prompt(prompt, self.project_root),
                "stream": False,
            }
        ).encode("utf-8")
        request = Request(
            f"{self.endpoint}/api/generate",
            data=request_data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urlopen(request, timeout=10) as response:
                if response.status != 200:
                    return {
                        "status": "error",
                        "endpoint": self.endpoint,
                        "model": self.model,
                        "message": f"Ollama returned HTTP {response.status}.",
                    }
                result = json.loads(response.read().decode("utf-8"))
        except (URLError, TimeoutError, socket.timeout) as error:
            return {
                "status": "unavailable",
                "endpoint": self.endpoint,
                "model": self.model,
                "error": str(error),
                "message": "Ollama inference request failed; no response was generated.",
            }
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            return {
                "status": "error",
                "endpoint": self.endpoint,
                "model": self.model,
                "error": str(error),
                "message": "Ollama returned an invalid inference response.",
            }

        if not isinstance(result, dict):
            return {
                "status": "error",
                "endpoint": self.endpoint,
                "model": self.model,
                "message": "Ollama returned an invalid inference response.",
            }

        generated_response = result.get("response")
        if not isinstance(generated_response, str) or not generated_response:
            return {
                "status": "error",
                "endpoint": self.endpoint,
                "model": self.model,
                "message": "Ollama returned no generated response.",
            }

        return {
            "status": "active",
            "model": self.model,
            "response": generated_response,
            "message": "Inference completed successfully via local Ollama.",
        }
