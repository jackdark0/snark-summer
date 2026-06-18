#!/usr/bin/env python3
"""Per-channel mention-time tracker for the snark-summer corpus.

Measures how much each channel talks about a SUBJECT via caption mention-time.
Subject is selectable with --subject (see SUBJECTS below); default is Destiny.

Two readings:
1. MEASURED (conservative) — pure caption mention-time across ALL videos, shown
   across the padding range ±0 (floor) / ±30 / ±90 (ceiling). Cues matching the
   subject keyword, each padded ±pad and overlaps merged.
2. GENEROUS upper bound — subject-TITLED published videos counted whole + measured
   ±30s bleed in the rest. Subject-titled livestreams (`was_live`) are excluded
   from the whole-count and measured instead (a long stream titled "X..." isn't
   100% about X).

Regenerate, e.g.:
    python scripts/actor_airtime.py --subject destiny      > docs/airtime-analysis/actor-airtime.md
    python scripts/actor_airtime.py --subject notsoerudite > docs/airtime-analysis/notsoerudite-mentions.md
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ADVERSARY = {
    "kuihman-live": "Kuihman",
    "mrow-live": "MrowLive",
    "ryle-kittenhouse": "Ryle / JSTLK (outlet)",
    "purple-parry-gaming": "Purple Parry",
    "liquid-sonic": "Liquid Sonic",   # NOTE: only the original 2-video scrape — never got the
                                      # full-channel true-up. its 45-51% is tiny-sample noise;
                                      # full-pull @LiquidSonic before relying on / publishing it.
    "aiden-underground": "Aiden Underground",
}
COMPARISON = {
    "whick-tv": "Whick TV (target-side)",
    "notsoerudite": "NotSoErudite (target-side)",
}

# Each subject: mention keyword (regex), the title keyword used for the generous
# "titled = whole" logic, display label, and output filename.
SUBJECTS = {
    "destiny": dict(
        label="Destiny",
        mention=r"\bdestiny\b|\bdgg\b|\bsteven bonn?ell\b",
        title_kw="destiny",
        kw_desc="`destiny | DGG | steven bonnell`",
        kw_note="Deliberately tight: bare `steven` was dropped because it matched false "
                "positives like \"Steven Universe\".",
        outfile="actor-airtime.md",
        grouped=True,
    ),
    "notsoerudite": dict(
        label="NotSoErudite",
        mention=r"\berudite\b|\bkyla turner\b|notsoerudite",
        title_kw="erudite",
        kw_desc="`erudite | NotSoErudite | Kyla Turner`",
        kw_note="`erudite` is also an ordinary English adjective, so some false positives are "
                "possible — run `methodology_check.py` to gauge it.",
        outfile="notsoerudite-mentions.md",
        grouped=False,
    ),
}

ROOT = Path(__file__).resolve().parent.parent
TRANSCRIPTS = ROOT / "transcripts"
PADS = [0, 30, 90]
BLEED_PAD = 30
_TIME = re.compile(r"(\d+):(\d{2}):(\d{2})[.,](\d{3})\s*-->\s*(\d+):(\d{2}):(\d{2})[.,](\d{3})")
_TAG = re.compile(r"<[^>]+>")

# set by main() from the chosen subject
MENTION = re.compile(r"\bdestiny\b")
TITLE_KW = "destiny"
LABEL = "Destiny"


def hrs(seconds: float) -> float:
    return seconds / 3600.0


def _secs(h, m, s, ms):
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000.0


def cue_hits(vtt_path: Path):
    """[(start, end)] for caption cues mentioning the subject."""
    try:
        lines = vtt_path.read_text(encoding="utf-8", errors="replace").splitlines()
    except Exception:
        return []
    out, i = [], 0
    while i < len(lines):
        m = _TIME.match(lines[i].strip())
        if not m:
            i += 1
            continue
        start, end = _secs(*m.groups()[:4]), _secs(*m.groups()[4:])
        i += 1
        buf = []
        while i < len(lines) and lines[i].strip():
            buf.append(lines[i])
            i += 1
        if MENTION.search(_TAG.sub(" ", " ".join(buf))):
            out.append((start, end))
    return out


def merged_secs(cues, pad, cap):
    if not cues:
        return 0.0
    iv = sorted((max(0.0, s - pad), e + pad) for s, e in cues)
    merged = [list(iv[0])]
    for a, b in iv[1:]:
        if a <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], b)
        else:
            merged.append([a, b])
    return sum(min(b, cap) - a for a, b in merged if a < cap)


def collect(actors, since=None):
    rows = []
    for ch, name in actors.items():
        tot = dtot = 0.0
        n = dn = cap_n = ts = 0
        dest_pad = {p: 0.0 for p in PADS}
        dest_unt = 0.0
        dates = []
        for f in sorted(glob.glob(str(TRANSCRIPTS / ch / "raw" / "*.info.json"))):
            base = os.path.basename(f)
            if base.startswith("NA-"):
                continue
            if since and not (base[:8].isdigit() and base[:8] >= since):
                continue
            try:
                d = json.load(open(f, encoding="utf-8"))
            except Exception:
                continue
            dur = d.get("duration") or 0
            if not dur:
                continue
            n += 1
            tot += dur
            if base[:8].isdigit():
                dates.append(base[:8])
            title_has = TITLE_KW in (d.get("title") or "").lower()
            is_stream = bool(d.get("was_live"))
            titled = title_has and not is_stream
            if titled:
                dn += 1
                dtot += dur
            elif title_has and is_stream:
                ts += 1
            vtt = Path(f[: -len(".info.json")] + ".en.vtt")
            if vtt.exists():
                cap_n += 1
                cues = cue_hits(vtt)
                for p in PADS:
                    dest_pad[p] += merged_secs(cues, p, dur)
                if not titled:
                    dest_unt += merged_secs(cues, BLEED_PAD, dur)
        span = ""
        if dates:
            dates.sort()
            span = f"{dates[0][:4]}-{dates[0][4:6]} to {dates[-1][:4]}-{dates[-1][4:6]}"
        if n:
            rows.append(dict(name=name, n=n, tot=tot, dn=dn, dtot=dtot, cap_n=cap_n,
                             span=span, dest_pad=dest_pad, dest_unt=dest_unt, ts=ts))
    return rows


def emit_measured(rows, pad):
    print(f"| Actor / channel | # vids (capt.) | airtime | {LABEL}-talk hrs | % of airtime | corpus span |")
    print("|---|---:|---:|---:|---:|---|")
    for r in sorted(rows, key=lambda r: -r["dest_pad"][pad]):
        d = r["dest_pad"][pad]
        pct = (d / r["tot"] * 100) if r["tot"] else 0
        print(f"| {r['name']} | {r['n']} ({r['cap_n']}) | {hrs(r['tot']):.1f} h | "
              f"{hrs(d):.1f} h | {pct:.0f}% | {r['span']} |")
    grand = sum(r["tot"] for r in rows)
    if grand:
        gd = sum(r["dest_pad"][pad] for r in rows)
        print(f"\n**Totals: ~{hrs(gd):.0f} h {LABEL}-talk across {hrs(grand):.0f} h airtime "
              f"({gd / grand * 100:.0f}%).**\n")


def emit_omni(rows):
    print(f"| Actor / channel | # vids (capt.) | # {LABEL}-titled vids | {LABEL}-titled streams (excl.) "
          f"| airtime | {LABEL}-titled hrs | % of hrs | bleed hrs | bleed % | = {LABEL} content | corpus span |")
    print("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|")
    for r in sorted(rows, key=lambda r: -(r["dtot"] + r["dest_unt"])):
        ptit = (r["dtot"] / r["tot"] * 100) if r["tot"] else 0
        pbleed = (r["dest_unt"] / r["tot"] * 100) if r["tot"] else 0
        print(f"| {r['name']} | {r['n']} ({r['cap_n']}) | {r['dn']} | {r['ts']} | "
              f"{hrs(r['tot']):.1f} h | {hrs(r['dtot']):.1f} h | {ptit:.0f}% | "
              f"{hrs(r['dest_unt']):.1f} h | {pbleed:.0f}% | {ptit + pbleed:.0f}% | {r['span']} |")


GROUPED = True   # set in main()


def emit_analysis(adv, cmp):
    """Measured (floor/±30/ceiling) + generous tables for one collected window."""
    allc = adv + cmp
    print(f"### Measured {LABEL}-talk — caption mention-time (conservative)\n")
    print(f"_Pure mention-time across **all** videos, no \"titled = 100%\" assumption; shown floor "
          f"→ ceiling. Sorted by {LABEL}-talk hours._\n")
    print("#### Floor — ±0s (only seconds the name is literally in the caption)\n")
    emit_measured(allc, 0)
    print("#### Middle — ±30s\n")
    emit_measured(allc, 30)
    print("#### Ceiling — ±90s\n")
    emit_measured(allc, 90)
    print(f"### Generous upper bound — {LABEL}-titled videos counted whole\n")
    print(f"_{LABEL}-titled **published video** = 100% {LABEL} content (short curated pieces) + "
          f"measured ±30s bleed in the rest. {LABEL}-titled **livestreams** excluded from the "
          "whole-count and measured instead. The optimistic read._\n")
    if GROUPED and cmp:
        print("#### Adversary channels\n")
        emit_omni(adv)
        print("\n#### Target-side\n")
        emit_omni(cmp)
    else:
        emit_omni(allc)


def main():
    global MENTION, TITLE_KW, LABEL, GROUPED
    ap = argparse.ArgumentParser()
    ap.add_argument("--subject", default="destiny", choices=list(SUBJECTS),
                    help="who/what to measure mentions of")
    ap.add_argument("--since", help="single-window override (videos on/after YYYYMMDD)")
    args = ap.parse_args()
    subj = SUBJECTS[args.subject]
    MENTION = re.compile(subj["mention"], re.I)
    TITLE_KW = subj["title_kw"]
    LABEL = subj["label"]
    GROUPED = subj["grouped"]

    def groups(since):
        if GROUPED:
            return collect(ADVERSARY, since), collect(COMPARISON, since)
        return collect({**ADVERSARY, **COMPARISON}, since), []

    print(f"# Per-channel {LABEL}-talk\n")
    print(f"_Generated {datetime.now():%Y-%m-%d %H:%M} by `scripts/actor_airtime.py --subject "
          f"{args.subject}`. Full `/videos`+`/streams` channel pulls. Keyword set: {subj['kw_desc']}._\n")

    if args.since:
        print(f"## Since {args.since[:4]}-{args.since[4:6]}\n")
        emit_analysis(*groups(args.since))
    else:
        print("## Whole channel\n")
        emit_analysis(*groups(None))
        print("## Lawsuit arc — since 2024-10\n")
        emit_analysis(*groups("20241001"))

    print("## Notes\n")
    print(f"- **Keyword set** — a hit cue matches {subj['kw_desc']}. {subj['kw_note']}")
    print("- **Padding** — each hit cue is extended by ±pad seconds and overlaps merged, to bridge "
          "pronoun stretches. ±0 counts only literal name-seconds (undercount); larger pads estimate "
          "surrounding discussion. **Magnitude scales with pad; ranking does not** "
          "(see `methodology-check.md`).")
    print("- **% of airtime** is the robust comparative figure; absolute hours scale with channel size.")
    print("- **Caveats** — keyword-anchored (can't tell *attacking* from *mentioning*); leans on "
          "caption quality. Ryle is an *outlet* republishing JSTLK + others. Airtime isn't unique "
          "content — clip-reacts replay footage.")
    print(f"\n## Regenerate\n```\npython scripts/actor_airtime.py --subject {args.subject} "
          f"> docs/airtime-analysis/{subj['outfile']}\n```")


if __name__ == "__main__":
    main()
