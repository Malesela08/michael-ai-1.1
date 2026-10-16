import json
from pathlib import Path
from datetime import datetime

class DomainAgentCoordinator:
    """Specialized domain agents handling property and vehicle defense using local threat intelligence."""
    
    def __init__(self, threat_intel_path="threat_intelligence.json"):
        self.threat_intel = self._load_threat_intelligence(threat_intel_path)
        print("🧠 Domain Agents initialized with South African Threat Intelligence profile.")

    def _load_threat_intelligence(self, path):
        intel_file = Path(path)
        if intel_file.exists():
            with open(intel_file, "r") as f:
                return json.load(f)
        return {"primary_threats": []}

    def evaluate_vehicle_and_perimeter(self, source, event_type):
        current_hour = datetime.now().hour
        threat_level = "NORMAL"
        
        # Check if current time falls within South African peak hijacking windows (6-9 or 18-21)
        if (6 <= current_hour <= 9) or (18 <= current_hour <= 21):
            threat_level = "ELEVATED_PEAK_WINDOW"
            print(f"⚠️ [THREAT ALERT]: Current hour ({current_hour}:00) matches SA peak threat window!")

        return {
            "source": source,
            "event_type": event_type,
            "threat_level": threat_level,
            "action_recommended": "Engage active camera tracking & secure perimeter gates"
        }

if __name__ == "__main__":
    agent = DomainAgentCoordinator()
    result = agent.evaluate_vehicle_and_perimeter("Tapo_C200_Perimeter", "GATE_MOTION_DETECTED")
    print(json.dumps(result, indent=2))
