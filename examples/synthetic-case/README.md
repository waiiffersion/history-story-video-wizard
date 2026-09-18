# Synthetic case: The Empty Granary

> This case is entirely fictional. The people, place, objects, and records do not represent real history.

The example demonstrates how the Skill separates an object observation, a later narrative, an inference, and an unsupported dramatic detail.

## Walkthrough

1. Read [BRIEF.md](BRIEF.md).
2. Inspect claim limits in [EVIDENCE.md](EVIDENCE.md).
3. See how those limits shape [STORY_PROMISE.md](STORY_PROMISE.md).
4. Create a working directory and advance only after the matching artifact exists:

```bash
python3 scripts/project_state.py init work/synthetic-case
cp examples/synthetic-case/EVIDENCE.md work/synthetic-case/EVIDENCE.md
python3 scripts/project_state.py advance work/synthetic-case EVIDENCE_READY --evidence work/synthetic-case/EVIDENCE.md
python3 scripts/project_state.py validate work/synthetic-case
```

The example stops before narration on purpose. It demonstrates method, not a hidden historical claim.
