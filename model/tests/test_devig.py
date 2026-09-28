"""Tests for football_edge.devig.

Reference match: Liverpool 2-0 Man City, Premier League, 2024-12-01.
Pinnacle closing 1X2 odds: home 2.06, draw 3.76, away 3.60.
Expected values were computed with a script, not by hand.
"""

import pytest

from football_edge.devig import devig_proportional, implied_probabilities, overround

LIVERPOOL_CITY = [2.06, 3.76, 3.60]


# --- implied_probabilities ---------------------------------------------------------------

def test_implied_probabilities_are_one_over_odds():
    assert implied_probabilities([2.0, 4.0, 5.0]) == pytest.approx([0.5, 0.25, 0.2])


def test_implied_probabilities_real_match():
    assert implied_probabilities(LIVERPOOL_CITY) == pytest.approx(
        [0.485437, 0.265957, 0.277778], abs=1e-6
    )


# --- overround ---------------------------------------------------------------------------

def test_overround_of_fair_odds_is_zero():
    assert overround([2.0, 2.0]) == pytest.approx(0.0)


def test_overround_coin_flip_at_190():
    assert overround([1.90, 1.90]) == pytest.approx(0.052632, abs=1e-6)


def test_overround_real_match():
    assert overround(LIVERPOOL_CITY) == pytest.approx(0.029172, abs=1e-6)


# --- devig_proportional ------------------------------------------------------------------

def test_devig_real_match():
    assert devig_proportional(LIVERPOOL_CITY) == pytest.approx(
        [0.471677, 0.258419, 0.269904], abs=1e-6
    )


def test_devig_sums_to_one():
    assert sum(devig_proportional(LIVERPOOL_CITY)) == pytest.approx(1.0)
    assert sum(devig_proportional([1.20, 6.50, 13.0])) == pytest.approx(1.0)


def test_devig_symmetric_two_way_market():
    assert devig_proportional([1.90, 1.90]) == pytest.approx([0.5, 0.5])


def test_devig_of_fair_odds_changes_nothing():
    assert devig_proportional([2.0, 4.0, 4.0]) == pytest.approx([0.5, 0.25, 0.25])


def test_devig_keeps_the_ratios_between_outcomes():
    home, draw, away = devig_proportional(LIVERPOOL_CITY)
    assert home / away == pytest.approx(3.60 / 2.06)


def test_devig_returns_a_list_in_the_same_order():
    result = devig_proportional((3.60, 2.06))  # a tuple must work too
    assert isinstance(result, list)
    assert result[0] < result[1]


# --- invalid input -----------------------------------------------------------------------

@pytest.mark.parametrize("function", [implied_probabilities, overround, devig_proportional])
@pytest.mark.parametrize(
    "bad_odds",
    [[], [2.0], [1.0, 2.0], [0.5, 3.0], [-2.0, 2.0], [float("nan"), 2.0]],
)
def test_invalid_odds_raise_value_error(function, bad_odds):
    with pytest.raises(ValueError):
        function(bad_odds)
