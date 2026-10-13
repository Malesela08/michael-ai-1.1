import numpy as np

from vision_agent import VisionAgent


def test_process_frame_returns_shape_for_local_video(monkeypatch, tmp_path):
    video_path = tmp_path / "clip.mp4"
    video_path.touch()

    class FakeCapture:
        def isOpened(self):
            return True

        def read(self):
            return True, np.zeros((240, 320, 3), dtype="uint8")

        def release(self):
            pass

    monkeypatch.setattr("vision_agent.cv2.imread", lambda _path: None)
    monkeypatch.setattr(
        "vision_agent.cv2.VideoCapture", lambda _source: FakeCapture()
    )

    assert VisionAgent(source=video_path).process_frame() == {
        "status": "success",
        "shape": (240, 320, 3),
    }


def test_process_frame_reports_unavailable_source(monkeypatch):
    class FakeCapture:
        def isOpened(self):
            return False

        def release(self):
            pass

    monkeypatch.setattr("vision_agent.cv2.VideoCapture", lambda _source: FakeCapture())

    assert VisionAgent(source="offline.mp4").process_frame() == {
        "status": "error",
        "message": "Could not open video source offline.mp4",
    }


def test_analyze_frame_keeps_brightness_result(monkeypatch, tmp_path):
    image_path = tmp_path / "frame.jpg"
    image_path.touch()
    monkeypatch.setattr(
        "vision_agent.cv2.imread",
        lambda _path: np.full((480, 640, 3), 128, dtype="uint8"),
    )

    result = VisionAgent(source=image_path).analyze_frame()

    assert result["status"] == "frame_processed"
    assert result["resolution"] == "640x480"
    assert result["frame_brightness"] == 128.0
    assert result["inference_status"] == "unavailable"
