# Archive attrition

Living record of tracked-channel videos that were once public and are no longer reachable, plus what we still hold locally. Kept separate from the sweep log because attrition is ongoing and the local copy is increasingly the only accessible one.

Rule for this project: a video disappearing from a channel listing is **not** evidence it never existed. Nothing in `transcripts/` gets deleted to "match" a live channel. Diffs are recorded here instead.

Last verified: 2026-07-24.

## Summary

| Channel | Archived locally | Not publicly reachable | State |
|---|---|---|---|
| ryle-kittenhouse | 631 | 631 (100%) | whole channel privatized |
| aiden-underground | 52 | 13 | selective privatization |
| mrow-live | 47 | 1 | single video privatized |
| kuihman-live | 505 | 0 | intact |
| notsoerudite | 113 | 0 | intact |
| purple-parry-gaming | 373 | 0 | intact |
| whick-tv | 504 | 0 | intact |
| liquid-sonic | 2 | 0 | intact (partial pull, see sweep log) |

Every "not reachable" ID above was probed individually and returned `Private video`, not `Video unavailable` or 404. These are privatizations, so the uploads still exist on YouTube's side and could return.

## ryle-kittenhouse — full channel privatized

The channel still exists under the same ID `UCKnch9nDXjDnOxp4kCmxBMQ` with 4,250 subscribers, but it was renamed from **Ryle Kittenhouse** to **justtalk_archive** and has no public videos. `/videos` and `/streams` both return "does not have a videos tab", and the channel root enumerates zero entries. Individually probed videos return `Private video`.

Archived span was 2025-04-08 to 2026-06-16, roughly 40-56 uploads per month with no gaps, so this was an all-at-once switch rather than a gradual cleanup.

### What the campaign side says about it

On 2026-07-24, roughly five weeks after the last archived upload, Stardust asked JSTLK directly on stream why the channel went dark, pressing him on the grounds that "you would know, you're, you know, you employ him."

He first said "I don't know. Why?", then: "I assume deleted his channel because of the prolific doxing and life ruination campaign Destiny keeps threatening, right?" — closing with "That really sucks for Ryle, huh?"

Worth holding carefully. It is offered as an **assumption**, not knowledge, by someone positioned to know, and it is the only on-record explanation we have. It is a claim about motive, not a confirmed cause, and it does not tell us whether the videos were deleted or privatized (our probes say privatized). Banked as EX-0108 for the reversal move. Source: `xSqfq8VXx3U` at 1:17:28, local diarized transcript plus the YouTube auto-caption track.

The useful factual residue: someone close to the channel treats the wipe as deliberate and self-initiated, which is consistent with the all-at-once pattern in the archive.

What we still hold:

- 631 `info.json` metadata records
- 621 `.en.vtt` auto-caption files
- 621 processed transcripts in `transcripts/ryle-kittenhouse/processed/`
- `transcripts/ryle-kittenhouse/ryle-metadata.tsv` (id, upload_date, duration, view_count, title, url, description)

This is now the project's only route to that channel's content.

### What is preserved where

Commit `37e1520` had already force-added most of the Ryle text archive before the blanket `transcripts/` ignore took effect, so the analysis-critical material is **already off-machine on GitHub**:

| Asset | Local | On GitHub | Desktop backup |
|---|---|---|---|
| processed reading transcripts | 621 | **621** | 621 |
| `clean.vtt` (deduped, timestamped) | 621 | **621** | 621 |
| `ryle-metadata.tsv` (id, date, duration, views, title, url, description) | yes | **yes** | yes |
| clips (MP4) | 6 | **6** (added 2026-07-25) | 6 |
| per-video `info.json` | 632 | 41 | 632 |
| raw `en.vtt` / `en-orig.vtt` | 621 / 620 | 40 / 40 | 621 / 620 |

Desktop backup path: `C:\Users\User\Desktop\research-memes-BACKUP-20260716\misc-cringe\daliban\snark-summer\transcripts\ryle-kittenhouse\`.

**Assessment:** every quote in the example bank can be re-verified from GitHub alone, because the processed transcripts and the timestamped `clean.vtt` set are both complete there. What is *not* off-machine is the bulk per-video `info.json` metadata and the pre-dedup raw captions — but `ryle-metadata.tsv` carries the same fields that the bank actually uses (title, date, duration, url), and `clean.vtt` supersedes the raw captions for analysis. So a disk failure would cost provenance detail and re-derivation convenience, not the evidence.

Earlier drafts of this doc called the archive single-copy. That was wrong on two counts: there is a Desktop backup, and the important part was already pushed.

Ten archived videos never had captions pulled and are metadata-only; those are unrecoverable now.

**Clips.** The 6 Ryle clips in `clips/ryle-kittenhouse/` are the only surviving *video* from this channel. On 2026-07-25 they were un-gitignored and committed so they are versioned and mirrored to GitHub, rather than living only in an ignored directory that `git clean -xdf` would remove. `CHECKSUMS.json` in that directory records sha256 + byte size for each so silent corruption is detectable. See `clips/ryle-kittenhouse/PROTECTED.md`.

## aiden-underground — 13 privatized

All from a 2026-03-27 to 2026-05-05 window, but not the whole window: 23 other archived uploads from the same span are still public.

| Date | ID | Title |
|---|---|---|
| 2026-03-27 | zeEzK0odW8M | FAITHFUL SHERRIFF, TECTONE, THE OP BLOCK, AND MORE... |
| 2026-03-29 | I_rNlSnc8Bg | RABBI SHMULEY VS SALVO PANCAKES |
| 2026-04-04 | 4MwYJmF-RTs | THE OPP BLOCK DRAMA,, CHIBIREVIEWS, FAITHUL SHERRIFF, AND MORE... |
| 2026-04-12 | 6klZUoJLuc4 | SYKKUNO DRAMA, ROBLOX DRAMA, AND MORE... |
| 2026-04-21 | lwfGaKQs_wo | CHIBIREVIEWS IS MY ARCH NEMESIS |
| 2026-04-22 | gVBKUe4QnZU | DEBATING A FOODSHOPS FAN? - FUENTES DONATOR EXPOSED - TACTICALTEMPLAR |
| 2026-04-24 | ZJY8eDGiocg | Finally Watching the Bunjee Video - AF Donators Exposed - and More... |
| 2026-04-27 | eL02xy1dKvI | LATE NIGHT DRAMA - CHIBIREVIEWS - AND MORE... |
| 2026-04-30 | Re6jf7pFd6g | Chibi vs Josh Moon - X Leftists Call Out 'Privileged' Influencer - and More |
| 2026-05-01 | ezljfAMFFlk | Lolcow Streamers, The Return of Jalyn, and More... |
| 2026-05-02 | tawok-zFgmE | Faithful Sherriff Stalker Exposed? Chibireviews scam, and More... |
| 2026-05-04 | 7EKJUJ2m2Ao | FOODSHOPS, DRAMA., AND CRINGE... |
| 2026-05-05 | fb2VDxKBUVc | NICK SHIRLEY IN CUBA, PARRY CALLS ME OUT, AND MORE... |

**Assessed impact on the Destiny thesis: low.** The privatized set skews to lolcow and commentary-scene material (ChibiReviews, Faithful Sherriff, Foodshops, Josh Moon). The Destiny/DGG/snark-heavy uploads from the same window are all still public, including `DEBATING DESTINY....` (2026-05-21), `SNARKKRIEG DAY 3 KUIHMAN SPEAKS OUT- DGG LIES` (2026-05-18), `Aiden vs DGG, LiquidSonic Video` (2026-05-28), and `WHICK VS COMMENTARY - PARRY LEAKED VC` (2026-05-26). ChibiReviews appears on both sides of the split, so the selection does not track a single clean topic and no motive should be read into it from title evidence alone.

## mrow-live — 1 privatized

| Date | ID | Title |
|---|---|---|
| 2026-06-17 | tkYWQUkx6gI | late night chill and dark souls 1 2026-06-17 03:03 |

Gaming stream, no apparent thesis relevance.

## Paywalled and age-gated, never archived

Not attrition. These were never pulled because they need cookies, and they showed up as errors during the 2026-07-24 sweep. Recorded so future sweeps do not re-probe them as if they were new.

- notsoerudite: 15 members-only
- purple-parry-gaming: 7 members-only, 1 age-gated
- kuihman-live: 1 age-gated
- liquid-sonic: 1 age-gated

Pulling these needs `--cookies-from-browser` against a signed-in account, and members-only content needs an active channel membership.

## Follow-ups

- [x] Confirm off-machine preservation. Processed transcripts, `clean.vtt`, `ryle-metadata.tsv` and the clips are all on GitHub; a Desktop backup holds the full raw set too.
- [ ] Optional: push the remaining 591 `info.json` records so per-video provenance survives a disk failure. Low priority — `ryle-metadata.tsv` already covers the fields the bank cites.
- [ ] Re-verify aiden and mrow privatized IDs on the next sweep to catch anything that goes public again.
- [ ] Decide whether any EX bank entry cites a now-private video. If so, note the source as privatized so the dead link is not read as a fabricated citation.
