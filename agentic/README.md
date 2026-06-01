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
