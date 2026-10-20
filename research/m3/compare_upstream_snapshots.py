"""Compare upstream M3 V4 research snapshots without selecting/trading models."""
import argparse
import csv
import json
from pathlib import Path

METRICS = ("log_loss", "brier", "roc_auc", "accuracy", "roi", "bets", "n_test")

def load(path):
    if not path.exists():
        return {}
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    return {(r.get("model"), r.get("test_season")): r for r in rows}

def compare(old_path, new_path, run_id):
    old, new = load(old_path), load(new_path)
    comparison = []
    for key in sorted(set(old) & set(new)):
        left, right = old[key], new[key]
        diffs = {}
        for metric in METRICS:
            if left.get(metric) in (None, "") or right.get(metric) in (None, ""):
                continue
            a, b = float(left[metric]), float(right[metric])
            diffs[metric] = {"previous": a, "current": b, "delta": b - a}
        comparison.append({"model": key[0], "test_season": key[1], "metrics": diffs})
    return {
        "protocol": "M3_ORIGINAL_V4_SNAPSHOT_COMPARISON_V1",
        "run_id": str(run_id),
        "scope": "upstream_original_v4_non_crown_research",
        "previous_available": bool(old),
        "previous_rows": len(old),
        "current_rows": len(new),
        "paired_model_seasons": len(comparison),
        "comparison": comparison,
        "automatic_model_promotion": False,
        "telegram": False,
        "note": "Descriptive run-to-run differences only. Changes in data, source revision and test coverage can explain deltas. No model is selected or promoted.",
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--previous", type=Path, required=True)
    p.add_argument("--current", type=Path, required=True)
    p.add_argument("--run-id", required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    if not args.current.exists():
        raise SystemExit("Current original V4 metrics missing; cannot compare")
    result = compare(args.previous, args.current, args.run_id)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print("M3_COMPARISON_WRITTEN", result["paired_model_seasons"])

if __name__ == "__main__":
    main()
