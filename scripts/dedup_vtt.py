#!/usr/bin/env python3
"""Collapse YouTube rolling auto-caption VTTs into clean, deduped, timestamped VTTs.

YouTube's auto-captions use a rolling window: every caption line appears twice
(once as a "settled" plain line, once as an "in-progress" line carrying inline
<00:00:00.000><c> per-word timestamp tags), and each successive cue repeats the
prior line plus a few new words. Naively read, this is ~2x duplicated text.

This reconstructs the underlying word stream from the inline per-word timestamps
(the highest-fidelity signal), dedups it, and re-emits a clean .vtt with one line
per ~caption, preserving real word-level timing but removing the rolling repeats
and the <c> tag noise.

Usage:
    python dedup_vtt.py IN.vtt [OUT.vtt]        # single file
    python dedup_vtt.py --dir RAWDIR [--suffix .clean.vtt]   # batch a folder
"""
import re
import sys
import glob
import os

TS = r"(\d{2}:\d{2}:\d{2}\.\d{3})"
CUE_RE = re.compile(rf"^{TS} --> {TS}")
# inline per-word timestamp tag: <00:00:01.600>
INLINE_TS = re.compile(r"<(\d{2}:\d{2}:\d{2}\.\d{3})>")
TAG = re.compile(r"</?c[^>]*>")


def ts_to_sec(ts):
    h, m, s = ts.split(":")
    return int(h) * 3600 + int(m) * 60 + float(s)


def sec_to_ts(sec):
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = sec % 60
    return f"{h:02d}:{m:02d}:{s:06.3f}"


def extract_words(text):
    """Yield (word, start_sec) from a caption line using inline <ts> tags.

    A line looks like: `This<00:00:00.160><c> is</c><00:00:00.320><c> from</c>...`
    The first token has no leading timestamp (inherits the cue start); each
    subsequent token is preceded by its own <ts>.
    """
    # Split on inline timestamps, keeping the timestamp that precedes each chunk.
    parts = INLINE_TS.split(text)
    # parts = [lead_text, ts1, chunk1, ts2, chunk2, ...]
    out = []
    lead = TAG.sub("", parts[0]).strip()
    if lead:
        out.append((lead, None))  # timing filled from cue start by caller
    i = 1
    while i + 1 < len(parts) + 1 and i < len(parts):
        ts = parts[i]
        chunk = TAG.sub("", parts[i + 1]) if i + 1 < len(parts) else ""
        chunk = chunk.strip()
        if chunk:
            out.append((chunk, ts_to_sec(ts)))
        i += 2
    return out


def parse(vtt_text):
    """Return an ordered, de-duplicated list of (word, start_sec)."""
    lines = vtt_text.splitlines()
    words = []  # (word, start_sec)
    cue_start = None
    for ln in lines:
        m = CUE_RE.match(ln)
        if m:
            cue_start = ts_to_sec(m.group(1))
            continue
        if "<" in ln and INLINE_TS.search(ln):
            for word, sec in extract_words(ln):
                if sec is None:
                    sec = cue_start
                words.append((word, sec))
    # Dedup: the rolling window re-emits the same (word, timestamp) repeatedly.
    # Key on (rounded timestamp, word) to collapse the repeats while keeping
    # genuine re-reads (same words, different time) distinct.
    seen = set()
    deduped = []
    for word, sec in words:
        key = (round(sec, 2), word)
        if key in seen:
            continue
        seen.add(key)
        deduped.append((word, sec))
    deduped.sort(key=lambda x: x[1])
    return deduped


def rechunk(words, max_gap=1.2, max_chars=60):
    """Group the word stream into caption cues (~one screen line each)."""
    cues = []  # (start, end, text)
    cur = []
    cur_start = None
    last = None
    for word, sec in words:
        if cur_start is None:
            cur_start = sec
        if cur and (sec - last > max_gap or len(" ".join(w for w, _ in cur)) >= max_chars):
            cues.append((cur_start, last, " ".join(w for w, _ in cur)))
            cur = []
            cur_start = sec
        cur.append((word, sec))
        last = sec
    if cur:
        cues.append((cur_start, last, " ".join(w for w, _ in cur)))
    return cues


def to_vtt(cues):
    out = ["WEBVTT", ""]
    for start, end, text in cues:
        out.append(f"{sec_to_ts(start)} --> {sec_to_ts(end)}")
        out.append(text)
        out.append("")
    return "\n".join(out)


def process_file(inp, outp):
    txt = open(inp, encoding="utf-8", errors="replace").read()
    words = parse(txt)
    cues = rechunk(words)
    open(outp, "w", encoding="utf-8").write(to_vtt(cues))
    return len(txt), os.path.getsize(outp), len(words), len(cues)


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(1)
    if args[0] == "--dir":
        rawdir = args[1]
        suffix = ".clean.vtt"
        if "--suffix" in args:
            suffix = args[args.index("--suffix") + 1]
        # only the .en.vtt (skip .en-orig.vtt, byte-identical) and skip existing clean
        files = sorted(
            f for f in glob.glob(os.path.join(rawdir, "*.en.vtt"))
            if not f.endswith(suffix)
        )
        tot_in = tot_out = 0
        for f in files:
            base = f[: -len(".en.vtt")]
            outp = base + suffix
            si, so, nw, nc = process_file(f, outp)
            tot_in += si
            tot_out += so
            print(f"{os.path.basename(f)}: {si:>9,} -> {so:>8,} bytes  ({nw} words, {nc} cues)")
        print(f"\n{len(files)} files. {tot_in:,} -> {tot_out:,} bytes "
              f"({100*(1-tot_out/tot_in):.0f}% smaller)")
    else:
        inp = args[0]
        outp = args[1] if len(args) > 1 else inp.rsplit(".", 2)[0] + ".clean.vtt"
        si, so, nw, nc = process_file(inp, outp)
        print(f"{si:,} -> {so:,} bytes ({nw} words, {nc} cues) -> {outp}")


if __name__ == "__main__":
    main()
