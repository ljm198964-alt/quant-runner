"""Compare M3 penaltyblog OOS snapshots without promoting models."""
from __future__ import annotations
import argparse
import json
from pathlib import Path

METRICS = ("log_loss", "brier", "n_predicted", "n_test_total")
MARKETS = ("1x2", "ah_home_0", "ou_over_2_5")


def load(path: Path):
    return json.loads(path.read_text()) if path.exists() else None


def compare(previous, current):
    if previous is None:
        return {
            "protocol": "M3_PENALTYBLOG_SNAPSHOT_COMPARISON_V1",
            "status": "INITIAL_BASELINE_NO_COMPARISON",
            "test_set_identity_matches": None,
            "comparison": [],
            "automatic_model_promotion": False,
            "telegram_sent": False,
        }
    same_test_set = previous.get("test_set_fingerprint_sha256") == current.get("test_set_fingerprint_sha256")
    comparison = []
    prev_models = {m["model"]: m for m in previous.get("models", [])}
    curr_models = {m["model"]: m for m in current.get("models", [])}
    for model in sorted(set(prev_models) & set(curr_models)):
        for market in MARKETS:
            left = prev_models[model].get("overall_metrics", {}).get(market, {})
            right = curr_models[model].get("overall_metrics", {}).get(market, {})
            same_predicted_n = left.get("n_predicted") == right.get("n_predicted")
            comparable = same_test_set and same_predicted_n
            values = {}
            for metric in METRICS:
                a, b = left.get(metric), right.get(metric)
                if a is None or b is None:
                    continue
                values[metric] = {"previous": a, "current": b,
                                  "delta": (b - a) if comparable else None}
            comparison.append({"model": model, "market": market, "metrics": values})
            comparison[-1]["test_set_identity_matches"] = same_test_set
            comparison[-1]["predicted_row_count_matches"] = same_predicted_n
    return {
        "protocol": "M3_PENALTYBLOG_SNAPSHOT_COMPARISON_V1",
        "status": "COMPARABLE_TEST_SET" if same_test_set else "TEST_SET_CHANGED_NO_DIRECT_DELTA",
        "previous_run_utc": previous.get("generated_utc"),
        "current_run_utc": current.get("generated_utc"),
        "test_set_identity_matches": same_test_set,
        "input_fingerprint_matches": previous.get("input_fingerprint_sha256") == current.get("input_fingerprint_sha256"),
        "penaltyblog_version_matches": previous.get("penaltyblog_version") == current.get("penaltyblog_version"),
        "comparison": comparison,
        "automatic_model_promotion": False,
        "telegram_sent": False,
        "note": "Metric deltas are emitted only when the full test-set identity and predicted-row count both match. A matching test set does not imply unchanged training inputs or model code; deltas are descriptive and no model is selected or promoted.",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--previous", type=Path)
    parser.add_argument("--current", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    current = load(args.current)
    previous = load(args.previous) if args.previous else None
    result = compare(previous, current)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print("M3_PENALTYBLOG_COMPARISON", result["status"], len(result["comparison"]))


if __name__ == "__main__":
    main()
