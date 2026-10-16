#!/usr/bin/env python3
"""Compare archived verified FT to existing M2 evidence, read-only."""
import argparse,json
from pathlib import Path
from research.m2.market_dataset import build,utc
from research.m2.ft_coverage_audit import audit

def compare(runs,formal_path,alternate_path):
    formal=json.loads(Path(formal_path).read_text(encoding="utf-8"))
    alternate=json.loads(Path(alternate_path).read_text(encoding="utf-8"))
    previous,_=build(runs,formal)
    original={(r["fixture_id"],r["market"]) for r in previous}
    extra={"results":dict(formal.get("results") or {})}
    excluded={"already_in_formal":0,"conflicts":0,"proof_or_identity_invalid":0,"eligible_alternate":0}
    for fid,r in (alternate.get("results") or {}).items():
        if not isinstance(r,dict):continue
        raw=r.get("raw") or {}
        proof=r.get("goals")
        if not (r.get("identity_verified") is True and r.get("result_status")=="full"
            and raw.get("status")=="full" and str(r.get("fixture_id"))==str(fid)
            and str(raw.get("id"))==str(fid) and r.get("result_hash")
            and isinstance(proof,list) and len(proof)==2 and
            all(type(v)==int and v>=0 for v in proof) and
            str(raw.get("hg"))==str(proof[0]) and str(raw.get("ag"))==str(proof[1]) and utc(r.get("observed_at"))):
            excluded["proof_or_identity_invalid"]+=1
            continue
        old=[e for k,revisions in extra["results"].items() if str(k).split("|")[0]==str(fid)
             for e in revisions if isinstance(revisions,list)]
        if old:
            excluded["already_in_formal"]+=1
            if any(e.get("home_goals")!=proof[0] or e.get("away_goals")!=proof[1] for e in old):
                excluded["conflicts"]+=1
            continue
        excluded["eligible_alternate"]+=1
        extra["results"][str(fid)+"|AUXILIARY_FT_COMPARISON"]=[{
            "source":"TotalCorner API /match/view","raw_sha256":r["result_hash"],
            "fixture_id":str(fid),"home_goals":proof[0],"away_goals":proof[1],
            "observed_at":r["observed_at"]}]
    updated,_=build(runs,extra)
    added={(r["fixture_id"],r["market"]) for r in updated}-original
    return {"protocol":"M2_FT_OVERLAP_COMPARISON_V1",
      "source_evidence_records":len(alternate.get("results") or {}),
      "original_samples":len(original),
      "potential_samples_with_alternate":len(updated),
      "new_market_samples":len(added),"new_unique_fixtures":len({f for f,m in added}),
      "excluded":excluded,"merged_into_training":False,
      "caveat":"Research-only provisional overlap; not independently established that every auxiliary source hash is a raw wire digest."}
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--runs",required=True);p.add_argument("--formal",required=True);p.add_argument("--alternate",required=True)
    a=p.parse_args()
    print(json.dumps(compare(a.runs,a.formal,a.alternate),ensure_ascii=False))
