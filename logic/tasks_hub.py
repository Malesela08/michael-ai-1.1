import time

class DigitalComrade:
    def __init__(self):
        print("[INIT] Digital Comrade: Universal Hub Active")

    def security_tactical(self, threat_score):
        # Logic for Tshenolo Investigations / Anti-Hijack
        if threat_score > 0.85:
            print("ALARM: Threat high! Coordinating with Tshenolo.")
            return "SMS_SENT"
        print("STATUS: Perimeter Secure.")
        return "SECURE"

    def property_margin_manager(self, hours, rate, margin=0.12):
        # Tracking expert hours for Smart Properties (Pty) Ltd
        total = hours * rate
        net = total * (1 - margin)
        print(f"PAYOUT: Total R{total} | Net After {int(margin*100)}% Margin: R{net}")
        return net

comrade = DigitalComrade()
comrade.security_tactical(0.92)
comrade.property_margin_manager(40, 550)
