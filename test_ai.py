from llamafile_client import LlamafileClient

result = LlamafileClient().generate("System check status.")

if result["status"] != "active":
    raise SystemExit(result.get("message", "Local brain returned no response."))

print(result["response"])
