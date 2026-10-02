import json
from datetime import datetime

class FrontalLobeController:
    def __init__(self):
        self.blackbox_log = "blackbox.log"
        self.agents = {
            "agent_1": "Perimeter & Vision Monitor",
            "agent_2": "Threat Evaluator",
            "agent_3": "Safety & Countermeasure Unit",
            "agent_4": "Community & Alert Dispatcher"
        }

    def evaluate_visitor_hitl(self, visitor_name: str, has_appointment: bool, suspicious_behavior: bool):
        """
        Human-in-the-Loop filter to prevent false alarms and engage human security when needed.
        """
        if not has_appointment or suspicious_behavior:
            return "ALERT_HUMAN_SECURITY"
        return "AUTO_CLEARED"

    def investigate_and_route(self, direction: str, source: str, payload: dict):
        timestamp = datetime.now().isoformat()
        
        # Check if payload contains visitor details for HITL screening
        visitor_name = payload.get("visitor_name", "Unknown")
        has_appointment = payload.get("has_appointment", True)
        suspicious_behavior = payload.get("suspicious_behavior", False)

        hitl_decision = self.evaluate_visitor_hitl(visitor_name, has_appointment, suspicious_behavior)

        print(f"\n[FRONTAL LOBE INVESTIGATION] [{direction.upper()}]")
        print(f"├── Origin / Source: {source}")
        print(f"├── Payload Data: {payload}")
        print(f"└── HITL Security Decision: {hitl_decision}")

        investigation_summary = {
            "timestamp": timestamp,
            "controller": "Frontal_Lobe",
            "direction": direction.upper(),
            "source": source,
            "payload": payload,
            "hitl_decision": hitl_decision,
            "investigation_status": "CLEARED_AND_DISPATCHED"
        }

        try:
            with open(self.blackbox_log, "a") as bb:
                bb.write(json.dumps(investigation_summary) + "\n")
            print("    └── Black Box Telemetry: LOGGED")
        except Exception as e:
            print(f"    └── Black Box Telemetry: ERROR ({e})")

        # Direct tasks across the 4 primary agents if security action is required
        if hitl_decision == "ALERT_HUMAN_SECURITY":
            print("    └── Dispatching emergency notification to Agent 4 (Community & Alert Dispatcher) for human intervention.")

if __name__ == "__main__":
    frontal = FrontalLobeController()

    # Test 1: Expected visitor
    frontal.investigate_and_route(
        direction="INGRESS",
        source="Gate_01",
        payload={"visitor_name": "Scheduled Contractor", "has_appointment": True, "suspicious_behavior": False}
    )

    # Test 2: Unexpected/Suspicious entry (Engages Human Security)
    frontal.investigate_and_route(
        direction="INGRESS",
        source="Gate_02",
        payload={"visitor_name": "Unregistered Individual", "has_appointment": False, "suspicious_behavior": True}
    )
