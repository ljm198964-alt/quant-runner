# M3 Crown stage A/B archive audit

Audit scope: read-only examination of the already retained Crown/Bet365 paired-research artifact from GitHub Actions run [37765506416](https://github.com/ljm198964-alt/quant-runner/actions/runs/37765506416), plus the independently verified match result. This is not an exhaustive Crown archive, a live forecast, or a strategy backtest. No new Crown request was made.

## Archive and identity

- The run's retained artifact contains 16 fixture comparisons. Fifteen are outside M3's existing six-league sample scope. One joins the M3 Germany Bundesliga D1 2026/27 test identity: Borussia Dortmund–Werder Bremen, kickoff `2026-10-09T18:30:00Z`. The match identity, date and 2–2 result are confirmed by the [official Bundesliga match report](https://www.bundesliga.com/en/bundesliga/news/borussia-dortmund-werder-bremen-match-report-highlights-matchday-5-39473/) and [official match center](https://www.bundesliga.com/en/bundesliga/matchday/2026-2027/5/borussia-dortmund-vs-sv-werder-bremen/liveticker/).
- The M3 record is a strict historical walk-forward row keyed to 2026-10-09; its training ended `2026-05-16T00:00:00Z` with 2,754 earlier D1 result rows. Its probabilities were regenerated retrospectively in the October batch. Therefore it is a hindcast with temporal train/test isolation, **not** a contemporaneously recorded forecast available at the archived quote time.
- The archived source response SHA-256 is `2b60bd3ff46828451f1d1b06514020bbf52531571155108f6a3749905bd46c52`. The artifact identifies the bookmaker as Crown, but explicitly reports `bookmaker_execution_verified=false`; these are Crown-labelled aggregator observations, not verified bettor executions.

## Quote coverage and time

Within this one archived artifact, one of 17,027 M3 test matches has a fixture match (0.0059%). That match has one pre-kickoff AH quote record and one pre-kickoff OU quote record. Thus the observed coverage lower bound in this artifact search is 1/17,027 for each market. This is not a claim about all Crown history. The other 17,026 M3 test identities were not matched in this artifact; the 15 other artifact fixtures are outside the M3 scope.

The source snapshot was received at `2026-10-08T10:46:01.791Z`, before the stated kickoff. The selected AH movement observation was `2026-10-08T03:15:22Z` (450.66 minutes before kickoff); the selected OU observation was `2026-10-07T16:51:41Z` (1,074.35 minutes before kickoff). The artifact had seven AH and two OU movement rows; one observation per market was selected for this diagnostic. Both timestamps precede kickoff, but are relatively early. The age is reported descriptively; no quote-freshness gate was created.

Raw quote lines and prices are intentionally not replicated into this public report. The archive artifact and source response hash are the traceability references. The archived research workflow's Crown source was a paired comparison source, and cannot establish execution or represent all M3 fixtures.

## Line-specific probability and outcome diagnostic

Using the saved D1 2026/27 walk-forward fit parameters and the archived Crown line in memory, the three fitted goal distributions were reconstructed. Their AH and OU probabilities agree with the saved OOS row's relevant goal-distribution probabilities to less than `1e-9` for the checked outcomes. The table reports probabilities for the archived line, not a general AH/OU metric:

| Model | AH home-side probability | AH away-side probability | OU over probability | OU under probability |
|---|---:|---:|---:|---:|
| Poisson | 0.490364 | 0.509636 | 0.485653 | 0.514347 |
| Dixon-Coles | 0.487631 | 0.512369 | 0.482778 | 0.517222 |
| Bivariate Poisson | 0.489722 | 0.510278 | 0.485544 | 0.514456 |

For this one recorded price pair per market, all 12 model × market × side theoretical unit-EV calculations were negative. That retrospective diagnostic is highly sample-limited and is not an ROI estimate. With the verified 2–2 final score, the selected AH home side lost and away side won; OU over won and under lost. No side-selection policy was fixed in advance and no bet was placed, so there is no valid realized PnL, ROI, or maximum drawdown sequence. The winning-side outcomes do not turn ex-ante negative EV into positive expected value.

AH and OU are reported separately. The result does not show whether either model is profitable over a sample. It only demonstrates that saved M3 parameters can be reconciled with one archived Crown-labelled line without using a post-kickoff quote.

## Coverage gap and next step

The archived artifact cannot supply a denominator-wide Crown historical panel. No conclusion about absence of Crown data elsewhere is warranted. M3 has not obtained an authorized, sufficiently broad, contemporaneous Crown archive, so Crown line-level OOS Log Loss/Brier, valid-strategy yield, ROI and drawdown remain unavailable. The no-market OOS and shadow results remain the broader model evidence; the shadow ledger has 4,215 unique forward forecast keys but zero settlements and no captured Crown quotes.

TotalCorner's current terms prohibit automated extraction without prior written consent ([Terms](https://www.totalcorner.com/page/terms)); its API documentation's historical movement endpoint does not itself establish data collection or redistribution permission ([API](https://www.totalcorner.com/page/api)). The accompanying [offline M3 Crown evidence intake contract](crown_evidence_contract.md) provides structural and UTC validation for separately authorized, operator-supplied evidence. It does not fetch, publish restricted prices, compute ROI or create a trading gate.

No production model, formal ledger, strategy rule, Telegram path or non-M3 workflow was changed by this audit.
