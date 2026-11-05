import datetime

class StrategicAIForecaster:
    def __init__(self):
        self.version = "1.1.0"

    def analyze_equipment_wear(self, device_id, failure_counts_60_days):
        probability = min(failure_counts_60_days * 0.41, 0.99)
        recommendation = "Recommend immediate replacement or servicing." if probability > 0.75 else "Operating within normal parameters."
        
        report = {
            "device_id": device_id,
            "failure_probability": f"{probability * 100:.1f}%",
            "assessment": recommendation,
            "timestamp": datetime.datetime.now().isoformat()
        }
        return report

if __name__ == "__main__":
    forecaster = StrategicAIForecaster()
    print(forecaster.analyze_equipment_wear("CAM-14", 2))
