# brain/coordinator.py
from safety.kill_switch import activate_emergency_shutdown


def run_main_intelligence():
    # 1. ALWAYS check safety first
    if system_status == "EMERGENCY_SHUTDOWN":
        activate_emergency_shutdown()
        return  # Stop everything immediately

    # ... proceed to threat detection ...
