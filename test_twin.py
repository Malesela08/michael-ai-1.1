import requests
import json

# Define the local Ollama API endpoint for generation
url = "http://localhost:11434/api/generate"

# Configure the payload with Llama 3.2 and a test prompt
payload = {
    "model": "llama3.2",
    "prompt": "System test online. Reply with OK.",
    "stream": False
}

print("Sending request to local Llama 3.2 model...")
response = requests.post(url, json=payload)

# Check for a successful HTTP 200 response
if response.status_code == 200:
    print("Success! Response from Llama 3.2:")
    print(response.json().get("response"))
else:
    print(f"Error: {response.status_code} - {response.text}")
