from __future__ import annotations

import argparse
import csv
import html
import json
import re
from dataclasses import dataclass, field
from pathlib import Path


DEFAULT_INVENTORY = Path("transcripts/ryle-kittenhouse/raw/ryle-destiny-transcript-inventory-20260602.tsv")
DEFAULT_REPORT_DIR = Path("agentic/reports")
DEFAULT_DOC = Path("docs/defamation-actionable-statements.md")


TARGETS = {
    "Destiny": [
        r"\bdestiny\b",
        r"\bsteven\b",
        r"\bsteven bonnell\b",
        r"\bsteven bunnel\b",
        r"\bdgg\b",
        r"\bdgger(?:s)?\b",
    ],
    "Dan Saltman": [r"\bdan saltman\b", r"\bsaltman\b"],
    "Foodshops": [
        r"\bfoodshops?\b",
        r"\bfood shops?\b",
        r"\bfood slops?\b",
        r"\bfood cops?\b",
        r"\bfood chops?\b",
        r"\bfood jobs?\b",
    ],
    "Pisco": [r"\bpisco\b"],
    "Wicked Supreme": [r"\bwicked supreme\b"],
    "Esports Batman": [r"\besports batman\b"],
    "LonerBox": [r"\blonerbox\b", r"\bloner box\b"],
    "Hutch": [r"\bhutch\b"],
    "Stardust": [r"\bstardust\b"],
    "Whick": [r"\bwhick\b", r"\bwhicktv\b", r"\bwhick tv\b"],
}


PER_SE_PATTERNS = {
    "crime_or_threat": [
        r"\bswat(?:ted|ting)?\b",
        r"\bdeath threat(?:s)?\b",
        r"\b(?:call(?:ed|ing)? for|want(?:ed|s)?|hope(?:d|s)?|tell(?:ing)?|told).{0,60}\b(?:kill|murder|die|death)\b",
        r"\b(?:threaten(?:ed|ing)?|threats?).{0,60}\b(?:swat|kill|murder|death)\b",
        r"\bblackmail(?:ed|ing)?\b",
        r"\bextort(?:ed|ing|ion)?\b",
        r"\bperjur(?:y|e|ed)\b",
        r"\bassault(?:ed|ing)?\b",
        r"\bfraud(?:ulent)?\b",
    ],
    "sexual_or_minor": [
        r"\bpedo(?:phile|philia)?\b",
        r"\brapist\b",
        r"\brape allegation(?:s)?\b",
        r"\baccus(?:ed|es|ing|ation).{0,60}\brape\b",
        r"\b(?:was|were|is|got|getting|being)\s+raped\b",
        r"\braped\s+(?:her|him|them|a woman|a girl|a minor|a child)\b",
        r"\be-?rap(?:e|ist)\b",
        r"\bsexual assault\b",
        r"\bsexual misconduct\b",
        r"\bconsent violation(?:s)?\b",
        r"\bnon[- ]?consensual\b",
        r"\b(?:minor|child).{0,60}\b(?:video|image|pic|picture|material|nude|sexual|sex|traffick|csam)\b",
        r"\bchild sex\b",
        r"\bcsam\b",
        r"\btraffick(?:ed|ing)?\b",
        r"\bgroom(?:er|ing)\b",
        r"\bpredator\b",
        r"\bpdf(?:[- ]?file|illia|ilia)?\b",
    ],
    "dox_or_privacy": [
        r"\bdoxx?(?:ed|ing|er|ers)?\b",
        r"\bpro[- ]?doxx?(?:ing)?\b",
        r"\bdoxx?(?:ing)? campaign\b",
        r"\b(?:leak(?:ed|ing)?|post(?:ed|ing)?|shar(?:ed|ing)?|releas(?:ed|ing)?).{0,60}\b(?:private|personal|identifying|confidential|nudes?|onlyfans)\b",
        r"\b(?:private|personal|identifying|confidential).{0,60}\b(?:information|address|details|name|nudes?|onlyfans)\b",
    ],
    "professional_or_integrity": [
        r"\bmalicious lie\b",
        r"\bfabricat(?:ed|ing|ion)\b",
        r"\b(?:forg(?:ed|ing)|doctored).{0,60}\b(?:evidence|clip|screenshot|receipt|log)\b",
        r"\bsmear campaign(?:s)?\b",
        r"\bcoordinating harassment\b",
        r"\bcoordinat(?:e|ed|ing).{0,60}\bharass(?:ed|ing|ment)?\b",
        r"\bcoordinating smear\b",
        r"\bpropagandist\b",
        r"\b(?:viewbot(?:ted|ting)?|botted viewers)\b",
        r"\bscam(?:med|ming|mer)?\b",
    ],
    "abuse_or_harassment": [
        r"\bpattern of abuse\b",
        r"\babuser\b",
        r"\babus(?:e|ed|es|ing)\b",
        r"\bharassment campaign\b",
        r"\bcoordinat(?:e|ed|ing).{0,60}\b(?:attack|smear|harass)\b",
    ],
}


INSULT_PATTERNS = [
    r"\bsociopath\b",
    r"\bpsychopath\b",
    r"\bcult(?:ist)?\b",
    r"\bliar\b",
    r"\bly(?:ing|ied)\b",
    r"\bcrazy\b",
    r"\binsane\b",
    r"\bunhinged\b",
    r"\bbroken\b",
    r"\bdesperate\b",
    r"\bbad faith\b",
    r"\bperformative\b",
    r"\bcrash(?:out|ed|ing)?\b",
    r"\blolcow\b",
    r"\bpedo(?:phile|philia)?\b",
    r"\brap(?:e|ed|ist|ing)\b",
    r"\be-?rap(?:e|ist)\b",
    r"\bdoxx?(?:er|ed|ing)?\b",
    r"\babuser\b",
    r"\bpredator\b",
    r"\bscumbag\b",
    r"\bpiece of\b",
]


TIMING_RE = re.compile(
    r"^(?P<sh>\d{2}):(?P<sm>\d{2}):(?P<ss>\d{2}\.\d{3})\s+-->\s+"
    r"(?P<eh>\d{2}):(?P<em>\d{2}):(?P<es>\d{2}\.\d{3})"
)
INLINE_TS_RE = re.compile(r"<\d{2}:\d{2}:\d{2}\.\d{3}>")
TAG_RE = re.compile(r"<[^>]+>")


@dataclass
class Cue:
    start: float
    end: float
    text: str


@dataclass
class Hit:
    video_id: str
    date: str
    title: str
    source_file: str
    raw_vtt_path: str
    start: float
    end: float
    target: str
    categories: set[str] = field(default_factory=set)
    terms: set[str] = field(default_factory=set)
    quote: str = ""


def seconds(parts: tuple[str, str, str]) -> float:
    h, m, s = parts
    return int(h) * 3600 + int(m) * 60 + float(s)


def stamp(value: float) -> str:
    total = int(value)
    h, rem = divmod(total, 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


def clean_text(value: str) -> str:
    value = INLINE_TS_RE.sub("", value)
    value = TAG_RE.sub("", value)
    value = html.unescape(value).replace("\xa0", " ")
    value = re.sub(r"\s+", " ", value).strip()
    return value


def parse_vtt(path: Path) -> list[Cue]:
    cues: list[Cue] = []
    start: float | None = None
    end: float | None = None
    text_lines: list[str] = []

    def flush() -> None:
        nonlocal start, end, text_lines
        if start is None or end is None:
            text_lines = []
            return
        text = clean_text(" ".join(text_lines))
        if text:
            cues.append(Cue(start=start, end=end, text=text))
        start = None
        end = None
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
            end = seconds((match.group("eh"), match.group("em"), match.group("es")))
            continue
        if start is not None:
            text_lines.append(line)
    flush()
    return cues


def compile_many(patterns: list[str]) -> list[re.Pattern[str]]:
    return [re.compile(pattern, re.IGNORECASE) for pattern in patterns]


TARGET_RES = {target: compile_many(patterns) for target, patterns in TARGETS.items()}
PER_SE_RES = {category: compile_many(patterns) for category, patterns in PER_SE_PATTERNS.items()}
INSULT_RES = compile_many(INSULT_PATTERNS)


def matches(patterns: list[re.Pattern[str]], text: str) -> list[str]:
    found: list[str] = []
    for pattern in patterns:
        for match in pattern.finditer(text):
            found.append(match.group(0))
    return found


def find_targets(text: str, title: str = "") -> list[str]:
    found: list[str] = []
    for target, patterns in TARGET_RES.items():
        if matches(patterns, text):
            found.append(target)
            continue
        if target == "Dan Saltman" and re.search(r"\bdan\b", text, re.IGNORECASE):
            if re.search(r"\b(?:dan saltman|saltman)\b", title, re.IGNORECASE):
                found.append(target)
        if target == "Wicked Supreme" and re.search(r"\bsupreme\b", text, re.IGNORECASE):
            if re.search(r"\bwicked supreme\b", title, re.IGNORECASE):
                found.append(target)
    return found


def collapse_repeated_ngrams(text: str) -> str:
    words = text.split()
    if len(words) < 8:
        return text
    output: list[str] = []
    index = 0
    while index < len(words):
        collapsed = False
        max_size = min(12, (len(words) - index) // 2)
        for size in range(max_size, 2, -1):
            chunk = words[index : index + size]
            next_chunk = words[index + size : index + (2 * size)]
            if chunk == next_chunk:
                output.extend(chunk)
                index += size
                while words[index : index + size] == chunk:
                    index += size
                collapsed = True
                break
        if not collapsed:
            output.append(words[index])
            index += 1
    return " ".join(output)


def compact_quote(text: str, limit: int = 520) -> str:
    text = collapse_repeated_ngrams(clean_text(text))
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= limit:
        return text
    cut = text[:limit].rsplit(" ", 1)[0]
    return cut + "..."


def context(cues: list[Cue], index: int, radius: int = 3) -> str:
    start = max(0, index - radius)
    end = min(len(cues), index + radius + 1)
    merged: list[str] = []
    previous = ""
    for cue in cues[start:end]:
        if cue.text != previous and cue.text not in merged:
            merged.append(cue.text)
        previous = cue.text
    return compact_quote(" ".join(merged), limit=900)


def title_targets(title: str) -> list[str]:
    return find_targets(title)


def row_date(row: dict[str, str]) -> str:
    return row.get("upload_date") or row.get("date") or "UNKNOWN"


def clip_url(video_id: str, start: float) -> str:
    return f"https://youtu.be/{video_id}?t={int(start)}"


def union_duration(intervals: list[tuple[float, float]], merge_gap: float = 2.0) -> float:
    if not intervals:
        return 0.0
    merged: list[tuple[float, float]] = []
    for start, end in sorted(intervals):
        if end < start:
            continue
        if not merged or start > merged[-1][1] + merge_gap:
            merged.append((start, end))
        else:
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
    return sum(end - start for start, end in merged)


def merge_hits(hits: list[Hit], gap: float = 20.0) -> list[Hit]:
    if not hits:
        return []
    hits = sorted(hits, key=lambda hit: (hit.video_id, hit.target, hit.start))
    merged: list[Hit] = []
    for hit in hits:
        if (
            merged
            and hit.video_id == merged[-1].video_id
            and hit.target == merged[-1].target
            and hit.start <= merged[-1].end + gap
        ):
            merged[-1].end = max(merged[-1].end, hit.end)
            merged[-1].categories.update(hit.categories)
            merged[-1].terms.update(hit.terms)
            if len(merged[-1].quote) < 420 and hit.quote not in merged[-1].quote:
                merged[-1].quote = (merged[-1].quote + " " + hit.quote).strip()
        else:
            merged.append(hit)
    return merged


def load_inventory(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def build_doc(
    *,
    doc_path: Path,
    candidate_rows: list[dict[str, str]],
    insult_rows: list[dict[str, str]],
    summary: dict[str, str],
    candidates_tsv: Path,
    insult_tsv: Path,
) -> None:
    high = [row for row in candidate_rows if row["priority"] == "high"]
    medium = [row for row in candidate_rows if row["priority"] == "medium"]
    lines = [
        "# Defamation Actionable Statements - Ryle Kittenhouse Corpus",
        "",
        "This is a triage extraction, not a legal conclusion. It keeps the prior",
        "ally scope: retained candidates are aimed at registered target/team-adjacent",
        "actors. `pro se` is treated as `defamation per se` for this pass.",
        "",
        "## Scope and Method",
        "",
        f"- Source inventory: `{DEFAULT_INVENTORY.as_posix()}`",
        f"- Actionable-statement candidates TSV: `{candidates_tsv.as_posix()}`",
        f"- Destiny-insult timing TSV: `{insult_tsv.as_posix()}`",
        f"- Processed videos scanned: {summary['videos_scanned']}",
        f"- Candidate statement clusters: {summary['candidate_count']}",
        f"- High-priority per-se-style clusters: {len(high)}",
        f"- Medium-priority clusters: {len(medium)}",
        f"- Approximate Destiny-insult time: {summary['destiny_insult_hms']} ({summary['destiny_insult_seconds']} seconds)",
        f"- Approximate corpus caption time: {summary['corpus_hms']} ({summary['corpus_seconds']} seconds)",
        f"- Approximate insult share of corpus: {summary['destiny_insult_share']}",
        "",
        "The extraction groups nearby caption hits into statement clusters. Because",
        "YouTube auto-captions repeat rolling fragments, the timing count uses unioned",
        "caption intervals rather than raw line counts.",
        "",
        "## Legal Heuristic",
        "",
        "- High-priority per-se-style categories used here: crime/threat allegations",
        "  and sexual or minor-related allegations.",
        "- Medium-priority actionable categories used here: professional/integrity",
        "  allegations, dox/privacy allegations, and abuse/harassment allegations.",
        "- U.S. public-figure analysis may also require actual malice. See",
        "  `New York Times Co. v. Sullivan` and `Milkovich v. Lorain Journal Co.`.",
        "- State law varies. This file is for source triage and clip prioritization.",
        "",
        "## Highest-Priority Candidates",
        "",
    ]
    for row in high[:40]:
        lines.extend(
            [
                f"### {row['candidate_id']} | {row['target']} | {row['categories']}",
                "",
                f"**Source:** Ryle Kittenhouse - `{row['title']}` / YouTube",
                f"**Date:** {row['date']}",
                f"**Timestamp:** {row['start_timestamp']} - {row['end_timestamp']}",
                f"**Clip source:** `{row['clip_url']}`",
                f"**Transcript:** `{row['source_file']}`",
                "",
                f"**Candidate statement:** {row['quote']}",
                "",
                f"**Why flagged:** {row['why_flagged']}",
                "",
                "**Verification need:** Audio/video verify wording, source-chain, and speaker attribution before external use.",
                "",
            ]
        )
    lines.extend(
        [
            "## Medium-Priority Candidates",
            "",
            "Medium-priority candidates are retained in the TSV. They are not expanded",
            "here unless they are needed for a clip pass.",
            "",
            "## Destiny-Insult Timing by Video",
            "",
            "| Date | Video | Approx. insult time | Share | Title |",
            "|---|---:|---:|---:|---|",
        ]
    )
    for row in insult_rows[:30]:
        lines.append(
            f"| {row['date']} | `{row['video_id']}` | {row['insult_hms']} | {row['insult_share']} | {row['title']} |"
        )
    lines.extend(
        [
            "",
            "## Next Steps",
            "",
            "1. Manually review the high-priority rows in the TSV for duplicates and source-chain context.",
            "2. Clip only after audio verification and speaker attribution.",
            "3. Move unregistered actor/entity questions into `docs/actor-classification-queue.md`.",
        ]
    )
    doc_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def hms(seconds_value: float) -> str:
    total = int(round(seconds_value))
    h, rem = divmod(total, 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract ally-aimed defamation-risk candidates from VTT captions.")
    parser.add_argument("--inventory", default=str(DEFAULT_INVENTORY))
    parser.add_argument("--report-dir", default=str(DEFAULT_REPORT_DIR))
    parser.add_argument("--doc", default=str(DEFAULT_DOC))
    parser.add_argument("--date-stamp", default="20260602")
    args = parser.parse_args()

    inventory_path = Path(args.inventory)
    report_dir = Path(args.report_dir)
    rows = load_inventory(inventory_path)

    all_hits: list[Hit] = []
    insult_rows: list[dict[str, str]] = []
    total_corpus_seconds = 0.0
    total_destiny_insult_seconds = 0.0
    videos_scanned = 0

    for row in rows:
        vtt_path = Path(row["raw_vtt_path"])
        if not vtt_path.exists():
            continue
        cues = parse_vtt(vtt_path)
        if not cues:
            continue
        videos_scanned += 1
        video_id = row["video_id"]
        date = row_date(row)
        title = row["title"]
        source_file = row["processed_path"]
        duration = max(cue.end for cue in cues)
        total_corpus_seconds += duration
        title_target_hits = title_targets(title)

        insult_intervals: list[tuple[float, float]] = []
        destiny_title = "Destiny" in title_target_hits

        for index, cue in enumerate(cues):
            ctx = context(cues, index)
            cue_targets = find_targets(ctx, title)

            categories: set[str] = set()
            terms: set[str] = set()
            for category, patterns in PER_SE_RES.items():
                matched = matches(patterns, ctx)
                if matched:
                    categories.add(category)
                    terms.update(matched)

            if categories and cue_targets:
                for target in cue_targets:
                    all_hits.append(
                        Hit(
                            video_id=video_id,
                            date=date,
                            title=title,
                            source_file=source_file,
                            raw_vtt_path=str(vtt_path).replace("\\", "/"),
                            start=cue.start,
                            end=cue.end,
                            target=target,
                            categories=categories.copy(),
                            terms=terms.copy(),
                            quote=compact_quote(ctx),
                        )
                    )

            insult_match = bool(matches(INSULT_RES, cue.text))
            destiny_targeted = "Destiny" in cue_targets or (
                destiny_title and re.search(r"\b(?:destiny|steven|he|him|his|this guy|this dude)\b", ctx, re.IGNORECASE)
            )
            if insult_match and destiny_targeted:
                insult_intervals.append((cue.start, cue.end))

        insult_seconds = union_duration(insult_intervals)
        total_destiny_insult_seconds += insult_seconds
        if insult_seconds:
            insult_rows.append(
                {
                    "date": date,
                    "video_id": video_id,
                    "title": title,
                    "duration_seconds": str(int(duration)),
                    "insult_seconds": str(int(round(insult_seconds))),
                    "insult_hms": hms(insult_seconds),
                    "insult_share": f"{(insult_seconds / duration):.1%}" if duration else "0.0%",
                    "source_file": source_file,
                    "source_url": clip_url(video_id, 0),
                }
            )

    merged_hits = merge_hits(all_hits)
    candidate_rows: list[dict[str, str]] = []
    for index, hit in enumerate(merged_hits, start=1):
        categories = sorted(hit.categories)
        priority = "high" if "sexual_or_minor" in categories or "crime_or_threat" in categories else "medium"
        candidate_rows.append(
            {
                "candidate_id": f"DA-{index:04d}",
                "priority": priority,
                "target": hit.target,
                "date": hit.date,
                "video_id": hit.video_id,
                "title": hit.title,
                "start_timestamp": stamp(hit.start),
                "end_timestamp": stamp(hit.end),
                "start_seconds": str(int(hit.start)),
                "end_seconds": str(int(hit.end)),
                "clip_url": clip_url(hit.video_id, hit.start),
                "source_file": hit.source_file,
                "raw_vtt_path": hit.raw_vtt_path,
                "categories": ", ".join(categories),
                "terms": " | ".join(sorted(hit.terms)),
                "quote": compact_quote(hit.quote),
                "why_flagged": (
                    "Actionable allegation category: "
                    + ", ".join(categories)
                    + "; aimed at registered target/team-adjacent actor."
                ),
            }
        )

    candidate_rows.sort(key=lambda row: (0 if row["priority"] == "high" else 1, row["target"], row["date"], row["start_seconds"]))
    for index, row in enumerate(candidate_rows, start=1):
        row["candidate_id"] = f"DA-{index:04d}"

    insult_rows.sort(key=lambda row: int(row["insult_seconds"]), reverse=True)

    candidates_tsv = report_dir / f"defamation-actionable-statements-{args.date_stamp}.tsv"
    insult_tsv = report_dir / f"destiny-insult-time-{args.date_stamp}.tsv"
    summary_json = report_dir / f"defamation-actionable-summary-{args.date_stamp}.json"

    candidate_fields = [
        "candidate_id",
        "priority",
        "target",
        "date",
        "video_id",
        "title",
        "start_timestamp",
        "end_timestamp",
        "start_seconds",
        "end_seconds",
        "clip_url",
        "source_file",
        "raw_vtt_path",
        "categories",
        "terms",
        "quote",
        "why_flagged",
    ]
    insult_fields = [
        "date",
        "video_id",
        "title",
        "duration_seconds",
        "insult_seconds",
        "insult_hms",
        "insult_share",
        "source_file",
        "source_url",
    ]
    write_tsv(candidates_tsv, candidate_rows, candidate_fields)
    write_tsv(insult_tsv, insult_rows, insult_fields)

    summary = {
        "videos_scanned": str(videos_scanned),
        "candidate_count": str(len(candidate_rows)),
        "destiny_insult_seconds": str(int(round(total_destiny_insult_seconds))),
        "destiny_insult_hms": hms(total_destiny_insult_seconds),
        "corpus_seconds": str(int(round(total_corpus_seconds))),
        "corpus_hms": hms(total_corpus_seconds),
        "destiny_insult_share": f"{(total_destiny_insult_seconds / total_corpus_seconds):.1%}"
        if total_corpus_seconds
        else "0.0%",
    }
    summary_json.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    build_doc(
        doc_path=Path(args.doc),
        candidate_rows=candidate_rows,
        insult_rows=insult_rows,
        summary=summary,
        candidates_tsv=candidates_tsv,
        insult_tsv=insult_tsv,
    )

    print(json.dumps(summary, indent=2))
    print(f"wrote {candidates_tsv}")
    print(f"wrote {insult_tsv}")
    print(f"wrote {args.doc}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
