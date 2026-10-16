import unittest
from research.m2.change_intervals import transitions

def scan(ts, prices, captured=None):
    m={"fixture_id":"42","market_raw_evidence":{"source_bookmaker":"crown",
       "source_bookmaker_verified":True,
       "asian_list":[[None,-0.5,*prices,"2026-10-16 08:00:00"]]},
       "market_capture_evidence":{"last_successful_fetch_at":captured}}
    return {"scan_status":"COMPLETE","finished_at":ts,"matches":[m]}

class ChangeIntervalTests(unittest.TestCase):
    def test_changed_and_unchanged_without_inventing_fetch(self):
        rows=[scan("2026-10-16T01:00:00Z",(1.9,2.0)),
              scan("2026-10-16T02:00:00Z",(1.9,2.0)),
              scan("2026-10-16T03:00:00Z",(1.91,2.0))]
        c=transitions(rows)
        self.assertEqual(c["AH_snapshots"],3)
        self.assertEqual(c["AH_unchanged_pairs"],1)
        self.assertEqual(c["AH_changed_pairs"],1)
        self.assertEqual(c["AH_change_time_unknown_pairs"],1)
    def test_verified_fetch_brackets_only_when_both_observed(self):
        rows=[scan("2026-10-16T01:00:00Z",(1.9,2.0),"2026-10-16T00:55:00Z"),
              scan("2026-10-16T02:00:00Z",(1.92,2.0),"2026-10-16T01:55:00Z")]
        self.assertEqual(transitions(rows)["AH_verified_fetch_brackets"],1)

if __name__=="__main__":
    unittest.main()
