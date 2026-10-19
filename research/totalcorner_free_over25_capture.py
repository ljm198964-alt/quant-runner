#!/usr/bin/env python3
"""Read-only capture of TotalCorner public over-2.5 recommendations.
No Crown price substitution, no trading, no Telegram, no automatic schedule.
"""
import argparse, hashlib, json, re
from datetime import datetime, timezone
from html.parser import HTMLParser
from urllib.request import Request, urlopen

BASE="https://www.totalcorner.com/zh-tw/prediction/football-predictions-over-25-goals"
class Tables(HTMLParser):
    def __init__(self):
        super().__init__();self.rows=[];self.row=None;self.cell=None;self.in_table=0;self.links=[];self.row_links=[]
    def handle_starttag(self,tag,attrs):
        if tag=="table":self.in_table+=1
        if not self.in_table:return
        if tag=="tr":self.row=[];self.row_links=[]
        elif tag in ("td","th") and self.row is not None:self.cell=[]
        elif tag=="a" and self.row is not None:
            href=dict(attrs).get("href")
            if href:self.row_links.append(href)
    def handle_data(self,data):
        if self.cell is not None:self.cell.append(data)
    def handle_endtag(self,tag):
        if tag in ("td","th") and self.cell is not None:
            self.row.append(" ".join(" ".join(self.cell).split()));self.cell=None
        elif tag=="tr" and self.row is not None:
            self.rows.append({"cells":self.row,"links":self.row_links});self.row=None
        elif tag=="table" and self.in_table:self.in_table-=1

def capture(page):
    url=BASE if page==1 else BASE+"/page:"+str(page)
    with urlopen(Request(url,headers={"User-Agent":"Mozilla/5.0 MR1-research-readonly"}),timeout=25) as res:
        raw=res.read();resolved=res.geturl()
        charset=res.headers.get_content_charset() or "utf-8"
    parser=Tables();parser.feed(raw.decode(charset,errors="replace"))
    result=[]
    for record in parser.rows:
        cells=record["cells"]
        idx=next((i for i,x in enumerate(cells) if x.strip() in ("大2.5","Over 2.5")),None)
        if idx is None:continue
        outcome=cells[idx+1].strip() if idx+1<len(cells) else ""
        scored=next((re.search(r"\\b(\\d+)\\s*-\\s*(\\d+)\\b",x) for x in cells if re.search(r"\\b(\\d+)\\s*-\\s*(\\d+)\\b",x)),None)
        result.append({"raw_cells":cells,"links":record["links"],"raw_label":"OVER_2_5",
                       "displayed_market_line":cells[idx-1] if idx else None,
                       "reported_outcome":outcome if outcome in ("贏","輸","Win","Loss") else None,
                       "displayed_score":[int(scored.group(1)),int(scored.group(2))] if scored else None,
                       "retrospective_at_capture":outcome in ("贏","輸","Win","Loss"),
                       "prematch_publication_time_verified":False})
    return {"source_url":url,"resolved_url":resolved,"html_sha256":hashlib.sha256(raw).hexdigest(),
            "rows":result}

def main():
    p=argparse.ArgumentParser();p.add_argument("--pages",type=int,default=2)
    p.add_argument("--output",required=True);args=p.parse_args()
    if args.pages<1:raise SystemExit("invalid pages")
    now=datetime.now(timezone.utc).isoformat()
    pages=[capture(i) for i in range(1,args.pages+1)]
    report={"protocol":"TOTALCORNER_FREE_OVER25_SOURCE_CAPTURE_V1",
            "captured_at_utc":now,"product":"FREE_OVER_2_5_PUBLIC_PAGE",
            "research_only":True,"telegram_write":False,"formal_model_changed":False,
            "crown_trade_quote_present":False,
            "cannot_claim_pre_match_provenance_for_completed_rows":True,
            "historical_rows_not_forward_trades":True,
            "pages":pages,"total_rows":sum(len(x["rows"]) for x in pages)}
    from pathlib import Path
    out=Path(args.output);out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps({"captured_at_utc":now,"pages":len(pages),
                      "rows":report["total_rows"],"research_only":True}))
if __name__=="__main__":main()
