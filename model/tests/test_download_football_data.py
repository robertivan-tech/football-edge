"""Tests for the pure helpers of the downloader. No network access."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from download_football_data import csv_url, local_path, season_code  # noqa: E402


def test_season_code():
    assert season_code(2016) == "1617"
    assert season_code(2025) == "2526"


def test_season_code_across_the_century():
    assert season_code(1999) == "9900"
    assert season_code(2009) == "0910"


def test_csv_url():
    assert csv_url(2025, "E0") == "https://football-data.co.uk/mmz4281/2526/E0.csv"


def test_local_path_is_under_data_raw():
    path = local_path(2016, "SP1")
    assert path.parts[-4:] == ("data", "raw", "1617", "SP1.csv")
