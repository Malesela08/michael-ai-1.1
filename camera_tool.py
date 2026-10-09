import socket
from urllib.parse import urlparse

import cv2


def check_live_camera_stream(rtsp_url: str, timeout_sec: int = 3):
    """Check whether a configured RTSP stream is reachable and returns a frame."""
    parsed = urlparse(rtsp_url)
    if parsed.scheme not in {"rtsp", "rtsps"} or not parsed.hostname:
        return {
            "camera_status": "invalid_configuration",
            "message": "A valid rtsp:// or rtsps:// camera URL is required.",
        }

    host = parsed.hostname
    port = parsed.port or (322 if parsed.scheme == "rtsps" else 554)

    try:
        with socket.create_connection((host, port), timeout=timeout_sec):
            pass
    except OSError as error:
        return {
            "camera_status": "offline_or_unreachable",
            "host": host,
            "port": port,
            "error": str(error),
        }

    cap = cv2.VideoCapture(
        rtsp_url,
        cv2.CAP_FFMPEG,
        [cv2.CAP_PROP_OPEN_TIMEOUT_MSEC, timeout_sec * 1000],
    )
    if not cap.isOpened():
        cap.release()
        return {
            "camera_status": "stream_auth_failed_or_invalid",
            "host": host,
            "details": "Port is open, but the RTSP handshake or authentication failed.",
        }

    success, _frame = cap.read()
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()

    if success:
        return {
            "camera_status": "online_and_streaming",
            "host": host,
            "resolution": f"{width}x{height}",
        }
    return {"camera_status": "connection_timed_out_on_read", "host": host}
