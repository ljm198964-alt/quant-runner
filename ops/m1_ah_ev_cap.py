"""Apply the user-approved M1 AH EV cap to an ephemeral legacy checkout.
Source of policy lives in public quant-runner, not the legacy repository.
Fail closed when upstream anchors change. Historical SENT receipts remain intact.
"""
from pathlib import Path

CAP = 0.10

def replace_exact(path, anchor, insert):
    p = Path(path)
    original = p.read_text(encoding="utf-8")
    if original.count(anchor) != 1:
        raise RuntimeError(f"EV cap patch anchor changed: {path}")
    p.write_text(original.replace(anchor, insert + anchor, 1), encoding="utf-8")

def main():
    replace_exact(
        "m1_formal_runtime.py",
        '        if candidate.get("status") != "CANDIDATE" or candidate.get("is_new_signal") is not True:',
        '''        # User approved: M1 AH forecast EV >= 10% must never become a new formal lock.
        if candidate.get("market") == "AH":
            from decimal import Decimal
            ev = candidate.get("ev")
            if ev is None:
                raise ValueError("M1_AH_EV_CAP_MISSING_FORECAST_EV")
            if Decimal(str(ev)) >= Decimal("0.10"):
                event(ledger, "M1_AH_EV_CAP_REJECTED", scan_id=scan_id,
                      fixture_id=str(candidate["fixture_id"]), market="AH",
                      observed_ev=str(ev), threshold="0.10")
                continue
''')
    replace_exact(
        "m1_notification.py",
        '        if ledger["picks"][key].get("market") in PAUSED_FORMAL_MARKETS:',
        '''        # Enforce cap at transport boundary for older locked but not SENT AH signals too.
        _lock = ledger["picks"][key]
        if _lock.get("market") == "AH":
            from decimal import Decimal
            _ev = (_lock.get("market_evidence") or {}).get("ev")
            if _ev is None or Decimal(str(_ev)) >= Decimal("0.10"):
                n.update(status="SKIPPED_M1_AH_EV_CAP",
                         skipped_at=receipt_now(), skip_reason="USER_M1_AH_EV_LT_10_PERCENT")
                event(ledger, "NOTIFICATION_SKIPPED_M1_AH_EV_CAP",
                      _lock["pick_id"], at=receipt_now(), channel="telegram",
                      notification_id=n["notification_id"])
                if persist: persist(ledger)
                continue
''')
    print("M1 AH EV < 10% formal cap applied: lock and Telegram dispatch")

if __name__ == "__main__":
    main()
