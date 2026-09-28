# Progress

The current state of the project. Updated at the end of every session, so a new session on any PC
can continue from here. Newest state at the top; older entries move to the log below.

---

## Current state — 2026-09-28

**1. Goal and scope**
Build a system that estimates football match probabilities and measures whether it beats the
market. Portfolio project for a backend / AI engineer part-time job. See `CLAUDE.md`.
Success is defined in four levels in `README.md`; a measured negative result is valid.

**2. Decisions made**
- Data: football-data.co.uk, 6 leagues, 2016/17–2026/27. Files stay out of git.
  *Why:* its terms allow private, non-commercial use only; the downloader recreates them.
- Claude never fetches from football-data.co.uk. *Why:* its `robots.txt` blocks Claude/Anthropic
  agents. Robert runs the downloader himself.
- Odds stored in long format `(match, bookmaker, market, is_closing, outcome, price)`.
  *Why:* the bookmaker set changes by season; new bookmakers add rows, not columns.
- Hybrid stack: Python for data, models and AI; Java 21 + Quarkus for the backend.
  *Why:* covers both target roles, and each language is used where it is strongest.
- Quarkus instead of Spring Boot (2026-09-28). *Why:* Robert knows it and prefers it.
- Maths first, backend later. *Why:* if the model does not beat the market, nothing else matters.
- The LLM extracts features and does not decide bets. *Why:* LLM output is not a calibrated probability.
- Public repo `robertivan-tech/football-edge`; `CLAUDE.md` and this file carry context between PCs.

**3. Work in progress**
Done, 66 tests passing:
- `model/` package (`pip install -e .`), downloader, CSV → SQLite loader
  (21,030 matches, 1.18M odds rows in `data/football.db`).
- `football_edge/devig.py`: implied probabilities, overround, proportional de-vig (Robert).
- `scripts/analyse_ticket.py`: 9 of the 16 ticket legs (1X2, double chance) vs Betfair Exchange
  closing: combined odds 9.75, fair probability 8.56%, EV −16.5%. Other markets not covered.

Data: Pinnacle closing odds stop after 2026-01-08; 2026/27 has Betfair Exchange (`BFE`) and xG.
Eredivisie 2019/20 (`1920/N1.csv`) failed to download.

**4. Next steps**
1. Re-run the downloader for `1920/N1.csv` and read the error.
2. Second de-vig method (power or Shin); test on history whether proportional under-rates
   favourites (favourite–longshot bias, seen on Ajax–Excelsior).
3. Elo ratings (Robert writes the update rule; tests first).

**5. Open questions**
- Market baseline after January 2026: Betfair Exchange (commission not in the odds) or `Avg`?
- Books → skills: Robert gets legal copies; skills are per topic, in our own words, with sources;
  book files git-ignored. Which books?
- License for the repo (MIT?).

**6. Conventions that still apply**
Talk in Romanian; code and docs in English. Robert writes the core logic; tests come first.
Numbers are computed with code. Code and tests are portfolio-grade: no notes about who writes what.

---

## Log

- **2026-09-28** — Switched backend to Quarkus. Built the data pipeline (download, SQLite), Robert
  implemented de-vig, analysed the 72.09 ticket against the closing market.

- **2026-09-27** — Planning session on PC1: analysed the 72.09 accumulator, chose the project,
  architecture and roadmap; renamed the GitHub account to `robertivan-tech`; set the git identity
  with the noreply email; created the repo.
