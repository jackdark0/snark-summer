# Channel sweep log

Project-level record of channels probed/swept and their disposition (archived, ingested, parked, or not-worth-it). Keeps off-archive probe results out of topic-specific docs. Topic-specific mention indices live elsewhere (e.g. `docs/dooby/dooby-mention-sweep.md`).

## locally archived channels (captions/metadata on disk under `transcripts/`)
`aiden-underground` · `kuihman-live` · `liquid-sonic` · `mrow-live` · `notsoerudite` · `purple-parry-gaming` · `ryle-kittenhouse` · `whick-tv`. Plus session ingests: `dooby-fbi-interviews` (the 4 Dooby videos), `whick-callin-2025AUG26`. (`transcripts/` is gitignored — local only.)

Channels delete and privatize content, so the local archive is treated as authoritative and is never pruned to match a live listing. Availability losses are tracked in `docs/archive-attrition.md`. As of 2026-07-24 the `ryle-kittenhouse` catalog is public nowhere and exists only here.

---

## 2026-07-24 — re-scrape of all tracked channels

First sweep since 2026-06-17 (whick-tv had been topped up to 2026-07-03). Enumerated `/videos` + `/streams` for all 8 archived channels with `yt-dlp --flat-playlist`, diffed against `transcripts/<channel>/raw/`, and pulled captions + metadata for everything newer than each channel's high-water mark. **94 new videos fetched, 92 with captions.** Availability losses are recorded in `docs/archive-attrition.md`.

| Channel | Archived before | New fetched | Now private | Notes |
|---|---|---|---|---|
| aiden-underground | 52 | 16 | 13 | privatized block 2026-03-27→05-05 |
| kuihman-live | 505 | 14 | 0 | `/streams` tab now merged into `/videos` |
| liquid-sonic | 2 | 3 | 0 | still a partial pull, see below |
| mrow-live | 47 | 1 | 1 | |
| notsoerudite | 113 | 2 | 0 | 15 members-only, not pullable |
| purple-parry-gaming | 373 | 28 | 0 | 7 members-only, 1 age-gated |
| ryle-kittenhouse | 631 | 0 | **631** | whole channel privatized + renamed |
| whick-tv | 504 | 30 | 0 | |

Two 2026-07-24 uploads (`aiden-underground` STARDUST VS JSTLK + WHICKTENT???, `purple-parry-gaming` Stardust vs Jstlk) had no auto-captions yet. Rather than wait, the underlying conversation was pulled from the source channel — see StardustIRL below.

### StardustIRL — new archive, 2026-07-25

`@StardustIRL` / `UC89YtRSTserHOSo_KTVBvlw` (3,050 subs). **12 on-topic streams archived** to `transcripts/stardust-irl/`; 2 more are members-only. Not previously tracked.

Distinct from the rest of the corpus: these are streams where JSTLK, Kuihman and Chudlogic appear and speak **first-person**, hosted target-side, rather than adversary hosts narrating the arc. Densest material in the whole sweep — `xSqfq8VXx3U` (Talking to JSTLK, 6h46m) and `6L029RAy80w` (THE GIRLS ARE STILL FIGHTING PART 3, 6h28m) each run 32.9% Destiny mention-time, with Kuihman at 248 keyword hits in the latter.

Nothing banked from it yet. These are 3–7 hour multi-party streams and auto-captions carry no speaker identity, so quoting a named coordinator needs diarization first. Full table and the attribution gate are in `docs/sweep-2026-07-24-candidates.md`.

Not yet added to the tracked-channel list at the top of this file, or to the ADVERSARY/COMPARISON maps in `scripts/actor_airtime.py` — decide that before the next sweep.

**The archive was never a full mirror.** The diff surfaced ~46 un-archived videos that sit *below* each channel's high-water mark, dated 2023–2024, i.e. a pre-existing historical gap rather than new uploads. These were deliberately not fetched, since "since our last scrape" means new material. Counts: whick-tv 22, liquid-sonic 12, kuihman-live 11, purple-parry-gaming 1. Note this contradicts the "full `/videos`+`/streams` pull" claim in `docs/airtime-analysis/README.md`; the airtime denominators are a filtered set, not the whole channel. Ranking conclusions are probably unaffected (they were shown invariant to filtered→full), but the wording should be corrected.

Liquid Sonic remains the weak spot flagged in the airtime caveats: 5 archived of 39 listed. Still not safe to quote its percentage.

---

## external / off-archive channels probed — PARKED (not ingested)

### 2026-06-25 — ChudLogic / President Sunday
Probed during a channel sweep. **Not ingested** — these are third-party snark commentary *about* Dooby/Destiny, not first-person, so they don't serve the Dooby hole-finding ("catch him in a lie"). Resume from here if scope widens to snark-narrative artifacts.

**ChudLogic** — no dedicated channel scan warranted. 1 of 80 recent uploads touches the thesis ("Jstlk Debated Tectone's Biggest Ally"); rest is general streamer drama. His relevant content is the already-ingested reaction stream (EX-0032–0037).

**President Sunday** (real channels are ID-based; the `@PresidentSunday` / `@PSAfterDark` handles are decoys):
- main `UCK1HtOUD5s_3hhzy-bkpsiw` — notable artifact: "Exposing The Destiny Abuse Machine" (`qUzXZtj7wBM`, 22:27, 2025-01-20, 115k views). Manufactured-abuse-narrative genre (Pixie/Lauren/Rose/Kiwi); **no Dooby**.
- second / "After Dark" = **"President Sunday: Dark"** `UCuNByaMIS9FVuudA-_cS6kw` (3.3k subs, 133 videos). Destiny-critical channel; ~7/133 title-relevant. Autocap scan of those 7:

| id | title | dur | Dooby/snark signal |
|---|---|---|---|
| `xRztQM-ayzw` | Steven Bonnell's Greatest Nightmare | 38:51 | **top pick** — Doobie ×4, snark ×7, server ×7, Pixie ×14; discusses Dooby's role directly |
| `xcrAe1aEyjY` | The Latest Destiny Claims Have Zero Evidence | 1:49 | Dubbie ×1, snark ×5; names "Jtock, Queman or Dubbie" |
| `XHqfPk_b078` | IRL Muppet Sweeps for Destiny's Kid Problem | 20:41 | abuse-narrative; no Dooby |
| `S3CHZ0P4STA` | Destiny (In Court For Minor Issue) Discovers Nick Land | 1:03 | server ×3; no Dooby |
| `BjdR1xAILkE` | DGG Bottom-Feeder's Career is on Life Support | 2:06 | server ×5, pixie ×2; no Dooby |
| `Hc_aiP_4d6s` | Steven Bonnell: Israel's Star Player | 1:47 | minimal |
| `BWy2GMGAiiQ` | Destiny is Actually a Terrible Debater | 1:15 | grooming-narrative; no Dooby |

If revisited: `xRztQM-ayzw` is the one worth a full ingest (snark-side characterization of Dooby), but it's commentary *about* him, not first-person.
