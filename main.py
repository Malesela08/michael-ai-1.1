# Master Execution Loop for Michael AI
# "Autonomous Edge Security, Zero-Tolerance, Adaptive Self-Learning & Anti-Reconnaissance"

from agents.provincial_threats import get_provincial_threat_level
from agents.zero_tolerance import enforce_zero_tolerance
from agents.femicide_intelligence import analyze_threat_pattern
from agents.self_learning import evaluate_adaptive_threat
from agents.recon_intelligence import evaluate_recon_threat
from agents.database_logger import MichaelTelemetryDB

def run_michael_ai_cycle():
    print("🛡️ Initializing Michael AI Defense & Recon Analysis Cycle...")
    
    db = MichaelTelemetryDB()
    province = "Gauteng"
    provincial_data = get_provincial_threat_level(province)
    print(f"📍 Region Checked: {province} | Risk Tier: {provincial_data.get('risk_tier')}")
    
    # Simulate Criminal Scouting / Tailing Scenario
    scout_entity = "UNIDENTIFIED_SILVER_SEDAN"
    scout_zone = "PERIMETER_GATE_SOUTH"
    
    # 1. Evaluate Pre-Attack Recon & Tailing
    recon_assessment = evaluate_recon_threat(
        entity_id=scout_entity,
        zone=scout_zone,
        dwell_time_minutes=8,
        follows_target=True
    )
    print(f"🔍 Pre-Attack Recon Score: {recon_assessment['threat_score']} | Status: {recon_assessment['classification']}")
    print(f"🚩 Indicators: {', '.join(recon_assessment['indicators'])}")
    
    # 2. If Recon Classification is Critical, Trigger Zero-Tolerance Early
    if recon_assessment['threat_score'] >= 60:
        event_type = "VEHICLE_HIJACKING"  # Threat escalated prior to attack
        severity = "CRITICAL"
    else:
        event_type = "PERIMETER_PROBE"
        severity = "HIGH"
        
    # 3. Adaptive Self-Learning Analysis
    adaptive_check = evaluate_adaptive_threat(event_type, severity)
    print(f"🧠 Adaptive Intelligence Check: {adaptive_check['status']}")
    
    # 4. Enforce Zero-Tolerance Directive
    defense_action = enforce_zero_tolerance(event_type, severity)
    print(f"⚡ Zero-Tolerance Directive: {defense_action['action']}")
    
    # 5. Immutably Log Telemetry
    db.log_threat(
        event_type=f"RECON_{event_type}",
        severity=severity,
        action_taken=f"{defense_action['action']} [Recon Score: {recon_assessment['threat_score']}]",
        evidence_status="ENCRYPTED_LOCAL_POPIA_COMPLIANT"
    )
    
    print("✅ Pre-attack anti-scouting security cycle executed successfully.")

if __name__ == "__main__":
    run_michael_ai_cycle()
