# Protection Order Proximity & Breach Engine for Michael AI
# "Facial Recognition, Distance Tracking & Early Breach Warning"

import sqlite3

class ProtectionOrderMonitor:
    def __init__(self, db_path="michael_telemetry.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS protection_orders (
                    order_id TEXT PRIMARY KEY,
                    restrained_name TEXT,
                    restricted_vehicle_plate TEXT,
                    restricted_face_id TEXT,
                    min_allowed_distance_km REAL,
                    status TEXT
                )
            ''')
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"⚠️ DB Init Error: {e}")

    def register_protection_order(self, order_id: str, restrained_name: str, plate: str = "", face_id: str = "", min_distance_km: float = 5.0):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO protection_orders 
                (order_id, restrained_name, restricted_vehicle_plate, restricted_face_id, min_allowed_distance_km, status)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (order_id, restrained_name, plate, face_id, min_distance_km, "ACTIVE"))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"⚠️ Registration Error: {e}")
            return False

    def evaluate_facial_proximity(self, detected_face_id: str, zone: str, current_distance_km: float) -> dict:
        matched = False
        restrained_party = "UNKNOWN"
        order_num = None
        allowed_min_dist = 5.0

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT order_id, restrained_name, restricted_face_id, min_allowed_distance_km FROM protection_orders WHERE status = 'ACTIVE'")
            orders = cursor.fetchall()
            conn.close()

            for order_id, name, face_id, min_dist in orders:
                if detected_face_id and face_id and detected_face_id.upper() == face_id.upper():
                    matched = True
                    restrained_party = name
                    order_num = order_id
                    allowed_min_dist = min_dist
                    break
        except Exception as e:
            print(f"⚠️ Evaluation Error: {e}")

        if matched:
            if current_distance_km == 0.0 or "ENTRY" in zone.upper() or "GATE" in zone.upper():
                status = "CRITICAL_BREACH_AT_ENTRY"
                threat_level = "CRITICAL"
                action = "IMMEDIATE_LOCKDOWN_AND_SOS"
                msg = f"🚨 [BREACH CONFIRMED] {restrained_party} detected directly at {zone}!"
            elif current_distance_km <= allowed_min_dist:
                status = "BREACH_PENDING"
                threat_level = "HIGH_ALERT"
                action = "RAISE_DEFENSIVE_SHIELD_AND_ALERT_VICTIM"
                msg = f"⚠️ [BREACH PENDING] Restrained party '{restrained_party}' is {current_distance_km:.1f} km from victim (Allowed Limit: {allowed_min_dist:.1f} km)!"
            else:
                status = "MONITORING_PROXIMITY"
                threat_level = "PASSIVE"
                action = "LOG_LOCATION"
                msg = f"ℹ️ {restrained_party} detected at {current_distance_km:.1f} km distance."
        else:
            status = "CLEAR"
            threat_level = "CLEAR"
            action = "PASSIVE_LOGGING"
            msg = "No restricted face match detected."

        return {
            "matched": matched,
            "order_id": order_num,
            "restrained_party": restrained_party,
            "zone": zone,
            "distance_km": current_distance_km,
            "status": status,
            "threat_level": threat_level,
            "action": action,
            "message": msg
        }

def evaluate_protection_order_face(detected_face_id: str, zone: str, current_distance_km: float) -> dict:
    monitor = ProtectionOrderMonitor()
    return monitor.evaluate_facial_proximity(detected_face_id, zone, current_distance_km)
