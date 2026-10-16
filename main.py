# Master Execution Loop for Michael AI
# "Autonomous Edge Security, Zero-Tolerance, Firearm Detection & Micro-Burst Defense"

from agents.provincial_threats import get_provincial_threat_level
from agents.zero_tolerance import enforce_zero_tolerance
from agents.self_learning import evaluate_adaptive_threat
from agents.recon_intelligence import evaluate_recon_threat
from agents.firearm_detection import evaluate_frame_for_weapons
from agents.database_logger import MichaelTelemetryDB

def run_michael_ai_cycle():
    print("🛡️ Initializing Michael AI Defense, Firearm & Micro-Burst Analysis Cycle...")
    
    db = MichaelTelemetryDB()
    province = "Gauteng"
    provincial_data = get_provincial_threat_level(province)
    print(f"📍 Region Checked: {province} | Risk Tier: {provincial_data.get('risk_tier')}")
    
    # Simulate Camera Optical Stream Detection (e.g., Tapo / Jetson Vision Frame)
    simulated_vision_frame = [
        {"label": "person", "confidence": 0.92},
        {"label": "handgun", "confidence": 0.89}
    ]
    frame_zone = "DRIVEWAY_ENTRANCE"
    
    # 1. Evaluate Vision Stream for Firearms
    weapon_assessment = evaluate_frame_for_weapons(
        frame_id="FRAME_109822",
        detected_objects=simulated_vision_frame,
        zone=frame_zone
    )
    
    if weapon_assessment["firearm_detected"]:
        print(f"🔫 [WEAPON CONFIRMED] Type: {weapon_assessment['weapon_type'].upper()} | Confidence: {weapon_assessment['confidence']*100:.1f}%")
        print(f"⚡ Action: {weapon_assessment['action']}")
        event_type = "ARMED_ROBBERY"
        severity = "CRITICAL"
    else:
        # Fallback to Pre-Attack Recon
        recon_assessment = evaluate_recon_threat("UNKNOWN_VEHICLE", frame_zone, dwell_time_minutes=5, follows_target=True)
        event_type = "PERIMETER_PROBE"
        severity = "HIGH"

    # 2. Adaptive Intelligence Check
    adaptive_check = evaluate_adaptive_threat(event_type, severity)
    print(f"🧠 Adaptive Intelligence Check: {adaptive_check['status']}")
    
    # 3. Enforce Zero-Tolerance Directive
    defense_action = enforce_zero_tolerance(event_type, severity)
    print(f"⚡ Zero-Tolerance Directive: {defense_action['action']}")
    
    # 4. Immutably Log Telemetry to Local SQLite
    db.log_threat(
        event_type=f"VISUAL_DETECTION_{event_type}",
        severity=severity,
        action_taken=f"{defense_action['action']} [Weapon: {weapon_assessment.get('weapon_type', 'NONE')}]",
        evidence_status="ENCRYPTED_LOCAL_POPIA_COMPLIANT"
    )
    
    print("✅ Firearm detection and active defense security cycle completed successfully.")

if __name__ == "__main__":
    run_michael_ai_cycle()
