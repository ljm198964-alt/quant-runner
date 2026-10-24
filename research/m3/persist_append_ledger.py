"""Persist append-only event ledger via fresh remote merge, retrying concurrent pushes."""
import argparse
import json
import subprocess
import tempfile
from pathlib import Path

LEDGER = "research/m3/results/totalcorner/forward_ev_ledger.jsonl"

def git(*args, check=True):
    p = subprocess.run(["git", *args], text=True, capture_output=True)
    if check and p.returncode:
        raise RuntimeError("git " + args[0] + ": " + p.stderr[-1200:])
    return p

def events(text):
    records={}
    for line in text.splitlines():
        if not line.strip(): continue
        event=json.loads(line)
        eid=event["event_id"]
        if eid in records and records[eid]!=event:
            raise ValueError("conflicting payload for event_id: "+eid)
        records[eid]=event
    return records

def persist(candidate_path, max_attempts=8):
    candidate=events(Path(candidate_path).read_text())
    for attempt in range(max_attempts):
        git("fetch","origin","main")
        original=git("show","origin/main:"+LEDGER).stdout
        existing=events(original)
        conflicts=[eid for eid,e in candidate.items() if eid in existing and existing[eid]!=e]
        if conflicts:raise ValueError("immutable existing event mismatch: "+str(len(conflicts)))
        addition=[e for eid,e in candidate.items() if eid not in existing]
        if not addition:
            print(json.dumps({"status":"NO_NEW_EVENTS","added":0,"attempt":attempt+1}));return
        combined=original.rstrip("\n")+"\n"+"".join(json.dumps(e,ensure_ascii=False,sort_keys=True)+"\n" for e in addition)
        with tempfile.TemporaryDirectory() as tmp:
            # Isolated worktree prevents touching the caller's uncommitted candidate.
            w=Path(tmp)/"writer"
            git("worktree","add","--detach",str(w),"origin/main")
            try:
                path=w/LEDGER
                path.write_text(combined)
                p=subprocess.run(["git","-C",str(w),"add",LEDGER],capture_output=True,text=True)
                if p.returncode:raise RuntimeError(p.stderr)
                p=subprocess.run(["git","-C",str(w),"commit","-m","Persist M3 append-only shadow events"],capture_output=True,text=True)
                if p.returncode:raise RuntimeError(p.stderr)
                push=subprocess.run(["git","-C",str(w),"push","origin","HEAD:main"],capture_output=True,text=True)
                if push.returncode==0:
                    print(json.dumps({"status":"PERSISTED","added":len(addition),"attempt":attempt+1}))
                    return
            finally:
                git("worktree","remove","--force",str(w))
    raise RuntimeError("concurrent ledger persistence failed after retries")

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--candidate",required=True)
    args=parser.parse_args()
    persist(args.candidate)
