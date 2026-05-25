def check_hijack_status(vehicle_data):
    # Logic to check if the vehicle is in a 'hijacked' state
    if vehicle_data.get("is_hijacked"):
        trigger_emergency_response()
    else:
        print("Vehicle status: Secure.")

def trigger_emergency_response():
    # This calls your core libraries to take action
    print("EMERGENCY: Hijack detected!")
    # Placeholder for your SMS/Police alert function
    # send_sms_alert("Hijack detected! Vehicle location: ...")
    # log_to_library_plane("Hijack Alert")

# Test the logic
if __name__ == "__main__":
    sample_data = {"is_hijacked": True}
    check_hijack_status(sample_data)

