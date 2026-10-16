#!/usr/bin/env python3
"""M2 forward observation ledger. Only AES-256-GCM ciphertext is committed.

Existing PRIVATE_REPO_TOKEN is used solely as a temporary key source; rotation
requires re-encryption before it changes. Never print the key or plaintext.
This ledger is an M1-side research comparator, NOT an independently trained M2.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes

PROTOCOL = "M2_ENCRYPTED_OBSERVATION_V1"
BJ = ZoneInfo("Asia/Shanghai")
AAD = b"quant-runner:m2:forward:v1"
MAX_AGE_HOURS = 6

def utc(t):
    d = datetime.fromisoformat(str(t).replace("Z", "+00:00"))
    if d.tzinfo is None:
        raise ValueError("Unzoned timestamp")
    return d.astimezone(timezone.utc)

def cipher(secret):
    if not secret or len(secret) < 25:
        raise ValueError("M2 protection secret missing or too short")
    key = HKDF(algorithm=hashes.SHA256(), length=32, salt=b"m2-forward-key-v1",
               info=AAD).derive(secret.encode())
    return AESGCM(key)

def encode(obj, secret):
    nonce = os.urandom(12)
    raw = json.dumps(obj, sort_keys=True, separators=(",",":"),
                     ensure_ascii=False).encode("utf-8")
    ciphertext = cipher(secret).encrypt(nonce, raw, AAD)
    return json.dumps({"protocol": PROTOCOL, "nonce": nonce.hex(),
                       "ciphertext": ciphertext.hex()}, separators=(",",":")) + "\n"

def decode(s, secret):
    data = json.loads(s)
    if data.get("protocol") != PROTOCOL:
        raise ValueError("Unexpected envelope")
    raw = cipher(secret).decrypt(bytes.fromhex(data["nonce"]),
                                 bytes.fromhex(data["ciphertext"]), AAD)
    return json.loads(raw)

def kickoff_utc(kickoff_bj):
    if not kickoff_bj:
        raise ValueError("Fixture kickoff absent")
    return datetime.fromisoformat(kickoff_bj.replace(" ", "T")).replace(tzinfo=BJ).astimezone(timezone.utc)

def stage(scan, rows, previous, now=None):
    now = now or datetime.now(timezone.utc)
    if now.tzinfo is None:
        raise ValueError("Unzoned current time")
    scan_at = utc(scan["source_scan_finished_at"])
    age = (now-scan_at).total_seconds()/3600
    if age < -0.1 or age > MAX_AGE_HOURS:
        raise ValueError("Scan too old/new for prospective record")
    by_key = {(x["fixture_id"],x["market"]): x for x in previous}
    accepted = []
    new_locks = []
    for r in rows:
        if r.get("telegram_write") is not False or r.get("shadow_order") is not False:
            raise ValueError("Unexpected trade or Telegram request")
        observed = utc(r["observed_at"])
        if observed > scan_at or observed > now:
            raise ValueError("Future quote observation")
        if kickoff_utc(r["kickoff_bj"]) <= now:
            continue
        if r["market"] not in ("AH","OU"):
            continue
        accepted.append(r)
        key = (r["fixture_id"],r["market"])
        if key not in by_key:
            record = {
                "model_identity": "M2_V0_M1_SIDE_BASELINE_ONLY",
                "evaluation_status": "UNTRAINED_FORWARD_COMPARATOR",
                "first_lock_time": now.isoformat(),
                "quote_observed_at": r["observed_at"],
                "fixture_id": r["fixture_id"], "market": r["market"],
                "side": r["side"], "line": r["line"],
                "crown_decimal_price": r["crown_decimal_price"],
                "kickoff_bj": r["kickoff_bj"],
                "source_run_id": scan["source_run_id"],
                "observation_id": r["observation_id"],
                "stake_u": 1, "settlement": None,
                "pnl_u": None, "telegram_sent": False
            }
            by_key[key] = record
            new_locks.append(record)
    return accepted,new_locks

def load_locks(folder, secret):
    locks = []
    for p in sorted(Path(folder).glob("*.enc.json")):
        entry = decode(p.read_text(encoding="utf-8"),secret)
        if entry.get("protocol") != PROTOCOL:
            raise ValueError("Ledger payload protocol mismatch")
        locks.extend(entry.get("new_locks",[]))
    if len({(r["fixture_id"],r["market"]) for r in locks}) != len(locks):
        raise ValueError("Duplicate lock across encrypted ledger files")
    return locks

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--observations",required=True)
    parser.add_argument("--ledger-folder",required=True)
    parser.add_argument("--key-env",default="M2_LEDGER_SECRET")
    args=parser.parse_args()
    secret=os.environ.get(args.key_env)
    if not secret: raise ValueError("Ledger key unavailable")
    src=json.loads(Path(args.observations).read_text(encoding="utf-8"))
    if src["protocol"]!="M2_MARKET_RESIDUAL_OBSERVER_V0_1":
        raise ValueError("Bad source protocol")
    folder=Path(args.ledger_folder)
    previous=load_locks(folder,secret)
    accepted,new_locks=stage(src,src["observations"],previous)
    # One immutable encrypted batch per source scan; repeat runs never overwrite.
    name=hashlib.sha256(str(src["source_run_id"]).encode()).hexdigest()[:24] + ".enc.json"
    dest=folder/name
    new_batch=not dest.exists()
    if new_batch:
        folder.mkdir(parents=True,exist_ok=True)
        payload={"protocol":PROTOCOL,"source_run_id":src["source_run_id"],
                 "source_scan_finished_at":src["source_scan_finished_at"],
                 "observations":accepted,"new_locks":new_locks,
                 "paper_baseline_only":True}
        with dest.open("x",encoding="utf-8") as f:
            f.write(encode(payload,secret))
    print(json.dumps({"protocol":PROTOCOL,"source_run_id":src["source_run_id"],
          "existing_paper_locks":len(previous),"new_eligible_observations":len(accepted) if new_batch else 0,
          "new_baseline_locks":len(new_locks) if new_batch else 0,
          "encrypted_batch_written":new_batch,"formal_tg_sent":0,
          "trained_m2_trades":0,"m2_roi":None},ensure_ascii=False))

if __name__=="__main__":
    main()
