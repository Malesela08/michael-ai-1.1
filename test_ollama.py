import requests

def test_ollama_inference():
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "llama3.2:1b",
        "prompt": "System test online. Reply with OK.",
        "stream": False
    }
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        if response.status_code == 200:
            result = response.json()
            print("Status: 200 OK")
            print("Model Response:", result.get("response", "").strip())
        else:
            print(f"Error: Received status code {response.status_code}")
            print(response.text)
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to Ollama. Ensure the server is running.")

if __name__ == "__main__":
    test_ollama_inference()
