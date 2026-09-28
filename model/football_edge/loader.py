"""Load the football-data.co.uk CSVs from data/raw/ into a SQLite database.

Two tables:
- matches: one row per match (teams, score, basic stats).
- odds:    one row per price, in long format:
           (match_id, bookmaker, market, is_closing, outcome, price).
           The set of bookmakers changes between seasons (Pinnacle disappears in 2026,
           Betfair Exchange appears), so new bookmakers only add rows, never columns.

Markets loaded: 1X2 (outcomes H/D/A) and over/under 2.5 goals (outcomes over/under).
Asian handicap is skipped for now: it also needs the handicap line.

Usage (from model/):
    .venv\\Scripts\\python -m football_edge.loader
"""

import re
import sqlite3
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = REPO_ROOT / "data" / "raw"
DB_PATH = REPO_ROOT / "data" / "football.db"

# Bookmaker prefixes used in the 1X2 columns, e.g. B365H, PSCD, AvgCA.
# Bb* are Betbrain aggregates (max / average) in older seasons.
BOOKMAKERS_1X2 = (
    "1XB", "B365", "BF", "BFD", "BFE", "BMGM", "BV", "BW", "CL", "IW",
    "LB", "PP", "PS", "SKB", "VC", "WH", "Max", "Avg", "BbMx", "BbAv",
)
# Prefixes used in the over/under 2.5 columns, e.g. B365>2.5, PC<2.5.
BOOKMAKERS_OU = ("Avg", "B365", "BFE", "BbAv", "BbMx", "Max", "P")

# Pinnacle is "PS" in 1X2 columns but "P" in over/under columns; store one name.
BOOKMAKER_ALIASES = {"P": "PS"}

# The regex tries the longer prefixes first where they overlap (BFD before BF), and backtracks
# when needed: "BFD" alone is Betfair (BF) + draw (D), "BFDH" is Betfred (BFD) + home (H).
_1X2 = re.compile(r"^(" + "|".join(sorted(BOOKMAKERS_1X2, key=len, reverse=True)) + r")(C?)([HDA])$")
_OU = re.compile(r"^(" + "|".join(sorted(BOOKMAKERS_OU, key=len, reverse=True)) + r")(C?)([<>])2\.5$")

SCHEMA = """
CREATE TABLE IF NOT EXISTS matches (
    id          INTEGER PRIMARY KEY,
    league      TEXT    NOT NULL,  -- football-data code: E0, SP1, I1, N1, P1, F1
    season      TEXT    NOT NULL,  -- '1617' = 2016/17
    date        TEXT    NOT NULL,  -- ISO yyyy-mm-dd
    kickoff     TEXT,              -- HH:MM, UK time; missing before 2019/20
    home_team   TEXT    NOT NULL,
    away_team   TEXT    NOT NULL,
    home_goals  INTEGER,           -- NULL for matches not played yet
    away_goals  INTEGER,
    ht_home_goals INTEGER,
    ht_away_goals INTEGER,
    home_shots  INTEGER,
    away_shots  INTEGER,
    home_shots_on_target INTEGER,
    away_shots_on_target INTEGER,
    home_corners INTEGER,
    away_corners INTEGER,
    home_xg     REAL,              -- only from 2026/27
    away_xg     REAL,
    UNIQUE (league, date, home_team, away_team)
);

CREATE TABLE IF NOT EXISTS odds (
    match_id    INTEGER NOT NULL REFERENCES matches(id),
    bookmaker   TEXT    NOT NULL,  -- PS = Pinnacle, B365 = Bet365, Avg/Max = market average/max, ...
    market      TEXT    NOT NULL,  -- '1x2' or 'ou2.5'
    is_closing  INTEGER NOT NULL,  -- 1 = closing odds, 0 = odds when the CSV was compiled
    outcome     TEXT    NOT NULL,  -- H/D/A for 1x2; over/under for ou2.5
    price       REAL    NOT NULL,  -- decimal odds
    PRIMARY KEY (match_id, bookmaker, market, is_closing, outcome)
);
"""

MATCH_COLUMNS = {
    "HomeTeam": "home_team", "AwayTeam": "away_team",
    "FTHG": "home_goals", "FTAG": "away_goals",
    "HTHG": "ht_home_goals", "HTAG": "ht_away_goals",
    "HS": "home_shots", "AS": "away_shots",
    "HST": "home_shots_on_target", "AST": "away_shots_on_target",
    "HC": "home_corners", "AC": "away_corners",
    "HxG": "home_xg", "AxG": "away_xg",
}


def parse_odds_column(name: str) -> tuple[str, str, bool, str] | None:
    """Map a CSV column name to (bookmaker, market, is_closing, outcome), or None if it is not odds.

    'PSCH'     -> ('PS', '1x2', True, 'H')
    'B365D'    -> ('B365', '1x2', False, 'D')
    'PC>2.5'   -> ('PS', 'ou2.5', True, 'over')
    'HC'       -> None   (home corners, not odds)
    """
    if m := _1X2.match(name):
        bookmaker, closing, outcome = m.groups()
        return BOOKMAKER_ALIASES.get(bookmaker, bookmaker), "1x2", closing == "C", outcome
    if m := _OU.match(name):
        bookmaker, closing, sign = m.groups()
        outcome = "over" if sign == ">" else "under"
        return BOOKMAKER_ALIASES.get(bookmaker, bookmaker), "ou2.5", closing == "C", outcome
    return None


def parse_dates(values: pd.Series) -> pd.Series:
    """football-data dates are dd/mm/yy in older seasons and dd/mm/yyyy in newer ones."""
    long_format = pd.to_datetime(values, format="%d/%m/%Y", errors="coerce")
    short_format = pd.to_datetime(values, format="%d/%m/%y", errors="coerce")
    return long_format.fillna(short_format).dt.strftime("%Y-%m-%d")


def read_csv(path: Path) -> pd.DataFrame:
    """Newer files are UTF-8 with a BOM, older ones plain ASCII/Latin-1."""
    try:
        df = pd.read_csv(path, encoding="utf-8-sig")
    except UnicodeDecodeError:
        df = pd.read_csv(path, encoding="latin-1")
    return df.dropna(subset=["HomeTeam", "AwayTeam"])  # some files end with empty rows


def load_file(conn: sqlite3.Connection, path: Path) -> tuple[int, int]:
    """Load one season/league CSV. Returns (matches, odds rows) written."""
    season, league = path.parent.name, path.stem
    df = read_csv(path)

    matches = pd.DataFrame({"league": league, "season": season, "date": parse_dates(df["Date"])})
    matches["kickoff"] = df["Time"] if "Time" in df.columns else None
    for source, target in MATCH_COLUMNS.items():
        matches[target] = df[source] if source in df.columns else None
    if matches["date"].isna().any():
        raise ValueError(f"{path}: unparseable dates")

    odds_columns = {col: parsed for col in df.columns if (parsed := parse_odds_column(col))}
    prices = df[list(odds_columns)].apply(pd.to_numeric, errors="coerce")
    corrupt = int((df[list(odds_columns)].notna() & prices.isna()).sum().sum())
    if corrupt:
        print(f"warning: {path.parent.name}/{path.name}: {corrupt} non-numeric odds values skipped")

    n_odds = 0
    for i, row in matches.iterrows():
        values = [None if pd.isna(v) else v for v in row.tolist()]
        cursor = conn.execute(
            f"INSERT INTO matches ({', '.join(matches.columns)}) "
            f"VALUES ({', '.join('?' * len(values))})",
            values,
        )
        match_id = cursor.lastrowid
        odds_rows = [
            (match_id, bookmaker, market, int(is_closing), outcome, float(prices.at[i, col]))
            for col, (bookmaker, market, is_closing, outcome) in odds_columns.items()
            if prices.at[i, col] > 1.0  # NaN compares False, so missing values are skipped
        ]
        conn.executemany("INSERT INTO odds VALUES (?, ?, ?, ?, ?, ?)", odds_rows)
        n_odds += len(odds_rows)
    return len(matches), n_odds


def load_all(raw_dir: Path = RAW_DIR, db_path: Path = DB_PATH) -> None:
    """Rebuild the database from scratch; the CSVs are the source of truth."""
    conn = sqlite3.connect(db_path)
    conn.executescript("DROP TABLE IF EXISTS odds; DROP TABLE IF EXISTS matches;" + SCHEMA)
    total_matches = total_odds = 0
    for path in sorted(raw_dir.glob("*/*.csv")):
        n_matches, n_odds = load_file(conn, path)
        total_matches += n_matches
        total_odds += n_odds
        print(f"{path.parent.name}/{path.name}: {n_matches} matches, {n_odds} odds")
    conn.commit()
    conn.close()
    print(f"\n{total_matches} matches, {total_odds} odds rows -> {db_path}")


if __name__ == "__main__":
    load_all()
