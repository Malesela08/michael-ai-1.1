import cv2
import time
import requests

class MichaelAIVideoStreamer:
    def __init__(self, video_source=0, alert_webhook_url=None):
        self.source = video_source
        self.webhook_url = alert_webhook_url
        self.cap = cv2.VideoCapture(self.source)

    def start_stream(self):
        if not self.cap.isOpened():
            print(f'[ERROR] Could not open video source: {self.source}')
            return
        print(f'[MICHAEL AI] Streaming initiated on source: {self.source}')
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                print('[MICHAEL AI] Stream finished or interrupted.')
                break
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            anomaly_detected = False
            if anomaly_detected and self.webhook_url:
                self.dispatch_online_alert(frame)
        self.cap.release()
        print('[MICHAEL AI] Stream closed successfully.')

    def dispatch_online_alert(self, frame):
        _, buffer = cv2.imencode('.jpg', frame)
        payload = {'timestamp': time.time(), 'patent_id': '2026/08163'}
        files = {'image': ('alert.jpg', buffer.tobytes(), 'image/jpeg')}
        try:
            response = requests.post(self.webhook_url, data=payload, files=files, timeout=3)
            print(f'[ONLINE DISPATCH] Alert sent successfully! Status: {response.status_code}')
        except Exception as e:
            print(f'[ONLINE DISPATCH ERROR] Failed to send telemetry: {e}')

if __name__ == '__main__':
    print('[MICHAEL AI] Video streamer module loaded cleanly.')
