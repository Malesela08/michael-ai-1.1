# Master Execution Loop for Michael AI
# "Autonomous Edge Security, Zero-Tolerance & Public Space Multi-Agency GBVF Protection"

from agents.provincial_threats import get_provincial_threat_level
from agents.zero_tolerance import enforce_zero_tolerance
from agents.self_learning import evaluate_adaptive_threat
from agents.protection_order import ProtectionOrderMonitor, evaluate_public_protection_order
from agents.database_logger import MichaelTelemetryDB

def run_michael_ai_cycle():
    print("🛡️ Initializing Michael AI Public Space Protection Order & Multi-Agency Dispatch Cycle...")
    
    db = MichaelTelemetryDB()
    po_monitor = ProtectionOrderMonitor()
    
    # Active Protection Order
    po_monitor.register_protection_order(
        order_id="PO-2026-9901",
        restrained_name="Restrained Entity",
        face_id="FACE_TARGET_RESTRAINED",
        min_distance_km=5.0
    )
    
    province = "Gauteng"
    provincial_data = get_provincial_threat_level(province)
    print(f"📍 Region Checked: {province} | Risk Tier: {provincial_data.get('risk_tier')}")
    
    # SIMULATION: Public space camera (e.g. Shopping Mall / Transit Hub) detects restrained individual 1.2 km from victim
    detected_face = "FACE_TARGET_RESTRAINED"
    public_location = "MAMELODI_CENTRAL_TRANSIT_HUB"
    gps_coords = "-25.7231,28.3711"
    current_distance_km = 1.2  # 1.2 km away in public space (Breach of 5 km limit)
    
    # 1. Evaluate Public Space Breach & Execute SAPS/GBVF Dispatches
    public_assessment = evaluate_public_protection_order(
        detected_face_id=detected_face,
        location_name=public_location,
        gps_coords=gps_coords,
        current_distance_km=current_distance_km
    )
    
    print(f"{public_assessment['message']}")
    print(f"📍 Location: {public_assessment['location_name']} | Distance: {public_assessment['distance_km']} km | Status: {public_assessment['status']}")
    
    if public_assessment["matched"]:
        event_type = f"PUBLIC_SPACE_{public_assessment['status']}"
        severity = "CRITICAL"
    else:
        event_type = "PUBLIC_PASSIVE_MONITORING"
        severity = "LOW"

    # 2. Adaptive Intelligence Check
    adaptive_check = evaluate_adaptive_threat(event_type, severity)
    print(f"🧠 Adaptive Intelligence Check: {adaptive_check['status']}")
    
    # 3. Enforce Zero-Tolerance Directive
    defense_action = enforce_zero_tolerance(event_type, severity)
    print(f"⚡ Zero-Tolerance Directive: {defense_action['action']}")
    
    # 4. Immutably Log Telemetry for Law Enforcement & Court Admissibility
    db.log_threat(
        event_type=event_type,
        severity=severity,
        action_taken=f"{defense_action['action']} [SAPS & GBVF Dispatched | Location: {public_location} | Distance: {public_assessment['distance_km']} km]",
        evidence_status="SEALED_CHAIN_OF_CUSTODY_PUBLIC_EVIDENCE_POPIA_COMPLIANT"
    )
    
    print("✅ Public space GBVF & law enforcement dispatch cycle completed successfully.")

if __name__ == "__main__":
    run_michael_ai_cycle()
