# M3 TotalCorner Crown offline import contract

`crown_totalcorner_import.py` is an offline adapter for a raw TotalCorner `match/bookmaker_odds/{match_id}` JSON response. It makes **no HTTP requests** and does not obtain credentials, subscribe, or decide whether collection is permitted. Use it only after obtaining written permission that covers automated retrieval, M3 research use, quote retention, and any intended publication. A VIP/API token by itself is not treated as written permission. TotalCorner's [API documentation](https://www.totalcorner.com/page/api) describes the `crown` slug, AH/goal movement arrays and source-profile timezone; the [Terms of Service](https://www.totalcorner.com/page/terms), last updated 2026-09-02, prohibit automated extraction without prior written consent.

## Input handling

- Keep both the raw API response and context sidecar in a private, access-controlled directory. Do not commit either file, normalized quotes, lines, prices or credentials to the public repo unless collection, retention and redistribution are separately authorized.
- The context must include `authorization.basis = "written_permission"` and a non-empty traceable `authorization.reference`. The CLI checks this before reading the raw response. Forecast provenance must explicitly set `forecast.system = "M3"`; other model systems are rejected. The public test fixtures use synthetic data only.
- The sidecar includes `capture.source_match_id`, capture receipt UTC, the IANA `capture.source_timezone` configured in the TotalCorner account, and a traceable `timezone_evidence_uri`; `source_fixture` must exactly match the provider's home/away names; `fixture` includes the independently verified UTC kickoff and exact M3 identity evidence; `forecast` references the saved M3 forecast or a strictly walk-forward hindcast.
- The API's unoffset match start and movement timestamps are parsed as source-local wall times, then converted to UTC using the explicitly supplied IANA zone. Nonexistent or ambiguous DST times fail closed. The API kickoff must exactly equal the independent UTC kickoff. No date-at-midnight substitution or fuzzy name mapping is allowed.

Example private sidecar (placeholders only):

```json
{
  "authorization": {"basis": "written_permission", "reference": "PERMISSION-REF"},
  "capture": {
    "source_match_id": "TOTALCORNER-MATCH-ID",
    "source_timezone": "Australia/Sydney",
    "timezone_evidence_uri": "private://timezone-setting-evidence",
    "received_at_utc": "2026-10-01T10:00:00Z"
  },
  "source_fixture": {"home_team": "Exact API home", "away_team": "Exact API away"},
  "fixture": {
    "competition": "M3 competition",
    "home_team": "Exact M3 home",
    "away_team": "Exact M3 away",
    "kickoff_at_utc": "2026-10-01T12:00:00Z",
    "identity_evidence_uri": "private://official-fixture-evidence",
    "m3_identity": {
      "join_method": "official_fixture_crosscheck",
      "league": "M3-LEAGUE",
      "season": "2627",
      "home_team": "Exact M3 home",
      "away_team": "Exact M3 away",
      "evidence_uri": "private://official-fixture-evidence"
    }
  },
  "forecast": {
    "system": "M3",
    "protocol": "RECORDED_FORWARD",
    "model": "M3 model name",
    "model_version": "M3 model version",
    "prediction_sha256": "64-lowercase-hex-digits",
    "train_end_utc": "2026-09-01T00:00:00Z",
    "predicted_at_utc": "2026-10-01T08:00:00Z"
  }
}
```

## Normalization rules

- Only the API response with `success=1`, one exact match ID, exact provider-side home/away names and exactly one `bookmakers[].slug == "crown"` entry is accepted.
- Only the documented 8-field `asian_list` and `goal_list` movement rows are considered: `[minute, line, price1, price2, time, home_score, away_score, closed]`.
- Keep rows only when the provider minute is null, `closed=0`, and converted observation time is strictly before the independent kickoff. In-play, suspended, at-kickoff and post-kickoff rows are excluded. The existing validator additionally checks quote time against receipt time, model cutoff and any contemporaneous forecast time.
- Lines must be a single numeric value. Comma-separated/compound lines are rejected pending an explicit, source-backed normalization rule; the adapter never guesses quarter-line semantics. The canonical evidence validator's private normalized record can preserve an accepted quarter line such as `-0.25` directly.
- Each quote row receives a canonical row hash; parsed JSON must exactly equal the UTF-8 JSON decoded from the supplied raw response, which is hashed byte-for-byte. The normalizer does not write either file.

Run in the authorized private environment:

```bash
python -m research.m3.crown_totalcorner_import \
  --response /private/path/authorized-crown-response.json \
  --context /private/path/authorized-capture-context.json
```

The CLI prints only counts and UTC-time ranges from `crown_evidence.validate_record`; it never prints prices or persists a normalized record. It does not calculate EV/ROI, settle bets, create orders, send Telegram, access M1/M2/MR1, or update the shadow ledger. This interface is not evidence that any historical quote exists or that permission has been obtained.
