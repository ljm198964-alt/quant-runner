"""Read-only M3 price movement research: compare same-source, same-line quotes.

No market gate, no formal order, and no historical price reconstruction.
"""
import argparse
import collections
import json
from pathlib import Path

PROTOCOL = "M3_PRICE_MOVEMENT_OBSERVATION_V1"
HORIZONS_MINUTES = (5, 15, 30, 45)

def observations(events):
    quotes = collections.defaultdict(list)
    for e in events:
        if e.get("protocol") != "M3_TOTALCORNER_FORWARD_EV_V1":
            continue
        if e.get("provider") != "TotalCorner" or not e.get("bookmaker"):
            continue
        if e.get("quote_snapshot_recorded_utc") is None:
            continue
        key = (str(e.get("totalcorner_match_id")), e.get("bookmaker"),
               e.get("market"), str(e.get("line")), e.get("side"))
        quotes[key].append(e)
    result = []
    for key, rows in quotes.items():
        # Repeated model forecasts at the same capture instant are one market snapshot.
        by_time = {}
        for e in rows:
            t = e["quote_snapshot_recorded_utc"]
            by_time.setdefault(t, e)
        series = sorted(by_time.values(), key=lambda e:e["quote_snapshot_recorded_utc"])
        from datetime import datetime, timezone
        for i, start in enumerate(series):
            t0 = datetime.fromisoformat(start["quote_snapshot_recorded_utc"].replace("Z","+00:00"))
            for horizon in HORIZONS_MINUTES:
                # First observed quote at or after target time, within the next
                # 5 minutes. Missing observations stay missing, not interpolated.
                eligible = []
                for end in series[i+1:]:
                    t1 = datetime.fromisoformat(end["quote_snapshot_recorded_utc"].replace("Z","+00:00"))
                    delta = (t1-t0).total_seconds()/60
                    if horizon <= delta <= horizon+5:
                        eligible.append((delta,end))
                if not eligible:
                    continue
                delta,end = min(eligible,key=lambda pair:pair[0])
                try:
                    opening=float(start["decimal_odd"])
                    closing=float(end["decimal_odd"])
                except (TypeError,ValueError):
                    continue
                if opening <= 1 or closing <= 1:
                    continue
                result.append({
                    "protocol":PROTOCOL,
                    "match_id":key[0],"bookmaker":key[1],"market":key[2],
                    "line":key[3],"side":key[4],
                    "start_quote_event_id":start.get("event_id"),
                    "end_quote_event_id":end.get("event_id"),
                    "start_utc":start["quote_snapshot_recorded_utc"],
                    "end_utc":end["quote_snapshot_recorded_utc"],
                    "target_horizon_minutes":horizon,
                    "actual_elapsed_minutes":round(delta,3),
                    "start_decimal_odd":opening,"end_decimal_odd":closing,
                    "decimal_odds_change":round(closing-opening,6),
                    "odds_shortened":closing<opening,
                    "source":"OBSERVED_SAME_BOOKMAKER_SAME_LINE_ONLY",
                    "research_only":True
                })
    return result

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--ledger",required=True,type=Path)
    parser.add_argument("--output",required=True,type=Path)
    args=parser.parse_args()
    events=(json.loads(s) for s in args.ledger.open() if s.strip())
    rows=observations(events)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps({
        "protocol":"M3_PRICE_MOVEMENT_REPORT_V1",
        "scope":"RESEARCH_ONLY_NO_ORDER_POLICY_CHANGE",
        "horizons_minutes":list(HORIZONS_MINUTES),
        "observations":rows,
        "count":len(rows)
    },ensure_ascii=False,indent=2)+"\n")
    print(json.dumps({"observations":len(rows),"output":str(args.output)}))

if __name__=="__main__":
    main()
