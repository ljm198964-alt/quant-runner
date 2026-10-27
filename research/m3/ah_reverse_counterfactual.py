"""M3 AH reverse-side counterfactual at the *recorded opposite-side quote*.
Read-only; shadow orders and actual policies are untouched.
"""
import argparse,collections,json
from pathlib import Path
from research.m3.probabilities import settle_score

def evaluate(events):
    quotes=collections.defaultdict(list)
    orders={};settlements=collections.defaultdict(list)
    for e in events:
        p=e.get("protocol")
        if p=="M3_TOTALCORNER_FORWARD_EV_V1" and e.get("market")=="AH":
            quotes[e.get("forecast_id")].append(e)
        elif p=="M3_SHADOW_ORDER_V1" and e.get("market")=="AH":
            orders[e["event_id"]]=e
        elif p=="M3_TOTALCORNER_FORWARD_SETTLEMENT_V1":
            settlements[e.get("shadow_order_event_id")].append(e)
    result={}
    for model in ("poisson","dixon_coles","bivariate_poisson"):
        counts=collections.Counter();orig=rev=0.0
        by_origin=collections.defaultdict(lambda:{"n":0,"original_u":0.0,"reverse_u":0.0})
        for oid,o in orders.items():
            if o.get("model")!=model:continue
            counts["orders"]+=1
            ss=settlements.get(oid,[])
            if len(ss)!=1:
                counts["not_singly_settled"]+=1;continue
            s=ss[0]
            if any(s.get(k)!=o.get(k) for k in ("market","line","side")):
                counts["settlement_mismatch"]+=1;continue
            opposite="away" if o["side"]=="home" else "home"
            matches=[q for q in quotes[o["forecast_id"]] if q.get("side")==opposite
                     and str(q.get("line"))==str(o["line"])
                     and q.get("bookmaker") and q.get("quote_snapshot_recorded_utc")==o.get("quote_snapshot_recorded_utc")
                     and q.get("totalcorner_match_id")==o.get("totalcorner_match_id")]
            if len(matches)!=1:
                counts["missing_unique_opposite_quote"]+=1;continue
            q=matches[0]
            try:
                odd=float(q["decimal_odd"])
                if odd<=1:raise ValueError("invalid opposite odd")
                _,reverse_u=settle_score("AH",o["line"],opposite,int(s["home_goals"]),int(s["away_goals"]),odd)
                original_u=float(s["hypothetical_unit_return"])
            except (ValueError,TypeError,KeyError):
                counts["invalid_score_or_quote"]+=1;continue
            counts["comparable_settled"]+=1
            orig+=original_u;rev+=reverse_u
            origin=o.get("selection_provenance","UNKNOWN")
            g=by_origin[origin];g["n"]+=1;g["original_u"]+=original_u;g["reverse_u"]+=reverse_u
        n=counts["comparable_settled"]
        result[model]={"counts":dict(counts),"original_net_u":round(orig,6),"reverse_net_u":round(rev,6),
                       "original_roi_percent":round(orig/n*100,4) if n else None,
                       "reverse_roi_percent":round(rev/n*100,4) if n else None,
                       "by_selection_provenance":{k:{"n":v["n"],"original_net_u":round(v["original_u"],6),
                          "reverse_net_u":round(v["reverse_u"],6),"reverse_roi_percent":round(v["reverse_u"]/v["n"]*100,4)}
                          for k,v in by_origin.items()}}
    return {"protocol":"M3_AH_REVERSE_COUNTERFACTUAL_V1",
            "note":"Research-only same-time opposing TotalCorner quote, no formal orders. Retrospective reconstructed records are not prospective validation. Model rows share fixtures; do not pool as independent bets.",
            "models":result}
def main():
    p=argparse.ArgumentParser();p.add_argument("--ledger",type=Path,required=True);p.add_argument("--output",type=Path,required=True);a=p.parse_args()
    result=evaluate([json.loads(s) for s in a.ledger.open() if s.strip()])
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps(result["models"],ensure_ascii=False))
if __name__=="__main__":main()
