class GateVerificationSystem:
    def __init__(self, resident_manifest, expected_couriers):
        self.resident_manifest = resident_manifest
        self.expected_couriers = expected_couriers

    def evaluate_visitor(self, visitor_data, resident_response):
        manifest_match = visitor_data['declared_recipient'] in self.resident_manifest
        courier_match = visitor_data['company'] in self.expected_couriers
        owner_verified = resident_response.get('ordered_goods', False) and \
                         (resident_response.get('goods_description') == visitor_data.get('declared_goods'))

        if manifest_match and courier_match and owner_verified:
            return self.grant_access()
        else:
            return self.trigger_tactical_escalation(visitor_data)

    def grant_access(self):
        return {
            "status": "GREEN_TICK",
            "action": "standard_access_granted",
            "message": "Verification successful. Boom gate opening."
        }

    def trigger_tactical_escalation(self, visitor_data):
        escalation_packet = {
            "event_type": "potential_home_intruder",
            "status": "pending_escalation",
            "action": "non_negotiable_dispatch",
            "target": "security_company_backup",
            "instructions": "Hurry, immediate tactical backup required.",
            "visitor_snapshot": visitor_data
        }
        self.dispatch_to_security_company(escalation_packet)
        return {
            "status": "RED_FLAG",
            "action": "tactical_lockdown_and_bluff",
            "guard_script": "Inform visitor: 'We are waiting for a drone to be powered up. It is coming.'"
        }

    def dispatch_to_security_company(self, packet):
        print("DISPATCH ALERT SENT TO SECURITY COMPANY:", packet)

if __name__ == "__main__":
    system = GateVerificationSystem(
        resident_manifest=["John Doe"],
        expected_couriers=["FastParcel"]
    )
    test_visitor = {
        "declared_recipient": "Jane Doe",
        "company": "Unknown",
        "declared_goods": "Package"
    }
    test_response = {"ordered_goods": False}
    result = system.evaluate_visitor(test_visitor, test_response)
    print("Result:", result)
