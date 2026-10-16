import unittest
from research.m1_weekly_account import report

class WeeklyReportTest(unittest.TestCase):
    def test_confirmed_only_and_separate_strategies(self):
        ledger={
          "picks":{
            "101|AH":{"pick_id":"a","market":"AH"},
            "102|OU":{"pick_id":"b","market":"OU","strategy_rule_version":"M1-OU-R1|M1_SELECTION_20260924_EARLY_ROBUST"},
            "103|OU":{"pick_id":"c","market":"OU","strategy_rule_version":"OLD"},
            "104|AH":{"pick_id":"d","market":"AH"}},
          "notifications":{
            "a":{"pick_id":"a","telegram":{"status":"SENT","sent_at":"2026-10-11T15:59:59Z","provider_message_id":"10"}},
            "b":{"pick_id":"b","telegram":{"status":"SENT","sent_at":"2026-10-11T16:00:00Z","provider_message_id":"11"}},
            "c":{"pick_id":"c","telegram":{"status":"SENT","sent_at":"2026-10-12T00:00:00Z","provider_message_id":"12"}},
            "d":{"pick_id":"d","telegram":{"status":"UNKNOWN","sent_at":"2026-10-12T00:00:00Z"}}},
          "settlements":{
            "101|AH":[{"state":"FULL_WIN","pnl_u":"0.9"}],
            "102|OU":[{"state":"HALF_LOSS","pnl_u":"-0.5"}],
          },
          "account_events":{}
        }
        got=report(ledger,"2026-10-12")
        self.assertEqual(got["tg_confirmed_unique"],3)
        self.assertEqual(got["week_tg_confirmed"],2)
        self.assertEqual(got["requested_week"]["M1 OU R1"]["net_u"],"-0.5")
        self.assertEqual(got["requested_week"]["M1 OU R1"]["roi"],"-0.5")
        self.assertEqual(got["requested_week"]["M1 OU old/other"]["pending"],1)
        self.assertEqual(got["all_time"]["M1 AH"]["sent"],1)

if __name__ == "__main__":
    unittest.main()
