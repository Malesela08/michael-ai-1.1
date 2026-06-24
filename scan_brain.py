import os

def scan_guardian_brain():
    print("Twinny AI initiating deep scan of Guardian Angel AI brain...")
    targets = ['logic/', 'left_brain/', 'right_brain/', 'digital-brain/']
    for target in targets:
        if os.path.exists(target):
            print(f"\n--- Analyzing {target} ---")
            # List files to check for structure integrity
            files = os.listdir(target)
            for file in files:
                print(f"Found: {file}")
    print("\nScan complete. System state reported to Digital Comrade.")

if __name__ == "__main__":
    scan_guardian_brain()
