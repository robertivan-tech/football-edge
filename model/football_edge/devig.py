"""Turn bookmaker odds into probabilities, and remove the bookmaker's margin ("de-vig").

Written by Robert. The tests in tests/test_devig.py describe the expected behaviour.
"""

from collections.abc import Sequence


def implied_probabilities(odds: Sequence[float]) -> list[float]:
    """Raw implied probability of each outcome: 1 / decimal odds.

    Their sum is more than 1: the excess is the bookmaker's margin.
    Raises ValueError for fewer than 2 outcomes or any odds <= 1.
    """
    raise NotImplementedError


def overround(odds: Sequence[float]) -> float:
    """The bookmaker's margin: sum of implied probabilities minus 1.

    Example: 1.90 / 1.90 on a coin flip -> 0.0526 (5.26%).
    """
    raise NotImplementedError


def devig_proportional(odds: Sequence[float]) -> list[float]:
    """Fair probabilities with the margin removed proportionally.

    Each implied probability is divided by their sum, so the result sums to exactly 1
    and the ratios between outcomes stay the same.
    """
    raise NotImplementedError
