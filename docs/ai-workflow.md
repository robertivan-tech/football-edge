# Working with AI — journal

How this project was built together with Claude (Claude Code): what worked, what had to be
corrected, and which techniques proved useful. One short entry per lesson, newest first.

Entry format:

```
## YYYY-MM-DD — short title
**Situation:** what I was trying to do
**What happened:** what Claude did / suggested
**Correction / decision:** what I changed or decided, and why
**Lesson:** what I will do differently next time
```

---

## 2026-09-28 — Edge cases become tests

**Situation:** I implemented `devig()` against tests written first, and all of them passed.

**What happened:** In review, Claude checked one case the tests did not cover: `NaN` odds.
`nan <= 1` is `False`, so the value passed validation and the function returned `[nan, nan]`
without an error. My first fix (`odd != NaN`) did not work either, because `NaN` is not equal to
anything, not even to itself.

**Correction / decision:** The check became `not odd > 1`, which also rejects `NaN`. A `NaN` case
was added to the parametrized validation test.

**Lesson:** Green tests only prove what they test. When a review finds an edge case, it goes into
the test suite, so the bug cannot quietly come back.

## 2026-09-28 — Write for the external reader from the start

**Situation:** The repo is a public portfolio, but the first drafts carried notes from the working
process: "Written by Robert" in a docstring, "the implementation is left for Robert" in a commit
message.

**What happened:** These notes make sense during the session and look unprofessional to anyone
reading the repo later. Removing them afterwards meant editing files and rewriting local commit
messages before the push.

**Correction / decision:** Code, tests, docstrings and commit messages describe what the code does,
not who wrote which part. The workflow is explained once, in the README.

**Lesson:** Every text that lands in git has an external reader. Write it for them the first time.

## 2026-09-27 — Context has to live in the repo, not in the chat

**Situation:** I work on two PCs, and the planning conversation happened on only one of them.

**What happened:** A Claude Code session does not move between machines, so the decisions from
that conversation would have been lost.

**Correction / decision:** The context lives in files. `CLAUDE.md` (loaded automatically in every
session) holds the rules, architecture and roadmap. `docs/progres.md` holds the current state, and
it is updated at the end of every session with a fixed "state summary" template. Two project skills,
`/start-session` and `/end-session`, turn the routine into a procedure.

**Lesson:** Applies Restart / Summarize / Persist from the Claude course (M1 §5.2): persist what
every session needs, summarize at milestones, restart instead of stretching one long session.

## 2026-09-27 — The LLM is a tool, not the decision-maker

**Situation:** My first idea was for an LLM to look at player data and decide which bets to place.

**What happened:** Claude pointed out that an LLM's answer sounds just as confident when it is
wrong (confident tone ≠ accuracy), and that it does not produce calibrated probabilities.

**Correction / decision:** A statistical model makes the decisions. The LLM only extracts structured
facts from news, and it has to prove in an ablation test that those facts improve the predictions.

**Lesson:** Use the LLM where its output can be checked and measured.
