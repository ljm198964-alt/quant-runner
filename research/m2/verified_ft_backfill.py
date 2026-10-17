#!/usr/bin/env python3
"""Confidential M2 FT coverage from existing TotalCorner API /match/view.

Reuses M1's exact fixture/team/league/kickoff and finished-game validator.
No alternative bookmaker odds, model inference, new selection constraints, or
public plaintext. Saves AES-GCM FT proofs for M2's already locked fixtures.
"""
from __future__ import annotations
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import hmac
import json
import os
from pathlib import Path
import sys

from research.m2.encrypted_ledger import decode, encode, kickoff_utc, load_locks

FT_PROTOCOL = "M2_V0_PRIVATE_VERIFIED_FT_V1"


def stored_finals(folder: Path, secret: str) -> dict:
    out = {}
    for path in sorted((folder / "verified_ft").glob("*.enc.json")):
        payload = decode(path.read_text(encoding="utf-8"), secret)
        if payload.get("protocol") != FT_PROTOCOL:
            raise ValueError("Unsupported private M2 FT record")
        proof = payload["evidence"]
        fixture_id = str(proof["fixture_id"])
        if fixture_id in out and out[fixture_id] != proof:
            raise ValueError("Conflicting immutable private M2 FT evidence")
        out[fixture_id] = proof
    return out


def select_locked_identities(run_dir: Path, target: dict) -> tuple[dict, set]:
    """Recover frozen fixture identity from the scan used by M2, not guess teams."""
    identities = {}
    conflicts = set()
    for path in sorted(run_dir.glob("M1_*.json")):
        try:
            scan = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if scan.get("scan_status") != "COMPLETE":
            continue
        for match in scan.get("matches") or []:
            if not isinstance(match, dict):
                continue
            fid = str(match.get("fixture_id") or "")
            if fid not in target or match.get("kickoff_bj") != target[fid]["kickoff_bj"]:
                continue
            required = ("league_id", "home", "away")
            if any(not match.get(k) for k in required):
                continue
            ident = {
                "league_id": str(match["league_id"]),
                "home": str(match["home"]),
                "away": str(match["away"]),
                "home_team_id": str(match.get("home_team_id") or ""),
                "away_team_id": str(match.get("away_team_id") or ""),
            }
            if fid in identities and identities[fid] != ident:
                conflicts.add(fid)
            else:
                identities[fid] = ident
    return identities, conflicts


def backfill(folder: Path, run_dir: Path, secret: str, formal: dict, fetch, validate, now=None) -> dict:
    from research.m2.settle_forward import verified_finals
    now = now or datetime.now(timezone.utc)
    locks = load_locks(folder, secret)
    existing_ft = stored_finals(folder, secret)
    m1_verified = verified_finals(formal)
    target = {}
    for lock in locks:
        fid = str(lock["fixture_id"])
        if kickoff_utc(lock["kickoff_bj"]) >= now:
            continue
        if fid in existing_ft or fid in m1_verified:
            continue
        if fid in target and target[fid]["kickoff_bj"] != lock["kickoff_bj"]:
            raise ValueError("Conflicting M2 locked kickoff for one fixture")
        target[fid] = lock
    identities, conflicts = select_locked_identities(run_dir, target)
    tally = Counter()
    for fid, lock in sorted(target.items()):
        if fid in conflicts:
            tally["SOURCE_SCAN_IDENTITY_CONFLICT"] += 1
            continue
        if fid not in identities:
            tally["SOURCE_SCAN_IDENTITY_UNAVAILABLE"] += 1
            continue
        identity = {
            **identities[fid],
            "fixture_id": fid,
            "kickoff": kickoff_utc(lock["kickoff_bj"]).isoformat(),
        }
        try:
            payload = fetch(fid)
            evidence = validate(identity, payload, now.isoformat())
        except Exception:
            # Never output the raw response, fixture ID or exception (may contain secrets).
            tally["PROVIDER_OR_IDENTITY_VALIDATION_ERROR"] += 1
            continue
        if evidence is None:
            tally["PROVIDER_NOT_YET_VERIFIED_FULL_TIME"] += 1
            continue
        proof = {
            "source": "TotalCorner API /match/view",
            "fixture_id": fid,
            "home_goals": evidence["home_goals"],
            "away_goals": evidence["away_goals"],
            "observed_at": evidence["observed_at"],
            "raw_sha256": evidence["raw_sha256"],
            "locked_kickoff": evidence["locked_kickoff"],
            "kickoff_changed": bool(evidence["kickoff_changed"]),
        }
        filename = hmac.new(secret.encode(), fid.encode(), hashlib.sha256).hexdigest()[:32] + ".enc.json"
        target_path = folder / "verified_ft" / filename
        target_path.parent.mkdir(parents=True, exist_ok=True)
        with target_path.open("x", encoding="utf-8") as fh:
            fh.write(encode({"protocol": FT_PROTOCOL, "evidence": proof}, secret))
        tally["VERIFIED_FT_ENCRYPTED_NEW"] += 1
        if proof["kickoff_changed"]:
            tally["VERIFIED_BUT_KICKOFF_CHANGED"] += 1
    return {
        "protocol": "M2_VERIFIED_FT_BACKFILL_AGGREGATE_V1",
        "candidate_started_fixtures_without_known_ft": len(target),
        "existing_private_verified_fixtures": len(existing_ft),
        "source_scan_identity_matches": len(identities),
        "counts": dict(tally),
        "private_payload_disclosed": False,
        "telegram_write": False,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger-folder", required=True)
    parser.add_argument("--runs", required=True)
    parser.add_argument("--formal", required=True)
    parser.add_argument("--source-code-dir", required=True)
    args = parser.parse_args()
    secret = os.environ.get("M2_LEDGER_SECRET")
    if not secret or not os.environ.get("TOTALCORNER_TOKEN"):
        raise ValueError("Existing authorized data or ledger credential unavailable")
    sys.path.insert(0, str(Path(args.source_code_dir).resolve()))
    from m1_live_scan import get
    from m1_formal_runtime import validate_final
    formal = json.loads(Path(args.formal).read_text(encoding="utf-8"))
    report = backfill(
        Path(args.ledger_folder), Path(args.runs), secret, formal,
        lambda fid: get("/match/view/" + fid), validate_final,
    )
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
