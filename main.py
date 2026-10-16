# Master Execution Loop for Michael AI
# "Autonomous Edge Security, Zero-Tolerance & Adaptive Self-Learning"

from agents.provincial_threats import get_provincial_threat_level
from agents.zero_tolerance import enforce_zero_tolerance
from agents.femicide_intelligence import analyze_threat_pattern
from agents.self_learning import evaluate_adaptive_threat
from agents.database_logger import MichaelTelemetryDB

def run_michael_ai_cycle():
    print("🛡️ Initializing Michael AI Adaptive Security Cycle...")
    
    # Initialize database
    db = MichaelTelemetryDB()
    
    # 1. Check Provincial Threat Context (e.g., Gauteng)
    province = "Gauteng"
    provincial_data = get_provincial_threat_level(province)
    print(f"📍 Region Checked: {province} | Risk Tier: {provincial_data.get('risk_tier')}")
    
    # 2. Simulate Incoming Threat Event
    event_type = "FORCED_ENTRY"
    severity = "CRITICAL"
    
    # 3. Run Self-Learning & Anti-Trickery Behavioral Analysis
    adaptive_check = evaluate_adaptive_threat(event_type, severity)
    print(f"🧠 Adaptive Learning Analysis: {adaptive_check['status']} | Evasion Risk: {adaptive_check.get('evasion_risk')}")
    
    # 4. Run Zero-Tolerance Evaluation
    defense_action = enforce_zero_tolerance(event_type, severity)
    print(f"⚡ Zero-Tolerance Directive: {defense_action['action']}")
    
    # 5. Run Historical Pattern Check
    pattern_check = analyze_threat_pattern(event_type, severity_score=9)
    print(f"🔍 Historical Pattern Check: {pattern_check['status']}")
    
    # 6. Log event immutably to SQLite database with adaptive status
    db.log_threat(
        event_type=event_type,
        severity=severity,
        action_taken=f"{defense_action['action']} [Adaptive Status: {adaptive_check['status']}]",
        evidence_status="ENCRYPTED_LOCAL_POPIA_COMPLIANT"
    )
    
    print("✅ Adaptive security cycle completed successfully. All telemetry hardened.")

if __name__ == "__main__":
    run_michael_ai_cycle()
