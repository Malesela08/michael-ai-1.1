import json
new_task = {"task": "stealth_scan", "action": "activate_sdr_brain"}
with open('/data/data/com.termux/files/home/AVPS_CORE/system_map.json', 'w') as f:
    json.dump(new_task, f)
print("✅ New task injected.")
