import json
from datetime import datetime

class HumanInTheLoopDispatcher:
    """
    Human-in-the-Loop (HITL) Protocol:
    Triggers when an entry is unverified, lacks an appointment, or appears suspicious,
    alerting on-site human security instead of firing false alarms.
    """
    def __init__(self):
        self.blackbox_log = "blackbox.log"

    def evaluate_visitor(self, visitor_name: str, has_appointment: bool, suspicious_behavior: bool):
        timestamp = datetime.now().isoformat()
        
        print(f"\n[HITL EVALUATION] Visitor: {visitor_name}")
        print(f"├── Appointment Status: {has_appointment}")
        print(f"├── Suspicious Indicators: {suspicious_behavior}")

        if not has_appointment or suspicious_behavior:
            action = "ALERT_HUMAN_SECURITY"
            message = f"SECURITY ALERT: Unexpected/suspicious visitor '{visitor_name}' detected at gate. Human verification required."
            print(f"└── [ACTION]: {message}")
        else:
            action = "AUTO_CLEARED"
            message = f"Visitor '{visitor_name}' verified with active appointment. Access granted."
            print(f"└── [ACTION]: {message}")

        log_entry = {
            "timestamp": timestamp,
            "module": "Human_In_The_Loop",
            "visitor": visitor_name,
            "has_appointment": has_appointment,
            "suspicious_behavior": suspicious_behavior,
            "action_taken": action
        }

        try:
            with open(self.blackbox_log, "a") as bb:
                bb.write(json.dumps(log_entry) + "\n")
            print("└── [BLACKBOX]: HITL telemetry recorded.")
        except Exception as e:
            print(f"└── [BLACKBOX ERROR]: {e}")

if __name__ == "__main__":
    hitl = HumanInTheLoopDispatcher()

    # Test Case 1: Expected visitor with an appointment
    hitl.evaluate_visitor(visitor_name="Delivery Service", has_appointment=True, suspicious_behavior=False)

    # Test Case 2: Unexpected/suspicious visitor (Triggers Human Security)
    hitl.evaluate_visitor(visitor_name="Unknown Individual", has_appointment=False, suspicious_behavior=True)
