#!/usr/bin/env python3
"""Methodology stress-tests for the Destiny-talk estimate.

1. Padding sensitivity — measured Destiny-talk % at several ±pad values.
2. Segment stats — mention-burst counts & lengths (scattered vs sustained).
3. Keyword attribution — share of hits from literal "destiny" vs aliases only
   (steven/bonnell/dessie/DGG), i.e. false-positive exposure.
4. Writes docs/non-titled-destiny-hits.md — every NON-Destiny-titled video with
   a hit, for manual review.

Caption timings; keyword-anchored. Run: python scripts/methodology_check.py
"""
from __future__ import annotations
import glob, json, os, re, sys
from pathlib import Path
from statistics import mean, median

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
TRANSCRIPTS = ROOT / "transcripts"
CHANNELS = {
    "kuihman-live": "Kuihman", "mrow-live": "MrowLive",
    "ryle-kittenhouse": "Ryle/JSTLK", "purple-parry-gaming": "Purple Parry",
    "liquid-sonic": "Liquid Sonic", "aiden-underground": "Aiden",
    "whick-tv": "Whick (target)", "notsoerudite": "NotSoErudite (target)",
}
DESTINY = re.compile(r"\bdestiny\b|\bdgg\b|\bsteven bonn?ell\b", re.I)
DEST_LIT = re.compile(r"\bdestiny\b", re.I)
PADS = [0, 10, 20, 30, 45, 60, 90]
TIME = re.compile(r"(\d+):(\d{2}):(\d{2})[.,](\d{3})\s*-->\s*(\d+):(\d{2}):(\d{2})[.,](\d{3})")
TAG = re.compile(r"<[^>]+>")


def secs(h, m, s, ms):
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000.0


def hit_cues(path):
    """[(start, end, has_literal_destiny)] for cues mentioning Destiny."""
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except Exception:
        return []
    out, i = [], 0
    while i < len(lines):
        m = TIME.match(lines[i].strip())
        if not m:
            i += 1
            continue
        st, en = secs(*m.groups()[:4]), secs(*m.groups()[4:])
        i += 1
        buf = []
        while i < len(lines) and lines[i].strip():
            buf.append(lines[i]); i += 1
        body = TAG.sub(" ", " ".join(buf))
        if DESTINY.search(body):
            out.append((st, en, bool(DEST_LIT.search(body))))
    return out


def merge(cues, pad, cap):
    if not cues:
        return []
    iv = sorted((max(0.0, s - pad), e + pad) for s, e, _ in cues)
    m = [list(iv[0])]
    for a, b in iv[1:]:
        if a <= m[-1][1]:
            m[-1][1] = max(m[-1][1], b)
        else:
            m.append([a, b])
    return [(a, min(b, cap)) for a, b in m if a < cap]


def videos(ch):
    for f in sorted(glob.glob(str(TRANSCRIPTS / ch / "raw" / "*.info.json"))):
        b = os.path.basename(f)
        if b.startswith("NA-"):
            continue
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        dur = d.get("duration") or 0
        if not dur:
            continue
        vid = b[9:-len(".info.json")] if b[:8].isdigit() else b[:-len(".info.json")]
        yield dict(date=b[:8], vid=vid, dur=dur, title=d.get("title") or "",
                   vtt=Path(f[:-len(".info.json")] + ".en.vtt"))


def hh(s):
    return f"{s/3600:.1f}"


def main():
    # gather hit_cues once per video
    data = {}  # ch -> list of dicts(meta + cues + titled)
    for ch in CHANNELS:
        rows = []
        for v in videos(ch):
            cues = hit_cues(v["vtt"]) if v["vtt"].exists() else []
            v["cues"] = cues
            v["titled"] = "destiny" in v["title"].lower()
            rows.append(v)
        data[ch] = rows

    # 1. PADDING SENSITIVITY
    print("# Methodology checks\n")
    print("## 1. Padding sensitivity (measured Destiny-talk % of airtime)\n")
    print("| Channel | " + " | ".join(f"±{p}s" for p in PADS) + " |")
    print("|---|" + "---:|" * len(PADS))
    tot_air_all = 0.0
    pad_tot_all = {p: 0.0 for p in PADS}
    for ch, label in CHANNELS.items():
        air = sum(v["dur"] for v in data[ch])
        if not air:
            continue
        tot_air_all += air
        cells = []
        for p in PADS:
            t = sum(sum(b - a for a, b in merge(v["cues"], p, v["dur"])) for v in data[ch])
            pad_tot_all[p] += t
            cells.append(f"{t/air*100:.0f}%")
        print(f"| {label} | " + " | ".join(cells) + " |")
    print(f"| **ALL** | " + " | ".join(f"**{pad_tot_all[p]/tot_air_all*100:.0f}%**" for p in PADS) + " |")
    print("\n_±0s = only the seconds his name is literally in the caption (hard floor); larger pads "
          "estimate surrounding discussion. If the ranking holds across pads, padding isn't driving it._\n")

    # 2. SEGMENT STATS (burst pattern)
    print("## 2. Mention pattern — bursts vs sustained\n")
    print("| Channel | raw hit-cues | bursts (±0s) | avg burst len | segments (±45s) | avg seg len (±45s) |")
    print("|---|---:|---:|---:|---:|---:|")
    for ch, label in CHANNELS.items():
        allcues = [c for v in data[ch] for c in v["cues"]]
        if not allcues:
            continue
        bursts = [b - a for v in data[ch] for a, b in merge(v["cues"], 0, v["dur"])]
        segs45 = [b - a for v in data[ch] for a, b in merge(v["cues"], 45, v["dur"])]
        print(f"| {label} | {len(allcues)} | {len(bursts)} | {mean(bursts):.0f}s | "
              f"{len(segs45)} | {mean(segs45):.0f}s |")
    print("\n_'burst (±0s)' = a cluster of name-mentions with no padding (rolling-caption dupes merge). "
          "Short avg burst = passing name-drops; long = he's named repeatedly in a stretch._\n")

    # 3. KEYWORD ATTRIBUTION
    print("## 3. Keyword attribution (false-positive exposure)\n")
    print("| Channel | hit-cues | w/ literal \"destiny\" | alias-only |")
    print("|---|---:|---:|---:|")
    for ch, label in CHANNELS.items():
        cues = [c for v in data[ch] for c in v["cues"]]
        if not cues:
            continue
        lit = sum(1 for _, _, d in cues if d)
        print(f"| {label} | {len(cues)} | {lit} ({lit/len(cues)*100:.0f}%) | "
              f"{len(cues)-lit} ({(len(cues)-lit)/len(cues)*100:.0f}%) |")
    print("\n_'alias-only' = cue matched via steven/bonnell/dessie/DGG but NOT the literal word "
          "\"destiny\" — the main false-positive risk (esp. unrelated \"Steven\"s)._\n")

    # 4. NON-TITLED HITS LIST -> file
    out = ROOT / "docs" / "airtime-analysis" / "non-titled-destiny-hits.md"
    lines = ["# Non-Destiny-titled videos with Destiny mentions (for manual review)\n",
             "_Videos NOT titled about Destiny but with caption hits (±45s merged). Sorted by "
             "Destiny-minutes desc. Review whether the hits are real Destiny discussion or false "
             "positives (e.g. an unrelated \"Steven\")._\n",
             "| Channel | Date | Destiny-min | bursts | lit/alias | Title | URL |",
             "|---|---|---:|---:|---|---|---|"]
    review = []
    for ch, label in CHANNELS.items():
        for v in data[ch]:
            if v["titled"] or not v["cues"]:
                continue
            mins = sum(b - a for a, b in merge(v["cues"], 45, v["dur"])) / 60.0
            bursts = len(merge(v["cues"], 0, v["dur"]))
            lit = sum(1 for _, _, d in v["cues"] if d)
            review.append((mins, label, v["date"], bursts, lit, len(v["cues"]) - lit,
                           v["title"], v["vid"]))
    review.sort(reverse=True)
    for mins, label, date, bursts, lit, ali, title, vid in review:
        d = f"{date[:4]}-{date[4:6]}-{date[6:8]}" if date.isdigit() else date
        t = title.replace("|", "\\|")[:60]
        lines.append(f"| {label} | {d} | {mins:.1f} | {bursts} | {lit}/{ali} | {t} | "
                     f"https://youtu.be/{vid} |")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"## 4. Non-titled hits\n\nWrote **{len(review)}** non-titled videos-with-hits to "
          f"`non-titled-destiny-hits.md` for manual review.\n")


if __name__ == "__main__":
    main()
