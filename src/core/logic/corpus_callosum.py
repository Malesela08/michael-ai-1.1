import queue

import ollama

from src.core.config import DEFAULT_MODEL
from src.core.logic.maintenance_crew import maintenance_crew
from src.core.logic.system_persona import get_system_prompt


class CorpusCallosum:
    def __init__(self):
        self.message_bus = queue.Queue()

    def query_model(self, prompt, model_name=DEFAULT_MODEL):
        response = ollama.chat(
            model=model_name,
            messages=[
                {"role": "system", "content": get_system_prompt()},
                {"role": "user", "content": prompt},
            ],
        )
        return response["message"]["content"]

    def send_signal(self, sender, data):
        payload = {"from": sender, "payload": data}
        self.message_bus.put(payload)
        with open("blackbox.log", "a") as log:
            log.write(f"SIGNAL_LOG: {sender} -> {data}\n")
        print("[Bridge] Signal passed to Cruncher & archived in Blackbox.")
        return payload

    def trigger_maintenance(self):
        print("[Bridge] Summoning Maintenance Crew...")
        return maintenance_crew.kickoff()

    def receive_signal(self):
        if not self.message_bus.empty():
            return self.message_bus.get()
        return None


bridge = CorpusCallosum()
