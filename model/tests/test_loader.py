"""Tests for the CSV -> SQLite loader. Uses a tiny CSV written to a temp dir; no real data needed."""

import sqlite3

import pandas as pd
import pytest

from football_edge.loader import load_all, parse_dates, parse_odds_column


@pytest.mark.parametrize(
    "column, expected",
    [
        ("PSCH", ("PS", "1x2", True, "H")),
        ("B365D", ("B365", "1x2", False, "D")),
        ("AvgCA", ("Avg", "1x2", True, "A")),
        ("BFD", ("BF", "1x2", False, "D")),      # Betfair draw, not Betfred
        ("BFDH", ("BFD", "1x2", False, "H")),    # Betfred home
        ("BFECD", ("BFE", "1x2", True, "D")),    # Betfair Exchange closing draw
        ("1XBCH", ("1XB", "1x2", True, "H")),
        ("P>2.5", ("PS", "ou2.5", False, "over")),
        ("PC<2.5", ("PS", "ou2.5", True, "under")),
        ("BbAv>2.5", ("BbAv", "ou2.5", False, "over")),
    ],
)
def test_parse_odds_column(column, expected):
    assert parse_odds_column(column) == expected


@pytest.mark.parametrize(
    "column",
    ["HC", "AC", "HS", "HST", "FTR", "HTR", "HomeTeam", "Date", "B365AHH", "AvgCAHA", "BbAHh", "BbOU"],
)
def test_non_odds_columns_are_ignored(column):
    assert parse_odds_column(column) is None


def test_parse_dates_handles_both_year_formats():
    dates = pd.Series(["13/08/16", "09/08/2019"])
    assert parse_dates(dates).tolist() == ["2016-08-13", "2019-08-09"]


CSV = """﻿Div,Date,Time,HomeTeam,AwayTeam,FTHG,FTAG,HC,AC,PSCH,PSCD,PSCA,B365H,B365D,B365A,P>2.5,P<2.5
E0,21/08/2026,20:00,Arsenal,Coventry,3,0,10,2,1.25,6.50,12.00,1.22,6.00,13.00,1.60,2.40
E0,22/08/2026,15:00,Everton,Fulham,,,,,2.40,3.30,3.10,#,,,,
,,,,,,,,,,,,,,,,
"""


@pytest.fixture
def db(tmp_path):
    raw = tmp_path / "raw" / "2627"
    raw.mkdir(parents=True)
    (raw / "E0.csv").write_text(CSV, encoding="utf-8")
    db_path = tmp_path / "test.db"
    load_all(tmp_path / "raw", db_path)
    conn = sqlite3.connect(db_path)
    yield conn
    conn.close()


def test_matches_are_loaded_and_empty_rows_dropped(db):
    rows = db.execute(
        "SELECT league, season, date, kickoff, home_team, away_team, home_goals, away_goals, home_corners "
        "FROM matches ORDER BY date"
    ).fetchall()
    assert rows == [
        ("E0", "2627", "2026-08-21", "20:00", "Arsenal", "Coventry", 3, 0, 10),
        ("E0", "2627", "2026-08-22", "15:00", "Everton", "Fulham", None, None, None),
    ]


def test_odds_are_stored_in_long_format(db):
    rows = db.execute(
        "SELECT bookmaker, market, is_closing, outcome, price FROM odds o "
        "JOIN matches m ON m.id = o.match_id WHERE m.home_team = 'Arsenal' "
        "ORDER BY bookmaker, market, is_closing, outcome"
    ).fetchall()
    assert rows == [
        ("B365", "1x2", 0, "A", 13.0),
        ("B365", "1x2", 0, "D", 6.0),
        ("B365", "1x2", 0, "H", 1.22),
        ("PS", "1x2", 1, "A", 12.0),
        ("PS", "1x2", 1, "D", 6.5),
        ("PS", "1x2", 1, "H", 1.25),
        ("PS", "ou2.5", 0, "over", 1.6),
        ("PS", "ou2.5", 0, "under", 2.4),
    ]


def test_missing_and_corrupt_odds_are_skipped(db):
    count = db.execute(
        "SELECT COUNT(*) FROM odds o JOIN matches m ON m.id = o.match_id WHERE m.home_team = 'Everton'"
    ).fetchone()[0]
    assert count == 3  # only the Pinnacle closing 1X2 prices; B365H is '#'


def test_loading_twice_does_not_duplicate(tmp_path, db):
    load_all(tmp_path / "raw", tmp_path / "test.db")
    assert db.execute("SELECT COUNT(*) FROM matches").fetchone()[0] == 2
