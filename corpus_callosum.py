import json
import logging
import re
from typing import Any, Callable

from ollama_client import OllamaClient

logging.basicConfig(level=logging.INFO, format="[CorpusCallosum:%(levelname)s] %(message)s")


def check_perimeter(zone: str = "North") -> dict[str, Any]:
    """Report perimeter status when no live camera/sensor provider is configured."""
    return {
        "status": "unavailable",
        "zone": zone,
        "cameras_active": None,
        "alerts": None,
        "message": "No live perimeter camera or sensor provider is configured.",
    }


class CorpusCallosum:
    def __init__(self, model: str = "llama3.2"):
        self.ollama = OllamaClient(default_model=model)
        self.tools: dict[str, dict[str, Any]] = {}
        self.register_mcp_tool(
            name="check_perimeter",
            description="Checks physical security and camera status for a perimeter zone.",
            handler=check_perimeter,
        )
        logging.info("Corpus Callosum bridge initialized. Neural pathways active.")

    def register_mcp_tool(self, name: str, description: str, handler: Callable):
        """Register a local MCP tool function that agents can invoke."""
        self.tools[name] = {
            "description": description,
            "handler": handler
        }
        logging.info(f"Registered MCP Tool: '{name}' -> {description}")

    def get_tool_manifest(self) -> list[dict[str, str]]:
        """Return a manifest of all available tools for agent awareness."""
        return [{"name": name, "info": data["description"]} for name, data in self.tools.items()]

    def route_intent(self, agent_prompt: str) -> dict[str, Any]:
        """
        Dispatch known perimeter requests directly; use Ollama for other intents.
        """
        if re.search(r"\b(water|meter|utility)\b", agent_prompt, re.IGNORECASE):
            if "check_water_meter" not in self.tools:
                return {
                    "status": "error",
                    "message": "No water-meter tool is registered.",
                }
            return self._dispatch_tool("check_water_meter", {})

        zone_match = re.search(r"\b(north|south|east|west)\b", agent_prompt, re.IGNORECASE)
        if re.search(r"\b(perimeter|camera|cameras)\b", agent_prompt, re.IGNORECASE):
            if "check_perimeter" not in self.tools:
                return {
                    "status": "error",
                    "message": "No perimeter camera tool is registered.",
                }
            zone = zone_match.group(1).title() if zone_match else "unspecified"
            return self._dispatch_tool("check_perimeter", {"zone": zone})

        manifest = json.dumps(self.get_tool_manifest(), indent=2)
        
        system_prompt = (
            "You are the Corpus Callosum, the central coordination bridge for Michael AI. "
            "You have access to the following local MCP tools:\n"
            f"{manifest}\n\n"
            "Analyze the user prompt. If a tool is required to fulfill the request, "
            "respond strictly in valid JSON format: {\"tool\": \"tool_name\", \"args\": {}}.\n"
            "If no tool is required, respond strictly in valid JSON format: {\"tool\": null, \"response\": \"your text response\"}."
        )

        full_prompt = f"{system_prompt}\n\nUser Request: {agent_prompt}"
        
        result = self.ollama.generate(prompt=full_prompt, timeout=60)
        raw_text = result.get("response")
        
        if not raw_text:
            return {
                "status": "error",
                "message": result.get("error", "Inference failed or timed out."),
            }

        # Clean and parse JSON intent
        try:
            cleaned_text = raw_text.strip()
            if cleaned_text.startswith("```json"):
                cleaned_text = cleaned_text[7:]
            if cleaned_text.endswith("```"):
                cleaned_text = cleaned_text[:-3]
            
            intent = json.loads(cleaned_text.strip())
        except json.JSONDecodeError:
            # Fallback if model conversationalizes output
            return {"status": "success", "routed": False, "response": raw_text}

        tool_name = intent.get("tool")
        if tool_name:
            if tool_name not in self.tools:
                return {"status": "error", "message": f"Unknown tool: {tool_name}"}
            args = intent.get("args", {})
            if not isinstance(args, dict):
                return {"status": "error", "tool": tool_name, "message": "Tool arguments must be a JSON object."}
            return self._dispatch_tool(tool_name, args)

        return {"status": "success", "routed": False, "response": intent.get("response", raw_text)}

    def _dispatch_tool(self, tool_name: str, args: dict[str, Any]) -> dict[str, Any]:
        logging.info(f"Dispatching intent to MCP Tool: {tool_name} with args {args}")
        try:
            tool_output = self.tools[tool_name]["handler"](**args)
        except (TypeError, ValueError) as error:
            return {"status": "error", "tool": tool_name, "message": str(error)}
        return {
            "status": "success",
            "routed": True,
            "tool": tool_name,
            "output": tool_output,
        }

if __name__ == "__main__":
    bridge = CorpusCallosum()

    print("\n--- Testing Corpus Callosum Routing ---")
    test_query = "Run a security check on the North zone perimeter."
    output = bridge.route_intent(test_query)
    print(json.dumps(output, indent=2))
