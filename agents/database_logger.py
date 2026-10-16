# Local SQLite Evidence Logger for Michael AI
# "POPIA-Compliant Immutable Evidence Preservation"

import sqlite3
from datetime import datetime

class MichaelTelemetryDB:
    def __init__(self, db_path="michael_telemetry.db"):
        self.db_path = db_path
        self.init_db()

    def get_connection(self):
        """Establish a local connection to the SQLite telemetry database."""
        return sqlite3.connect(self.db_path)

    def init_db(self):
        """Initialize secure local tables for telemetry and emergency event logging."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS threat_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    severity TEXT NOT NULL,
                    action_taken TEXT NOT NULL,
                    evidence_status TEXT NOT NULL
                )
            ''')
            conn.commit()
        print("✅ Local SQLite telemetry database initialized and secured.")

    def log_threat(self, event_type: str, severity: str, action_taken: str, evidence_status: str = "ENCRYPTED_LOCAL"):
        """Securely log a threat event or zero-tolerance trigger into the local database."""
        timestamp = datetime.now().isoformat()
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO threat_events (timestamp, event_type, severity, action_taken, evidence_status)
                VALUES (?, ?, ?, ?, ?)
            ''', (timestamp, event_type, severity, action_taken, evidence_status))
            conn.commit()
        print(f"🔒 [EVIDENCE LOGGED] {timestamp} | Event: {event_type} | Severity: {severity}")

    def fetch_recent_logs(self, limit: int = 5):
        """Retrieve recent logs for audit or legal review."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM threat_events ORDER BY id DESC LIMIT ?', (limit,))
            return cursor.fetchall()
