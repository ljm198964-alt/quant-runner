"""Apply user-approved M1 AH selection rule in the scanned candidate decision.
Public Runner owns the change; checkout modifications are ephemeral.
"""
from pathlib import Path

def main():
    path = Path("m1_live_scan.py")
    source = path.read_text(encoding="utf-8")
    anchor = '    selected_first = executed["side"] in ("HOME","OVER")'
    if source.count(anchor) != 1:
        raise RuntimeError("M1 selection anchor changed")
    policy = '''    # M1 AH base selection: exclude model EV >=10% before signal registration.
    # This is the final execution-side EV, including national-team reverse.
    if market == "全场让球" and gate.get("formal", False) and float(executed["ev"]) >= 0.10:
        gate = {**gate, "status": "REJECT_M1_AH_EV_GE_10_PERCENT", "formal": False}
'''
    path.write_text(source.replace(anchor,policy+anchor,1),encoding="utf-8")
    print("M1 AH base candidate rule: executed EV <10%; no extra lock/delivery gates")

if __name__ == "__main__":
    main()
