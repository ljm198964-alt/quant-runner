import unittest
from datetime import datetime, timezone
from research.m2.market_dataset import two_sided

NOW=datetime(2026,10,16,10,0,tzinfo=timezone.utc)
def match():
    return {"market_raw_evidence":{"source_bookmaker":"crown",
      "source_bookmaker_verified":True,
      "asian_list":[[None,-0.25,1.9,2.0,"2026-10-16 17:50:00"]]}}

class MarketDatasetTests(unittest.TestCase):
    def test_two_sides_from_crown(self):
        x,e=two_sided(match(),"AH",NOW)
        self.assertIsNone(e)
        self.assertAlmostEqual(x["no_vig_first"],(1/1.9)/(1/1.9+1/2.0))
        self.assertAlmostEqual(x["no_vig_first"]+x["no_vig_second"],1)
        self.assertGreater(x["overround"],1)
    def test_reject_non_crown_and_stale(self):
        m=match()
        m["market_raw_evidence"]["source_bookmaker"]="other"
        self.assertEqual(two_sided(m,"AH",NOW)[1],"NOT_CROWN")
        m=match()
        m["market_raw_evidence"]["asian_list"][0][4]="2026-10-16 12:00:00"
        self.assertEqual(two_sided(m,"AH",NOW)[1],"NO_FRESH_TWO_SIDED_CROWN")
    def test_no_future_quote(self):
        m=match()
        m["market_raw_evidence"]["asian_list"][0][4]="2026-10-16 19:00:00"
        self.assertEqual(two_sided(m,"AH",NOW)[1],"NO_FRESH_TWO_SIDED_CROWN")

if __name__=="__main__":
    unittest.main()
