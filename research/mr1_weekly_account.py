#!/usr/bin/env python3
"""MR1 AH Telegram-confirmed weekly and cumulative accounts (Beijing send week)."""
import argparse,json
from collections import Counter
from datetime import datetime,timedelta,timezone
from decimal import Decimal
from pathlib import Path
from zoneinfo import ZoneInfo

BJ=ZoneInfo("Asia/Shanghai")
STATES=("FULL_WIN","HALF_WIN","PUSH","HALF_LOSS","FULL_LOSS")
def timestamp(x):
    return datetime.fromisoformat(x.replace("Z","+00:00")).astimezone(BJ)
def main():
    a=argparse.ArgumentParser()
    a.add_argument("--source",default="source")
    a.add_argument("--week-start",required=True)
    args=a.parse_args()
    root=Path(args.source)/"data/mr1-v6-cross-market/formal"
    sent=[json.loads(x) for x in (root/"sent.jsonl").read_text().splitlines() if x.strip()]
    settled=json.loads((root/"settled.json").read_text()).get("entries",{})
    start=datetime.fromisoformat(args.week_start).replace(tzinfo=BJ)
    end=start+timedelta(days=7)
    if start.weekday()!=0:raise ValueError("Beijing week must begin Monday")
    ids=set()
    for x in sent:
        if not x.get("telegram_message_id") or not x.get("sent_at"):raise ValueError("Unconfirmed sent receipt")
        if x["signal_id"] in ids:raise ValueError("Duplicate formal signal")
        ids.add(x["signal_id"])
    if set(settled)-ids:raise ValueError("Settlement has no formal TG sent receipt")
    def summarize(items):
        actual=[settled[x["signal_id"]] for x in items if x["signal_id"] in settled]
        counts=Counter(x["settlement"] for x in actual)
        if any(k not in STATES for k in counts):raise ValueError("Unknown settlement state")
        pnl=sum((Decimal(str(x["realized_pnl"])) for x in actual),Decimal(0))
        return {"sent":len(items),"settled":len(actual),"pending":len(items)-len(actual),
                "states":{k:counts[k] for k in STATES},"net_u":str(pnl),
                "roi":str(pnl/len(actual)) if actual else None}
    data={"protocol":"MR1_AH_FORMAL_TG_WEEKLY_V1","week_start":args.week_start,
          "source_report_generated_at":json.loads((root/"settled.json").read_text()).get("generated_at"),
          "requested_week":summarize([x for x in sent if start<=timestamp(x["sent_at"])<end]),
          "all_time":summarize(sent),"shadow_excluded":True,"telegram_confirmed_only":True}
    print(json.dumps(data,ensure_ascii=False,indent=2))
if __name__=="__main__":main()
