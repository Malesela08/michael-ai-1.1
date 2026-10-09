import requests

from src.core.config import DEFAULT_MODEL, OLLAMA_HOST

# Define the local Ollama API endpoint for generation
url = f"{OLLAMA_HOST}/api/generate"

# Configure the payload with Llama 3.2 and a test prompt
payload = {
    "model": DEFAULT_MODEL,
    "prompt": "System test online. Reply with OK.",
    "stream": False
}

print("Sending request to local Llama 3.2 model...")
response = requests.post(url, json=payload, timeout=30)

# Check for a successful HTTP 200 response
if response.status_code == 200:
    print("Success! Response from Llama 3.2:")
    print(response.json().get("response"))
else:
    print(f"Error: {response.status_code} - {response.text}")
