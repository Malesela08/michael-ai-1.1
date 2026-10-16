# Master Execution Loop for Michael AI
# "Autonomous Edge Security, Multi-Agency Dispatch & Victim Safe Zone Routing"

from agents.provincial_threats import get_provincial_threat_level
from agents.zero_tolerance import enforce_zero_tolerance
from agents.self_learning import evaluate_adaptive_threat
from agents.protection_order import ProtectionOrderMonitor, evaluate_public_protection_order
from agents.database_logger import MichaelTelemetryDB

def run_michael_ai_cycle():
    print("🛡️ Initializing Michael AI Public Space Protection & Safe Zone Guidance Cycle...")
    
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
    
    # SIMULATION: Public space detection 1.2 km away from victim
    detected_face = "FACE_TARGET_RESTRAINED"
    public_location = "MAMELODI_CENTRAL_TRANSIT_HUB"
    gps_coords = "-25.7231,28.3711"
    current_distance_km = 1.2
    
    # 1. Evaluate Breach, Dispatch Emergency Telemetry, & Generate Safe Route
    public_assessment = evaluate_public_protection_order(
        detected_face_id=detected_face,
        location_name=public_location,
        gps_coords=gps_coords,
        current_distance_km=current_distance_km
    )
    
    print(f"{public_assessment['message']}")
    
    if public_assessment.get("safe_zone"):
        sz = public_assessment["safe_zone"]
        print(f"🗺️ [VICTIM SAFE ROUTING] Threat approaching ({current_distance_km} km)! Immediate evacuation directed to:")
        print(f"   📍 Safe Haven: {sz['name']} ({sz['type']})")
        print(f"   📏 Distance to Safe Zone: {sz['distance_km']} km | Status: {sz['status']}")
    
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
    
    # 4. Immutably Log Evidence
    db.log_threat(
        event_type=event_type,
        severity=severity,
        action_taken=f"{defense_action['action']} [Routed to: {public_assessment['safe_zone']['name']} | SAPS/GBVF Dispatched]",
        evidence_status="SEALED_CHAIN_OF_CUSTODY_PUBLIC_EVIDENCE_POPIA_COMPLIANT"
    )
    
    print("✅ Public space GBVF defense & victim safe-routing cycle completed successfully.")

if __name__ == "__main__":
    run_michael_ai_cycle()
