import sqlite3
import requests
import time

CLOUD_API_URL = "http://localhost:8000/api/v1/telemetry/ingest"

def sync_edge_telemetry():
    print("[SYNC BRIDGE] Connecting local Michael AI edge nodes to Michael AI 1.1 Cloud Command...")
    try:
        conn = sqlite3.connect('../michael_telemetry.db')
        cursor = conn.cursor()
        cursor.execute("SELECT timestamp, node_id, domain, event_type, confidence_score, status FROM telemetry_logs")
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            print("[SYNC BRIDGE] No local telemetry records found to sync.")
            return

        for row in rows:
            timestamp, node_id, domain, event_type, confidence_score, status = row
            payload = {
                "node_id": node_id,
                "domain": domain,
                "event_type": event_type,
                "confidence_score": confidence_score,
                "status": status
            }
            try:
                response = requests.post(CLOUD_API_URL, json=payload, timeout=3)
                if response.status_code == 200:
                    print(f"[SYNCED TO CLOUD] Node: {node_id} | Event: {event_type} -> Success")
                else:
                    print(f"[SYNC ERROR] Cloud responded with status {response.status_code}")
            except requests.exceptions.ConnectionError:
                print("[OFFLINE MODE] Cloud command center unreachable. Edge node operating autonomously.")
                break
    except Exception as e:
        print(f"[ERROR] Sync bridge failure: {e}")

if __name__ == "__main__":
    sync_edge_telemetry()
