import unittest
from research.m3.crown_fixture_join_audit import check_pair

class FixtureJoinAuditTests(unittest.TestCase):
    def setUp(self):
        self.f = dict(fixture_identity_id='id', league='E0', season='2627', home_team='Home', away_team='Away', forecasted_at_utc='2026-10-21T09:00:00Z')
        self.s = dict(fixture_identity_id='id', league='E0', season='2627', home_team='Home', away_team='Away', totalcorner_match_id='123', join_method='official_fixture_crosscheck', identity_evidence_uri='private://identity/123', kickoff_at_utc='2026-10-23T12:00:00Z', kickoff_evidence_captured_at_utc='2026-10-21T10:00:00Z')
    def test_exact_valid(self):
        self.assertTrue(check_pair(self.f, self.s))
    def test_no_tz(self):
        self.s['kickoff_at_utc'] = '2026-10-23T12:00:00'
        self.assertFalse(check_pair(self.f, self.s))
    def test_identity_mismatch(self):
        self.s['away_team'] = 'Other'
        self.assertFalse(check_pair(self.f, self.s))
    def test_unverifiable_source(self):
        self.s.pop('identity_evidence_uri')
        self.assertFalse(check_pair(self.f, self.s))
    def test_forecast_after_evidence(self):
        self.s['kickoff_evidence_captured_at_utc'] = '2026-10-21T08:00:00Z'
        self.assertFalse(check_pair(self.f, self.s))

if __name__ == '__main__':
    unittest.main()
