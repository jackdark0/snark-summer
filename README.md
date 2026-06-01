# Coordinated Narrative Tracker

A community pipeline for documenting, reviewing, and analyzing coordinated talking points and harassment campaign narratives.

---

## How it works

```
Open submission (Issue form)
        ↓
Triage queue (auto-labeled by Actions)
        ↓
Mod review (checklist comment posted automatically)
        ↓
Approved database (data/approved.csv — auto-updated on approval)
```

## Agentic review workflow

For channel/transcript scans, use the scaffold in `agentic/`:

```powershell
python scripts\agentic\make_packets.py --glob "transcripts\ryle-kittenhouse\processed\*.txt"
python scripts\agentic\validate_candidates.py agentic\candidates\*.jsonl
python scripts\agentic\validate_bank.py
python scripts\agentic\validate_clips.py --min-height 1080
```

Scouts write candidate JSONL; duplicate/score reviewers write reports; only the
merge editor updates the example bank. See
[`docs/agentic-workflow.md`](docs/agentic-workflow.md). Use
[`docs/actor-aliases.md`](docs/actor-aliases.md) for canonical names and
[`docs/coordinator-consistency.md`](docs/coordinator-consistency.md) for the
dated coordinator pattern tracker.

---

## Submitting a talking point

1. Open a [new Issue](../../issues/new/choose) and select **Talking Point Submission**
2. Fill out the form — verbatim claim, platform, date, and source are the most important fields
3. Tactic tag and narrative cluster are optional but helpful
4. Your submission enters the mod review queue automatically

**Do not include private personal information about individuals.**

---

## Narrative clusters

Submissions can be tagged to a named cluster. Current clusters:

| Cluster | Description |
|---|---|
| `lawsuit` | Claims related to the ongoing lawsuit narrative |
| `sexual-misconduct` | Sexual misconduct allegations and insinuations |
| `financial` | Financial corruption or profit-motive framing |
| `association` | Complicity-by-association claims |
| `platform-manipulation` | Claims about platform or algorithmic manipulation |
| `uncategorized` | New or unclassified clusters |

New clusters can be proposed via Issue.

---

## Tactic taxonomy

Submissions can optionally be tagged to one of 13 documented tactics. See [docs/counter-tactics-guide.md](docs/counter-tactics-guide.md) for full descriptions and counter-moves.

| # | Tactic |
|---|---|
| 1 | Always on offense |
| 2 | Isolated demands for rigor |
| 3 | Schrodinger's joke |
| 4 | Unilateral principles |
| 5 | No-win framing |
| 6 | Victim reversal (DARVO) |
| 7 | Moving goalposts |
| 8 | Permission structures |
| 9 | Maximize yours, minimize theirs |
| 10 | Fragmentation |
| 11 | Narrative laundering |
| 12 | Cross-community infiltration |
| 13 | Paint them as crazy |

---

## Approved database

`data/approved.csv` is the canonical record of all approved entries. It is updated automatically when a submission is approved and closed.

**Schema:**

| Field | Description |
|---|---|
| `tp_id` | Immutable ID (TP-####) |
| `title` | Short title from submission |
| `verbatim` | Exact phrasing as observed |
| `platform` | Platform where observed |
| `narrative_cluster` | Cluster tag |
| `tactic_tag` | Tactic tag |
| `first_seen` | Earliest confirmed date |
| `source_url` | Link or reference |
| `date_approved` | Date approved by mods |
| `issue_url` | Link to original GitHub Issue |

---

## For moderators

When a new submission comes in:

1. A triage checklist comment is posted automatically on the Issue
2. Work through the checklist — verify source, check for duplicates, correct labels if needed
3. To **approve**: add `status: approved` label, close the Issue — CSV updates automatically
4. To **reject**: add `status: rejected` label, close with a brief reason in comments
5. To **request info**: add `status: needs-info`, comment on the Issue

Label definitions are in [docs/labels.md](docs/labels.md).

---

## Setup

1. Create a new GitHub repo (public or private)
2. Copy this repo structure in
3. Create all labels defined in `docs/labels.md`
4. Enable GitHub Actions (Actions tab → enable)
5. Set repo to allow Issues (Settings → General → Features)
6. Optionally: connect a Google Form via Zapier/Make to auto-open Issues from external submissions

---

## Classifier integration

`data/approved.csv` is structured for direct ingestion as labeled training data. Fields map to:

- `verbatim` → input text
- `tactic_tag` → classification label
- `narrative_cluster` → secondary label / metadata
- `first_seen` + `platform` → temporal and source metadata
