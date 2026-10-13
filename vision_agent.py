import os
from pathlib import Path
from typing import Any

try:
    import cv2
except ImportError:
    cv2 = None
import numpy as np
from dotenv import load_dotenv

load_dotenv()


class VisionAgent:
    """Capture and measure local frames without claiming model inference."""

    def __init__(
        self,
        confidence_threshold: float = 0.6,
        source: str | os.PathLike[str] | int | None = None,
    ) -> None:
        if not 0.0 <= confidence_threshold <= 1.0:
            raise ValueError("confidence_threshold must be between 0 and 1.")
        self.confidence_threshold = confidence_threshold
        self.source = source
        self.requested_model = "YOLOv8-Nano-Edge"

    def _capture_frame(
        self, source_text: str
    ) -> tuple[Any | None, str, str | None]:
        source_path = Path(source_text)
        capture_source: str | int = source_text
        is_local_file = source_path.is_file()

        if is_local_file:
            frame = cv2.imread(source_text)
            if frame is not None:
                return frame, "not_applicable", None
        else:
            frame = None
            if source_text.isdecimal():
                capture_source = int(source_text)

        capture = cv2.VideoCapture(capture_source)
        try:
            if not capture.isOpened():
                return None, "video_frame_captured", (
                    f"Could not open video source {source_text}"
                )
            success, frame = capture.read()
            if not success:
                return None, "video_frame_captured", (
                    "Failed to read frame from source"
                )
        finally:
            capture.release()

        camera_status = (
            "video_frame_captured"
            if is_local_file
            else "stream_captured"
            if source_text.startswith(("rtsp://", "rtsps://", "http://", "https://"))
            else "video_frame_captured"
        )
        return frame, camera_status, None

    def process_frame(
        self,
        source: str | os.PathLike[str] | int | None = None,
    ) -> dict[str, Any]:
        """Capture one frame and return its array shape without inference."""
        selected_source = source if source is not None else self.source
        if selected_source is None:
            selected_source = os.getenv("CAMERA_SOURCE") or "0"
        if cv2 is None:
            return {
                "status": "error",
                "message": "OpenCV is required to read or capture video frames.",
            }

        source_text = os.fspath(selected_source) if not isinstance(
            selected_source, int
        ) else str(selected_source)
        frame, _camera_status, error_message = self._capture_frame(source_text)
        if frame is None:
            return {"status": "error", "message": error_message}
        return {"status": "success", "shape": frame.shape}

    def analyze_frame(
        self,
        frame_path_or_stream: str | os.PathLike[str] | None = None,
        *,
        zone: str = "North",
    ) -> dict[str, Any]:
        """Capture one image/video frame and report its mean brightness."""
        source = (
            frame_path_or_stream
            if frame_path_or_stream is not None
            else self.source
        )
        if source is None or source == "":
            source = os.getenv("CAMERA_SOURCE") or os.getenv("CAMERA_RTSP_URL")
        if not source:
            return {
                "status": "unavailable",
                "zone": zone,
                "inference_status": "unavailable",
                "threat_detected": None,
                "gait_profile": "unavailable",
                "message": (
                    "No local image/video source or camera stream configured."
                ),
            }
        if cv2 is None:
            return {
                "status": "unavailable",
                "zone": zone,
                "inference_status": "unavailable",
                "threat_detected": None,
                "gait_profile": "unavailable",
                "message": "OpenCV is required to read or capture video frames.",
            }

        source_text = os.fspath(source) if not isinstance(source, int) else str(source)
        frame, camera_status, _error_message = self._capture_frame(source_text)
        if frame is None:
            return {
                "status": "error",
                "zone": zone,
                "inference_status": "unavailable",
                "threat_detected": None,
                "gait_profile": "unavailable",
                "message": f"Failed to capture or read frame from source: {source_text}",
            }

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
