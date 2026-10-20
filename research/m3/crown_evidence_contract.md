# M3 Crown evidence intake contract

This is an **offline validation contract**, not a collector. It accepts an operator-supplied normalized JSON record only after the operator has confirmed written permission for the particular collection, use and retention. The validator does not make HTTP requests, access TotalCorner, read M1/M2/MR1, persist the input, compute EV/ROI, create orders or send Telegram messages.

Run it with:

```bash
python -m research.m3.crown_evidence path/to/authorized-record.json
```

The resulting summary contains counts and UTC timing only; it omits team names, lines, prices and payloads. Keep the supplied input outside the public repository unless publication and redistribution of every field are separately authorized. Record its SHA-256 in the authorized research environment, not by committing restricted quote values.

## Required checks

- `authorization.basis` is `written_permission`, with a traceable authorization reference.
- Source is the TotalCorner `crown` bookmaker endpoint, and capture method is an authorized manual export or authorized API. A public endpoint or API credential alone does not establish permission.
- Fixture identity is exact via a shared provider ID or an official fixture cross-check; fuzzy team-name joins are rejected. Store UTC kickoff and the evidence reference.
- Forecast identity includes model version, training cutoff and prediction digest. A recorded-forward prediction requires its actual prediction UTC timestamp. A retrospectively generated strict walk-forward result must be labelled `STRICT_WALK_FORWARD_HINDCAST` and is not represented as a contemporaneous live forecast.
- Every quote is an open, pre-match AH or OU record with both decimal prices, an observation UTC timestamp before kickoff and source receipt, and a source-row digest. It must postdate the training cutoff; a recorded forecast must predate the quote.

The validator's `VALID_PREMATCH_CROWN_EVIDENCE` status means only that these structural and timestamp checks passed. It is not execution proof, a profitability result, an admission rule or permission to trade. AH and OU remain separately evaluated. No freshness, EV, confidence, volume or league gates are introduced.

Synthetic records in `test_crown_evidence.py` are test fixtures only; they are not sports observations and must never be used as research results.
