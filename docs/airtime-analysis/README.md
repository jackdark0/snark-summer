# airtime analysis — how much does each channel talk about a subject?

measures **caption mention-time** of a subject (Destiny by default) across each channel's
**full** `/videos`+`/streams` pull. answers "what share of their airtime is about X."

## scripts
- **`scripts/actor_airtime.py`** — the tables. flags: `--subject destiny|notsoerudite`,
  `--since YYYYMMDD`. default output breaks out **whole channel** vs **lawsuit arc (since
  2024-10)**, each with measured tables (±0 / ±30 / ±90 padding) + a generous "titled-whole"
  upper-bound table.
- **`scripts/methodology_check.py`** — stress tests: padding sensitivity, mention-burst
  stats (scattered vs sustained), keyword false-positive attribution; also writes
  `non-titled-destiny-hits.md`.

## regenerate
```
python scripts/actor_airtime.py --subject destiny      > docs/airtime-analysis/actor-airtime.md
python scripts/actor_airtime.py --subject notsoerudite > docs/airtime-analysis/notsoerudite-mentions.md
python scripts/methodology_check.py                    > docs/airtime-analysis/methodology-check.md
```

## docs here
- `actor-airtime.md` — the Destiny analysis (main tables).
- `notsoerudite-mentions.md` — mirror: "who talks about NotSoErudite / Kyla Turner."
- `methodology-check.md` — the stress tests.
- `non-titled-destiny-hits.md` — non-titled videos with hits, for manual review.

## headline
adversary channels run **~10–21%** of airtime on Destiny (±30s); target-side **Whick ~5%**.
the *ranking* is invariant to every knob tested — padding (±0→±90), keyword tightness,
filtered→full channel, video-vs-stream counting, and whole-vs-lawsuit-arc window. only the
*magnitude* moves.

## caveats
- keyword-anchored: counts *mentioning*, not *attacking*; can't read tone.
- leans on auto-caption quality; absolute % scales with padding (ranking doesn't).
- keyword set is tight (`destiny | DGG | steven bonnell`) to avoid FPs like "Steven Universe".
- **Liquid Sonic** is a 2-video partial scrape (never trued-up) — its % is noise; full-pull
  before relying on it (note also in `actor_airtime.py`).

## data
`transcripts/<channel>/raw/` holds auto-captions (`.en.vtt`) + `info.json`, pulled via yt-dlp.
`transcripts/` is gitignored (regeneratable); some original Kuihman files predate the ignore
and remain tracked.
