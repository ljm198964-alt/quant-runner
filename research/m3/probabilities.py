"""Independent M3 AH/OU score-distribution evaluation; no production or Telegram dependencies."""
import argparse
import json
import math
from pathlib import Path


def _poisson(mean, maximum):
    if not isinstance(mean, (int, float)) or not math.isfinite(mean) or mean < 0:
        raise ValueError("Expected goals must be finite and nonnegative")
    probs = [math.exp(-mean)]
    for goals in range(1, maximum + 1):
        probs.append(probs[-1] * mean / goals)
    return probs


def _asian_component(diff, price):
    if diff > 1e-9:
        return ("FULL_WIN", price - 1)
    if diff < -1e-9:
        return ("FULL_LOSS", -1)
    return ("PUSH", 0)


def _asian_result(metric, line, decimal):
    if not math.isfinite(line) or not math.isfinite(decimal) or decimal <= 1:
        raise ValueError("Invalid quoted line/price")
    quarter = round(line * 4)
    if abs(line * 4 - quarter) > 1e-8:
        raise ValueError("Asian lines must use quarter-goal increments")
    # Whole and half-goal contracts settle as one bet; quarter-goal contracts
    # settle as half a stake on each neighboring half-goal line.
    if quarter % 2:
        components = [(math.floor(line * 2) / 2, .5),
                      (math.ceil(line * 2) / 2, .5)]
    else:
        components = [(line, 1.)]
    pnl = sum(weight * _asian_component(metric + component_line, decimal)[1]
              for component_line, weight in components)
    if pnl > 1e-9:
        state = "FULL_WIN" if abs(pnl - (decimal - 1)) <= 1e-8 else "HALF_WIN"
    elif pnl < -1e-9:
        state = "FULL_LOSS" if abs(pnl + 1) <= 1e-8 else "HALF_LOSS"
    else:
        state = "PUSH"
    return state, pnl


def settle_score(market, line, side, home_goals, away_goals, decimal):
    """Settle a Crown-style Asian market line against an exact final score.

    ``line`` is the home-team handicap for AH or total-goals line for OU.
    ``decimal`` is the price on the named selection. Source provenance and quote
    timestamps must be validated separately before calling this helper.
    """
    for name, score in (("home_goals", home_goals), ("away_goals", away_goals)):
        if isinstance(score, bool) or not isinstance(score, int) or score < 0:
            raise ValueError(f"{name} must be a non-negative integer")
    if market == "AH":
        if side == "home":
            metric, selected_line = home_goals - away_goals, line
        elif side == "away":
            metric, selected_line = away_goals - home_goals, -line
        else:
            raise ValueError("AH side must be home or away")
    elif market == "OU":
        if side == "over":
            metric, selected_line = home_goals + away_goals, -line
        elif side == "under":
            metric, selected_line = -(home_goals + away_goals), line
        else:
            raise ValueError("OU side must be over or under")
    else:
        raise ValueError("market must be AH or OU")
    return _asian_result(metric, selected_line, decimal)


def expected_unit_return(state_probabilities, decimal):
    """Compute unit EV from probabilities of Asian settlement outcomes."""
    if not isinstance(state_probabilities, dict):
        raise ValueError("state_probabilities must be an object")
    states = ("FULL_WIN", "HALF_WIN", "PUSH", "HALF_LOSS", "FULL_LOSS")
    if set(state_probabilities) != set(states):
        raise ValueError(f"state_probabilities must contain exactly {list(states)}")
    if not isinstance(decimal, (int, float)) or isinstance(decimal, bool) \
            or not math.isfinite(decimal) or decimal <= 1:
        raise ValueError("decimal must be finite and greater than 1")
    values = []
    for state in states:
        value = state_probabilities[state]
        if not isinstance(value, (int, float)) or isinstance(value, bool) \
                or not math.isfinite(value) or not 0 <= value <= 1:
            raise ValueError(f"probability {state} must be finite and between 0 and 1")
        values.append(value)
    if not math.isclose(sum(values), 1.0, rel_tol=0, abs_tol=1e-9):
        raise ValueError("state probabilities must sum to 1")
    p = state_probabilities
    return ((p["FULL_WIN"] + 0.5 * p["HALF_WIN"]) * (decimal - 1)
            - p["FULL_LOSS"] - 0.5 * p["HALF_LOSS"])


def market_probabilities(home_mean, away_mean, market, line, price, maximum=30):
    """Home AH/over OU probabilities from independent home/away expected goals.

    Returns conditional distribution within the enumerated score grid; exact
    omitted probability mass is shown to prevent a false claim of exactness.
    """
    if market not in ("AH_HOME", "AH_AWAY", "OU_OVER", "OU_UNDER"):
        raise ValueError("Unknown market")
    home, away = _poisson(home_mean, maximum), _poisson(away_mean, maximum)
    sums = {x: 0.0 for x in ("FULL_WIN", "HALF_WIN", "PUSH", "HALF_LOSS", "FULL_LOSS")}
    for h, hp in enumerate(home):
        for a, ap in enumerate(away):
            mass = hp * ap
            metric = (h - a if market == "AH_HOME" else
                      a - h if market == "AH_AWAY" else
                      h + a if market == "OU_OVER" else
                      -(h + a))
            state, _ = _asian_result(metric, line, price)
            sums[state] += mass
    coverage = sum(sums.values())
    state_probabilities = {k: v / coverage for k, v in sums.items()}
    return {"states": state_probabilities,
            "expected_profit_per_unit": expected_unit_return(state_probabilities, price),
            "score_grid_probability_coverage": coverage}


def evaluate(input_row):
    h, a = float(input_row["lambda_home"]), float(input_row["lambda_away"])
    ah, ou = input_row["ah"], input_row["ou"]
    line_h = float(ah["home_line"])
    line_ou = float(ou["total_line"])
    return {"protocol": "M3_INDEPENDENT_AH_OU_PROBABILITIES_V1",
            "fixture_id": input_row["fixture_id"],
            "model_expected_goals": {"home": h, "away": a},
            "ah": {
                "home": market_probabilities(h, a, "AH_HOME", line_h, float(ah["home_decimal"])),
                "away": market_probabilities(h, a, "AH_AWAY", -line_h, float(ah["away_decimal"]))
            },
            "ou": {
                "over": market_probabilities(h, a, "OU_OVER", -line_ou, float(ou["over_decimal"])),
                "under": market_probabilities(h, a, "OU_UNDER", line_ou, float(ou["under_decimal"]))
            },
            "research_only": True, "telegram_write": False, "trained_model": False}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    opts = parser.parse_args()
    row = json.loads(Path(opts.input).read_text())
    result = evaluate(row)
    Path(opts.output).write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
