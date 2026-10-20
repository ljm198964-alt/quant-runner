"""Append-only private M3 Crown evidence store; offline and value-suppressing.

Quote values are retained only outside the repository after the evidence record
passes M3 Crown checks and its written permission explicitly covers retention.
No network client, model ledger access, order, or Telegram integration exists.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path

from research.m3.crown_evidence import validate_record

GENESIS = "0" * 64


def _canonical(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _sha(value: object) -> str:
    return hashlib.sha256(_canonical(value)).hexdigest()


def _check_private_destination(path: Path, repository_root: Path) -> Path:
    destination = path.expanduser().resolve()
    root = repository_root.expanduser().resolve()
    if destination == root or root in destination.parents:
        raise ValueError("private Crown ledger must be outside the repository")
    return destination


def _read(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid private ledger JSON at line {number}") from exc
        if not isinstance(row, dict):
            raise ValueError(f"invalid private ledger event at line {number}")
        expected = row.get("event_sha256")
        body = {k: v for k, v in row.items() if k != "event_sha256"}
        if expected != _sha(body):
            raise ValueError(f"private ledger hash mismatch at line {number}")
        rows.append(row)
    previous = GENESIS
    for number, row in enumerate(rows, 1):
        if row.get("previous_event_sha256") != previous:
            raise ValueError(f"private ledger chain mismatch at line {number}")
        previous = row["event_sha256"]
    return rows


def append_records(path: Path, records: list[dict], repository_root: Path) -> dict:
    destination = _check_private_destination(path, repository_root)
    if not isinstance(records, list):
        raise ValueError("input must be an array of validated evidence records")
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        os.chmod(destination, 0o600)
    events = _read(destination)
    existing = {e["record_sha256"] for e in events}
    added = 0
    previous = events[-1]["event_sha256"] if events else GENESIS
    for record in records:
        validate_record(record)
        authorization = record["authorization"]
        uses = authorization.get("allowed_uses", [])
        if not isinstance(uses, list) or not {"m3_research", "quote_retention"}.issubset(set(uses)):
            raise ValueError("written permission must explicitly cover M3 research and quote retention")
        if record["source"].get("capture_method") == "authorized_api" and "automated_api" not in uses:
            raise ValueError("written permission must explicitly cover automated API capture")
        record_hash = _sha(record)
        if record_hash in existing:
            continue
        body = {
            "event_type": "CROWN_EVIDENCE_IMPORTED",
            "protocol": "M3_PRIVATE_CROWN_LEDGER_V1",
            "event_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "record_sha256": record_hash,
            "previous_event_sha256": previous,
            "record": record,
        }
        event = {**body, "event_sha256": _sha(body)}
        with destination.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")
        os.chmod(destination, 0o600)
        previous = event["event_sha256"]
        existing.add(record_hash)
        added += 1
    return audit_private_ledger(destination, repository_root, appended=added)


def audit_private_ledger(path: Path, repository_root: Path, appended: int = 0) -> dict:
    destination = _check_private_destination(path, repository_root)
    events = _read(destination)
    counts = {"AH": 0, "OU": 0}
    for event in events:
        record = event["record"]
        validate_record(record)
        for quote in record["quotes"]:
            counts[quote["market"]] += 1
    return {
        "protocol": "M3_PRIVATE_CROWN_LEDGER_AUDIT_V1",
        "generated_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "ledger_sha256": hashlib.sha256(destination.read_bytes()).hexdigest() if destination.exists() else None,
        "event_count": len(events),
        "appended_this_run": appended,
        "retained_quote_count_by_market": counts,
        "quote_values_persisted_outside_repository": True,
        "integrity_chain_valid": True,
        "formal_order": False,
        "telegram_sent": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ledger", type=Path, help="private JSONL ledger path outside the repository")
    parser.add_argument("--repository-root", type=Path, required=True)
    parser.add_argument("--input", type=Path, help="private JSON array of authorized evidence records")
    args = parser.parse_args()
    if args.input:
        records = json.loads(args.input.read_text(encoding="utf-8"))
        result = append_records(args.ledger, records, args.repository_root)
    else:
        result = audit_private_ledger(args.ledger, args.repository_root)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
