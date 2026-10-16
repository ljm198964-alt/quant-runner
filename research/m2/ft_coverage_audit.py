#!/usr/bin/env python3
"""Read-only audit of independently verified FT records already stored in source repo.

Does not merge results into M2 dataset or infer approval from source labels.
"""
import argparse,json
from pathlib import Path
from collections import Counter

def audit(runs, evidence_file):
    saved={}
    for p in Path(runs).glob("M1_*.json"):
        try: d=json.loads(p.read_text(encoding="utf-8"))
        except (OSError,ValueError):continue
        if d.get("scan_status")!="COMPLETE":continue
        for m in d.get("matches") or []:
            if not isinstance(m,dict):continue
            fid=str(m.get("fixture_id") or "")
            if fid:saved.setdefault(fid,[]).append(m)
    e=json.loads(Path(evidence_file).read_text(encoding="utf-8"))
    c=Counter()
    for fid,r in (e.get("results") or {}).items():
        c["evidence_records"]+=1
        if not isinstance(r,dict):continue
        if fid not in saved:
            c["not_in_saved_scan"]+=1;continue
        c["matched_fixture_id"]+=1
        raw=r.get("raw") or {}
        if (r.get("identity_verified") is not True or
            str(r.get("fixture_id"))!=str(fid) or str(raw.get("id"))!=str(fid) or
            r.get("result_status")!="full" or raw.get("status")!="full" or
            not r.get("result_hash") or not r.get("observed_at") or
            not isinstance(r.get("goals"),list) or len(r["goals"])!=2):
            c["incomplete_identity_or_proof"]+=1;continue
        if any(str(raw.get(k))!=str(m.get(field)) for m in saved[fid] for k,field in
               (("l_id","league_id"),("h_id","home_team_id"),("a_id","away_team_id"))
               if m.get(field) is not None):
            c["identity_mismatch"]+=1;continue
        c["matched_with_proof_fields_and_ids"]+=1
    return dict(c)
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--runs",required=True);p.add_argument("--evidence",required=True)
    a=p.parse_args()
    print(json.dumps({"protocol":"M2_ADDITIONAL_FT_COVERAGE_AUDIT_V1",
      "counts":audit(a.runs,a.evidence),"merged_into_training":False},ensure_ascii=False))
