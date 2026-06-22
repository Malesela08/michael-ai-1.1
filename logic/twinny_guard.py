import sys, json
from datetime import datetime
from black_box import on_attack
from ollama import chat

DANGER_WORDS = ["attack", "breach", "hack", "compromised", "leak", "ransom"]

def twinny_guard(message, client_data=None, model='llama3.2:1b'):
    """AI brain + Black Box trigger"""
    
    # 1. Twinny thinks - using your llama3.2
    response = chat(model=model, messages=[{'role': 'user', 'content': message}])
    reply = response['message']['content']
    
    # 2. Scan for danger
    msg_lower = message.lower()
    if any(word in msg_lower for word in DANGER_WORDS):
        if client_data:
            print("🚨 DANGER DETECTED - BLACK BOX ACTIVATED")
            backup = on_attack(client_data['name'], client_data)
            reply += f"\n\n⚫️ Black Box triggered. Data backed up to: {backup}"
        else:
            reply += "\n\n⚠️ Attack detected but no client_data provided"
    
    return reply

if __name__ == "__main__":
    # Test with llama3.2:1b - fastest
    test_msg = "We have an attack on ClientX system"
    test_client = {"name": "ClientX", "status": "breach", "time": str(datetime.now())}
    print(twinny_guard(test_msg, test_client, model='llama3.2:1b'))
