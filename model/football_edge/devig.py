"""Turn bookmaker odds into probabilities, and remove the bookmaker's margin ("de-vig")."""

from collections.abc import Sequence


def implied_probabilities(odds: Sequence[float]) -> list[float]:
    """Raw implied probability of each outcome: 1 / decimal odds.

    Their sum is more than 1: the excess is the bookmaker's margin.
    Raises ValueError for fewer than 2 outcomes, or for any odds that are not greater
    than 1 (including NaN).
    """
    if len(odds) < 2:
        raise ValueError("At least two outcomes are required")
    if any(not odd > 1 for odd in odds):
        raise ValueError(f"All odds must be greater than 1, got {list(odds)}")
    return [1 / odd for odd in odds]


def overround(odds: Sequence[float]) -> float:
    """The bookmaker's margin: sum of implied probabilities minus 1.

    Example: 1.90 / 1.90 on a coin flip -> 0.0526 (5.26%).
    """
    return sum(implied_probabilities(odds)) - 1


def devig_proportional(odds: Sequence[float]) -> list[float]:
    """Fair probabilities with the margin removed proportionally.

    Each implied probability is divided by their sum, so the result sums to exactly 1
    and the ratios between outcomes stay the same.
    """
    probs = implied_probabilities(odds)
    total = sum(probs)
    return [p / total for p in probs]
