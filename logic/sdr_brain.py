from rtlsdr import RtlSdr
import numpy as np

# Connect to the hardware
sdr = RtlSdr()
sdr.sample_rate = 2.048e6
sdr.center_freq = 433.92e6
sdr.gain = 'auto'

print("Spectrum Analyst is active. Watching for anomalies...")

try:
    while True:
        samples = sdr.read_samples(1024)
        if np.max(np.abs(samples)) > 0.05:
            print("ALERT: Unauthorized radio activity detected!")
except KeyboardInterrupt:
    sdr.close()

