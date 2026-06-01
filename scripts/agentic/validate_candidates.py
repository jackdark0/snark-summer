from __future__ import annotations

import argparse
import glob
import json
import re
import sys
from pathlib import Path
from typing import Any


TACTICS = {
    "Always on Offense",
    "Isolated Demands for Rigor",
    "Schrodinger's Joke",
    "Unilateral Principles",
    "No-Win Framing",
    "Victim Reversal (DARVO)",
    "Moving Goalposts",
    "Permission Structures",
    "Maximize Yours, Minimize Theirs",
    "Fragmentation",
    "Narrative Laundering",
    "Cross-Community Infiltration",
    "Paint Them as Crazy",
}

DUPLICATE_STATUSES = {"new", "possible_duplicate", "duplicate", "secondhand_new_frame"}
REQUIRED_FIELDS = {
    "candidate_id",
    "source_file",
    "channel",
    "title",
    "platform",
    "date",
    "video_id",
    "timestamp",
    "clip_url",
    "tactic",
    "score",
    "score_call",
    "quote",
    "what_happened",
    "why_it_fits",
    "duplicate_check",
}


def expand_inputs(patterns: list[str]) -> list[Path]:
    paths: list[Path] = []
    for pattern in patterns:
        matches = glob.glob(pattern)
        if matches:
            paths.extend(Path(match) for match in matches)
        elif glob.has_magic(pattern):
            continue
        else:
            paths.append(Path(pattern))
    return sorted(dict.fromkeys(paths))


def load_jsonl(path: Path) -> list[tuple[int, dict[str, Any]]]:
    rows: list[tuple[int, dict[str, Any]]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_number}: invalid JSON: {exc}") from exc
        if not isinstance(value, dict):
            raise ValueError(f"{path}:{line_number}: JSONL row must be an object")
        rows.append((line_number, value))
    return rows


def parse_bank(bank_path: Path) -> dict[str, dict[str, str]]:
    if not bank_path.exists():
        return {}
    text = bank_path.read_text(encoding="utf-8", errors="replace")
    blocks = re.finditer(r"(?ms)^### (EX-\d{4}) \| (?P<tactic>.*?)\n(?P<body>.*?)(?=^### EX-|\Z)", text)
    examples: dict[str, dict[str, str]] = {}
    for match in blocks:
        body = match.group("body")
        url_match = re.search(r"\*\*Clip URL:\*\*\s*(\S+)", body)
        timestamp_match = re.search(r"\*\*Timestamp:\*\*\s*([^\n\r]+)", body)
        examples[match.group(1)] = {
            "tactic": match.group("tactic").strip(),
            "clip_url": url_match.group(1) if url_match else "",
            "timestamp": timestamp_match.group(1).strip() if timestamp_match else "",
            "retired": "RETIRED" if "RETIRED" in body else "",
        }
    return examples


def video_id_from_url(url: str) -> str:
    for pattern in [r"youtu\.be/([^?&/]+)", r"(?:watch\?v=|live/)([^?&/]+)"]:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return ""


def seconds_from_url(url: str) -> int | None:
    match = re.search(r"[?&]t=(\d+)", url)
    return int(match.group(1)) if match else None


def validate_row(row: dict[str, Any], bank: dict[str, dict[str, str]]) -> list[str]:
    errors: list[str] = []
    missing = sorted(REQUIRED_FIELDS - set(row))
    if missing:
        errors.append(f"missing required fields: {', '.join(missing)}")

    candidate_id = str(row.get("candidate_id", ""))
    if not re.fullmatch(r"cand-[A-Za-z0-9._-]+", candidate_id):
        errors.append("candidate_id must look like cand-source-date-0001")

    tactic = row.get("tactic")
    if tactic not in TACTICS:
        errors.append(f"unknown tactic: {tactic!r}")

    score = row.get("score")
    if not isinstance(score, int) or not 1 <= score <= 5:
        errors.append("score must be an integer from 1 to 5")

    date = str(row.get("date", ""))
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}|UNKNOWN", date):
        errors.append("date must be YYYY-MM-DD or UNKNOWN")

    timestamp = str(row.get("timestamp", ""))
    if not re.fullmatch(r"(?:\d{1,2}:)?\d{1,2}:\d{2}(?:\.\d{1,3})?|UNKNOWN", timestamp):
        errors.append("timestamp must be HH:MM:SS, M:SS, or UNKNOWN")

    clip_url = str(row.get("clip_url", ""))
    if clip_url != "PENDING" and not video_id_from_url(clip_url):
        errors.append("clip_url must be a YouTube URL with a video id or PENDING")

    duplicate_check = row.get("duplicate_check")
    if not isinstance(duplicate_check, dict):
        errors.append("duplicate_check must be an object")
    else:
        status = duplicate_check.get("status")
        if status not in DUPLICATE_STATUSES:
            errors.append(f"duplicate_check.status must be one of {sorted(DUPLICATE_STATUSES)}")
        related = duplicate_check.get("related_examples")
        if not isinstance(related, list):
            errors.append("duplicate_check.related_examples must be a list")
        else:
            for ex_id in related:
                if not isinstance(ex_id, str) or not re.fullmatch(r"EX-\d{4}", ex_id):
                    errors.append(f"invalid related example id: {ex_id!r}")
                elif ex_id not in bank:
                    errors.append(f"related example not found in bank: {ex_id}")

    if clip_url != "PENDING":
        cand_video = video_id_from_url(clip_url)
        cand_seconds = seconds_from_url(clip_url)
        for ex_id, existing in bank.items():
            if existing.get("retired"):
                continue
            existing_url = existing.get("clip_url", "")
            if not existing_url:
                continue
            if video_id_from_url(existing_url) != cand_video:
                continue
            existing_seconds = seconds_from_url(existing_url)
            if existing_seconds is None or cand_seconds is None:
                continue
            if abs(existing_seconds - cand_seconds) <= 120 and duplicate_check:
                status = duplicate_check.get("status")
                related = duplicate_check.get("related_examples") or []
                if status == "new" and ex_id not in related:
                    errors.append(
                        f"candidate is within 120s of {ex_id}; mark possible_duplicate, duplicate, "
                        "or explain as secondhand_new_frame"
                    )
                break

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate agent candidate JSONL files.")
    parser.add_argument("paths", nargs="+", help="Candidate JSONL files or glob patterns.")
    parser.add_argument("--bank", default="docs/tactic-example-bank.md", help="Example bank path.")
    args = parser.parse_args()

    bank = parse_bank(Path(args.bank))
    paths = expand_inputs(args.paths)
    errors: list[str] = []
    seen_ids: set[str] = set()
    count = 0

    for path in paths:
        if not path.exists():
            errors.append(f"{path}: file not found")
            continue
        try:
            rows = load_jsonl(path)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        for line_number, row in rows:
            count += 1
            candidate_id = str(row.get("candidate_id", ""))
            if candidate_id in seen_ids:
                errors.append(f"{path}:{line_number}: duplicate candidate_id {candidate_id}")
            seen_ids.add(candidate_id)
            for error in validate_row(row, bank):
                errors.append(f"{path}:{line_number}: {candidate_id or '<missing id>'}: {error}")

    if errors:
        print(f"validated {count} candidate(s); {len(errors)} error(s)", file=sys.stderr)
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"validated {count} candidate(s); no errors")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
