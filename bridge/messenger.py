# bridge/messenger.py
# The Voice: This module handles external police and SMS notifications.


def dispatch_emergency_alert(location, threat_level):
    """
    Handles the transmission of emergency data to authorities.
    This is the final exit point of the Guardian Angel AI.
    """
    print(f"BRIDGE: Initiating emergency protocol for {location}...")

    # Logic to interface with SMS/Data gateway for South African emergency services
    alert_payload = {
        "location": location,
        "threat_level": threat_level,
        "timestamp": "auto-generated",
    }

    # Placeholder for actual API call
    return f"Alert sent for {location}."


def send_live_video_link(video_url, police_unit_id):
    """Bridge for streaming drone investigation footage to police units."""
    print(f"BRIDGE: Relaying live aerial feed to Unit: {police_unit_id}")


# bridge/messenger.py


def communicate_client_alert(client_id, threat_type):
    """
    Phase 1: Immediate Advisor.
    The AI alerts the client and provides tactical advice
    instead of calling the police immediately.
    """
    print(f"BRIDGE: Alerting client {client_id}. Threat: {threat_type}")
    advice = "STAY CALM. Make 3 sharp turns to verify if you are being followed."
    return advice


def escalate_to_security(client_id, location):
    """
    Phase 2: Emergency Dispatcher.
    Only called if the threat persists after client turns.
    """
    print(f"BRIDGE: Client escalation initiated. Contacting Police for {location}")
    # Integration for automated police SMS dispatch


# brain/coordinator.py


def monitor_threat_escalation(client_data):
    if threat_verified:
        # Phase 1: Advise before Police
        advice = bridge.messenger.communicate_client_alert(client_id, "Potential Tail")
        print(f"Main AI Action: Provided evasion advice to client: {advice}")

        # Wait for feedback or sensor confirmation after client attempts turns
        if threat_continues:
            # Phase 2: Only now trigger police
            bridge.messenger.escalate_to_security(client_id, current_location)
