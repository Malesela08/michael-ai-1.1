# Master Execution Loop for Michael AI
# "Autonomous Edge Security & Zero-Tolerance Victim Protection"

from agents.provincial_threats import get_provincial_threat_level
from agents.zero_tolerance import enforce_zero_tolerance
from agents.femicide_intelligence import analyze_threat_pattern
from agents.database_logger import MichaelTelemetryDB

def run_michael_ai_cycle():
    print("🛡️ Initializing Michael AI Security Cycle...")
    
    # Initialize database
    db = MichaelTelemetryDB()
    
    # Simulate checking a high-risk provincial context (e.g., Gauteng / The Orchards)
    province = "Gauteng"
    provincial_data = get_provincial_threat_level(province)
    print(f"📍 Region Checked: {province} | Risk Tier: {provincial_data.get('risk_tier')}")
    
    # Simulate an incoming intrusion or emergency event
    event_type = "FORCED_ENTRY"
    severity = "CRITICAL"
    
    # Run Zero-Tolerance Evaluation
    defense_action = enforce_zero_tolerance(event_type, severity)
    print(f"⚡ Zero-Tolerance Directive: {defense_action['action']}")
    
    # Run Historical Pattern Check
    pattern_check = analyze_threat_pattern(event_type, severity_score=9)
    print(f"🧠 Intelligence Analysis: {pattern_check['status']}")
    
    # Log event immutably to SQLite database
    db.log_threat(
        event_type=event_type,
        severity=severity,
        action_taken=defense_action['action'],
        evidence_status="ENCRYPTED_LOCAL_POPIA_COMPLIANT"
    )
    
    print("✅ Security cycle completed successfully. All telemetry secured.")

if __name__ == "__main__":
    run_michael_ai_cycle()
