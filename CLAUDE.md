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

agentic/
  roles/                     # Agent role prompts
  packets/                   # Generated transcript packets for scout agents
  candidates/                # Scout-agent JSONL candidate records
  reports/                   # Duplicate, score, clip, and merge reports

scripts/agentic/
  make_packets.py            # Split processed transcripts into scout packets
  validate_candidates.py     # Validate scout JSONL before review/merge
  validate_bank.py           # Check bank/audit consistency
  validate_clips.py          # Verify local MP4 clip quality

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
**Source:** [Channel] - [Video title] / [Platform]
**Date:** YYYY-MM-DD
**Timestamp:** HH:MM:SS or N/A
**Clip URL:** `https://youtu.be/[VIDEO_ID]?t=[seconds]` (or `https://www.youtube.com/live/[VIDEO_ID]?t=[seconds]` for livestream IDs) — or PENDING if video ID not yet in transcript header
**Status:** TIMESTAMP / CLIP / VERIFIED

**What happened:** [1-3 sentences]
**Why it fits:** [1-2 sentences]
**Notes:** [Optional]
```

Status progression: `TIMESTAMP` → `CLIP` → `VERIFIED`

Source naming rule: prefer metadata when available. Use the channel/uploader name and exact video title for source captures, e.g. `Whick TV - Destiny vs the Snarkers / YouTube Live`. Put contextual actor notes in `**Notes:**` rather than the source label.

Duplicate handling rule: many later videos are review streams or clip reviews of earlier videos. Treat those as secondhand by default. Do not add a new EX entry when the underlying event, tactic, and key wording are already covered. Prefer the canonical source with the clearest evidence: original/primary footage first, then earliest upload, then best audio/transcript quality. A review video can become a separate example only if it adds a distinct tactic move, such as new permission framing, narrative laundering, audience routing, minimization, or a separate denial/reversal. In that case, note the relationship in `**Notes:**`, e.g. `secondhand review of EX-####; added for new laundering frame`.

When adding examples, assign the next available `EX-####` ID. Current highest: `EX-0097`.

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
4. Check actor/entity names against `docs/actor-aliases.md`. If a new or ambiguous actor/entity appears and its role matters, ask the user for classification before using it in authored analysis. If a batch run cannot stop cleanly, add it to `docs/actor-classification-queue.md` and mark it `unknown / needs-classification`.
5. Check `docs/tactic-example-bank.md` for existing examples before adding new ones. Search distinctive names, claims, phrases, and timestamps, especially when the source is reacting to or replaying another video.
6. Add new examples using the `EX-####` schema, incrementing from current highest ID, and fill `**Source:**` from metadata when available
7. Flag any talking points for `data/approved.csv` if they meet the bar: specific, sourced, dateable
8. Note any tactic instances that don't fit existing taxonomy as Tactic candidates

**Do not modify raw transcripts.** Work from processed copies only.

If a duplicate is found after an EX entry was added, keep the ID retired in place. Add a short `RETIRED — duplicate of EX-####` note to the bank, remove it from active earmarked coverage, and list the ID under retired IDs in this file. Do not reuse retired IDs.

### Agentic review workflow

Use `docs/agentic-workflow.md` for parallel review. The short version:

1. Generate scout packets with `python scripts\agentic\make_packets.py --glob "<processed transcript glob>"`
2. Send packets to scout agents using `agentic/roles/scout.md`
3. Save scout output as JSONL in `agentic/candidates/`
4. Validate with `python scripts\agentic\validate_candidates.py agentic\candidates\*.jsonl`
5. Run duplicate and score review before any bank edit
6. Let only the merge editor apply accepted candidates to `docs/tactic-example-bank.md` and `docs/tactic-example-score-audit.md`
7. Run `validate_bank.py`, `validate_clips.py`, and `git diff --check` before commit

Semantic work can be parallelized. Bank edits are serialized through the merge editor.

Actor classification gate: `Snark Server` is a coordination hub where
coordinators coordinate, not a person. Do not assign hub-level activity to a
specific coordinator unless the source identifies that person or an accepted
example documents the relationship.

### Clip URL generation

Processed transcript headers should include a `video_id:` line, e.g.:

```
video_id: dQw4w9WgXcQ
```

If available, also preserve metadata for source naming: `channel:`, `title:`, and `platform:`. Example bank entries should use `Channel - Video title / Platform`.

When writing EX entries, convert the timestamp to seconds and generate:
- Normal video IDs: `https://youtu.be/[VIDEO_ID]?t=[seconds]`
- Headers stored as `live/[VIDEO_ID]`: `https://www.youtube.com/live/[VIDEO_ID]?t=[seconds]`

Conversion: `H:MM:SS` → `H×3600 + M×60 + S`; `M:SS` → `M×60 + S`

Examples: `42:29` → 2549 → `https://youtu.be/ABC123?t=2549`
`1:13:35` → 4415 → `https://youtu.be/ABC123?t=4415`

If no `video_id:` line is present, use `PENDING`. Status stays `TIMESTAMP` until a clip URL is added.

### Physical clip quality

For local MP4 clips, maximize quality unless the user asks for small files. Use split best video plus best audio, not the low-resolution combined fallback. Preferred MP4 selector: `bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/bv*+ba/b`. If output container is not constrained to MP4, `bv*+ba/b` is acceptable. Always provide `ffmpeg` through PATH or `--ffmpeg-location` so yt-dlp can merge streams.

For short sections from long YouTube archives, `yt-dlp --download-sections` can hang on split high-quality streams. In that case, download the unique source video once with the preferred selector, cut clips locally with `ffmpeg -ss <start> -i <source> -t <duration> -map 0:v:0 -map 0:a:0? -c copy -movflags +faststart`, verify resolution with `ffprobe`, then delete the temporary source. Do not treat 640x360 clips as archival when a higher source exists.

---

## Context Reading Pattern

For tasks that need project context but not full file reads:

1. Read this file (CLAUDE.md) first — always loaded
2. For taxonomy questions → `docs/counter-tactics-guide.md`
3. For example/duplicate checks → `docs/tactic-example-bank.md`
4. For talking point checks → `data/approved.csv`
5. For transcript work → `transcripts/processed/[file]`
6. For parallel review setup → `docs/agentic-workflow.md`

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

**Transcripts ingested:** 11 batches
- Wick TV debate (2026-05-20) — EX-0001–EX-0015 documented
- Chudlogic post-debate reaction stream (2026-05-14) — EX-0018, EX-0021, EX-0032–EX-0037 documented
- Destiny v Dooby on Wick TV (2025-12-18) — EX-0026–EX-0031 documented
- Conor stream: snark coverage + Dooby debate (2026-05-18/22) — EX-0038–EX-0040 documented
- JSTLK/Kuihman/Mrow react to Stale 2000 (2026-05-19) — EX-0041–EX-0045 documented
- Ryle Kittenhouse YouTube channel scan (available archive found back to 2025-04-08; 40 captions pulled so far) — EX-0046–EX-0051 documented
- Score-5 coverage pass across processed corpus — EX-0052–EX-0058 documented
- KuihmanLive YouTube channel scan (55 captions pulled from filtered recent/title-matched set) — EX-0059–EX-0087 documented
- MrowLive/Liquid Sonic filtered channel scan (17 accessible captions pulled; Liquid Sonic Whick video age-gated without cookies) — EX-0088–EX-0090 documented
- Purple Parry Gaming triage pass — EX-0091–EX-0096 documented (bank declared **uncapped** at this point)
- **Local high-fidelity re-transcription + verification pass (2026-06-16):** all 54 live KuihmanLive videos re-transcribed via the youtube-clipper whisper+diarize pipeline (outputs in `transcripts/kuihman-live/_transcripts/`, gitignored). Bank entries from the auto-caption scans are being verified verbatim against these local transcripts and carry "wording verified" notes as checked (so far: gi1M, I697f4pNk48, hPba9Hu2ltg, iaGkqiDHY24, 5P--7ZRZaz8 → 27 entries). **Correction made:** EX-0081 had a wrong timestamp (16:41 → 58:30) and a fabricated "deserve to sweat" quote, both fixed. Net-new scan of the rest of the channel yielded no new entries (off-topic DeOrio/H3/commentary drama or already covered).

**Active examples:** EX-0001–EX-0015, EX-0018, EX-0021, EX-0026–EX-0097 minus the 3 duplicates below (86 active)
**Retired IDs (do not reuse):** EX-0016, EX-0017, EX-0019, EX-0020, EX-0022–EX-0025 (removed); EX-0052, EX-0058, EX-0080 (flagged in place as duplicates of EX-0004, EX-0010, EX-0039 respectively)
**Next available ID:** EX-0098
**Score audit:** `docs/tactic-example-score-audit.md`
**Actor/entity register:** `docs/actor-aliases.md`
**Actor classification queue:** `docs/actor-classification-queue.md`
**Coordinator consistency tracker:** `docs/coordinator-consistency.md`
**Coordinator contradiction pass:** `docs/coordinator-contradictions.md`

**Tactic coverage:** The bank is **uncapped** (as of the Purple Parry pass, EX-0091+). New examples are accepted when they add distinct source/event coverage, not to fill a per-tactic quota; the old 6–7 "soft cap" no longer applies. Per-tactic counts and scoring live in `docs/tactic-example-score-audit.md`.

**Approved talking points:** 1 (TP-0001 — `association` cluster)

**Known actors:**
- Coordinators (adversary): JSTLK (aliases: JTO/Jtock/Jaystalk), Kuihman (auto-caption variants: Queman/Queenman), Nikandros (Nick Andros; do not collapse Shimu without source confirmation)
- Coordination hubs: Snark Server (aliases: Snark Discord, Snark Left, secret Snark Discord)
- Targets (team-adjacent): LonerBox, Hutch, Stardust, Whick
- Adversary debate participants: Dooby (Dec 2025 Wick TV), Aiden Underground, Dickers (May 2026 Wick TV), Chudlogic (May 2026 reaction stream), Counterpoints/Conor (former Destiny friend "lost to the snarkers," classified 2026-06-16; tactic actor in EX-0062/0067/0078)
- Actors pending classification (queued, see `docs/actor-classification-queue.md`): DeOrio, BigBunjeee, Beckett, TurkeyTom, CameronF305, Anisa Jomha, Alex Novell — mostly the intra-commentary-community "DeOrio drama," whose relevance to the Destiny-harassment thesis is unresolved

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
- [x] Ingest Ryle Kittenhouse YouTube channel scan — EX-0046–EX-0051 documented
- [x] Score current examples and add higher-scored coverage examples — EX-0049–EX-0058 added/promoted; audit in `docs/tactic-example-score-audit.md`
- [x] Ingest KuihmanLive filtered channel scan — EX-0059–EX-0087 documented
- [x] Ingest MrowLive/Liquid Sonic filtered channel scan — EX-0088–EX-0090 documented; Liquid Sonic yielded no bank additions after filtering
- [x] Generate clip URLs for all active examples — all 79 active examples at CLIP status
- [ ] Verify all CLIP examples (watch clips, confirm timestamps match entries)
- [x] Replace legacy 640x360 local MP4s with max-quality clips (49 existing clips verified at 1920x1080)
- [x] Build agentic review scaffold for packetized transcript scans, candidate JSONL, and validation gates
- [ ] Push to GitHub repo and wire up Actions workflows
