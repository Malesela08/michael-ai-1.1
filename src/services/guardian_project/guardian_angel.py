import cv2
import numpy as np


def run_guardian():
    print("Guardian Angel AI: Analysis engine active...")
    cap = cv2.VideoCapture("test_video.mp4")

    # Background subtractor to detect motion
    fgbg = cv2.createBackgroundSubtractorMOG2()

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Apply motion detection
            fgmask = fgbg.apply(frame)

            # Calculate amount of motion
            motion_level = np.sum(fgmask) / 255

            # Threshold for alarm (adjust as needed)
            if motion_level > 50000:
                print("ALERT: Abnormal motion detected!")
                # Here is where your SMS pipeline will hook in
    finally:
        cap.release()
        print("Analysis stopped.")


if __name__ == "__main__":
    run_guardian()
