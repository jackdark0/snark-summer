from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


DEFAULT_WINGET_FFPROBE = Path(
    r"C:\Users\User\AppData\Local\Microsoft\WinGet\Packages"
    r"\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe"
    r"\ffmpeg-8.1.1-full_build\bin\ffprobe.exe"
)


def find_ffprobe(explicit: str | None) -> str:
    if explicit:
        return explicit
    path = shutil.which("ffprobe")
    if path:
        return path
    if DEFAULT_WINGET_FFPROBE.exists():
        return str(DEFAULT_WINGET_FFPROBE)
    raise SystemExit("ffprobe not found; pass --ffprobe")


def probe(ffprobe: str, path: Path) -> dict[str, float | int | str]:
    raw = subprocess.check_output(
        [
            ffprobe,
            "-v",
            "error",
            "-select_streams",
            "v:0",
            "-show_entries",
            "stream=width,height",
            "-show_entries",
            "format=duration",
            "-of",
            "json",
            str(path),
        ],
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    payload = json.loads(raw)
    stream = payload["streams"][0]
    return {
        "path": str(path),
        "width": int(stream["width"]),
        "height": int(stream["height"]),
        "duration": round(float(payload["format"]["duration"]), 3),
        "size_mb": round(path.stat().st_size / (1024 * 1024), 2),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate local clip quality.")
    parser.add_argument("--clips-dir", default="clips")
    parser.add_argument("--ffprobe")
    parser.add_argument("--min-height", type=int, default=720)
    parser.add_argument("--json", action="store_true", help="Print JSON inventory.")
    args = parser.parse_args()

    ffprobe = find_ffprobe(args.ffprobe)
    paths = sorted(Path(args.clips_dir).rglob("EX-*.mp4"))
    rows = [probe(ffprobe, path) for path in paths]
    failures = [row for row in rows if int(row["height"]) < args.min_height]

    if args.json:
        print(json.dumps(rows, indent=2))
    else:
        for row in rows:
            print(
                f"{row['path']}: {row['width']}x{row['height']} "
                f"{row['duration']}s {row['size_mb']}MB"
            )
        print(f"TOTAL={len(rows)} BELOW_MIN_HEIGHT={len(failures)} MIN_HEIGHT={args.min_height}")

    if failures:
        for row in failures:
            print(f"ERROR: below minimum height: {row['path']} ({row['height']})", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
