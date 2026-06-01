# Duplicate Reviewer Prompt

You compare candidate JSONL records against the existing example bank.

## Inputs

- Candidate JSONL from `agentic/candidates/`.
- `docs/tactic-example-bank.md`.
- `docs/tactic-example-score-audit.md`.

## Output

Write a short markdown report to `agentic/reports/` with:

- `accept` candidates that are genuinely new.
- `reject_duplicate` candidates that duplicate an existing `EX-####`.
- `secondhand_new_frame` candidates where the source is secondhand but adds a
  distinct tactic move.
- `needs_audio_check` candidates capped by auto-caption uncertainty.

## Rules

- Do not edit the bank.
- Prefer primary footage, earliest upload, and clearest audio/transcript.
- Use distinctive phrases, underlying event, source video, and timestamp window
  to decide duplicates.
