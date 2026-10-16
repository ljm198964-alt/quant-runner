import json
import unittest
from datetime import datetime, timedelta, timezone
from research.m2.encrypted_ledger import encode, decode, stage, kickoff_utc

KEY="test-only-nonproduction-secret-0123456789abcdef"

def observation():
    return {"fixture_id":"123", "market":"OU", "side":"OVER",
            "line":2.5, "crown_decimal_price":1.95,
            "observed_at":"2026-10-15T10:05:00Z",
            "kickoff_bj":"2026-10-16 19:00:00",
            "observation_id":"ob-test", "shadow_order":False,
            "telegram_write":False}

class LedgerTests(unittest.TestCase):
    def test_opaque_aead_and_tampering(self):
        entry={"market":"OU","crown_decimal_price":1.95}
        encrypted=encode(entry,KEY)
        self.assertNotIn("1.95",encrypted)
        self.assertEqual(decode(encrypted,KEY),entry)
        with self.assertRaises(Exception):
            decode(encrypted,"different-test-secret-01234567890123456789")
        d=json.loads(encrypted)
        d["ciphertext"]="ff"+d["ciphertext"][2:]
        with self.assertRaises(Exception):
            decode(json.dumps(d),KEY)

    def test_only_prospective_and_no_duplicate(self):
        now=datetime(2026,10,15,10,20,tzinfo=timezone.utc)
        source={"source_run_id":"scan1","source_scan_finished_at":"2026-10-15T10:15:00Z"}
        obs=observation()
        rows,locks=stage(source,[obs],[],now)
        self.assertEqual(len(rows),1)
        self.assertEqual(len(locks),1)
        self.assertEqual(locks[0]["model_identity"],"M2_V0_M1_SIDE_BASELINE_ONLY")
        self.assertIsNone(locks[0]["pnl_u"])
        self.assertFalse(locks[0]["telegram_sent"])
        self.assertEqual(len(stage(source,[obs],locks,now)[1]),0)
        obs["kickoff_bj"]="2026-10-15 18:00:00"
        self.assertEqual(len(stage(source,[obs],[],now)[1]),0)

    def test_reject_stale_and_future_quote(self):
        now=datetime(2026,10,15,10,20,tzinfo=timezone.utc)
        old={"source_run_id":"scan1","source_scan_finished_at":"2026-10-15T02:15:00Z"}
        with self.assertRaises(ValueError):
            stage(old,[observation()],[],now)
        src={"source_run_id":"scan1","source_scan_finished_at":"2026-10-15T10:15:00Z"}
        bad=observation()
        bad["observed_at"]="2026-10-15T11:00:00Z"
        with self.assertRaises(ValueError):
            stage(src,[bad],[],now)

if __name__=="__main__":
    unittest.main()
