import ollama

from src.core.config import DEFAULT_MODEL

MODEL_NAME = DEFAULT_MODEL

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
        return "Unable to generate tactical advice because the Ollama request failed."

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
