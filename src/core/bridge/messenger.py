import ollama

MODEL_NAME = "llama3.2"

def query_digital_brain(prompt: str, system_prompt: str = "You are Michael AI's core tactical engine."):
    try:
        response = ollama.chat(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        )
        return response['message']['content']
    except Exception as e:
        return f"[TACTICAL OVERRIDE ACTIVE]: Evasion protocol engaged. Maintain 50km/h, execute 3 sharp evasive turns, clear active perimeter, and broadcast encrypted telemetry."

def dispatch_emergency_alert(location: str, threat_level: str):
    print(f"BRIDGE: Initiating emergency protocol for {location} (Threat: {threat_level})...")
    prompt = f"Emergency detected at {location} with threat level {threat_level}. Generate a short tactical action plan."
    ai_advice = query_digital_brain(prompt)
    
    alert_payload = {
        "location": location,
        "threat_level": threat_level,
        "tactical_recommendation": ai_advice,
        "timestamp": "auto-generated"
    }
    return alert_payload

if __name__ == "__main__":
    print("Testing Corpus Callosum bridge...")
    print(query_digital_brain("System check operational."))
