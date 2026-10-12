import hashlib
import json

import pytest

from forensic_vault import ForensicVaultHandler


def test_forensic_record_has_matching_sha256_and_discloses_not_encrypted(tmp_path):
    vault = ForensicVaultHandler(tmp_path / "vault")
    result = vault.handle({"event": "alarm", "zone": "North"})

    record_path = tmp_path / "vault" / result["evidence_file"]
    stored = json.loads(record_path.read_text(encoding="utf-8"))
    canonical_payload = json.dumps(
        stored["payload"],
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )
    assert result["status"] == "recorded"
    assert result["encrypted"] is False
    assert stored["sha256"] == hashlib.sha256(
        canonical_payload.encode("utf-8")
    ).hexdigest()
    assert result["sha256_checksum"] == stored["sha256"]
    assert "not encrypted or tamper-proof" in result["message"]


def test_forensic_vault_preserves_empty_payload_and_uses_unique_files(tmp_path):
    vault = ForensicVaultHandler(tmp_path / "vault")
    first = vault.handle({})
    second = vault.handle({})

    assert first["evidence_file"] != second["evidence_file"]
    first_record = json.loads(
        (tmp_path / "vault" / first["evidence_file"]).read_text(encoding="utf-8")
    )
    assert first_record["payload"]["data"] == {}


def test_forensic_vault_rejects_non_json_payload_without_creating_record(tmp_path):
    vault_dir = tmp_path / "vault"
    vault = ForensicVaultHandler(vault_dir)

    with pytest.raises(TypeError):
        vault.handle({"invalid": object()})

    assert not vault_dir.exists()
