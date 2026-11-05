import os
import json
from rt_detr_perception import RTDETRPerception

class InvestigationRoom:
    def __init__(self):
        self.perception = RTDETRPerception()
        os.makedirs("michael_ai/investigation_room", exist_ok=True)

    def analyze_frontal_lobe_feed(self, frame_data=None):
        print("🧠 [Investigation Room] Engaging Frontal Lobe Perception...")
        results = self.perception.detect_threats(frame_data)
        
        # Log findings to Investigation Room workspace
        log_path = "michael_ai/investigation_room/frontal_lobe_log.json"
        with open(log_path, "w") as f:
            json.dump(results, f, indent=4)
            
        print(f"✅ Threat analysis logged to {log_path}")
        return results

if __name__ == "__main__":
    room = InvestigationRoom()
    print(room.analyze_frontal_lobe_feed())
