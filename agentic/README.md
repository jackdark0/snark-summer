# Agentic Workflow Scaffold

This directory is the staging area for parallel transcript review.

Agents should not edit `docs/tactic-example-bank.md` directly. They produce
candidate records first, then a merge/editor pass validates and applies the
best candidates.

## Directories

- `packets/` - generated transcript packets to hand to scout agents.
- `candidates/` - JSONL candidate records returned by scout agents.
- `reports/` - duplicate, score, clip, and merge-review notes.
- `roles/` - role prompts for the agents in the workflow.

## Basic Flow

1. Generate packets from processed transcripts.
2. Assign packets to scout agents.
3. Save scout outputs as JSONL in `candidates/`.
4. Run candidate validation.
5. Run duplicate/score review.
6. Merge only the approved examples into the bank and audit.
7. Run bank and clip validators before commit.

## Actor Classification

Use `docs/actor-aliases.md` for canonical names and classifications. If a new
or ambiguous actor/entity appears and its role matters, ask the user for
classification. During batch work, add unresolved items to
`docs/actor-classification-queue.md` and keep the role as
`unknown / needs-classification`.

`Snark Server` is classified as a coordination hub. Do not attribute hub-level
activity to a specific coordinator unless the source identifies that person or
an accepted example documents the relationship.
