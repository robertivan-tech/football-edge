"""Tests for the pure helpers of the ticket analysis. No database needed."""

import pytest

from analyse_ticket import selection_probability

FAIR = {"H": 0.50, "D": 0.30, "A": 0.20}


@pytest.mark.parametrize(
    "selection, expected",
    [("1", 0.50), ("X", 0.30), ("2", 0.20), ("1X", 0.80), ("X2", 0.50), ("12", 0.70)],
)
def test_selection_probability(selection, expected):
    assert selection_probability(FAIR, selection) == pytest.approx(expected)
