"""M3 retry tests: same slot does not create a second order."""
import unittest
from unittest.mock import patch
from research.m3.m3_shadow_orders import build,slot_for

class M3Idempotency(unittest.TestCase):
    def test_slot_timezone_and_midnight(self):
        self.assertEqual(slot_for("2026-10-27T01:30:00Z"),"2026-10-27T06:00+08:00")
        self.assertEqual(slot_for("2026-10-27T09:30:00Z"),"2026-10-27T12:00+08:00")
        self.assertEqual(slot_for("2026-10-26T21:30:00Z"),"2026-10-26T12:00+08:00")

    def test_retry_does_not_duplicate_previous_run(self):
        def data(run,time):
            forecast={'protocol':'M3_TOTALCORNER_FORWARD_FORECAST_V1','forecast_id':run,
              'run_id':run,'forecasted_at_utc':time,'fixture_identity_id':'fixture-1',
              'model':'poisson','score_probability_grid':[],'kickoff_utc_verified':'2026-10-28T20:00:00Z'}
            quotes=[{'protocol':'M3_TOTALCORNER_FORWARD_EV_V1','forecast_id':run,'market':m,
              'line':2.5,'side':side,'decimal_odd':1.9,'totalcorner_match_id':'1',
              'expected_unit_return':0,'quote_snapshot_recorded_utc':time}
              for m,sides in [('AH',('home','away')),('OU',('over','under'))] for side in sides]
            return [forecast]+quotes
        with patch('research.m3.m3_shadow_orders.choose',side_effect=lambda f,m,q:(q[0],{})):
            first,_,_=build(data('first','2026-10-27T04:10:00Z'),run_id='first')
            self.assertEqual(len(first),2)
            retry,_,_=build(data('first','2026-10-27T04:10:00Z')+first+data('retry','2026-10-27T09:00:00Z'),run_id='retry')
            self.assertEqual(len(retry),0)
            next_slot,_,_=build(data('first','2026-10-27T04:10:00Z')+first+data('next','2026-10-27T22:15:00Z'),run_id='next')
            self.assertEqual(len(next_slot),2)
if __name__=='__main__':unittest.main()
