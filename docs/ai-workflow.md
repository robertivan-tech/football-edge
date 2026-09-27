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
