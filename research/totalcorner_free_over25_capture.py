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
        super().__init__();self.rows=[];self.row=None;self.cell=None;self.in_table=0
    def handle_starttag(self,tag,attrs):
        if tag=="table":self.in_table+=1
        if not self.in_table:return
        if tag=="tr":self.row=[]
        elif tag in ("td","th") and self.row is not None:self.cell=[]
    def handle_data(self,data):
        if self.cell is not None:self.cell.append(data)
    def handle_endtag(self,tag):
        if tag in ("td","th") and self.cell is not None:
            self.row.append(" ".join(" ".join(self.cell).split()));self.cell=None
        elif tag=="tr" and self.row is not None:
            self.rows.append(self.row);self.row=None
        elif tag=="table" and self.in_table:self.in_table-=1

def capture(page):
    url=BASE if page==1 else BASE+"/page:"+str(page)
    with urlopen(Request(url,headers={"User-Agent":"Mozilla/5.0 MR1-research-readonly"}),timeout=25) as res:
        raw=res.read();resolved=res.geturl()
        charset=res.headers.get_content_charset() or "utf-8"
    parser=Tables();parser.feed(raw.decode(charset,errors="replace"))
    result=[]
    for cells in parser.rows:
        if not any("大2.5" in x or "Over 2.5" in x for x in cells):continue
        result.append({"raw_cells":cells,"raw_label":"OVER_2_5",
                       "retrospective_at_capture":any(x in ("全","FT","Win","Loss","贏","輸") for x in cells)})
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
            "pages":pages,"total_rows":sum(len(x["rows"]) for x in pages)}
    from pathlib import Path
    out=Path(args.output);out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps({"captured_at_utc":now,"pages":len(pages),
                      "rows":report["total_rows"],"research_only":True}))
if __name__=="__main__":main()
