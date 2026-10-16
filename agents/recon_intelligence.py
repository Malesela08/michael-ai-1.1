# Criminal Reconnaissance & Anti-Tailing Module for Michael AI
# "Pre-Attack Scouting Detection & Countermeasures Engine"

import sqlite3
import os
from datetime import datetime, timedelta

class ReconIntelligenceEngine:
    def __init__(self, db_path="michael_telemetry.db"):
        self.db_path = db_path

    def analyze_scouting_behavior(self, entity_id: str, zone: str, dwell_time_minutes: int, follows_target: bool = False) -> dict:
        """
        Evaluates entity behavior for pre-attack indicators: loitering, vehicle tailing,
        perimeter probing, and recurring scouting runs.
        """
        threat_score = 0
        indicators = []

        # 1. Tailing Detection (Vehicle or foot trailing)
        if follows_target:
            threat_score += 50
            indicators.append("ACTIVE_TAILING_PATTERN_DETECTED")

        # 2. Perimeter Dwell / Loitering Thresholds
        if dwell_time_minutes > 10:
            threat_score += 30
            indicators.append("HIGH_DWELL_TIME_LOITERING")
        elif dwell_time_minutes > 3:
            threat_score += 15
            indicators.append("SUSPICIOUS_STATIONARY_MONITORING")

        # 3. Check Database for Historical Recon Runs by Same Entity or Location
        historical_probes = self._check_historical_probes(zone)
        if historical_probes > 2:
            threat_score += 25
            indicators.append(f"RECURRING_PROBING_ZONE ({historical_probes} prior passes)")

        # Determine Classification
        if threat_score >= 60:
            status = "CRITICAL_PRE_ATTACK_RECON"
            directive = "ELEVATE_PERIMETER_ALERT_AND_SPOTLIGHTS"
        elif threat_score >= 30:
            status = "SUSPICIOUS_SCOUTING_ACTIVITY"
            directive = "INCREASE_TELEMETRY_LOGGING_FREQUENCY"
        else:
            status = "ROUTINE_ENVIRONMENTAL_MOTION"
            directive = "MONITOR_PASSIVELY"

        return {
            "entity_id": entity_id,
            "zone": zone,
            "threat_score": threat_score,
            "classification": status,
            "indicators": indicators,
            "directive": directive
        }

    def _check_historical_probes(self, zone: str) -> int:
        if not os.path.exists(self.db_path):
            return 0
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM telemetry_logs WHERE event_type LIKE '%SCOUT%' OR event_type LIKE '%RECON%'")
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except Exception:
            return 0

def evaluate_recon_threat(entity_id: str, zone: str, dwell_time_minutes: int, follows_target: bool = False) -> dict:
    engine = ReconIntelligenceEngine()
    return engine.analyze_scouting_behavior(entity_id, zone, dwell_time_minutes, follows_target)
