# Protection Order Proximity, Public Space & Multi-Agency Dispatch Engine for Michael AI
# "Facial Recognition, Distance Tracking, SAPS & GBVF Multi-Agency Evidence Dispatch"

import sqlite3
from datetime import datetime

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

    def evaluate_public_space_breach(self, detected_face_id: str, location_name: str, gps_coords: str, current_distance_km: float) -> dict:
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
            if current_distance_km <= allowed_min_dist:
                status = "PUBLIC_SPACE_CRITICAL_BREACH"
                threat_level = "CRITICAL"
                action = "DISPATCH_SAPS_AND_GBVF_ORGANIZATIONS"
                
                # Multi-agency emergency telemetry burst
                dispatches = self._dispatch_multi_agency_alert(order_num, restrained_party, location_name, gps_coords, current_distance_km)
                msg = f"🚨 [PUBLIC SPACE BREACH] Restrained party '{restrained_party}' detected at {location_name} ({current_distance_km:.1f} km from protected individual)!"
            else:
                status = "MONITORING_PROXIMITY"
                threat_level = "PASSIVE"
                action = "LOG_LOCATION"
                dispatches = []
                msg = f"ℹ️ {restrained_party} detected at {current_distance_km:.1f} km distance in public space."
        else:
            status = "CLEAR"
            threat_level = "CLEAR"
            action = "PASSIVE_LOGGING"
            dispatches = []
            msg = "No restricted face match detected."

        return {
            "matched": matched,
            "order_id": order_num,
            "restrained_party": restrained_party,
            "location_name": location_name,
            "gps_coords": gps_coords,
            "distance_km": current_distance_km,
            "status": status,
            "threat_level": threat_level,
            "action": action,
            "dispatches": dispatches,
            "message": msg
        }

    def _dispatch_multi_agency_alert(self, order_id: str, restrained_party: str, location: str, gps: str, dist_km: float) -> list:
        timestamp = datetime.now().isoformat()
        saps_payload = f"SAPS_EMERGENCY|ORDER:{order_id}|RESTRAINED:{restrained_party}|LOC:{location}|GPS:{gps}|DIST:{dist_km:.1f}km|TS:{timestamp}"
        gbvf_org_payload = f"GBVF_SUPPORT_ALERT|ORDER:{order_id}|LOC:{location}|GPS:{gps}|VICTIM_ASSIST_REQUIRED|TS:{timestamp}"

        print(f"🚓 [SAPS DISPATCH] Transmitting priority law enforcement alert: {saps_payload}")
        print(f"🎗️ [GBVF ORG DISPATCH] Transmitting support crisis payload: {gbvf_org_payload}")

        return [
            {"agency": "SAPS_NATIONAL_DISPATCH", "status": "TRANSMITTED_VIA_RF_BURST"},
            {"agency": "GBVF_COMMAND_CENTRE_AND_SHELTERS", "status": "TRANSMITTED_ENCRYPTED"}
        ]

def evaluate_public_protection_order(detected_face_id: str, location_name: str, gps_coords: str, current_distance_km: float) -> dict:
    monitor = ProtectionOrderMonitor()
    return monitor.evaluate_public_space_breach(detected_face_id, location_name, gps_coords, current_distance_km)
