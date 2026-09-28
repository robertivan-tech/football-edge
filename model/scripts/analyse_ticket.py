"""Compare the legs of an accumulator ticket with the de-vigged closing market.

For every leg that can be derived from the 1X2 market (1X2 and double chance), the script
looks up the closing odds in the database, removes the margin, and compares the fair
probability with the probability implied by the price on the ticket.

Other markets (bet builders, goal totals other than 2.5, corners, player props) have no
two-sided market in the data, so they are reported as not covered.

Usage (from model/):
    .venv\\Scripts\\python scripts\\analyse_ticket.py
    .venv\\Scripts\\python scripts\\analyse_ticket.py --ticket ..\\data\\tickets\\other.csv --reference Avg
"""

import argparse
import math
import sqlite3
from pathlib import Path

import pandas as pd

from football_edge.devig import devig_proportional
from football_edge.loader import DB_PATH, REPO_ROOT

DEFAULT_TICKET = REPO_ROOT / "data" / "tickets" / "accumulator_2026-09-19.csv"

# Team names as printed by the bookmaker -> names used by football-data.co.uk.
TEAM_ALIASES = {
    "Athletic Bilbao": "Ath Bilbao",
    "AS Roma": "Roma",
    "Sporting CP": "Sp Lisbon",
    "Manchester City": "Man City",
    "Atletico Madrid": "Ath Madrid",
    "AC Milan": "Milan",
    "PSG": "Paris SG",
    "Hull City": "Hull",
}

# Which 1X2 outcomes make up each selection.
SELECTION_OUTCOMES = {
    "1": ("H",), "X": ("D",), "2": ("A",),
    "1X": ("H", "D"), "X2": ("D", "A"), "12": ("H", "A"),
}
COVERED_MARKETS = {"1x2", "double_chance"}


def selection_probability(fair: dict[str, float], selection: str) -> float:
    """Fair probability of a 1X2 or double-chance selection from de-vigged H/D/A probabilities."""
    return sum(fair[outcome] for outcome in SELECTION_OUTCOMES[selection])


def fair_1x2(conn: sqlite3.Connection, date: str, home: str, away: str, reference: str) -> dict[str, float] | None:
    """De-vigged closing H/D/A probabilities for one match, or None if the odds are missing."""
    rows = conn.execute(
        """SELECT o.outcome, o.price FROM odds o JOIN matches m ON m.id = o.match_id
           WHERE m.date = ? AND m.home_team = ? AND m.away_team = ?
             AND o.market = '1x2' AND o.is_closing = 1 AND o.bookmaker = ?""",
        (date, home, away, reference),
    ).fetchall()
    prices = dict(rows)
    if set(prices) != {"H", "D", "A"}:
        return None
    return dict(zip("HDA", devig_proportional([prices["H"], prices["D"], prices["A"]])))


def analyse(ticket: pd.DataFrame, conn: sqlite3.Connection, reference: str) -> pd.DataFrame:
    rows = []
    for leg in ticket.itertuples():
        home = TEAM_ALIASES.get(leg.home, leg.home)
        away = TEAM_ALIASES.get(leg.away, leg.away)
        fair = None
        if leg.market in COVERED_MARKETS:
            fair = fair_1x2(conn, leg.date, home, away, reference)
        p_fair = selection_probability(fair, leg.selection) if fair else math.nan
        rows.append({
            "match": f"{leg.home} - {leg.away}",
            "selection": leg.selection if leg.market in COVERED_MARKETS else leg.market,
            "odds": leg.odds,
            "p_ticket": 1 / leg.odds,
            "p_fair": p_fair,
            "fair_odds": 1 / p_fair,
            "ev_per_unit": p_fair * leg.odds - 1,
            "result": leg.result,
        })
    return pd.DataFrame(rows)


def print_report(legs: pd.DataFrame, reference: str) -> None:
    table = legs.copy()
    for col in ("p_ticket", "p_fair", "ev_per_unit"):
        table[col] = table[col].map(lambda x: "-" if pd.isna(x) else f"{x:+.2%}" if col == "ev_per_unit" else f"{x:.2%}")
    table["fair_odds"] = table["fair_odds"].map(lambda x: "-" if pd.isna(x) else f"{x:.3f}")
    print(f"Reference: {reference} closing odds, margin removed proportionally\n")
    print(table.to_string(index=False))

    covered = legs.dropna(subset=["p_fair"])
    ticket_odds = math.prod(covered["odds"])
    p_fair = math.prod(covered["p_fair"])
    print(f"\nCovered legs: {len(covered)} of {len(legs)}")
    print(f"  combined odds on the ticket:        {ticket_odds:.2f}")
    print(f"  probability implied by those odds:  {1 / ticket_odds:.2%}")
    print(f"  fair probability (product):         {p_fair:.2%}")
    print(f"  fair combined odds:                 {1 / p_fair:.2f}")
    print(f"  expected value per unit staked:     {p_fair * ticket_odds - 1:+.2%}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--ticket", type=Path, default=DEFAULT_TICKET)
    parser.add_argument("--reference", default="BFE", help="bookmaker code used as the fair market (default: BFE)")
    args = parser.parse_args()

    ticket = pd.read_csv(args.ticket)
    with sqlite3.connect(DB_PATH) as conn:
        legs = analyse(ticket, conn, args.reference)
    print_report(legs, args.reference)


if __name__ == "__main__":
    main()
