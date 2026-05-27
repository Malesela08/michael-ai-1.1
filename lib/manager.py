import sys
# Pointing to the new location inside lib/assets
sys.path.append('./lib/assets/brain')
sys.path.append('./lib/assets/intelligence')
sys.path.append('./lib/assets/guardian_crew')

class IntelligenceManager:
    def __init__(self):
        self.modules = {
            "SNN_CORE": "Ready",
            "LLM_LOGIC": "Ready",
            "AGENT_CREW": "Ready"
        }
    def status(self):
        return self.modules
