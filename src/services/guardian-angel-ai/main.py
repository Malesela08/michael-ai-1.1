import os
from src.cruncher import climatize_file

if __name__ == "__main__":
    print("[Environment] Environment stabilized. Local AI guardrails active.")
    
    # Ensure data folder exists and write a sample file to test
    os.makedirs("data", exist_ok=True)
    target_file = "data/sample_data.txt"
    
    if not os.path.exists(target_file):
        with open(target_file, "w", encoding="utf-8") as f:
            f.write("System online. Ready for CrewAI data processing.")

    chunks = climatize_file(target_file)
    if chunks:
        print(f"[Success] File climatized successfully into {len(chunks)} safe buffer block(s).")
