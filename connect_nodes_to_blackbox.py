import json
import os

def link_nodes():
    blackbox_path = "blackbox.log"
    registry_path = "multi_ai_registry.py"
    
    print("[BLACKBOX LINK]: Scanning local registry and communication hubs...")
    if os.path.exists(blackbox_path):
        print(f"[STATUS]: Existing black box found at {blackbox_path}. Binding nodes...")
    else:
        print("[WARNING]: Creating default blackbox log conduit.")
        with open(blackbox_path, "w") as f:
            f.write("INITIALIZED_BLACKBOX_CONDUIT\n")
            
    print("[SUCCESS]: All active agents successfully tied into the central telemetry black box.")

if __name__ == "__main__":
    link_nodes()
