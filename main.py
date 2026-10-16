# Master Execution Loop for Michael AI
# "Autonomous Edge Security, Zero-Tolerance & Protection Order Proximity Tracking"

from agents.provincial_threats import get_provincial_threat_level
from agents.zero_tolerance import enforce_zero_tolerance
from agents.self_learning import evaluate_adaptive_threat
from agents.protection_order import ProtectionOrderMonitor, evaluate_protection_order_face
from agents.database_logger import MichaelTelemetryDB

def run_michael_ai_cycle():
    print("🛡️ Initializing Michael AI Facial Proximity & Protection Order Cycle...")
    
    db = MichaelTelemetryDB()
    po_monitor = ProtectionOrderMonitor()
    
    po_monitor.register_protection_order(
        order_id="PO-2026-9901",
        restrained_name="Restrained Entity",
        face_id="FACE_TARGET_RESTRAINED",
        min_distance_km=5.0
    )
    
    province = "Gauteng"
    provincial_data = get_provincial_threat_level(province)
    print(f"📍 Region Checked: {province} | Risk Tier: {provincial_data.get('risk_tier')}")
    
    detected_face = "FACE_TARGET_RESTRAINED"
    entry_zone = "PERIMETER_ENTRY_CAMERA"
    current_distance_km = 2.5
    
    proximity_assessment = evaluate_protection_order_face(
        detected_face_id=detected_face,
        zone=entry_zone,
        current_distance_km=current_distance_km
    )
    
    print(f"{proximity_assessment['message']}")
    print(f"📍 Distance to Victim: {proximity_assessment['distance_km']} km | Status: {proximity_assessment['status']}")
    
    if proximity_assessment["matched"]:
        event_type = f"PROTECTION_ORDER_{proximity_assessment['status']}"
        severity = "CRITICAL" if proximity_assessment["status"] == "CRITICAL_BREACH_AT_ENTRY" else "HIGH"
    else:
        event_type = "STANDARD_MONITORING"
        severity = "LOW"

    adaptive_check = evaluate_adaptive_threat(event_type, severity)
    print(f"🧠 Adaptive Intelligence Check: {adaptive_check['status']}")
    
    defense_action = enforce_zero_tolerance(event_type, severity)
    print(f"⚡ Zero-Tolerance Directive: {defense_action['action']}")
    
    db.log_threat(
        event_type=event_type,
        severity=severity,
        action_taken=f"{defense_action['action']} [Distance: {proximity_assessment['distance_km']} km]",
        evidence_status="SEALED_COURT_EVIDENCE_POPIA_COMPLIANT"
    )
    
    print("✅ Facial recognition & distance proximity cycle completed successfully.")

if __name__ == "__main__":
    run_michael_ai_cycle()
