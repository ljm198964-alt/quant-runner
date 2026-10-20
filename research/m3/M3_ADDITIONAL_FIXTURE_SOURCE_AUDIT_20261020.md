# M3 additional no-market schedule source audit — 2026-10-20 UTC

Status: CANDIDATE_NOT_INTEGRATED. No new M3 fixtures, FT settlements, Crown quotes or Telegram actions produced.

## Current production evidence
- M3 OpenFootball forward-only shadow: 4,215 canonical model×fixture forecasts, 0 settled; current ledger performance status `NO_SETTLED_FORWARD_SAMPLES`, generated 2026-10-20T14:00:44Z.
- Most recent read-only confirmed Actions runs: M3 shadow 39438762203 SUCCESS and stability 39438762094 SUCCESS.
- Crown pairing latest status: 0 matched historical AH/OU pairs; `future_capture=not_started`, permissions for unattended M3 Crown collection not confirmed.
- Existing OpenFootball JSON source does not include B1 league and its calendar dates cannot be interpreted as exact UTC kickoff.

## New potential source (not approved)
- `oladeeayo/open-matchday` README: 2026/27 free fixture/result CSVs for 75 leagues; `leagues.py` has `BEL_1_pro-league` mapped to ESPN competition `bel.1` and Football-Data division `B1`.
- README states `fixtures_2627.csv` includes `date`, `time`, `home`, `away`, but describes `time` as "kickoff time CET-1 where known" and acknowledges missing times. This string is not a sufficiently documented, DST-safe IANA timezone or exact historical UTC evidence.
- This project collects third-party sources in a pipeline. Reuse requires source license/provenance verification, per-row source and fixture uniqueness checks, UTC timezone/DST audit, and direct comparison against original provider before adding observations to M3.
- It may eventually improve independent schedule coverage for B1 and fixture results; it is **not** a Crown bookmaker source or proof of permission to capture Crown.
- Do not backfill past forecasts or claim historic prediction-time availability based on current downloaded fixture snapshots.

## Verification tasks
1. Inspect candidate `BEL_1_pro-league/fixtures_2627.csv`, `results_2627.csv`, `build_summary.json` and underlying ESPN `bel.1` source at a consistent acquisition UTC time.
2. Validate exact fixture identity, presence and provenance of kickoff timestamp, and date/time timezone semantics, including summer/winter DST transitions, reschedules, and missing values.
3. Verify license and right to retain/derive research records, including upstream provider restrictions.
4. Only if above pass, implement an append-only M3-only kickoff/FT evidence store, retaining capture UTC and digest, with ambiguous records unpaired. No legacy model files or official ledger changes.
5. Recalculate no-market forward performance only when an objectively later FT matches previously recorded forward prediction and meets source/temporal validation; no Crown EV/ROI without verified authorized pre-kickoff quote.

Research only. No new trading gate, automatic promotion, Crown API request or TG.
