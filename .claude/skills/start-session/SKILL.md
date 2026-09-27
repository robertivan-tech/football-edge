---
name: start-session
description: Start a work session on football-edge — sync with GitHub, read the current state, and propose a plan for today's ~2 hours. Use when Robert says a work session is starting, or invokes /start-session.
---

# Start a session

1. Run `git pull`. If there are local uncommitted changes or conflicts, stop and tell Robert
   before doing anything else.
2. Read `docs/progres.md`, the "Current state" section, especially **Next steps** and **Open questions**.
3. Check `git log --oneline -5` to see what was done last.
4. Tell Robert, in Romanian and briefly:
   - where we left off (2–3 sentences);
   - the plan for today: 2–4 concrete steps that fit in ~2 hours and end with something committed;
   - today's concept, and which part **Robert** will write;
   - any open question that Robert must decide first.
5. Wait for Robert's confirmation before writing code.
