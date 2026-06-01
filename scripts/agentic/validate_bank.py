from __future__ import annotations

import argparse
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def parse_bank(path: Path) -> dict[str, dict[str, str]]:
    text = read_text(path)
    examples: dict[str, dict[str, str]] = {}
    for match in re.finditer(r"(?ms)^### (EX-\d{4}) \| (?P<tactic>.*?)\n(?P<body>.*?)(?=^### EX-|\Z)", text):
        ex_id = match.group(1)
        body = match.group("body")
        examples[ex_id] = {
            "tactic": match.group("tactic").strip(),
            "retired": "yes" if "RETIRED" in body else "",
            "status": field(body, "Status"),
            "clip_url": field(body, "Clip URL"),
            "source": field(body, "Source"),
            "date": field(body, "Date"),
            "timestamp": field(body, "Timestamp"),
        }
    return examples


def bank_ids(path: Path) -> list[str]:
    text = read_text(path)
    return re.findall(r"^### (EX-\d{4}) \|", text, flags=re.MULTILINE)


def field(body: str, name: str) -> str:
    match = re.search(rf"\*\*{re.escape(name)}:\*\*\s*(.*)", body)
    return match.group(1).strip() if match else ""


def parse_scores(path: Path) -> dict[str, dict[str, str]]:
    text = read_text(path)
    scores: dict[str, dict[str, str]] = {}
    for line in text.splitlines():
        match = re.match(r"\|\s*(~~)?(EX-\d{4})(~~)?\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|", line)
        if not match or match.group(2) == "EX-####":
            continue
        ex_id = match.group(2)
        score_text = match.group(5).strip()
        scores[ex_id] = {
            "retired": "yes" if match.group(1) or match.group(3) else "",
            "tactic": match.group(4).strip(),
            "score": score_text,
            "call": match.group(6).strip(),
        }
    return scores


def parse_earmarked(path: Path) -> dict[str, list[str]]:
    text = read_text(path)
    section_match = re.search(r"(?ms)^## Earmarked Examples.*?(?=^## |\Z)", text)
    if not section_match:
        return {}
    earmarked: dict[str, list[str]] = {}
    for line in section_match.group(0).splitlines():
        match = re.match(r"\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|", line)
        if not match or match.group(1).strip() in {"Tactic", "---"}:
            continue
        ids = re.findall(r"EX-\d{4}", match.group(2))
        earmarked[match.group(1).strip()] = ids
    return earmarked


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate example bank and score audit consistency.")
    parser.add_argument("--bank", default="docs/tactic-example-bank.md")
    parser.add_argument("--audit", default="docs/tactic-example-score-audit.md")
    args = parser.parse_args()

    bank_path = Path(args.bank)
    bank = parse_bank(bank_path)
    scores = parse_scores(Path(args.audit))
    earmarked = parse_earmarked(Path(args.audit))
    errors: list[str] = []

    duplicates = [ex_id for ex_id, count in Counter(bank_ids(bank_path)).items() if count > 1]
    if duplicates:
        errors.append(f"duplicate bank IDs: {', '.join(duplicates)}")

    active_bank = {ex_id: row for ex_id, row in bank.items() if not row["retired"]}
    active_scores = {ex_id: row for ex_id, row in scores.items() if not row["retired"]}

    for ex_id, row in active_bank.items():
        if row["status"] not in {"TIMESTAMP", "CLIP", "VERIFIED"}:
            errors.append(f"{ex_id}: invalid or missing status {row['status']!r}")
        if not row["source"]:
            errors.append(f"{ex_id}: missing Source")
        if not row["date"]:
            errors.append(f"{ex_id}: missing Date")
        if row["status"] in {"CLIP", "VERIFIED"} and not row["clip_url"].startswith(("http", "PENDING")):
            errors.append(f"{ex_id}: CLIP/VERIFIED status without usable Clip URL")
        if ex_id not in active_scores:
            errors.append(f"{ex_id}: active bank example missing active score row")

    for ex_id in active_scores:
        if ex_id not in active_bank:
            errors.append(f"{ex_id}: active score row missing active bank example")

    score_ge_3 = {
        ex_id
        for ex_id, row in active_scores.items()
        if row["score"].isdigit() and int(row["score"]) >= 3
    }
    earmarked_ids = {ex_id for ids in earmarked.values() for ex_id in ids}
    missing_earmarks = sorted(score_ge_3 - earmarked_ids)
    extra_earmarks = sorted(earmarked_ids - score_ge_3)
    if missing_earmarks:
        errors.append(f"score>=3 examples missing from earmarks: {', '.join(missing_earmarks)}")
    if extra_earmarks:
        errors.append(f"earmarked examples not active score>=3: {', '.join(extra_earmarks)}")

    tactic_counts: dict[str, int] = defaultdict(int)
    for ex_id in score_ge_3:
        tactic_counts[active_scores[ex_id]["tactic"]] += 1

    print(f"bank_total={len(bank)} active_bank={len(active_bank)} retired_bank={len(bank) - len(active_bank)}")
    print(f"score_rows={len(scores)} active_scores={len(active_scores)} score_ge_3={len(score_ge_3)}")
    print("earmarked_by_tactic:")
    for tactic in sorted(tactic_counts):
        print(f"  {tactic}: {tactic_counts[tactic]}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("bank validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
