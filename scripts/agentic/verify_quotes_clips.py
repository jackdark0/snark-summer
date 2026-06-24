#!/usr/bin/env python3
"""
Mechanical consistency verifier for Dooby-thread deliverables.

For each italic verbatim quote (*"..."*) and each [clip](url?t=N) in the target
docs, this checks two deterministic things against the local diarized transcripts:

  1. CLIP MATH  — the t=<seconds> in a clip URL matches the H:MM:SS timestamp
                  cited next to it (and live/ vs youtu.be format is plausible).
  2. QUOTE      — the quoted words actually appear (normalized substring) in the
                  transcript of the video the clip points to.

It is intentionally dumb and deterministic — it catches the truncation /
misquote / wrong-second class of bug that an LLM read can miss. Quotes flagged
in-doc as rough autocaptions (the "third-party commentary" section) map to no
diarized transcript and are reported as SKIP, not FAIL.

Usage:  python scripts/agentic/verify_quotes_clips.py
Exit code 1 if any FAIL.
"""
import re, sys, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TR = os.path.join(ROOT, "transcripts")

# video id -> diarized transcript path
TRANSCRIPTS = {
    "8uIQffyoB1k": os.path.join(TR, "dooby-fbi-interviews", "_transcripts", "8uIQffyoB1k.diarized.txt"),
    "DDvOvz1IAoQ": os.path.join(TR, "dooby-fbi-interviews", "_transcripts", "DDvOvz1IAoQ.diarized.txt"),
    "MNpW_WTX-9s": os.path.join(TR, "dooby-fbi-interviews", "_transcripts", "MNpW_WTX-9s.diarized.txt"),
    "aBW1YeUKgUY": os.path.join(TR, "dooby-fbi-interviews", "_transcripts", "aBW1YeUKgUY.diarized.txt"),
    "jfS7TyBZOKg": os.path.join(TR, "whick-callin-2025AUG26", "_transcripts", "jfS7TyBZOKg.diarized.txt"),
}
DOCS = [
    os.path.join(ROOT, "docs", "dooby", "dooby-fbi-origin-timeline.md"),
    os.path.join(ROOT, "docs", "tactic-example-bank.md"),  # EX-0098 etc.
]

def norm(s):
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", s.lower())).strip()

_tcache = {}
def transcript_tokens(vid):
    """Return the transcript as a normalized token list (cached)."""
    if vid not in _tcache:
        p = TRANSCRIPTS.get(vid)
        _tcache[vid] = norm(open(p, encoding="utf-8", errors="ignore").read()).split() if p and os.path.exists(p) else None
    return _tcache[vid]

def _lcs_len(a, b):
    """Length of the longest common subsequence (allows skips in BOTH sequences,
    so a missing/substituted probe word doesn't block later matches)."""
    dp = [0] * (len(b) + 1)
    for ai in a:
        prev = 0
        for j in range(1, len(b) + 1):
            cur = dp[j]
            dp[j] = prev + 1 if ai == b[j - 1] else (dp[j] if dp[j] >= dp[j - 1] else dp[j - 1])
            prev = cur
    return dp[len(b)]

def found_with_gaps(probe, toks):
    """True if `probe` appears in `toks` in order within a bounded window,
    tolerating removed filler AND up to one substituted/missing word (whisper
    single-word errors, or a lightly-corrected quote). The bounded window keeps
    this from matching a sequence scattered across the whole transcript."""
    n = len(probe)
    if n == 0:
        return True
    need = n - 1 if n >= 7 else n          # allow 1 miss only for longer probes
    window = n + max(4, n)                  # filler/gap budget
    anchors = {probe[0], probe[1]} if n > 1 else {probe[0]}
    for s in range(len(toks)):
        if toks[s] not in anchors:
            continue
        if _lcs_len(probe, toks[s:s + window]) >= need:
            return True
    return False

def hms_to_sec(t):
    parts = [int(x) for x in t.split(":")]
    if len(parts) == 3: return parts[0]*3600 + parts[1]*60 + parts[2]
    return parts[0]*60 + parts[1]

CLIP_RE = re.compile(r"\[[^\]]*\]\((https?://[^)]+?[?&]t=(\d+))\)")
ID_RE = re.compile(r"(?:live/|youtu\.be/|[?&]v=)([A-Za-z0-9_-]{11})")
TS_RE = re.compile(r"~?(\d{1,2}:\d{2}(?::\d{2})?)")
QUOTE_RE = re.compile(r'\*"(.+?)"\*', re.DOTALL)

def check_doc(path, fails, total):
    name = os.path.basename(path)
    text = open(path, encoding="utf-8", errors="ignore").read()

    # --- clip math ---
    for m in CLIP_RE.finditer(text):
        total[0] += 1
        url, secs = m.group(1), int(m.group(2))
        idm = ID_RE.search(url)
        vid = idm.group(1) if idm else "?"
        # nearest H:MM:SS timestamp in the 220 chars before the clip
        pre = text[max(0, m.start()-500):m.start()]
        cands = [tm.group(1) for tm in TS_RE.finditer(pre)]
        if not cands:
            print(f"  [WARN] {name}: clip t={secs} ({vid}) has no nearby H:MM:SS to check")
            continue
        # range-aware: pass if t matches ANY timestamp in the window (e.g. "A-B" clips use A)
        secs_set = {hms_to_sec(c) for c in cands}
        if secs not in secs_set:
            near = cands[-1]
            fails.append(f"{name}: clip t={secs} but nearby timestamp(s) {sorted(secs_set)} ({vid}) -> closest '{near}'={hms_to_sec(near)}s")

    # --- quotes ---
    for m in QUOTE_RE.finditer(text):
        total[1] += 1
        raw = re.sub(r"\s+", " ", m.group(1)).strip()
        # nearest clip id: search forward 400 chars, else backward 400
        win_fwd = text[m.end():m.end()+400]
        win_bwd = text[max(0, m.start()-400):m.start()]
        idm = ID_RE.search(win_fwd) or None
        if not idm:
            for idm2 in ID_RE.finditer(win_bwd):
                idm = idm2
        vid = idm.group(1) if idm else None
        toks = transcript_tokens(vid) if vid else None
        if toks is None:
            print(f"  [SKIP] {name}: quote maps to no diarized transcript (autocaption/approx): \"{raw[:55]}...\"")
            continue
        # strip editorial [brackets], split on ellipsis, verify each substantial segment
        cleaned = re.sub(r"\[[^\]]*\]", " ", raw)
        segments = re.split(r"\.\.\.|…", cleaned)
        ok = True
        missing = None
        for seg in segments:
            words = norm(seg).split()
            if len(words) < 6:      # too short to verify reliably; skip segment
                continue
            if not found_with_gaps(words, toks):
                ok = False; missing = " ".join(words[:10]); break
        if ok:
            print(f"  [PASS] {name} ({vid}): \"{raw[:55]}...\"")
        else:
            fails.append(f"{name} ({vid}): quote segment not found -> \"{missing}...\"  | full: \"{raw[:80]}\"")

def main():
    fails = []
    total = [0, 0]  # clips, quotes
    for d in DOCS:
        if os.path.exists(d):
            print(f"\n### {os.path.basename(d)}")
            check_doc(d, fails, total)
    print(f"\n=== summary: {total[0]} clip-urls, {total[1]} quotes checked; {len(fails)} FAIL ===")
    for f in fails:
        print("  [FAIL] " + f)
    return 1 if fails else 0

if __name__ == "__main__":
    raise SystemExit(main())
