"""Cheap pre-diarization screen: is this a conversation or a watch-along?

Diarization costs ~40-65 min of GPU per long stream and is worthless on react
content, because played VOD audio gets speaker labels indistinguishable from
live participants. This screens the auto-captions in seconds instead.

Scores each video on reaction markers vs live-conversation markers, and reports
whether a named actor is addressed in the second person (real evidence of
presence) or only referred to in the third person (evidence of absence).

Usage: python presence_screen.py <channel-slug> [actor ...]
"""
import glob
import json
import os
import re
import sys

PROJ = r"C:\Users\User\Documents\research-memes\dgg\snark-summer"
sys.path.insert(0, os.path.join(PROJ, "scripts"))
from dedup_vtt import parse  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# Corpus never spells these correctly; match what the transcribers actually emit.
ACTOR_VARIANTS = {
    "kuihman": r"queenman|queeman|queman|kuihman|queen man",
    "jstlk": r"jay ?stock|jay ?stalk|jtock|jstlk|justical",
    "chudlogic": r"chud ?logic",
    "destiny": r"\bdestiny\b",
    "dan": r"\bdgg dan\b|\bdan\b",
    "dickers": r"\bdickers\b",
}

REACTION = [
    r"what are they debating", r"we were watching", r"are you watching",
    r"let'?s (?:pull|watch|see) (?:this|that|it) up", r"play the clip",
    r"the full thing is up", r"his vod", r"her vod", r"vods instead",
    r"react(?:ing)? to (?:this|his|her|the)", r"let me pull (?:this|that|it) up",
    r"what part were we", r"remind me of what",
]
PRESENCE = [
    r"can you hear me", r"i'?m letting you in", r"you'?re unmuted", r"unmute",
    r"thanks for (?:coming on|joining)", r"welcome to the (?:stream|stage|show)",
    r"opening statement", r"your turn", r"let (?:him|her|them) (?:speak|finish)",
    r"stop talking over", r"go ahead,? (?:you|and)",
]

# Second-person address is the strongest presence evidence for a specific actor.
def addressed(text, variants):
    pat = r"(?:%s)[,]?\s+(?:you|do you|can you|are you|would you|did you|why do you|what do you)\b" % variants
    a = len(re.findall(pat, text, re.I))
    pat2 = r"\b(?:you|you're|your)\b[^.?!]{0,40}\b(?:%s)\b" % variants
    return a


def main():
    slug = sys.argv[1] if len(sys.argv) > 1 else "stardust-irl"
    actors = sys.argv[2:] or ["kuihman", "jstlk", "chudlogic"]
    raw = os.path.join(PROJ, "transcripts", slug, "raw")

    rows = []
    for vtt in sorted(glob.glob(os.path.join(raw, "*.en.vtt"))):
        stem = os.path.basename(vtt)[: -len(".en.vtt")]
        info = os.path.join(raw, stem + ".info.json")
        title, dur = "", 0
        if os.path.exists(info):
            d = json.load(open(info, encoding="utf-8"))
            title, dur = d.get("title") or "", d.get("duration") or 0
        w = parse(open(vtt, encoding="utf-8", errors="replace").read())
        text = " ".join(x[0] for x in w)
        low = text.lower()
        rct = sum(len(re.findall(p, low)) for p in REACTION)
        prs = sum(len(re.findall(p, low)) for p in PRESENCE)
        per_actor = {}
        for a in actors:
            v = ACTOR_VARIANTS.get(a, a)
            mentions = len(re.findall(v, low))
            addr = addressed(text, v)
            per_actor[a] = (mentions, addr)
        rows.append((stem, title, dur, rct, prs, per_actor))

    rows.sort(key=lambda r: (r[3] - r[4]))
    print("%-22s %-5s %-5s %-6s %s" % ("video", "react", "live", "verdict", "actors (mentions/2nd-person)"))
    print("-" * 118)
    for stem, title, dur, rct, prs, pa in rows:
        if rct == 0 and prs >= 2:
            verdict = "CONV"
        elif rct >= 3 and prs <= rct:
            verdict = "REACT"
        else:
            verdict = "mixed"
        acts = "  ".join("%s=%d/%d" % (a, m, ad) for a, (m, ad) in pa.items())
        print("%-22s %-5d %-5d %-6s %s" % (stem[:22], rct, prs, verdict, acts))
        print("%24s%s" % ("", title[:88]))
    print()
    print("CONV  = candidate for diarization.  REACT = do not diarize, played audio is unattributable.")
    print()
    print("Read the verdict as a hint and the 2nd-person column as the evidence, then spot-check.")
    print("Known limits, both observed on this corpus 2026-07-25:")
    print("  - The react/live composite misfires on hybrids. xSqfq8VXx3U scores REACT but is a")
    print("    genuine conversation (it produced EX-0107..0109); it just has react segments too.")
    print("  - 2nd-person address is necessary but NOT sufficient. If the played video is itself")
    print("    a debate, the recording contains people addressing your actor directly. PKP6bGriRTI")
    print("    shows 'Queenman, you're lost' -- spoken inside the VOD, not by the host.")
    print("  So: high mentions + 0 address means absent, reliably. Non-zero address means read the")
    print("  opening two minutes before committing GPU time.")


if __name__ == "__main__":
    main()
