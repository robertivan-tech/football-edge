# Progress

The current state of the project. Updated at the end of every session, so a new session on any PC
can continue from here. Newest state at the top; older entries move to the log below.

---

## Current state — 2026-09-27

**1. Goal and scope**
Build a system that estimates football match probabilities and measures whether it beats the
market. Portfolio project for a backend / AI engineer part-time job. See `CLAUDE.md`.

**2. Decisions made**
- Hybrid stack: Python for data, models and AI; Java 21 + Quarkus for the backend.
  *Why:* covers both target roles, and each language is used where it is strongest.
- Quarkus instead of Spring Boot for the backend (changed 2026-09-28).
  *Why:* Robert has used Quarkus before and finds it more interesting to work with than Spring.
- Maths first, backend later. *Why:* if the model does not beat the market, nothing else matters.
- The LLM extracts features and does not decide bets. *Why:* LLM output is not a calibrated probability.
- Public repo on GitHub (`robertivan-tech/football-edge`); `CLAUDE.md` plus this file carry the
  context between PCs and sessions.

**3. Work in progress**
- Repo created with `CLAUDE.md`, `README.md`, `docs/`, `.gitignore`, and the session skills.
- No code yet.

**4. Next steps (session 1, phase 1)**
1. Create the Python virtual environment in `model/` (`py -m venv .venv`) and install pandas.
2. Download football-data.co.uk CSVs: Premier League, LaLiga, Serie A, Eredivisie, Primeira Liga,
   Ligue 1, for the last ~10 seasons.
3. Loader script: CSV → SQLite (tables `matches` and `odds`).
4. **Concept:** implied probability, the overround, and de-vigging.
   Robert writes `devig()`; Claude writes the tests first.
5. Apply it to the 72.09 accumulator: the real margin per leg and the "fair" ticket probability.

**5. Open questions**
- Which bookmaker's odds to use as the baseline? Pinnacle closing odds (`PSCH/PSCD/PSCA`) are the
  usual reference for a "sharp" market. Check what the CSVs contain.
- License for the repo (MIT?) — decide before making it presentable.

**6. Conventions that still apply**
Talk in Romanian; code and docs in English. Robert writes the core logic; tests come first.
Numbers are computed with code.

---

## Log

- **2026-09-27** — Planning session on PC1: analysed the 72.09 accumulator, chose the project,
  architecture and roadmap; renamed the GitHub account to `robertivan-tech`; set the git identity
  with the noreply email; created the repo.
