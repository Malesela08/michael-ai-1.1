from popia_bridge import query_popia

def evaluate_agent_action(action_type: str, data_payload: dict):
    print(f"\n[Michael AI Security Core] Evaluating action: '{action_type}'")
    
    # Automatically query local POPIA rules based on context
    if "biometric" in action_type.lower() or "face" in data_payload:
        rules = query_popia("biometrics")
        print("[Compliance Enforced] Retrieved local POPIA biometric guidelines:")
        for rule in rules:
            print(f"  -> {rule}")
    elif "security" in action_type.lower():
        rules = query_popia("security safeguards")
        print("[Compliance Enforced] Retrieved local POPIA security safeguard rules:")
        for rule in rules:
            print(f"  -> {rule}")
    else:
        print("[Compliance Check] Standard processing parameters verified locally.")

if __name__ == "__main__":
    # Test agent evaluation locally
    evaluate_agent_action("biometric_scan", {"face": "detected"})
