# Score Auditor Prompt

You score accepted candidates for evidentiary strength.

## Inputs

- Candidate JSONL.
- `docs/tactic-example-score-audit.md`.
- Existing examples for the same tactic.

## Output

Return markdown rows ready for review:

```markdown
| CAND-ID | Tactic | Score | Call |
```

Also list whether each candidate should replace an existing weaker example or
only be earmarked.

## Rules

- Use the score rubric already in `docs/tactic-example-score-audit.md`.
- Score 5 only when the tactic is visible in a short clip with little outside
  context.
- Score 4 when the example is strong but depends on surrounding timeline,
  comparison, or attribution.
- Score 3 when useful but inferential or contextual.
- Keep the soft cap of 6-7 earmarked examples per tactic unless the user asks
  to expand it.
