class VisionInferenceAdapter:
    def __init__(self, bus, domain="VEHICLE"):
        self.bus = bus
        self.domain = domain # VEHICLE, PROPERTY, or BUSINESS
        self.turn_counter = 0
        self.MAX_TURNS = 3

    def process_signal(self, threat_level):
        if threat_level == "YELLOW":
            self.turn_counter += 1
            # Route to the specific Investigation Room for the domain
            self.bus.transmit("VISION_SYSTEM", f"{self.domain}_INVESTIGATION", "LOGGING_SUSPICIOUS_ACTIVITY")
            return f"MONITORING_{self.domain}: Turn {self.turn_counter}"
            
        elif threat_level == "RED":
            if self.turn_counter >= self.MAX_TURNS:
                self.bus.transmit("VISION_SYSTEM", "SMS_GATEWAY", f"EMERGENCY_{self.domain}_THREAT")
                return "THREAT_CONFIRMED: ACTION_TRIGGERED"
