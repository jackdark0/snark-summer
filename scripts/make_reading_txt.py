#!/usr/bin/env python3
"""Regenerate clean reading-format .txt transcripts from the deduped VTT word stream.

Uses dedup_vtt.parse() to get the de-duplicated (word, start_sec) stream, chunks it
into ~12-second paragraphs, and writes the project's canonical reading format
(BOM + CRLF, header block, `[m:ss]`/`[h:mm:ss]` timestamps) so the whole set is
consistent regardless of which earlier processing pass a file came from.

Usage: python make_reading_txt.py --dir transcripts/ryle-kittenhouse
"""
import os
import sys
import json
import glob

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dedup_vtt import parse  # noqa: E402

CHUNK_SEC = 12


def stamp(sec):
    sec = int(sec)
    h, m, s = sec // 3600, (sec % 3600) // 60, sec % 60
    return f"[{h}:{m:02d}:{s:02d}]" if h else f"[{m}:{s:02d}]"


def chunk_paragraphs(words):
    paras = []  # (start_sec, text)
    cur, cur_start = [], None
    for word, sec in words:
        if cur_start is None:
            cur_start = sec
        if cur and int(sec // CHUNK_SEC) != int(cur_start // CHUNK_SEC):
            paras.append((cur_start, " ".join(cur)))
            cur, cur_start = [], sec
        cur.append(word)
    if cur:
        paras.append((cur_start, " ".join(cur)))
    return paras


def build(vid_dir, vid):
    vtt = os.path.join(vid_dir, "raw", vid + ".en.vtt")
    info = os.path.join(vid_dir, "raw", vid + ".info.json")
    words = parse(open(vtt, encoding="utf-8", errors="replace").read())
    if not words:
        return None
    meta = json.load(open(info, encoding="utf-8")) if os.path.exists(info) else {}
    title = meta.get("fulltitle") or meta.get("title") or ""
    ud = meta.get("upload_date") or ""
    date = f"{ud[:4]}-{ud[4:6]}-{ud[6:8]}" if len(ud) == 8 else vid.split("-")[0]
    ytid = meta.get("id") or vid.split("-", 1)[-1]
    lines = [
        f"﻿{date} — {title}",
        f"video_id: {ytid}",
        f"source_url: https://youtu.be/{ytid}",
        "Raw source: YouTube auto-caption; processed for analysis (deduped)",
        "",
    ]
    for start, text in chunk_paragraphs(words):
        lines.append(f"{stamp(start)} {text}")
    out = os.path.join(vid_dir, "processed", vid + ".txt")
    open(out, "w", encoding="utf-8", newline="\r\n").write("\n".join(lines) + "\n")
    return out, len(words)


def main():
    vid_dir = sys.argv[sys.argv.index("--dir") + 1]
    vtts = sorted(glob.glob(os.path.join(vid_dir, "raw", "*.en.vtt")))
    n = 0
    for f in vtts:
        vid = os.path.basename(f)[: -len(".en.vtt")]
        r = build(vid_dir, vid)
        if r:
            n += 1
    print(f"regenerated {n} reading .txt in {vid_dir}/processed/")


if __name__ == "__main__":
    main()
