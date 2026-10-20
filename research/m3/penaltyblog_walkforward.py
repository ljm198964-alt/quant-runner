"""Strict season-forward evaluation of penaltyblog goal models for independent M3 research.

Uses Football-Data.co.uk results only (date, teams, FT goals). No odds are read.
A test season is predicted from matches strictly before that season's first UTC match date.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
from collections import defaultdict
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path

import numpy as np
import pandas as pd
from penaltyblog.models import (
    BivariatePoissonGoalModel,
    DixonColesGoalModel,
    PoissonGoalsModel,
)

MODEL_TYPES = {
    "poisson": PoissonGoalsModel,
    "dixon_coles": DixonColesGoalModel,
    "bivariate_poisson": BivariatePoissonGoalModel,
}
REQUIRED = ("Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def read_matches(input_dir: Path) -> tuple[pd.DataFrame, list[dict]]:
    rows = []
    files = []
    for path in sorted(input_dir.glob("*.csv")):
        digest = sha256(path)
        try:
            frame = pd.read_csv(path)
        except Exception as exc:
            files.append({"file": path.name, "sha256": digest, "status": "read_error", "error": str(exc)})
            continue
        if not all(col in frame.columns for col in REQUIRED):
            files.append({"file": path.name, "sha256": digest, "status": "missing_columns"})
            continue
        # Upstream filenames are <season>_<league>.csv; retain both as provenance.
        stem = path.stem.split("_")
        season = stem[0] if len(stem) > 1 else "unknown"
        league = stem[1] if len(stem) > 1 else "unknown"
        frame = frame.loc[:, REQUIRED].copy()
        # Preserve only the source's calendar date in UTC. Football-Data.co.uk
        # provides date fields without a timezone, so discard any time component
        # and exclude every match on the test date from training.
        frame["match_date_utc"] = pd.to_datetime(
            frame["Date"], format="mixed", dayfirst=True, errors="coerce", utc=True
        ).dt.normalize()
        frame["home_goals"] = pd.to_numeric(frame["FTHG"], errors="coerce")
        frame["away_goals"] = pd.to_numeric(frame["FTAG"], errors="coerce")
        frame["home_team"] = frame["HomeTeam"].astype("string").str.strip()
        frame["away_team"] = frame["AwayTeam"].astype("string").str.strip()
        frame["season"] = season
        frame["league"] = league
        valid = (
            frame["match_date_utc"].notna()
            & frame["home_goals"].notna()
            & frame["away_goals"].notna()
            & frame["home_team"].notna()
            & frame["away_team"].notna()
            & frame["home_team"].ne("")
            & frame["away_team"].ne("")
        )
        valid_frame = frame.loc[valid].copy()
        valid_frame["home_goals"] = valid_frame["home_goals"].astype(int)
        valid_frame["away_goals"] = valid_frame["away_goals"].astype(int)
        valid_frame["source_file"] = path.name
        rows.extend(valid_frame.to_dict("records"))
        files.append({"file": path.name, "sha256": digest, "bytes": path.stat().st_size,
                      "rows_read": int(len(frame)), "rows_with_valid_date_teams_ft": int(valid.sum()),
                      "status": "ok"})
    if not rows:
        raise ValueError(f"No usable independent match results under {input_dir}")
    data = pd.DataFrame(rows).sort_values(["league", "match_date_utc", "source_file"], kind="stable")
    # Date-only source values are explicitly represented as midnight UTC. We exclude
    # the entire kickoff date from the training set, so an absent kickoff time cannot
    # allow same-day results into a forecast.
    data["kickoff_date_utc"] = data["match_date_utc"].dt.strftime("%Y-%m-%dT00:00:00Z")
    return data, files


def build_predictions(data: pd.DataFrame) -> tuple[list[dict], list[dict], list[dict]]:
    predictions: list[dict] = []
    splits: list[dict] = []
    fitted_models: list[dict] = []
    for league, league_data in data.groupby("league", sort=True):
        seasons = sorted(league_data["season"].unique(), key=lambda s: (league_data.loc[league_data.season.eq(s), "match_date_utc"].min(), s))
        for season_index, season in enumerate(seasons[1:], start=1):
            test = league_data.loc[league_data["season"].eq(season)].copy()
            cutoff = test["match_date_utc"].min()
            prior_seasons = set(seasons[:season_index])
            train = league_data.loc[
                league_data["season"].isin(prior_seasons)
                & league_data["match_date_utc"].lt(cutoff)
            ].copy()
            split_id = f"{league}-{season}"
            if train.empty:
                splits.append({"split_id": split_id, "league": league, "test_season": season,
                               "status": "no_prior_training_rows", "train_rows": 0, "test_rows": int(len(test))})
                continue
            if not (train["match_date_utc"].max() < cutoff and test["match_date_utc"].min() == cutoff):
                raise AssertionError(f"time leakage in {split_id}")
            split_meta = {"split_id": split_id, "league": league, "test_season": season,
                          "status": "predicted", "train_rows": int(len(train)), "test_rows": int(len(test)),
                          "train_start_utc": train["match_date_utc"].min().isoformat(),
                          "train_end_utc": train["match_date_utc"].max().isoformat(),
                          "test_start_utc": cutoff.isoformat(), "test_end_utc": test["match_date_utc"].max().isoformat(),
                          "cutoff_rule": "strictly_before_first_test_match_date_utc"}
            for model_name, model_cls in MODEL_TYPES.items():
                model = model_cls(train["home_goals"], train["away_goals"], train["home_team"], train["away_team"])
                model.fit()
                known = set(model.teams)
                fitted_models.append({
                    "model": model_name, "league": league, "test_season": season,
                    "train_rows": int(len(train)),
                    "train_start_utc": train["match_date_utc"].min().isoformat(),
                    "train_end_utc": train["match_date_utc"].max().isoformat(),
                    "training_teams": [str(team) for team in model.teams],
                    "parameters": {str(key): float(value) for key, value in model.get_params().items()},
                })
                for row in test.itertuples(index=False):
                    record = {
                        "model": model_name, "league": league, "season": season,
                        "match_date_utc": row.match_date_utc.isoformat(), "kickoff_date_utc": row.kickoff_date_utc,
                        "home_team": row.home_team, "away_team": row.away_team,
                        "actual_home_goals": int(row.home_goals), "actual_away_goals": int(row.away_goals),
                        "actual_result_1x2": "H" if row.home_goals > row.away_goals else "A" if row.home_goals < row.away_goals else "D",
                        "actual_ah_home_0": "win" if row.home_goals > row.away_goals else "lose" if row.home_goals < row.away_goals else "push",
                        "actual_ou_over_2_5": int(row.home_goals + row.away_goals > 2.5),
                        "source_file": row.source_file, "prediction_status": "predicted",
                        "train_rows": int(len(train)), "train_end_utc": train["match_date_utc"].max().isoformat(),
                    }
                    if row.home_team not in known or row.away_team not in known:
                        record["prediction_status"] = "unseen_team_in_training"
                        for col in ("p_home", "p_draw", "p_away", "ah_home_0_p_win", "ah_home_0_p_push", "ah_home_0_p_lose", "ou_p_over_2_5"):
                            record[col] = ""
                    else:
                        grid = model.predict(row.home_team, row.away_team)
                        p_h, p_d, p_a = (float(v) for v in grid.home_draw_away)
                        ah = grid.asian_handicap_probs("home", 0.0)
                        record.update({"p_home": p_h, "p_draw": p_d, "p_away": p_a,
                                       "ah_home_0_p_win": float(ah["win"]),
                                       "ah_home_0_p_push": float(ah["push"]),
                                       "ah_home_0_p_lose": float(ah["lose"]),
                                       "ou_p_over_2_5": float(grid.total_goals("over", 2.5))})
                    predictions.append(record)
            splits.append(split_meta)
    return predictions, splits, fitted_models


def score_rows(rows: list[dict], model: str, market: str) -> dict:
    valid = [r for r in rows if r["model"] == model and r["prediction_status"] == "predicted"]
    if not valid:
        return {"n_predicted": 0, "log_loss": None, "brier": None}
    eps = 1e-15
    if market == "1x2":
        cols, labels = ("p_home", "p_draw", "p_away"), {"H": 0, "D": 1, "A": 2}
        probs = np.asarray([[float(r[c]) for c in cols] for r in valid])
        actual = np.asarray([labels[r["actual_result_1x2"]] for r in valid])
    elif market == "ah_home_0":
        cols, labels = ("ah_home_0_p_win", "ah_home_0_p_push", "ah_home_0_p_lose"), {"win": 0, "push": 1, "lose": 2}
        probs = np.asarray([[float(r[c]) for c in cols] for r in valid])
        actual = np.asarray([labels[r["actual_ah_home_0"]] for r in valid])
    else:
        probs = np.asarray([float(r["ou_p_over_2_5"]) for r in valid])
        actual = np.asarray([int(r["actual_ou_over_2_5"]) for r in valid])
        p = np.clip(probs, eps, 1 - eps)
        log_loss = float(-np.mean(actual * np.log(p) + (1 - actual) * np.log(1 - p)))
        brier = float(np.mean((probs - actual) ** 2))
        calibration = []
        for bucket in range(10):
            lo, hi = bucket / 10, (bucket + 1) / 10
            mask = (probs >= lo) & ((probs < hi) if bucket < 9 else (probs <= hi))
            calibration.append({"probability_bin": f"{lo:.1f}-{hi:.1f}", "n": int(mask.sum()),
                                "mean_predicted_probability": float(np.mean(probs[mask])) if mask.any() else None,
                                "observed_rate": float(np.mean(actual[mask])) if mask.any() else None})
        return {"n_predicted": int(len(valid)), "n_test_total": int(sum(1 for r in rows if r["model"] == model)),
                "log_loss": log_loss, "brier": brier, "mean_predicted_probability": float(np.mean(probs)),
                "observed_rate": float(np.mean(actual)), "calibration_bins": calibration}
    probs = np.clip(probs, eps, 1)
    probs = probs / probs.sum(axis=1, keepdims=True)
    log_loss = float(-np.mean(np.log(probs[np.arange(len(actual)), actual])))
    one_hot = np.eye(probs.shape[1])[actual]
    brier = float(np.mean(np.sum((probs - one_hot) ** 2, axis=1)))
    class_names = ("home_win", "draw_push", "away_lose")
    calibration = {}
    for class_idx, class_name in enumerate(class_names):
        actual_class = (actual == class_idx).astype(int)
        bins = []
        for bucket in range(10):
            lo, hi = bucket / 10, (bucket + 1) / 10
            class_prob = probs[:, class_idx]
            mask = (class_prob >= lo) & ((class_prob < hi) if bucket < 9 else (class_prob <= hi))
            bins.append({"probability_bin": f"{lo:.1f}-{hi:.1f}", "n": int(mask.sum()),
                         "mean_predicted_probability": float(np.mean(class_prob[mask])) if mask.any() else None,
                         "observed_rate": float(np.mean(actual_class[mask])) if mask.any() else None})
        calibration[class_name] = bins
    return {"n_predicted": int(len(valid)), "n_test_total": int(sum(1 for r in rows if r["model"] == model)),
            "log_loss": log_loss, "brier": brier, "calibration_bins": calibration}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--previous-meta", type=Path)
    parser.add_argument("--quant-runner-commit", default="unknown")
    parser.add_argument("--upstream-commit", default="unknown")
    args = parser.parse_args()
    data, files = read_matches(args.input_dir)
    predictions, splits, fitted_models = build_predictions(data)
    models = []
    for model in MODEL_TYPES:
        model_rows = [r for r in predictions if r["model"] == model]
        by_season = []
        for season in sorted({r["season"] for r in model_rows}):
            season_rows = [r for r in model_rows if r["season"] == season]
            by_season.append({"season": season, "league_metrics": {
                league: {market: score_rows([r for r in season_rows if r["league"] == league], model, market)
                         for market in ("1x2", "ah_home_0", "ou_over_2_5")}
                for league in sorted({r["league"] for r in season_rows})}})
        overall = {market: score_rows(predictions, model, market) for market in ("1x2", "ah_home_0", "ou_over_2_5")}
        models.append({"model": model, "overall_metrics": overall, "by_test_season": by_season})
    data_fingerprint = hashlib.sha256("\n".join(f"{x['file']}:{x.get('sha256','')}" for x in files).encode()).hexdigest()
    test_identity = "\n".join(
        "|".join(str(r[k]) for k in ("league", "season", "match_date_utc", "home_team", "away_team", "actual_home_goals", "actual_away_goals"))
        for r in predictions if r["model"] == next(iter(MODEL_TYPES))
    )
    test_set_fingerprint = hashlib.sha256(test_identity.encode()).hexdigest()
    previous_fingerprint = None
    if args.previous_meta and args.previous_meta.exists():
        try:
            previous_fingerprint = json.loads(args.previous_meta.read_text()).get("input_fingerprint_sha256")
        except Exception:
            previous_fingerprint = None
    meta = {
        "protocol": "M3_PENALTYBLOG_STRICT_SEASON_FORWARD_V1",
        "model_identity": "M3", "generated_utc": datetime.now(timezone.utc).isoformat(),
        "data_source": "Football-Data.co.uk match-result CSV; only Date/HomeTeam/AwayTeam/FTHG/FTAG consumed; bookmaker columns ignored",
        "data_source_url": "https://www.football-data.co.uk/",
        "input_directory": str(args.input_dir), "input_files": files,
        "input_fingerprint_sha256": data_fingerprint,
        "test_set_fingerprint_sha256": test_set_fingerprint,
        "data_changed_vs_previous_snapshot": None if previous_fingerprint is None else data_fingerprint != previous_fingerprint,
        "usable_matches": int(len(data)), "league_counts": {k: int(v) for k, v in data.groupby("league").size().items()},
        "season_counts": {k: int(v) for k, v in data.groupby("season").size().items()},
        "test_matches_total": int(sum(s.get("test_rows", 0) for s in splits)),
        "test_matches_scored": int(sum(r["prediction_status"] == "predicted" for r in predictions if r["model"] == "poisson")),
        "scored_coverage_of_test_matches": (
            float(sum(r["prediction_status"] == "predicted" for r in predictions if r["model"] == "poisson"))
            / int(sum(s.get("test_rows", 0) for s in splits))
            if sum(s.get("test_rows", 0) for s in splits) else None
        ),
        "time_basis": "UTC; upstream date-only values parsed as UTC midnight; entire test match date excluded from training",
        "train_test_isolation": "For each league and test season, train rows come only from earlier season files and satisfy match_date_utc < earliest test-season match_date_utc. No same-date or test-season outcome is used to fit that split.",
        "handicap_diagnostic": "home Asian Handicap 0.0 (draw-no-bet); generic probability diagnostic only, no Crown price/line linkage or ROI",
        "ou_diagnostic": "Over 2.5 probability diagnostic only; no Crown price/line linkage or ROI",
        "penaltyblog_version": version("penaltyblog"), "quant_runner_commit": args.quant_runner_commit,
        "football_predictor_commit": args.upstream_commit,
        "fitted_models_count": len(fitted_models),
        "models": models, "automatic_model_promotion": False, "telegram_sent": False,
        "crown_roi": None,
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    pred_path = args.output_dir / "penaltyblog_oos_predictions.csv"
    if predictions:
        buffer = io.StringIO(newline="")
        writer = csv.DictWriter(buffer, fieldnames=list(predictions[0].keys()))
        writer.writeheader(); writer.writerows(predictions)
        prediction_csv = buffer.getvalue()
        pred_path.write_text(prediction_csv)
        meta["predictions_sha256"] = hashlib.sha256(prediction_csv.encode()).hexdigest()
        meta["prediction_rows"] = len(predictions)
        meta["prediction_artifact"] = f"research/m3/results/predictions/{meta['predictions_sha256']}.csv"
    parameter_text = json.dumps(fitted_models, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    parameter_path = args.output_dir / "penaltyblog_oos_model_parameters.json"
    parameter_path.write_text(parameter_text)
    meta["model_parameters_sha256"] = hashlib.sha256(parameter_text.encode()).hexdigest()
    meta["model_parameters_artifact"] = (
        f"research/m3/results/model_parameters/{meta['model_parameters_sha256']}.json"
    )
    (args.output_dir / "penaltyblog_oos_report.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n")
    (args.output_dir / "penaltyblog_oos_splits.json").write_text(json.dumps(splits, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({"protocol": meta["protocol"], "generated_utc": meta["generated_utc"],
                      "input_fingerprint_sha256": data_fingerprint, "usable_matches": meta["usable_matches"],
                      "test_matches_total": meta["test_matches_total"], "test_matches_scored": meta["test_matches_scored"],
                      "fitted_models_count": meta["fitted_models_count"],
                      "model_parameters_sha256": meta["model_parameters_sha256"],
                      "penaltyblog_version": meta["penaltyblog_version"], "models": models}, ensure_ascii=False))


if __name__ == "__main__":
    main()
