import logging
import os

logging.basicConfig(
    filename="guardian_integrity.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def scan_guardian_brain():
    print("Initiating deep scan...")
    logging.info("Deep scan initiated.")
    targets = ["logic/", "left_brain/", "right_brain/", "digital-brain/"]

    for target in targets:
        try:
            if os.path.exists(target):
                files = os.listdir(target)
                for file in files:
                    logging.info(f"Integrity Check: Found {file} in {target}")
            else:
                logging.warning(f"Target missing: {target}")
        except Exception as e:
            logging.error(f"Failed to scan {target}: {e}")

    print("Scan complete. Log saved to guardian_integrity.log.")
    logging.info("Scan complete.")


if __name__ == "__main__":
    scan_guardian_brain()
