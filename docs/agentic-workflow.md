# Agentic Review Workflow

This project uses agents for semantic discovery and scripts for mechanical
validation. Agents find and assess examples; scripts catch schema, ID, coverage,
and clip-quality mistakes.

## Roles

| Role | Writes files? | Output |
|---|---:|---|
| Scout | No | Candidate JSONL |
| Duplicate reviewer | Report only | Duplicate/accept report |
| Score auditor | Report only | Score recommendations |
| Clipper | Clips/reports only | MP4 clips and clip report |
| Merge editor | Yes | Bank, audit, project context |

Only the merge editor should change `docs/tactic-example-bank.md` or
`docs/tactic-example-score-audit.md`.

## Candidate JSONL Schema

Each line in `agentic/candidates/*.jsonl` is one candidate object:

```json
{
  "candidate_id": "cand-ryle-20260516-0001",
  "agent": "scout-a",
  "source_file": "transcripts/ryle-kittenhouse/processed/20260516-JdUb8fYGKpc.txt",
  "channel": "Ryle Kittenhouse",
  "title": "Example video title",
  "platform": "YouTube",
  "date": "2026-05-16",
  "video_id": "JdUb8fYGKpc",
  "timestamp": "00:12:34",
  "clip_url": "https://youtu.be/JdUb8fYGKpc?t=754",
  "tactic": "Always on Offense",
  "score": 4,
  "score_call": "Direct redirect, capped until audio verification.",
  "quote": "Exact words from the transcript packet.",
  "what_happened": "One to three sentences describing the exchange.",
  "why_it_fits": "One to two sentences tying the exchange to the tactic.",
  "actors": [
    {
      "name": "Snark Server",
      "classification": "coordination hub",
      "role_in_candidate": "Hub where the discussed coordination allegedly happened."
    }
  ],
  "actor_classification_requests": [],
  "duplicate_check": {
    "status": "new",
    "related_examples": [],
    "reason": "No same-source or same-event match found in bank."
  },
  "notes": "auto-caption approximate; needs audio verification"
}
```

Allowed `duplicate_check.status` values:

- `new`
- `possible_duplicate`
- `duplicate`
- `secondhand_new_frame`

`actors` and `actor_classification_requests` are optional for validator
purposes, but required by workflow whenever actor/entity roles affect the
analysis. Use classifications from `docs/actor-aliases.md`. If a meaningful
actor/entity is missing or ambiguous, add an `actor_classification_requests`
entry instead of guessing:

```json
{
  "observed_name": "Example Name",
  "source_context": "Where and how the name appeared.",
  "proposed_classification": "unknown / needs-classification",
  "why_it_matters": "Why the role affects the analysis."
}
```

## Commands

Generate packets from processed transcripts:

```powershell
python scripts\agentic\make_packets.py --glob "transcripts\ryle-kittenhouse\processed\*.txt"
```

Validate candidate JSONL:

```powershell
python scripts\agentic\validate_candidates.py agentic\candidates\*.jsonl
```

Validate the bank and score audit after merge:

```powershell
python scripts\agentic\validate_bank.py
```

Validate local clip quality:

```powershell
python scripts\agentic\validate_clips.py --min-height 1080
```

If `ffprobe` is not on PATH, pass it explicitly:

```powershell
python scripts\agentic\validate_clips.py --ffprobe "C:\path\to\ffprobe.exe" --min-height 1080
```

## Merge Gate

Before commit, the merge editor should run:

```powershell
python scripts\agentic\validate_candidates.py agentic\candidates\*.jsonl
python scripts\agentic\validate_bank.py
python scripts\agentic\validate_clips.py --min-height 1080
git diff --check -- CLAUDE.md docs\tactic-example-bank.md docs\tactic-example-score-audit.md
```

## Operating Rules

- Agents produce candidates; they do not directly add examples to the bank.
- Duplicate checks happen before scoring decisions are merged.
- Review streams are secondhand by default.
- Score-3+ examples are preserved for possible future use.
- The bank is uncapped. Prioritize higher scores, source diversity,
  non-duplicate events, and examples that add a distinct tactic angle.
- Use `docs/actor-aliases.md` canonical names in authored prose. Preserve source
  wording inside direct quotes, transcript excerpts, titles, filenames, and URLs.
- Treat `Snark Server` as a coordination hub, not a person. Do not attribute
  hub-level activity to a specific coordinator unless the source identifies that
  person or an accepted example documents the relationship.
- If an unregistered actor/entity comes up and the classification matters, ask
  the user. If a batch run cannot stop cleanly, add it to
  `docs/actor-classification-queue.md` and keep the role as
  `unknown / needs-classification`.
- Clip quality is mechanical: best split video/audio, `ffmpeg` merge, `ffprobe`
  verification.
