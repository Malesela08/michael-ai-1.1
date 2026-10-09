from collections.abc import Callable


def run_main_intelligence(
    system_status: str, activate_emergency_shutdown: Callable[[], None]
) -> None:
    if system_status == "EMERGENCY_SHUTDOWN":
        activate_emergency_shutdown()
        return

    # Threat detection continues in the coordinator.
