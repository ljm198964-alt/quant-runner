import unittest
from datetime import datetime,timezone
from decimal import Decimal
from research.m2.settle_forward import components, realized, summarize, verified_finals

def lock(market,side,line,price,fixture="123"):
    return {"model_identity":"M2_V0_M1_SIDE_BASELINE_ONLY",
            "fixture_id":fixture,"market":market,"side":side,"line":line,
            "crown_decimal_price":price,
            "kickoff_bj":"2026-10-14 19:00:00",
            "observation_id":"hash"}

def source(home=2,away=1):
    proof={"source":"TotalCorner API /match/view","raw_sha256":"verified-hash",
           "fixture_id":"123","home_goals":home,"away_goals":away,
           "locked_kickoff":"2026-10-14T11:00:00+00:00",
           "observed_at":"2026-10-14T15:00:00+00:00",
           "kickoff_changed":False}
    return {"results":{"123|AH":[proof]}}

class SettlementTests(unittest.TestCase):
    def test_quarter_handicap_and_goals(self):
        self.assertEqual(components("-0.25"),(-2,0))
        self.assertEqual(realized(lock("AH","HOME",-0.25,1.9),0,0),
                         ("HALF_LOSS",Decimal("-0.5")))
        self.assertEqual(realized(lock("AH","HOME",-0.25,1.9),1,0),
                         ("FULL_WIN",Decimal("0.9")))
        self.assertEqual(realized(lock("AH","AWAY",0.25,1.92),1,1),
                         ("HALF_WIN",Decimal("0.46")))
        self.assertEqual(realized(lock("OU","OVER",2.25,1.95),2,0),
                         ("HALF_LOSS",Decimal("-0.5")))
        self.assertEqual(realized(lock("OU","UNDER",2.25,1.95),1,0),
                         ("FULL_WIN",Decimal("0.95")))
    def test_proof_identity_and_dedup(self):
        today=datetime(2026,10,15,12,tzinfo=timezone.utc)
        row=lock("AH","HOME",-0.25,1.9)
        rows,reasons=summarize([row],[],source(),today)
        self.assertEqual(len(rows),1)
        self.assertEqual(rows[0]["state"],"FULL_WIN")
        self.assertEqual(summarize([row],rows,source(),today)[0],[])
        altered=source()
        altered["results"]["123|AH"][0]["locked_kickoff"]="2026-10-14T10:00:00+00:00"
        self.assertEqual(summarize([row],[],altered,today)[0],[])
    def test_unverified_does_not_settle(self):
        proof=source()
        proof["results"]["123|AH"][0]["raw_sha256"]=None
        self.assertEqual(summarize([lock("AH","HOME",-0.25,1.9)],[],proof,
             datetime(2026,10,15,12,tzinfo=timezone.utc))[0],[])

if __name__=="__main__":
    unittest.main()
