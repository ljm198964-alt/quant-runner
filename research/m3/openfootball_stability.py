"""Deterministic stability audit for an existing M3 OpenFootball OOS run.

This consumes saved artifacts only. It does not fit models, fetch data, inspect
other M models, or calculate Crown EV/ROI.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import random
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


MODEL_NAMES = ("poisson", "dixon_coles", "bivariate_poisson")
MATCH_FIELDS = (
    "league", "season", "match_date_utc", "home_team", "away_team",
    "actual_home_goals", "actual_away_goals",
)
METRICS = ("log_loss", "brier")
MARKETS = {
    "AH0_DNB_3WAY": "ah_home_0",
    "OU_OVER_2_5": "ou_over_2_5",
}
EPS = 1e-15


def _utc(value: str, field: str) -> datetime:
    if not isinstance(value, str):
        raise ValueError(f"{field} must be an ISO-8601 UTC timestamp")
    try:
        result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"{field} must be an ISO-8601 UTC timestamp") from exc
    if result.tzinfo is None or result.utcoffset() != timezone.utc.utcoffset(result):
        raise ValueError(f"{field} must have a UTC offset of zero")
    return result.astimezone(timezone.utc)


def _match_key(row: dict[str, str]) -> tuple[str, ...]:
    if any(not row.get(field) for field in MATCH_FIELDS):
        raise ValueError("scored prediction row is missing an exact match identity field")
    return tuple(row[field] for field in MATCH_FIELDS)


def _load_predictions(path: Path) -> tuple[dict[str, dict[tuple[str, ...], dict]], str, int]:
    model_rows: dict[str, dict[tuple[str, ...], dict]] = {m: {} for m in MODEL_NAMES}
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    generated_rows = 0
    with path.open(newline="", encoding="utf-8") as stream:
        for row in csv.DictReader(stream):
            model = row.get("model")
            if model not in model_rows:
                continue
            generated_rows += 1
            if row.get("prediction_status") != "predicted":
                continue
            key = _match_key(row)
            train_end = _utc(row.get("train_end_utc", ""), "train_end_utc")
            test_date = _utc(row.get("source_match_date_calendar_key_utc", ""), "source_match_date_calendar_key_utc")
            if train_end >= test_date:
                raise ValueError(f"future-data leakage: training cutoff is not before test date for {model} {key}")
            if key in model_rows[model]:
                raise ValueError(f"duplicate scored match identity for {model}: {key}")
            model_rows[model][key] = row

    key_sets = [set(model_rows[m]) for m in MODEL_NAMES]
    if not key_sets[0] or any(keys != key_sets[0] for keys in key_sets[1:]):
        counts = {m: len(model_rows[m]) for m in MODEL_NAMES}
        raise ValueError(f"models do not share an identical scored match set: {counts}")
    return model_rows, digest, generated_rows


def _row_losses(row: dict[str, str], market: str) -> dict[str, float]:
    if market == "AH0_DNB_3WAY":
        labels = {"win": 0, "push": 1, "lose": 2}
        if row.get("actual_ah_home_0") not in labels:
            raise ValueError("unexpected AH0/DNB result label")
        probs = [float(row[k]) for k in ("ah_home_0_p_win", "ah_home_0_p_push", "ah_home_0_p_lose")]
        probs = [min(1.0, max(EPS, p)) for p in probs]
        total = sum(probs)
        probs = [p / total for p in probs]
        actual = labels[row["actual_ah_home_0"]]
        return {
            "log_loss": -math.log(probs[actual]),
            "brier": sum((p - (1.0 if idx == actual else 0.0)) ** 2 for idx, p in enumerate(probs)),
        }
    p = float(row["ou_p_over_2_5"])
    actual = int(row["actual_ou_over_2_5"])
    clipped = min(1 - EPS, max(EPS, p))
    return {
        "log_loss": -(actual * math.log(clipped) + (1 - actual) * math.log(1 - clipped)),
        "brier": (p - actual) ** 2,
    }


def _cluster_bootstrap(model_rows: dict, seed: int, replicates: int) -> dict:
    cluster_losses: dict[str, dict[str, dict[str, dict[str, float]]]] = {
        market: defaultdict(lambda: {m: {metric: 0.0 for metric in METRICS} for m in MODEL_NAMES})
        for market in MARKETS
    }
    cluster_counts: dict[str, dict[str, int]] = {market: defaultdict(int) for market in MARKETS}
    for model in MODEL_NAMES:
        for row in model_rows[model].values():
            cluster = f"{row['league']}-{row['season']}"
            for market in MARKETS:
                values = _row_losses(row, market)
                for metric in METRICS:
                    cluster_losses[market][cluster][model][metric] += values[metric]
                if model == MODEL_NAMES[0]:
                    cluster_counts[market][cluster] += 1

    rng = random.Random(seed)
    output = {}
    for market in MARKETS:
        clusters = sorted(cluster_counts[market])
        if len(clusters) < 2:
            raise ValueError("cluster bootstrap requires at least two league-season blocks")
        samples = {
            model: {metric: [] for metric in METRICS}
            for model in MODEL_NAMES if model != "poisson"
        }
        for _ in range(replicates):
            chosen = rng.choices(clusters, k=len(clusters))
            n = sum(cluster_counts[market][cell] for cell in chosen)
            base = {metric: sum(cluster_losses[market][cell]["poisson"][metric] for cell in chosen)
                    for metric in METRICS}
            for model in samples:
                for metric in METRICS:
                    total = sum(cluster_losses[market][cell][model][metric] for cell in chosen)
                    samples[model][metric].append((total - base[metric]) / n)
        market_result = {}
        for model, by_metric in samples.items():
            market_result[model] = {}
            for metric, values in by_metric.items():
                values.sort()
                low = values[int(0.025 * (replicates - 1))]
                high = values[int(0.975 * (replicates - 1))]
                market_result[model][metric] = {
                    "mean_difference_vs_poisson": sum(values) / replicates,
                    "cluster_bootstrap_95pct_interval": [low, high],
                    "interval_includes_zero": low <= 0 <= high,
                }
        output[market] = {
            "block_unit": "league-season",
            "blocks": len(clusters),
            "replicates": replicates,
            "seed": seed,
            "comparisons_vs": "poisson",
            "models": market_result,
            "interpretation": "descriptive cluster-bootstrap uncertainty; not a strategy test or model promotion rule",
        }
    return output


def _probability_bias(rows: list[dict]) -> dict:
    """Describe forecast-minus-observed outcome rates without fitting a calibrator."""
    if not rows:
        return {"n": 0, "markets": {}}
    ah_labels = ("win", "push", "lose")
    ah_probability_columns = {
        "win": "ah_home_0_p_win", "push": "ah_home_0_p_push", "lose": "ah_home_0_p_lose",
    }
    ah_actual_column = "actual_ah_home_0"
    markets = {"AH0_DNB_3WAY": {"outcomes": {}}, "OU_OVER_2_5": {}}
    for label, column in ah_probability_columns.items():
        predicted = sum(float(row[column]) for row in rows) / len(rows)
        observed = sum(row[ah_actual_column] == label for row in rows) / len(rows)
        markets["AH0_DNB_3WAY"]["outcomes"][label] = {
            "mean_predicted_probability": predicted,
            "observed_rate": observed,
            "predicted_minus_observed": predicted - observed,
        }
    ou_predicted = sum(float(row["ou_p_over_2_5"]) for row in rows) / len(rows)
    ou_observed = sum(int(row["actual_ou_over_2_5"]) for row in rows) / len(rows)
    markets["OU_OVER_2_5"] = {
        "mean_predicted_probability": ou_predicted,
        "observed_rate": ou_observed,
        "predicted_minus_observed": ou_predicted - ou_observed,
    }
    return {"n": len(rows), "markets": markets}


def _probability_bias_by_group(model_rows: dict) -> dict:
    output = {}
    for model in MODEL_NAMES:
        rows = list(model_rows[model].values())
        by_season: dict[str, list[dict]] = defaultdict(list)
        by_league: dict[str, list[dict]] = defaultdict(list)
        by_league_season: dict[str, list[dict]] = defaultdict(list)
        for row in rows:
            by_season[row["season"]].append(row)
            by_league[row["league"]].append(row)
            by_league_season.setdefault(f"{row['league']}-{row['season']}", []).append(row)
        output[model] = {
            "overall": _probability_bias(rows),
            "by_test_season": {key: _probability_bias(value) for key, value in sorted(by_season.items())},
            "by_league": {key: _probability_bias(value) for key, value in sorted(by_league.items())},
            "by_league_season": {key: _probability_bias(value) for key, value in sorted(by_league_season.items())},
        }
    return output


def build_stability_report(report_path: Path, predictions_path: Path, bootstrap_seed: int = 20261020,
                           bootstrap_replicates: int = 10000) -> dict:
    report = json.loads(report_path.read_text(encoding="utf-8"))
    if report.get("protocol") != "M3_OPENFOOTBALL_STRICT_WALKFORWARD_V1":
        raise ValueError("unexpected M3 OOS report protocol")
    model_rows, prediction_sha, generated_rows = _load_predictions(predictions_path)
    model_reports = {row["model"]: row for row in report["models"]}
    if set(model_reports) != set(MODEL_NAMES):
        raise ValueError("OOS report must contain exactly the three audited penaltyblog models")

    scored_keys = set(model_rows[MODEL_NAMES[0]])
    expected_rows = report.get("scored_predictions")
    if expected_rows != generated_rows:
        raise ValueError("prediction CSV generated row count does not match OOS report")
    for model in MODEL_NAMES:
        metric_n = model_reports[model]["overall_metrics"]["ah_home_0"]["n_predicted"]
        if metric_n != len(model_rows[model]):
            raise ValueError(f"scored prediction row count does not match OOS metrics for {model}")
        for market, report_key in MARKETS.items():
            scored = [_row_losses(row, market) for row in model_rows[model].values()]
            summary = model_reports[model]["overall_metrics"][report_key]
            for metric in METRICS:
                calculated = sum(row[metric] for row in scored) / len(scored)
                if not math.isclose(calculated, float(summary[metric]), rel_tol=0.0, abs_tol=2e-8):
                    raise ValueError(f"prediction-level recomputation disagrees with OOS report for {model} {market} {metric}")

    split_rows: dict[str, dict[str, dict[str, dict]]] = {market: {} for market in MARKETS}
    for model in MODEL_NAMES:
        by_season = model_reports[model].get("by_test_season", [])
        for season_row in by_season:
            season = season_row["test_season"]
            for league, metrics in season_row.get("metrics", {}).items():
                for market, report_key in MARKETS.items():
                    metric = metrics.get(report_key)
                    if not metric or metric.get("n_predicted", 0) == 0:
                        continue
                    split_rows[market].setdefault(f"{league}-{season}", {})[model] = metric

    markets_out = {}
    for market, report_key in MARKETS.items():
        cells = split_rows[market]
        paired = {
            cell: values for cell, values in cells.items()
            if set(values) == set(MODEL_NAMES)
            and len({values[m]["n_predicted"] for m in MODEL_NAMES}) == 1
        }
        if not paired:
            raise ValueError(f"no fully paired OOS cells for {market}")

        cell_wins = {metric: {m: 0 for m in MODEL_NAMES} for metric in METRICS}
        weighted_total = {m: {metric: 0.0 for metric in METRICS} for m in MODEL_NAMES}
        total_n = 0
        season_acc = defaultdict(lambda: {"n": 0, **{m: {metric: 0.0 for metric in METRICS} for m in MODEL_NAMES}})
        for cell, values in paired.items():
            n = values[MODEL_NAMES[0]]["n_predicted"]
            total_n += n
            season = cell.rsplit("-", 1)[-1]
            season_acc[season]["n"] += n
            for metric in METRICS:
                cell_values = {m: float(values[m][metric]) for m in MODEL_NAMES}
                winner = min(cell_values.values())
                for model in MODEL_NAMES:
                    weighted_total[model][metric] += n * cell_values[model]
                    season_acc[season][model][metric] += n * cell_values[model]
                    if math.isclose(cell_values[model], winner, rel_tol=0.0, abs_tol=1e-12):
                        cell_wins[metric][model] += 1

        overall = {}
        for model in MODEL_NAMES:
            overall[model] = {}
            summary_metric = model_reports[model]["overall_metrics"][report_key]
            for metric in METRICS:
                pooled = weighted_total[model][metric] / total_n
                observed = float(summary_metric[metric])
                if not math.isclose(pooled, observed, rel_tol=0.0, abs_tol=2e-8):
                    raise ValueError(f"paired split aggregation disagrees with report for {model} {market} {metric}")
                overall[model][metric] = observed
                overall[model][f"{metric}_range_across_league_season_cells"] = [
                    min(float(p[model][metric]) for p in paired.values()),
                    max(float(p[model][metric]) for p in paired.values()),
                ]

        seasonal = {}
        for season, values in sorted(season_acc.items()):
            n = values["n"]
            seasonal[season] = {
                "paired_scored_matches": n,
                "metrics": {
                    model: {metric: values[model][metric] / n for metric in METRICS}
                    for model in MODEL_NAMES
                },
            }
        markets_out[market] = {
            "meaning": "AH0/DNB win-push-lose three-state probabilities" if market.startswith("AH") else "fixed Over 2.5 binary probability",
            "paired_league_season_cells": len(paired),
            "paired_scored_matches_per_model": total_n,
            "lower_is_better_cell_wins": cell_wins,
            "overall_metrics": overall,
            "weighted_metrics_by_test_season": seasonal,
        }

    calibration = {}
    for model in MODEL_NAMES:
        rows = list(model_rows[model].values())
        n = len(rows)
        ou_pred = sum(float(r["ou_p_over_2_5"]) for r in rows) / n
        ou_actual = sum(int(r["actual_ou_over_2_5"]) for r in rows) / n
        expected_ou = model_reports[model]["overall_metrics"]["ou_over_2_5"]
        if not math.isclose(ou_pred, expected_ou["mean_predicted_probability"], rel_tol=0.0, abs_tol=1e-8):
            raise ValueError(f"OU prediction mean mismatch for {model}")
        if not math.isclose(ou_actual, expected_ou["observed_rate"], rel_tol=0.0, abs_tol=1e-8):
            raise ValueError(f"OU outcome rate mismatch for {model}")
        calibration[model] = {
            "scored_matches": n,
            "OU_O2_5_mean_predicted_probability": ou_pred,
            "OU_O2_5_observed_over_rate": ou_actual,
            "OU_O2_5_calibration_bias_predicted_minus_observed": ou_pred - ou_actual,
        }

    if bootstrap_replicates < 1000:
        raise ValueError("use at least 1000 cluster bootstrap replicates")
    bootstrap = _cluster_bootstrap(model_rows, bootstrap_seed, bootstrap_replicates)
    for market, result in bootstrap.items():
        for model, by_metric in result["models"].items():
            for metric, summary in by_metric.items():
                summary["observed_pooled_difference_vs_poisson"] = (
                    markets_out[market]["overall_metrics"][model][metric]
                    - markets_out[market]["overall_metrics"]["poisson"][metric]
                )

    return {
        "protocol": "M3_OOS_STABILITY_AUDIT_V1",
        "source_report_protocol": report["protocol"],
        "data_source": report["data_source"],
        "data_source_commit": report["data_source_commit"],
        "source_report_generated_utc": report["generated_utc"],
        "input_fingerprint_sha256": report["input_fingerprint_sha256"],
        "evaluation_fingerprint_sha256": report["evaluation_fingerprint_sha256"],
        "prediction_file_sha256": prediction_sha,
        "test_matches": report["test_matches_total"],
        "prediction_rows": expected_rows,
        "scored_predictions_per_model": len(scored_keys),
        "paired_scored_matches_per_model": len(scored_keys),
        "models": list(MODEL_NAMES),
        "train_test_isolation": report["train_test_isolation"],
        "strict_utc_cutoff_rows_verified": len(scored_keys) * len(MODEL_NAMES),
        "markets": markets_out,
        "calibration": calibration,
        "probability_bias": _probability_bias_by_group(model_rows),
        "cluster_bootstrap": bootstrap,
        "crown_quotes_used": False,
        "Crown_EV": None,
        "Crown_ROI": None,
        "note": "Descriptive paired OOS stability only. No significance test, strategy, Crown quote, EV, ROI, drawdown, parameter selection or model promotion is implied.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--predictions", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = build_stability_report(args.report, args.predictions)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(args.output),
        "paired_scored_matches_per_model": result["paired_scored_matches_per_model"],
        "strict_utc_cutoff_rows_verified": result["strict_utc_cutoff_rows_verified"],
        "paired_cells_by_market": {k: v["paired_league_season_cells"] for k, v in result["markets"].items()},
        "Crown_ROI": None,
    }, indent=2))


if __name__ == "__main__":
    main()
