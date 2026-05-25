import os
import shutil

BRAIN_HOME = "/data/data/com.termux/files/home/AVPS_CORE/brain/"
VAULT_DIR = os.path.join(BRAIN_HOME, "vault/")
FIFO_PATH = os.path.join(BRAIN_HOME, "sensor_feed.fifo")

def move_to_vault(file_path):
    clean_path = file_path.strip()
    if os.path.exists(clean_path):
        shutil.move(clean_path, VAULT_DIR)
        print(f"Angel: [VAULT] Secured: {clean_path}")
    else:
        print(f"Angel: [ERROR] Cannot find: {clean_path}")

print("Guardian Angel initialized. Watching...")

while True:
    with open(FIFO_PATH, "r") as fifo:
        for line in fifo:
            cmd = line.strip()
            if cmd.startswith("VAULT:"):
                move_to_vault(cmd.split("VAULT:")[1])
            else:
                print(f"Angel: Received command -> {cmd}")
