import os
from pathlib import Path
from typing import Any

import cv2
import numpy as np


class VisionAgent:
    """Capture and measure local frames without claiming model inference."""

    def __init__(self, confidence_threshold: float = 0.6) -> None:
        if not 0.0 <= confidence_threshold <= 1.0:
            raise ValueError("confidence_threshold must be between 0 and 1.")
        self.confidence_threshold = confidence_threshold
        self.requested_model = "YOLOv8-Nano-Edge"

    def analyze_frame(
        self,
        frame_path_or_stream: str | os.PathLike[str] | None = None,
        *,
        zone: str = "North",
    ) -> dict[str, Any]:
        """Capture one image/video frame and report its mean brightness."""
        source = frame_path_or_stream or os.getenv("CAMERA_RTSP_URL")
        if not source:
            return {
                "status": "unavailable",
                "zone": zone,
                "inference_status": "unavailable",
                "threat_detected": None,
                "gait_profile": "unavailable",
                "message": (
                    "No active video stream, image path, or camera URL configured."
                ),
            }

        source_text = os.fspath(source)
        source_path = Path(source_text)
        if source_path.is_file():
            frame = cv2.imread(source_text)
            if frame is None:
                return {
                    "status": "error",
                    "zone": zone,
                    "inference_status": "unavailable",
                    "threat_detected": None,
                    "gait_profile": "unavailable",
                    "message": f"Failed to read image frame from source: {source_text}",
                }
            camera_status = "not_applicable"
        else:
            capture = cv2.VideoCapture(source_text)
            try:
                if not capture.isOpened():
                    frame = None
                else:
                    success, frame = capture.read()
                    if not success:
                        frame = None
            finally:
                capture.release()
            if frame is None:
                return {
                    "status": "error",
                    "zone": zone,
                    "inference_status": "unavailable",
                    "threat_detected": None,
                    "gait_profile": "unavailable",
                    "message": (
                        f"Failed to capture or read frame from source: {source_text}"
                    ),
                }
            camera_status = (
                "stream_captured"
                if source_text.startswith(("rtsp://", "rtsps://"))
                else "video_frame_captured"
            )

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        mean_brightness = float(np.mean(gray))
        height, width = frame.shape[:2]

        return {
            "status": "frame_processed",
            "zone": zone,
            "camera_status": camera_status,
            "resolution": f"{width}x{height}",
            "frame_brightness": round(mean_brightness, 2),
            "model": self.requested_model,
            "inference_status": "unavailable",
            "threat_detected": None,
            "gait_profile": "unavailable",
            "message": (
                "Frame captured and brightness measured; YOLO inference is not "
                "configured."
            ),
        }
