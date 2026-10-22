import datetime,unittest
from research.m3.kickoff_gate import gate,MIN_LEAD_MINUTES,totalcorner_shanghai_kickoff
UTC=datetime.timezone.utc
class GateTests(unittest.TestCase):
    def test_minimum(self):
        t=datetime.datetime(2026,10,22,10,tzinfo=UTC)
        self.assertTrue(gate({'kickoff_utc_verified':'2026-10-22T11:30:00Z'},t)[0])
        self.assertFalse(gate({'kickoff_utc_verified':'2026-10-22T11:29:59Z'},t)[0])
    def test_profile_shanghai_conversion(self):
        self.assertEqual(totalcorner_shanghai_kickoff({'start':'2026-10-23 20:00:00'}),'2026-10-23T12:00:00+00:00')
        self.assertIsNone(totalcorner_shanghai_kickoff({'start':'bogus'}))
        self.assertIsNone(totalcorner_shanghai_kickoff({'start':'2026-10-23T20:00:00Z'}))
    def test_naive_block(self):
        t=datetime.datetime(2026,10,22,10,tzinfo=UTC)
        self.assertEqual(gate({'start':'2026-10-22 12:00:00'},t)[2],'KICKOFF_UTC_UNVERIFIED')
        self.assertFalse(gate({'kickoff_utc_verified':'2026-10-22 12:00:00'},t)[0])
if __name__=='__main__':unittest.main()
