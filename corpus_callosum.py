import queue
from maintenance_crew import maintenance_crew

class CorpusCallosum:
    def __init__(self):
        self.message_bus = queue.Queue()

    def send_signal(self, sender, data):
        self.message_bus.put({"from": sender, "payload": data})
        with open("blackbox.log", "a") as log:
            log.write(f"SIGNAL_LOG: {sender} -> {data}\n")
        print(f"[Bridge] Signal passed to Cruncher & archived in Blackbox.")

    def trigger_maintenance(self):
        print("[Bridge] Summoning Maintenance Crew...")
        return maintenance_crew.kickoff()

    def receive_signal(self):
        if not self.message_bus.empty():
            return self.message_bus.get()
        return None

bridge = CorpusCallosum()
