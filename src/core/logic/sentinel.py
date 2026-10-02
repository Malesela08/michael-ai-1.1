import os

import numpy as np
from rtlsdr import RtlSdr

# --- CONFIGURATION ---
MY_NUMBER = "+27812863953"
# ---------------------

# 1. Initialize SDR
try:
    sdr = RtlSdr(device_index="127.0.0.1:1234")
    sdr.sample_rate = 2.048e6
    sdr.center_freq = 433.92e6
    sdr.gain = "auto"
    print("Sentinel Active: Monitoring radio spectrum...")
except Exception as e:
    print(f"Connection Error: {e}")
    exit()


# 2. Logic to send SMS
def send_sms_alert(strength):
    message = f"ALERT: High energy signal detected (Strength: {strength:.4f})."
    # Using the fixed number
    os.system(f'termux-sms-send -n {MY_NUMBER} "{message}"')
    print("Alert sent to your phone.")


# 3. Monitoring Loop
try:
    while True:
        samples = sdr.read_samples(1024)
        power = np.mean(np.abs(samples))

        # Threshold (Adjust this if you get false alarms)
        if power > 0.05:
            print(f"Anomaly detected! Strength: {power:.4f}")
            send_sms_alert(power)

except KeyboardInterrupt:
    sdr.close()
    print("Sentinel Offline.")
