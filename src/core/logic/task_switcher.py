import json

new_task = {"task": "stealth_scan", "action": "activate_sdr_brain"}
with open("system_map.json", "w") as f:
    json.dump(new_task, f)
print("✅ New task injected.")
