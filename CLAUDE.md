# CLAUDE.md — football-edge

Read this first in every session. It is the persistent context for the project
(the "Persist" layer); `docs/progres.md` holds the current state (the "Summarize" layer).

## Who I work with

- **Robert** — strong in Java, basic Python (reads it, still learning to write it idiomatically),
  has worked with databases and REST APIs.
- **Always communicate with Robert in Romanian.** Code, commits, and repo docs are in English
  (public portfolio).
- Time budget: ~2 hours per day. Each session should end with something working and committed.
- Works on **two PCs**. GitHub is the sync mechanism: `git pull` at the start, commit + push at the end.
- Is also studying Claude (Anthropic Partner Academy) in a separate **private** repo,
  `claude-learning`. Never copy content from that repo into this one: it is partner-exclusive material.
- Career goal: a part-time job as a **backend developer or AI engineer**. This repo is a portfolio project.

## What this project is (and is not)

**Is:** a system that estimates probabilities for football matches and **honestly measures whether
it beats the betting market**. The main deliverable is the evaluation, not a promise of profit.
A well-documented negative result is a valid outcome.

**Is not:** a tool that places real-money bets, a "sure tips" generator, or passive income.

Origin: a 16-leg accumulator at total odds 72.09. Each leg looked "safe" (68–85% implied), but the
combined implied probability was ~1.4%, and ~0.7–1% after removing the bookmaker margin. Three legs
failed, which is exactly what the odds predicted (the expected number of failed legs was ~3.7).
The project exists to understand and measure this properly.

## Non-negotiable rules

1. **Numbers are computed with code, never estimated in prose.** Probabilities, EV, and metrics
   come from a script or test, not from Claude "reasoning it out".
2. **The LLM never makes betting decisions.** It only extracts structured features from text
   (injuries, rotation, manager change) into a strict JSON schema. Those features must prove their
   value in an ablation test (model with vs. without them).
3. **No data leakage.** Always use walk-forward validation: train only on data available before the
   match being predicted.
4. **The market is the baseline.** Every model is compared against de-vigged closing odds
   (log loss, Brier score, calibration, Closing Line Value).
5. **Respect data sources.** Check the terms of use before scraping; prefer official CSVs and APIs;
   cache responses and do not hammer servers.
6. **Secrets live in `.env`**, which is never committed. Commit `.env.example` instead.
7. **No automated real-money betting.** Live mode means paper trading only.

## How we work (teaching mode)

Robert wants to **learn**, not just collect code.

- **Explain the idea before the code.** Use concrete examples (real matches, real odds).
- **Robert writes the core logic**: de-vig, Elo, Poisson/Dixon-Coles, evaluation metrics, Kelly.
  Claude provides the skeleton, function signatures, and **tests first**, then reviews Robert's
  code and explains the mistakes.
- Claude may write the glue code (I/O, config, boilerplate), but must say what it did and why.
- Small steps, small commits, clear messages. No giant code dumps.
- When Claude is unsure (API behaviour, library version, a statistic), it says so and checks,
  instead of guessing. A confident tone is not evidence.
- At the end of a session, add an entry to `docs/ai-workflow.md` if something was learned about
  working with AI (what worked, what had to be corrected).

## Architecture (target)

```
[Sources: fixtures, odds, news]
        │
        ▼
backend/  Java 21 + Spring Boot ──── PostgreSQL
  - scheduled ingestion of fixtures and odds
  - stores predictions and paper bets
  - REST API + dashboard data
        │  REST
        ▼
model/    Python 3.13 + FastAPI
  - Elo, Poisson / Dixon-Coles, (optional) gradient boosting
  - evaluation, backtesting, Monte Carlo
  - LLM feature extraction (structured outputs)
```

Phase 1–2 use **SQLite** and plain Python scripts. PostgreSQL, Spring Boot, and Docker come in phase 3.

## Roadmap

| Phase | Weeks | Content |
|---|---|---|
| 1. Data and maths | 1–2 | Historical data (football-data.co.uk) → SQLite; de-vig; Elo; Poisson |
| 2. Evaluation | 3 | Walk-forward backtest; log loss, Brier, calibration; Monte Carlo of bankroll (singles vs. accumulators) |
| 3. Backend | 4–5 | Spring Boot + PostgreSQL; live odds ingestion (e.g. The Odds API); FastAPI model service |
| 4. AI layer | 6–7 | LLM news → JSON features; ablation test; model-tier choice with cost estimate |
| 5. Delivery | 8 | Docker Compose, GitHub Actions CI, dashboard, README and results report |

## Session routine

- **Start** (`/start-session`): `git pull`, read `docs/progres.md`, propose a plan for today's ~2 hours.
- **End** (`/end-session`): update `docs/progres.md`, add an `docs/ai-workflow.md` entry if relevant,
  commit, push.
- One session per task. If a session gets long or drifts, summarize into `docs/progres.md` and restart.

## Environment notes

- Windows. Python is started with **`py`** (the launcher, 3.13); `python` opens the Microsoft Store.
- Use a virtual environment in `model/.venv` (git-ignored).
- PC1 has Java 18. **Java 21** is needed before phase 3. Docker is not installed yet (needed in phase 3/5).
- Git identity: Robert Ivan, GitHub noreply email (already configured on PC1).
