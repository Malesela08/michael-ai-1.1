import os
import sys
import json

BRAIN_HOME = "/data/data/com.termux/files/home/AVPS_CORE/brain/"
REGISTRY_FILE = os.path.join(BRAIN_HOME, "property_registry.json")

def get_registry():
    if os.path.exists(REGISTRY_FILE):
        with open(REGISTRY_FILE, 'r') as f:
            return json.load(f)
    return {}

def get_angel_guidance(text):
    command = text.lower().strip()
    registry = get_registry()
    
    if "register" in command:
        parts = command.split()
        if len(parts) >= 3:
            registry[parts[1]] = parts[2]
            with open(REGISTRY_FILE, 'w') as f:
                json.dump(registry, f, indent=4)
            return f"Angel: Registered {parts[1]}."
        return "Angel: Format: register [Name] [Path]"
    
    if "find" in command or "where" in command:
        parts = command.split()
        if len(parts) >= 2:
            prop = parts[1]
            path = registry.get(prop)
            return f"Angel: {prop} is located at: {path}" if path else "Angel: Property not found in registry."
        return "Angel: Search for what property?"
    
    return f"Angel: Monitoring active. Received: {text}"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(get_angel_guidance(sys.argv[1]))
    else:
        print("Angel: Ready to manage your database.")
