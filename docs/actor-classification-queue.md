# Actor Classification Queue

Use this queue when a transcript, candidate, or report introduces an actor/entity
whose role matters but is not yet classified in `docs/actor-aliases.md`.

## Queue Rules

- Preserve the source wording for the observed name.
- Add enough source context for the user to decide the role later.
- Do not normalize the name in authored analysis until classification is
  resolved.
- Use `unknown / needs-classification` in interim notes.
- After the user resolves the item, move it to `docs/actor-aliases.md` and add a
  short note under resolved decisions below.

## Current Queue

| Observed name | Source context | Proposed classification | Why it matters | Status | User decision |
|---|---|---|---|---|---|
| _none_ |  |  |  |  |  |

## Resolved Decisions

| Date | Canonical name | Classification | Decision |
|---|---|---|---|
| 2026-06-02 | Snark Server | coordination hub | User clarified that the Snark Server is a major hub where coordinators coordinate. |
