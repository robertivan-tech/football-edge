# football-edge

> **Status: work in progress.** Phase 1: data and models.

Can a small, transparent model estimate football match probabilities better than the betting market?
This project builds one and measures the answer honestly.

## Why

A typical 16-leg accumulator at total odds of 72.09 is made of legs that each look "safe"
(68–85% implied probability). Together they have about a **1.4%** chance, and closer to **1%**
once the bookmaker's margin is removed. With 16 legs you should *expect* 3–4 to fail.
Intuition is bad at compounding probabilities. This project replaces intuition with models and
measurement.

## What it does (planned)

1. **Data:** historical results and odds for the major European leagues → SQLite / PostgreSQL.
2. **Market baseline:** bookmaker odds converted to fair probabilities (margin removed).
3. **Models:** Elo ratings, then a Poisson / Dixon-Coles goals model (1X2, over/under, BTTS).
4. **Evaluation:** walk-forward backtesting, log loss, Brier score, calibration curves, and Closing
   Line Value, all against the market baseline.
5. **Betting strategy simulation:** expected value, fractional Kelly staking, and Monte Carlo bankroll
   simulations comparing singles with accumulators.
6. **AI layer:** an LLM extracts structured features from pre-match news (injuries, rotation,
   manager changes) into a strict JSON schema. It never picks bets. Its value is measured with an
   ablation test.
7. **Paper trading:** a scheduled pipeline logs weekly predictions without real money and tracks the results.

## What counts as success

Beating the Pinnacle closing line on 1X2 in the top leagues, with public data and classic models, is
very unlikely: those odds already contain the information of professional syndicates with far more
data. So success is defined in levels, and each level is a result worth reporting:

1. **Calibrated:** when the model says 60%, the event happens about 60% of the time.
2. **Close to the market:** log loss within a small gap of de-vigged Pinnacle closing odds.
3. **Beats soft bookmakers:** better than soft bookmakers' opening odds, at least in some markets.
4. **Beats the closing line:** very unlikely; if it happens, the first suspect is data leakage.

A negative result, measured and explained, is a valid outcome.

## Architecture (target)

```
backend/  Java 21 + Quarkus + PostgreSQL       ingestion, storage, REST API
model/    Python + FastAPI                     models, evaluation, LLM features
```

## Roadmap

- [ ] Phase 1: data pipeline, de-vig, Elo, Poisson
- [ ] Phase 2: backtesting and evaluation report
- [ ] Phase 3: Quarkus backend and model service
- [ ] Phase 4: LLM feature extraction and ablation study
- [ ] Phase 5: Docker Compose, CI, dashboard, final report

## How it is built

The project is developed with Claude Code as a pair programmer, in a "teaching mode": the core
maths and models are written by hand, and the AI provides tests, reviews, and explanations.
The rules are in [`CLAUDE.md`](CLAUDE.md), and the lessons learned are in
[`docs/ai-workflow.md`](docs/ai-workflow.md).

## Data

Historical results and odds come from [football-data.co.uk](https://www.football-data.co.uk),
which provides them free for private, non-commercial use. The data files are not redistributed in
this repository; `model/scripts/download_football_data.py` downloads them for personal use.

## Disclaimer

This is an educational and research project. It does not provide betting advice, and it does not
place real-money bets. Gambling involves financial risk.
