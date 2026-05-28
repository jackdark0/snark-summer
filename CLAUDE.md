# Harassment Campaign Tracker — Project Context

This is a research and documentation project for analyzing coordinated harassment campaigns:
identifying tactics, cataloging examples, and building a counter-narrative reference.

---

## Project Purpose

Document, classify, and counter coordinated harassment tactics observed in online streaming
and political communities. The primary source material is transcripts from affected creators.
Output is a structured knowledge base usable for community education, debate prep, and
classifier training data.

---

## File Structure

```
counter-insurgency.md        # Public-facing community guide; clip URLs in example bank link here

docs/
  counter-tactics-guide.md   # Master taxonomy: 13 tactics with counter-moves
  tactic-example-bank.md     # Living example catalog keyed to taxonomy (EX-####)
  labels.md                  # GitHub Issues label definitions

data/
  approved.csv               # Canonical approved talking points database (auto-updated)

transcripts/
  raw/                       # Raw auto-caption transcripts (do not modify)
  processed/                 # Cleaned transcripts ready for analysis

.github/
  ISSUE_TEMPLATE/
    talking-point-submission.yml   # Community submission form
  workflows/
    submission-intake.yml          # Auto-label + triage checklist on new Issues
    export-approved.yml            # Rebuild approved.csv on Issue approval
```

---

## Core Documents — Read These First

Before any analysis or drafting task, orient against:

1. `docs/counter-tactics-guide.md` — the 13-tactic taxonomy with definitions and counter-moves
2. `docs/tactic-example-bank.md` — existing examples; check before adding new ones to avoid duplicates

For transcript ingestion tasks, also check `data/approved.csv` for existing talking points
before flagging new ones.

---

## Taxonomy Summary

13 documented tactics. Full definitions in `counter-tactics-guide.md`.

| # | Tactic | One-line recognition |
|---|---|---|
| 1 | Always on offense | Every response redirects to the target's sins |
| 2 | Isolated demands for rigor | They speculate freely; you need court-level proof |
| 3 | Schrodinger's joke | Serious accusation wrapped in irony |
| 4 | Unilateral principles | Standards applied to you but not them |
| 5 | No-win framing | Every response pre-interpreted as negative |
| 6 | Victim reversal (DARVO) | They provoke; your reaction becomes the crime |
| 7 | Moving goalposts | Concede one claim, immediately shift to another |
| 8 | Permission structures | "I wouldn't but I understand why someone would" |
| 9 | Maximize yours, minimize theirs | Your actions are sinister; theirs are jokes |
| 10 | Fragmentation | Retreat to "just one incident" when pattern is clear |
| 11 | Narrative laundering | Workshopped talking points appear organically |
| 12 | Cross-community infiltration | Small server runs ops funded by larger beneficiaries |
| 13 | Paint them as crazy | Name the coordination; get called "unhinged" |

---

## Narrative Clusters

Talking points and examples are tagged to named clusters:

| Cluster | Description |
|---|---|
| `lawsuit` | Claims related to the ongoing lawsuit narrative |
| `sexual-misconduct` | Sexual misconduct allegations and insinuations |
| `financial` | Financial corruption or profit-motive framing |
| `association` | Complicity-by-association claims |
| `platform-manipulation` | Claims about platform or algorithmic manipulation |
| `uncategorized` | New or unclassified clusters |

---

## Example Bank Schema

Each entry in `tactic-example-bank.md` follows this format:

```
### EX-#### | [Tactic Name]
**Source:** [Stream/platform/account]
**Date:** YYYY-MM-DD
**Timestamp:** HH:MM:SS or N/A
**Clip URL:** `https://youtu.be/[VIDEO_ID]&t=[seconds]` — or PENDING if video ID not yet in transcript header
**Status:** TIMESTAMP / CLIP / VERIFIED

**What happened:** [1-3 sentences]
**Why it fits:** [1-2 sentences]
**Notes:** [Optional]
```

Status progression: `TIMESTAMP` → `CLIP` → `VERIFIED`

When adding examples, assign the next available `EX-####` ID. Current highest: `EX-0045`.

---

## Approved Database Schema

`data/approved.csv` fields:

| Field | Description |
|---|---|
| `tp_id` | Immutable ID (TP-####) |
| `verbatim` | Exact phrasing as observed |
| `normalized` | Generalized version of the claim |
| `tactic_tag` | Tactic number and slug |
| `narrative_cluster` | Cluster tag |
| `first_seen` | Earliest confirmed date (YYYY-MM-DD) |
| `platform` | Platform where observed |
| `source_url` | Link or reference |
| `date_approved` | Date approved |
| `issue_url` | GitHub Issue link |

---

## Transcript Ingestion Workflow

When given a new transcript:

1. Clean timestamps and auto-caption artifacts if raw (store cleaned version in `transcripts/processed/`)
2. Read `docs/counter-tactics-guide.md` to orient against the taxonomy
3. Scan for tactic instances — note timestamp, speaker, verbatim quote
4. Check `docs/tactic-example-bank.md` for existing examples before adding new ones
5. Add new examples using the `EX-####` schema, incrementing from current highest ID
6. Flag any talking points for `data/approved.csv` if they meet the bar: specific, sourced, dateable
7. Note any tactic instances that don't fit existing taxonomy as Tactic candidates

**Do not modify raw transcripts.** Work from processed copies only.

### Clip URL generation

Processed transcript headers should include a `video_id:` line, e.g.:

```
video_id: dQw4w9WgXcQ
```

When writing EX entries, convert the timestamp to seconds and generate:
`https://youtu.be/[VIDEO_ID]&t=[seconds]`

Conversion: `H:MM:SS` → `H×3600 + M×60 + S`; `M:SS` → `M×60 + S`

Examples: `42:29` → 2549 → `https://youtu.be/ABC123&t=2549`  
`1:13:35` → 4415 → `https://youtu.be/ABC123&t=4415`

If no `video_id:` line is present, use `PENDING`. Status stays `TIMESTAMP` until a clip URL is added.

---

## Context Reading Pattern

For tasks that need project context but not full file reads:

1. Read this file (CLAUDE.md) first — always loaded
2. For taxonomy questions → `docs/counter-tactics-guide.md`
3. For example/duplicate checks → `docs/tactic-example-bank.md`
4. For talking point checks → `data/approved.csv`
5. For transcript work → `transcripts/processed/[file]`

Do not read raw transcripts unless explicitly asked to process them.

---

## Output Conventions

- Example IDs: `EX-####` (zero-padded to 4 digits)
- Talking point IDs: `TP-####` (zero-padded to 4 digits)
- Dates: `YYYY-MM-DD`
- Tactic references: use number + slug (e.g. `Tactic 3 — Schrodinger's Joke`)
- Status flags: `TIMESTAMP` / `CLIP` / `VERIFIED` (all caps)
- Platform tags: `twitter` / `discord-public` / `discord-leaked` / `twitch` / `youtube` / `reddit` / `other`

---

## Current Status

**Transcripts ingested:** 7
- Wick TV debate (2026-05-20) — EX-0001–EX-0015 documented
- Chudlogic post-debate reaction stream (2026-05-14) — EX-0018, EX-0021, EX-0032–EX-0037 documented
- Destiny v Dooby on Wick TV (2025-12-18) — EX-0026–EX-0031 documented
- Conor stream: snark coverage + Dooby debate (2026-05-18/22) — EX-0038–EX-0040 documented
- JSTLK/Kuihman/Mrow react to Stale 2000 (2026-05-19) — EX-0041–EX-0045 documented

**Active examples:** EX-0001–EX-0015, EX-0018, EX-0021, EX-0026–EX-0045 (37 total)
**Retired IDs (do not reuse):** EX-0016, EX-0017, EX-0019, EX-0020, EX-0022–EX-0025
**Next available ID:** EX-0046

**Tactic coverage** (target: 3 per tactic):

| # | Tactic | Count | Status |
|---|---|---|---|
| 1 | Always on Offense | 3 | ✓ |
| 2 | Isolated Demands for Rigor | 4 | ✓ |
| 3 | Schrodinger's Joke | 3 | ✓ |
| 4 | Unilateral Principles | 3 | ✓ |
| 5 | No-Win Framing | 2 | needs 1 |
| 6 | Victim Reversal (DARVO) | 2 | needs 1 |
| 7 | Moving Goalposts | 3 | ✓ |
| 8 | Permission Structures | 3 | ✓ |
| 9 | Maximize Yours, Minimize Theirs | 4 | ✓ |
| 10 | Fragmentation | 3 | ✓ |
| 11 | Narrative Laundering | 2 | needs 1 |
| 12 | Cross-Community Infiltration | 2 | needs 1 |
| 13 | Paint Them as Crazy | 3 | ✓ |

**Approved talking points:** 1 (TP-0001 — `association` cluster)

**Known actors:**
- Coordinators (adversary): JSTLK (JTO), Nikandros (Nick Andros/Shimu), Kuihman (Queman)
- Targets (team-adjacent): LonerBox, Hutch, Stardust, Whick
- Adversary debate participants: Dooby (Dec 2025 Wick TV), Aiden Underground, Dickers (May 2026 Wick TV), Chudlogic (May 2026 reaction stream)

---

## What's Next

- [x] Backfill EX-0008–EX-0015 from `whicktv-destiny-v-snarkers-1.txt` (adversary perspective only)
- [x] Find examples for Tactics 6, 9, 13 from adversary behavior (not team members)
- [x] Ingest `destiny-v-dooby-2025DEC18.txt`
- [ ] Write processed transcript for `destiny-v-dooby-2025DEC18.txt` to `transcripts/processed/`
- [x] Review EX-0016 — retired (LonerBox/Hutch/Stardust confirmed targets/team side)
- [x] Ingest `destiny+dan-v-chud+shamoo+kuihman-2026MAY14.txt` — EX-0032–EX-0037 documented
- [x] Ingest `conor-dooby-2025MAY22.txt` — EX-0038–EX-0040 documented (note: filename year is a typo; content is 2026-05-18/22/23)
- [x] Ingest `jstlk-mrow-kuihman-v-stale.txt` — EX-0041–EX-0045 documented
- [x] Generate clip URLs for all examples — all 37 at CLIP status
- [ ] Verify all CLIP examples (watch clips, confirm timestamps match entries)
- [ ] Push to GitHub repo and wire up Actions workflows