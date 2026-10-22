import unittest
from research.m3.evolution_rolling_gate import evaluate

class RollingGateTests(unittest.TestCase):
    def test_no_settlements_means_no_promotion(self):
        candidate={"model":"poisson","train_years":2,"fixture_id":"fx","source_date":"2026-10-28",
            "registered_at_utc":"2026-10-22T00:00:00+00:00",
            "score_grid":[[0.25,0.25],[0.25,0.25]]}
        result=evaluate([], [candidate])
        self.assertEqual(result["models"]["poisson"]["rolling_shadow_active"],"baseline")
        self.assertEqual(result["models"]["poisson"]["decision"],"HOLD")
    def test_invalid_previous_active_rollback(self):
        prior={"models":{"poisson":{"rolling_shadow_active":"rolling_2y"}}}
        result=evaluate([], [], prior)
        self.assertEqual(result["models"]["poisson"]["decision"],"ROLLBACK_SHADOW_ONLY")
        self.assertEqual(result["models"]["poisson"]["rolling_shadow_active"],"baseline")

if __name__=="__main__": unittest.main()

class PromotionEvidenceTests(unittest.TestCase):
    def test_chronological_evidence_promotes_rolling_2y(self):
        import datetime
        base=[];challengers=[]
        start=datetime.date(2026,11,1)
        for index in range(100):
            date=(start+datetime.timedelta(days=index)).isoformat()
            fid='f'+str(index);pred='p'+str(index)
            base.extend([
                {'protocol':'M3_TOTALCORNER_FORWARD_FORECAST_V1','forecast_id':pred,
                 'model':'poisson','fixture_identity_id':fid,'forecasted_at_utc':date+'T00:00:00+00:00',
                 'source_fixture_date':date,'score_probability_grid':[[0.01,0.98],[0.00,0.01]]},
                {'protocol':'M3_TOTALCORNER_FORWARD_SETTLEMENT_V1','forecast_id':pred,
                 'home_goals':1,'away_goals':0}
            ])
            challengers.append({'model':'poisson','train_years':2,'fixture_id':fid,
                'source_date':date,'registered_at_utc':'2026-10-22T00:00:00+00:00',
                'score_grid':[[0.02,0.01],[0.95,0.02]]})
        result=evaluate(base,challengers)
        self.assertEqual(result['models']['poisson']['decision'],'PROMOTE_SHADOW_ONLY')
        self.assertEqual(result['models']['poisson']['rolling_shadow_active'],'rolling_2y')
        rolled_back=evaluate([],[],result)
        self.assertEqual(rolled_back['models']['poisson']['decision'],'ROLLBACK_SHADOW_ONLY')
        self.assertEqual(rolled_back['models']['poisson']['rolling_shadow_active'],'baseline')
