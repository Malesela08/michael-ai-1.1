import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4


class ForensicVaultHandler:
    """Write local JSON evidence records with a SHA-256 integrity checksum."""

    def __init__(self, vault_dir: str | os.PathLike[str] = "./secure_vault") -> None:
        self.vault_dir = Path(vault_dir)

    def handle(
        self, payload: dict[str, Any] | None = None
    ) -> dict[str, str | bool]:
        """Store a JSON-serializable payload; records are not encrypted or immutable."""
        incident_data = (
            payload
            if payload is not None
            else {
                "event": "routine_audit",
                "details": "No threat payload provided.",
            }
        )
        timestamp = datetime.now(timezone.utc)
        record_payload = {
            "timestamp": timestamp.isoformat(),
            "node": "michael-ai-edge-01",
            "data": incident_data,
        }
        canonical_payload = json.dumps(
            record_payload,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        )
        evidence_hash = hashlib.sha256(canonical_payload.encode("utf-8")).hexdigest()
        filename = (
            f"evidence_{timestamp.strftime('%Y%m%dT%H%M%S.%fZ')}_{uuid4().hex}.json"
        )
        self.vault_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
        filepath = self.vault_dir / filename
        file_content = json.dumps(
            {"payload": record_payload, "sha256": evidence_hash},
            indent=2,
            ensure_ascii=False,
        )

        file_descriptor = os.open(
            filepath,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL,
            0o600,
        )
        with os.fdopen(file_descriptor, "w", encoding="utf-8") as evidence_file:
            evidence_file.write(file_content)
            evidence_file.write("\n")
            evidence_file.flush()
            os.fsync(evidence_file.fileno())

        return {
            "status": "recorded",
            "storage": "local_disk",
            "evidence_file": filename,
            "sha256_checksum": evidence_hash,
            "encrypted": False,
            "message": (
                "Evidence saved locally with a SHA-256 checksum. "
                "The record is not encrypted or tamper-proof."
            ),
        }
