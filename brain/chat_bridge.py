import sys
import subprocess

def run_bridge():
    print("--- Digital Comrade Bridge Online ---")
    while True:
        try:
            user_input = input("You > ")
            if user_input.lower() == "exit":
                break
            if not user_input.strip():
                continue
            
            # Direct execution of the Angel's brain logic
            result = subprocess.run(
                ["python3", "/data/data/com.termux/files/home/AVPS_CORE/brain/intelligent_brain.py", user_input],
                capture_output=True, text=True
            )
            print(result.stdout.strip())
        except KeyboardInterrupt:
            print("\nAngel: Shutting down bridge...")
            break

if __name__ == "__main__":
    run_bridge()
