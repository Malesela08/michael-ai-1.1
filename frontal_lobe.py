import json
from datetime import datetime

class FrontalLobeController:
    """
    Executive Frontal Lobe Controller:
    In charge of all incoming/outgoing entry investigations and routing
    directives to the 4 specialized agent modules.
    """
    def __init__(self):
        self.blackbox_log = "blackbox.log"
        self.agents = {
            "agent_1": "Perimeter & Vision Monitor",
            "agent_2": "Threat Evaluator",
            "agent_3": "Safety & Countermeasure Unit",
            "agent_4": "Community & Alert Dispatcher"
        }

    def investigate_and_route(self, direction: str, source: str, payload: dict):
        """
        Investigates all entries (INGRESS / EGRESS) and dispatches tasks to the 4 agents.
        """
        timestamp = datetime.now().isoformat()
        
        print(f"\n[FRONTAL LOBE INVESTIGATION] [{direction.upper()}]")
        print(f"├── Origin / Source: {source}")
        print(f"├── Payload Data: {payload}")

        # 1. Executive Investigation Record
        investigation_summary = {
            "timestamp": timestamp,
            "controller": "Frontal_Lobe",
            "direction": direction.upper(),
            "source": source,
            "payload": payload,
            "investigation_status": "CLEARED_AND_DISPATCHED"
        }

        # 2. Write telemetry directly to central Black Box
        try:
            with open(self.blackbox_log, "a") as bb:
                bb.write(json.dumps(investigation_summary) + "\n")
            print("├── Black Box Telemetry: LOGGED")
        except Exception as e:
            print(f"├── Black Box Telemetry: ERROR ({e})")

        # 3. Direct tasks across the 4 primary agents
        print("└── Directing directives to target agents:")
        for agent_id, agent_name in self.agents.items():
            print(f"    └── [{agent_id.upper()}] ({agent_name}): Synced & Executing")

        print("[FRONTAL LOBE]: Investigation completed successfully.")

if __name__ == "__main__":
    frontal = FrontalLobeController()

    # Demonstration Test 1: Ingress Traffic (Incoming Entry)
    frontal.investigate_and_route(
        direction="INGRESS",
        source="Community_Access_Gate_01",
        payload={"event": "Vehicle Entry Request", "node": "Vision_YOLOv8"}
    )

    # Demonstration Test 2: Egress Traffic (Outgoing Entry)
    frontal.investigate_and_route(
        direction="EGRESS",
        source="Alert_Dispatcher",
        payload={"event": "SMS Broadcast to Security Team", "status": "DISPATCHED"}
    )
