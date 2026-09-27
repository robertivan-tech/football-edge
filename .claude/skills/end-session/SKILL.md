---
name: end-session
description: End a work session on football-edge — update docs/progres.md with a state summary, log AI-workflow lessons, commit and push. Use when Robert says the session is over, or invokes /end-session.
---

# End a session

1. Run the tests that exist (for example `pytest` in `model/`). Report failures honestly; do not
   hide them in the summary.
2. Update `docs/progres.md`: rewrite the **Current state** section with the six headings below,
   and add one line to the **Log** (date, PC if known, what was done). Keep it under ~400 words.
   1. Goal and scope
   2. Decisions made (with the reason for each)
   3. Work in progress
   4. Next steps (concrete, for the next session)
   5. Open questions
   6. Conventions that still apply
3. If something was learned about working with AI today (a correction, a useful technique, a
   mistake Claude made), add an entry to `docs/ai-workflow.md` using its format. Ask Robert what the
   lesson was, and do not just write your own.
4. Show Robert the `git status` and a proposed commit message. Commit and push after Robert confirms.
5. Remind Robert: on the other PC, start with `git pull` (or `/start-session`).
