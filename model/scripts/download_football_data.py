"""Download match results and odds CSVs from football-data.co.uk.

Terms of the source (checked 2026-09-28): the data is free for private individuals and for
league match prediction; it is NOT for commercial or data-training products. This script is
for personal research only. It downloads each file once, caches it under data/raw/, and waits
between requests so the server is not hammered.

Usage (from the repo root):
    model\\.venv\\Scripts\\python model\\scripts\\download_football_data.py
    model\\.venv\\Scripts\\python model\\scripts\\download_football_data.py --refresh-current
"""

import argparse
import time
import urllib.request
from pathlib import Path

BASE_URL = "https://football-data.co.uk/mmz4281"

# football-data.co.uk file codes for the top division of each country.
LEAGUES = {
    "E0": "Premier League",
    "SP1": "LaLiga",
    "I1": "Serie A",
    "N1": "Eredivisie",
    "P1": "Primeira Liga",
    "F1": "Ligue 1",
}

FIRST_SEASON = 2016    # 2016/17
CURRENT_SEASON = 2026  # 2026/27, still in progress: the file grows every week

DELAY_SECONDS = 3
USER_AGENT = "football-edge/0.1 (personal research; github.com/robertivan-tech/football-edge)"

REPO_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = REPO_ROOT / "data" / "raw"


def season_code(start_year: int) -> str:
    """2016 -> '1617' (the season 2016/17), as used in football-data.co.uk URLs."""
    return f"{start_year % 100:02d}{(start_year + 1) % 100:02d}"


def csv_url(start_year: int, league: str) -> str:
    return f"{BASE_URL}/{season_code(start_year)}/{league}.csv"


def local_path(start_year: int, league: str) -> Path:
    return RAW_DIR / season_code(start_year) / f"{league}.csv"


def download(url: str, target: Path) -> None:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=30) as response:
        content = response.read()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(content)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--refresh-current",
        action="store_true",
        help=f"re-download the in-progress season {season_code(CURRENT_SEASON)}",
    )
    args = parser.parse_args()

    downloaded = skipped = failed = 0
    for year in range(FIRST_SEASON, CURRENT_SEASON + 1):
        for league in LEAGUES:
            target = local_path(year, league)
            refresh = args.refresh_current and year == CURRENT_SEASON
            if target.exists() and not refresh:
                skipped += 1
                continue

            url = csv_url(year, league)
            try:
                download(url, target)
                downloaded += 1
                print(f"ok      {url}")
            except Exception as error:  # keep going; report at the end
                failed += 1
                print(f"FAILED  {url}  ({error})")
            time.sleep(DELAY_SECONDS)

    print(f"\ndownloaded {downloaded}, already cached {skipped}, failed {failed}")
    print(f"files are in {RAW_DIR}")


if __name__ == "__main__":
    main()
