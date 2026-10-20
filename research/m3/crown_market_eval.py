"""Pure offline Asian market settlement and unit-EV helpers for M3 research.

This module does not fetch or persist odds, select bets, add admission rules, or
infer that a quote came from Crown. Callers must first validate quote provenance
with ``crown_evidence.validate_record`` and provide model outcome probabilities.
"""
from __future__ import annotations

import math


OUTCOMES = ("win", "half_win", "push", "half_loss", "loss")


def _validate_market_line(market: str, line: float, side: str) -> None:
    if market not in {"AH", "OU"}:
        raise ValueError("market must be AH or OU")
    if isinstance(line, bool) or not isinstance(line, (int, float)) or not math.isfinite(line):
        raise ValueError("line must be finite")
    if not math.isclose(line * 4, round(line * 4), abs_tol=1e-9):
        raise ValueError("line must use a whole, half, or quarter Asian line")
    valid_sides = {"home", "away"} if market == "AH" else {"over", "under"}
    if side not in valid_sides:
        raise ValueError(f"side must be one of {sorted(valid_sides)} for {market}")


def _components(line: float) -> list[tuple[float, float]]:
    """Return component lines and their stake weights for an Asian line."""
    doubled = line * 2
    if math.isclose(doubled, round(doubled), abs_tol=1e-9):
        return [(line, 1.0)]
    low = math.floor(doubled) / 2
    high = math.ceil(doubled) / 2
    return [(low, 0.5), (high, 0.5)]


def settle_unit(market: str, line: float, side: str, home_goals: int,
                away_goals: int, decimal_odds: float) -> dict:
    """Settle one unit on a selection; return its outcome and net unit profit.

    For AH, ``line`` is the home-team handicap as recorded by Crown; the away
    selection automatically uses the opposite handicap. For OU, it is the
    total-goals line. Quarter lines split one unit evenly across adjacent
    half-lines. Decimal odds are for the selected side.
    """
    _validate_market_line(market, line, side)
    for name, score in (("home_goals", home_goals), ("away_goals", away_goals)):
        if isinstance(score, bool) or not isinstance(score, int) or score < 0:
            raise ValueError(f"{name} must be a non-negative integer")
    if isinstance(decimal_odds, bool) or not isinstance(decimal_odds, (int, float)) \
            or not math.isfinite(decimal_odds) or decimal_odds <= 1:
        raise ValueError("decimal_odds must be finite and greater than 1")

    if market == "AH":
        selected_line = line if side == "home" else -line
        margin = home_goals - away_goals if side == "home" else away_goals - home_goals
        adjusted = lambda component: margin + component
    else:
        total = home_goals + away_goals
        adjusted = lambda component: total - component if side == "over" else component - total

    components = []
    profit = 0.0
    for component, weight in _components(selected_line if market == "AH" else line):
        value = adjusted(component)
        outcome = "win" if value > 0 else "loss" if value < 0 else "push"
        component_profit = (decimal_odds - 1) if outcome == "win" else -1.0 if outcome == "loss" else 0.0
        profit += weight * component_profit
        components.append({"line": component, "stake_fraction": weight, "outcome": outcome})

    component_outcomes = {component["outcome"] for component in components}
    if component_outcomes == {"win"}:
        outcome = "win"
    elif component_outcomes == {"loss"}:
        outcome = "loss"
    elif component_outcomes == {"push"}:
        outcome = "push"
    elif "win" in component_outcomes:
        outcome = "half_win"
    else:
        outcome = "half_loss"
    return {"outcome": outcome, "net_units": profit, "components": components}


def expected_unit_return(decimal_odds: float, outcome_probabilities: dict[str, float]) -> float:
    """Compute unit EV from win/half-win/push/half-loss/loss probabilities."""
    if isinstance(decimal_odds, bool) or not isinstance(decimal_odds, (int, float)) \
            or not math.isfinite(decimal_odds) or decimal_odds <= 1:
        raise ValueError("decimal_odds must be finite and greater than 1")
    if not isinstance(outcome_probabilities, dict) or set(outcome_probabilities) != set(OUTCOMES):
        raise ValueError(f"outcome_probabilities must contain exactly {list(OUTCOMES)}")
    values = []
    for outcome in OUTCOMES:
        value = outcome_probabilities[outcome]
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or not 0 <= value <= 1:
            raise ValueError(f"probability {outcome} must be finite and between 0 and 1")
        values.append(value)
    if not math.isclose(sum(values), 1.0, rel_tol=0, abs_tol=1e-9):
        raise ValueError("outcome probabilities must sum to 1")
    p = outcome_probabilities
    return ((p["win"] + 0.5 * p["half_win"]) * (decimal_odds - 1)
            - p["loss"] - 0.5 * p["half_loss"])
