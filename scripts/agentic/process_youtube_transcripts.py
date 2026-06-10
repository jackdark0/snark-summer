from __future__ import annotations

import argparse
import csv
import html
import json
import re
from dataclasses import dataclass
from pathlib import Path


TIMING_RE = re.compile(
    r"^(?P<sh>\d{2}):(?P<sm>\d{2}):(?P<ss>\d{2}\.\d{3})\s+-->\s+"
    r"(?P<eh>\d{2}):(?P<em>\d{2}):(?P<es>\d{2}\.\d{3})"
)
INLINE_TS_RE = re.compile(r"<\d{2}:\d{2}:\d{2}\.\d{3}>")
TAG_RE = re.compile(r"<[^>]+>")


@dataclass
class Cue:
    start: float
    text: str


def seconds(parts: tuple[str, str, str]) -> float:
    hours, minutes, seconds_text = parts
    return int(hours) * 3600 + int(minutes) * 60 + float(seconds_text)


def stamp(value: float) -> str:
    total = int(value)
    hours, remainder = divmod(total, 3600)
    minutes, seconds_value = divmod(remainder, 60)
    if hours:
        return f"{hours}:{minutes:02d}:{seconds_value:02d}"
    return f"{minutes}:{seconds_value:02d}"


def clean_text(value: str) -> str:
    value = INLINE_TS_RE.sub("", value)
    value = TAG_RE.sub("", value)
    value = html.unescape(value).replace("\xa0", " ")
    return re.sub(r"\s+", " ", value).strip()


def parse_vtt(path: Path) -> list[Cue]:
    cues: list[Cue] = []
    start: float | None = None
    text_lines: list[str] = []

    def flush() -> None:
        nonlocal start, text_lines
        if start is None:
            text_lines = []
            return
        text = clean_text(" ".join(text_lines))
        if text:
            cues.append(Cue(start=start, text=text))
        start = None
        text_lines = []

    for raw_line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw_line.strip()
        if not line or line == "WEBVTT" or line.startswith("Kind:") or line.startswith("Language:"):
            flush()
            continue
        match = TIMING_RE.match(line)
        if match:
            flush()
            start = seconds((match.group("sh"), match.group("sm"), match.group("ss")))
            continue
        if start is not None:
            text_lines.append(line)
    flush()
    return cues


def matching_info(vtt_path: Path) -> Path | None:
    prefix = vtt_path.name.removesuffix(".en.vtt")
    candidate = vtt_path.with_name(prefix + ".info.json")
    if candidate.exists():
        return candidate
    return None


def load_info(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8", errors="replace"))


def safe_date(info: dict[str, object], fallback: str) -> str:
    upload_date = str(info.get("upload_date") or fallback[:8])
    if re.fullmatch(r"\d{8}", upload_date):
        return f"{upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:8]}"
    return upload_date


def build_processed_text(info: dict[str, object], cues: list[Cue], source_url: str) -> str:
    upload_date = str(info.get("upload_date") or "UNKNOWN")
    date_text = safe_date(info, upload_date)
    title = str(info.get("title") or "Untitled")
    channel = str(info.get("channel") or info.get("uploader") or "Unknown channel")
    video_id = str(info.get("id") or "")
    lines = [
        f"{date_text} - {title}",
        f"channel: {channel}",
        f"video_id: {video_id}",
        f"source_url: {source_url}",
        "Raw source: YouTube caption; processed for analysis",
        "",
    ]
    previous = ""
    for cue in cues:
        if cue.text == previous:
            continue
        lines.append(f"[{stamp(cue.start)}] {cue.text}")
        previous = cue.text
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert downloaded YouTube VTT captions to processed transcript files.")
    parser.add_argument("--raw-dir", required=True)
    parser.add_argument("--processed-dir", required=True)
    parser.add_argument("--inventory", required=True)
    args = parser.parse_args()

    raw_dir = Path(args.raw_dir)
    processed_dir = Path(args.processed_dir)
    processed_dir.mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, str]] = []
    for vtt_path in sorted(raw_dir.glob("*.en.vtt")):
        info_path = matching_info(vtt_path)
        if info_path is None:
            continue
        info = load_info(info_path)
        cues = parse_vtt(vtt_path)
        if not cues:
            continue
        upload_date = str(info.get("upload_date") or vtt_path.name[:8])
        video_id = str(info.get("id") or vtt_path.stem.split("-")[-1])
        source_url = f"https://youtu.be/{video_id}"
        processed_path = processed_dir / f"{upload_date}-{video_id}.txt"
        processed_path.write_text(build_processed_text(info, cues, source_url), encoding="utf-8")
        rows.append(
            {
                "upload_date": upload_date,
                "date": safe_date(info, upload_date),
                "video_id": video_id,
                "channel": str(info.get("channel") or info.get("uploader") or "Unknown channel"),
                "title": str(info.get("title") or "Untitled"),
                "source_url": source_url,
                "raw_vtt_path": vtt_path.as_posix(),
                "info_json_path": info_path.as_posix(),
                "processed_path": processed_path.as_posix(),
                "cue_count": str(len(cues)),
            }
        )

    inventory_path = Path(args.inventory)
    inventory_path.parent.mkdir(parents=True, exist_ok=True)
    with inventory_path.open("w", encoding="utf-8", newline="") as handle:
        fieldnames = [
            "upload_date",
            "date",
            "video_id",
            "channel",
            "title",
            "source_url",
            "raw_vtt_path",
            "info_json_path",
            "processed_path",
            "cue_count",
        ]
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    print(f"processed {len(rows)} transcript(s)")
    print(f"wrote {inventory_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
