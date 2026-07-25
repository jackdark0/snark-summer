# PROTECTED — do not delete

These 6 MP4s are the only surviving video from the Ryle Kittenhouse channel.

On or before 2026-07-24 the channel (`UCKnch9nDXjDnOxp4kCmxBMQ`) renamed itself to `justtalk_archive` and privatized its entire 631-video catalog. Every source URL these clips were cut from now returns `Private video`. They cannot be re-downloaded.

## Why these are tracked when `clips/` is otherwise gitignored

`.gitignore` excludes `clips/` in general because clip output is normally regeneratable from YouTube. That assumption no longer holds here. `clips/ryle-kittenhouse/` is explicitly un-ignored so the files are versioned, pushed to the remote, and survive `git clean -xdf` — which would otherwise delete them without warning.

Do not add `clips/ryle-kittenhouse/` back to `.gitignore`.

## What they are

| File | Bank entry | Source video (now private) |
|---|---|---|
| EX-0046.mp4 | EX-0046 — Cross-Community Infiltration | `Y91C-2onTSs` — DGGer's Guide to the Destiny Content Nuke |
| EX-0047.mp4 | EX-0047 — Permission Structures | `Cjmf97AGdTI` — Destiny Orbiter returns for Debate... |
| EX-0048.mp4 | EX-0048 — Fragmentation | `Z31osFs0rCk` — Did Jaystalk D@XX WillyMacShow?? |
| EX-0049.mp4 | EX-0049 — No-Win Framing | `_-xdWrdI24I` — DEBUNKING the most PATHETIC Hit Piece yet... |
| EX-0050.mp4 | EX-0050 — Victim Reversal (DARVO) | `E7lH52HZzAg` — ChudLogic Just FOLDED Completely... |
| EX-0051.mp4 | EX-0051 — Narrative Laundering | `uZ5Fe_k-xfQ` — The "Secret" SNARK Discord Logs EXPOSED |

`CHECKSUMS.json` holds sha256 and byte size for each file. Re-run a hash compare if you suspect corruption:

```
python -c "import hashlib,json,os;d=json.load(open('CHECKSUMS.json'));[print(f,'OK' if hashlib.sha256(open(f,'rb').read()).hexdigest()==v['sha256'] else 'MISMATCH') for f,v in d.items()]"
```

## Bank entries with no clip

Eight further entries cite now-private Ryle videos but were never clipped: EX-0041–EX-0045, EX-0053, EX-0054, EX-0056. Their quotes remain verifiable against the local auto-caption transcripts in `transcripts/ryle-kittenhouse/processed/` (gitignored, and see `docs/archive-attrition.md` for backup status). There is no surviving video for those.

See `docs/archive-attrition.md` for the full attrition record.
