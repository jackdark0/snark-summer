from __future__ import annotations

import argparse
import glob
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


TACTIC_PATTERNS: dict[str, list[str]] = {
    "Always on Offense": [
        r"\bwhat about\b",
        r"\bbut (?:destiny|dgg|dan|pisco|hutch|foodshops|willymac|nicholas|deorio|aiden|kuihman)\b",
        r"\b(?:instead|rather) (?:talk|talking) about\b",
        r"\b(?:why|how) (?:aren't|isn't|don't|doesn't|didn't) (?:you|he|they)\b.{0,120}\b(?:destiny|dgg|dan|pisco|hutch|foodshops|willymac|nicholas|deorio|aiden|kuihman)\b",
    ],
    "Isolated Demands for Rigor": [
        r"\bwhere(?:'s| is) (?:the )?(?:evidence|proof|clip|source)\b",
        r"\bshow (?:me|the) (?:evidence|proof|clip|source|receipts?)\b",
        r"\bno (?:evidence|proof|source|receipts?)\b",
        r"\bprove (?:it|that)\b",
    ],
    "Schrodinger's Joke": [
        r"\b(?:joke|meme|troll(?:ing)?|ironic|bit|kidding)\b.{0,140}\b(?:pedo|predator|dox|swat|criminal|harass|abuse)\b",
        r"\b(?:pedo|predator|dox|swat|criminal|harass|abuse)\b.{0,140}\b(?:joke|meme|troll(?:ing)?|ironic|bit|kidding)\b",
    ],
    "Unilateral Principles": [
        r"\bdouble standard\b",
        r"\bhypocrisy\b",
        r"\b(?:principle|standard)s?\b.{0,100}\b(?:but|except|when)\b",
        r"\bit'?s (?:fine|okay|different) when\b",
    ],
    "No-Win Framing": [
        r"\bno matter what\b",
        r"\bdamned if\b",
        r"\bcan't win\b",
        r"\beither way\b.{0,100}\b(?:bad|wrong|guilty|lying)\b",
    ],
    "Victim Reversal (DARVO)": [
        r"\b(?:i|we|they|he|she) (?:am|are|is|was|were) (?:the )?victim\b",
        r"\b(?:harass(?:ed|ing)|attack(?:ed|ing)|go(?:ing)? after) (?:me|us|him|her|them)\b",
        r"\b(?:they|you|he|she) (?:started|caused|forced) (?:this|it)\b",
        r"\bself[- ]?defen[sc]e\b",
    ],
    "Moving Goalposts": [
        r"\bnot what i said\b",
        r"\bwhat i (?:mean|meant)\b",
        r"\bthat's different\b",
        r"\bnow (?:you're|you are|they're|they are) saying\b",
        r"\bgoal ?posts?\b",
    ],
    "Permission Structures": [
        r"\bi (?:do not|don't) condone\b.{0,120}\b(?:but|however)\b",
        r"\bi understand why\b",
        r"\bcan't blame (?:him|her|them|people)\b",
        r"\b(?:deserve|deserved|deserves) (?:it|that|to be|what)\b",
    ],
    "Maximize Yours, Minimize Theirs": [
        r"\b(?:massive|crazy|insane|criminal|predator|evil)\b.{0,120}\b(?:destiny|dgg|dan|pisco|hutch|foodshops)\b",
        r"\b(?:nothing ?burger|not a big deal|just a joke|just one|only)\b",
        r"\bharassment campaign\b",
        r"\bdox(?:ing)? campaign\b",
    ],
    "Fragmentation": [
        r"\bjust one (?:person|guy|message|clip|tweet)\b",
        r"\bone person\b",
        r"\bsingle (?:person|message|clip|tweet|example)\b",
        r"\bisolated (?:incident|example|case)\b",
        r"\bnot (?:the|a) (?:community|server|group)\b",
    ],
    "Narrative Laundering": [
        r"\bpeople (?:are saying|say|said)\b",
        r"\bi (?:heard|saw) (?:that|people)\b",
        r"\bapparently\b",
        r"\ballegedly\b",
        r"\bthe narrative\b",
        r"\brumou?r\b",
    ],
    "Cross-Community Infiltration": [
        r"\bmass report(?:ing)?\b",
        r"\breport (?:him|her|them|it|this|the channel|the video)\b",
        r"\b(?:send|sent|bring|brought) (?:this|it|that) to\b",
        r"\b(?:sponsor|employer|college|school|twitch|youtube|discord)\b.{0,120}\b(?:report|ban|strike|remove)\b",
    ],
    "Paint Them as Crazy": [
        r"\b(?:crazy|insane|unhinged|schizo|psychotic|paranoid)\b",
        r"\bmentally ill\b",
        r"\bgangstalk(?:ed|ing)?\b",
    ],
}

KNOWN_ACTOR_PATTERNS = [
    r"\bdestiny\b",
    r"\bsteven\b",
    r"\bdgg\b",
    r"\bdan\b",
    r"\bsaltman\b",
    r"\bpisco\b",
    r"\bfood ?shops?\b",
    r"\bhutch\b",
    r"\bloner ?box\b",
    r"\bjstlk\b",
    r"\bjtock\b",
    r"\bkuihman\b",
    r"\bqueman\b",
    r"\baiden\b",
    r"\bdickers\b",
    r"\bmrow\b",
    r"\bchud\b",
    r"\bnicholas\b",
    r"\bdeorio\b",
    r"\bwillymac\b",
    r"\bcounterpoints\b",
    r"\bnotsoerudite\b",
    r"\bsnark\b",
]

CAMPAIGN_TITLE_RE = re.compile(
    r"(destiny|dgg|pisco|foodshops?|doxx?|willymac|willymacshow|jstlk|"
    r"college student|harass|witness|footsoldier|orbiters?|predator|criminal|"
    r"gangstalk|hutch|lonerbox|commentary community|counterpoints|snark)",
    re.IGNORECASE,
)


@dataclass
class Cue:
    timestamp: str
    seconds: int
    text: str


@dataclass
class Candidate:
    source_file: str
    channel: str
    title: str
    date: str
    video_id: str
    timestamp: str
    seconds: int
    tactic: str
    quote: str
    score: int
    score_call: str
    terms: set[str] = field(default_factory=set)


def timestamp_to_seconds(value: str) -> int:
    pieces = [int(part) for part in value.split(":")]
    if len(pieces) == 2:
        return pieces[0] * 60 + pieces[1]
    return pieces[0] * 3600 + pieces[1] * 60 + pieces[2]


def parse_processed(path: Path) -> tuple[dict[str, str], list[Cue]]:
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    header: dict[str, str] = {"source_file": path.as_posix()}
    if lines:
        first = lines[0]
        match = re.match(r"(?P<date>\d{4}-\d{2}-\d{2}|UNKNOWN)\s+[-—]\s+(?P<title>.+)", first)
        if match:
            header["date"] = match.group("date")
            header["title"] = match.group("title")
        else:
            header["date"] = "UNKNOWN"
            header["title"] = first
    for line in lines[1:12]:
        if ":" in line:
            key, value = line.split(":", 1)
            header[key.strip()] = value.strip()

    cues: list[Cue] = []
    for line in lines:
        match = re.match(r"^\[(?P<ts>(?:\d+:)?\d+:\d{2})\]\s+(?P<text>.+)$", line)
        if not match:
            continue
        timestamp = match.group("ts")
        cues.append(Cue(timestamp=timestamp, seconds=timestamp_to_seconds(timestamp), text=match.group("text")))
    return header, cues


def context(cues: list[Cue], index: int, radius: int = 4) -> str:
    start = max(0, index - radius)
    end = min(len(cues), index + radius + 1)
    seen: set[str] = set()
    lines: list[str] = []
    for cue in cues[start:end]:
        if cue.text in seen:
            continue
        lines.append(cue.text)
        seen.add(cue.text)
    return " ".join(lines)


def has_actor(text: str, title: str) -> bool:
    haystack = f"{title} {text}"
    return any(re.search(pattern, haystack, re.IGNORECASE) for pattern in KNOWN_ACTOR_PATTERNS)


def compact(text: str, limit: int = 360) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= limit:
        return text
    return text[:limit].rsplit(" ", 1)[0] + "..."


def score_candidate(text: str, title: str, tactic: str, matched_terms: list[str]) -> tuple[int, str]:
    score = 2
    reasons: list[str] = []
    if len(set(matched_terms)) >= 2:
        score += 1
        reasons.append("multiple tactic signals")
    if has_actor(text, title):
        score += 1
        reasons.append("known actor/topic present")
    if tactic in {"Schrodinger's Joke", "Permission Structures", "Fragmentation", "Cross-Community Infiltration"}:
        score += 1
        reasons.append("high-specificity tactic pattern")
    score = min(score, 4)
    if score < 3:
        reasons.append("weak/context-dependent signal")
    return score, "; ".join(reasons) + "; auto-caption, needs audio review"


def extract(paths: list[Path]) -> list[Candidate]:
    candidates: list[Candidate] = []
    compiled = {
        tactic: [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
        for tactic, patterns in TACTIC_PATTERNS.items()
    }
    for path in paths:
        header, cues = parse_processed(path)
        title = header.get("title", "Untitled")
        if not CAMPAIGN_TITLE_RE.search(title):
            continue
        channel = header.get("channel", "Unknown channel")
        date = header.get("date", "UNKNOWN")
        if date != "UNKNOWN" and date < "2025-02-01":
            continue
        video_id = header.get("video_id", "")
        for index, cue in enumerate(cues):
            text = context(cues, index)
            if not has_actor(text, title):
                continue
            for tactic, patterns in compiled.items():
                terms: list[str] = []
                for pattern in patterns:
                    terms.extend(match.group(0) for match in pattern.finditer(text))
                if not terms:
                    continue
                score, score_call = score_candidate(text, title, tactic, terms)
                if score < 3:
                    continue
                candidates.append(
                    Candidate(
                        source_file=path.as_posix(),
                        channel=channel,
                        title=title,
                        date=date,
                        video_id=video_id,
                        timestamp=cue.timestamp,
                        seconds=cue.seconds,
                        tactic=tactic,
                        quote=compact(text),
                        score=score,
                        score_call=score_call,
                        terms=set(terms),
                    )
                )
    return merge_candidates(candidates)


def merge_candidates(candidates: list[Candidate], gap_seconds: int = 180) -> list[Candidate]:
    candidates.sort(key=lambda item: (item.video_id, item.tactic, item.seconds, -item.score))
    merged: list[Candidate] = []
    for candidate in candidates:
        if (
            merged
            and candidate.video_id == merged[-1].video_id
            and candidate.tactic == merged[-1].tactic
            and candidate.seconds <= merged[-1].seconds + gap_seconds
        ):
            merged[-1].terms.update(candidate.terms)
            if candidate.score > merged[-1].score:
                merged[-1].score = candidate.score
                merged[-1].score_call = candidate.score_call
                merged[-1].quote = candidate.quote
                merged[-1].timestamp = candidate.timestamp
                merged[-1].seconds = candidate.seconds
            continue
        merged.append(candidate)
    merged.sort(key=lambda item: (-item.score, item.tactic, item.date, item.video_id, item.seconds))
    return merged


def to_json_row(candidate: Candidate, index: int, source_slug: str) -> dict[str, Any]:
    clip_url = f"https://youtu.be/{candidate.video_id}?t={candidate.seconds}" if candidate.video_id else "PENDING"
    return {
        "candidate_id": f"cand-{source_slug}-{index:04d}",
        "source_file": candidate.source_file,
        "channel": candidate.channel,
        "title": candidate.title,
        "platform": "YouTube",
        "date": candidate.date,
        "video_id": candidate.video_id,
        "timestamp": candidate.timestamp,
        "clip_url": clip_url,
        "tactic": candidate.tactic,
        "score": candidate.score,
        "score_call": candidate.score_call,
        "quote": candidate.quote,
        "what_happened": "Heuristic pre-scan flagged this timestamp as a possible tactic example in the transcript context.",
        "why_it_fits": f"Matched {candidate.tactic} signal(s): {', '.join(sorted(candidate.terms)[:6])}.",
        "actors": [],
        "actor_classification_requests": [],
        "duplicate_check": {
            "status": "new",
            "related_examples": [],
            "reason": "No same-video bank match was detected by the candidate validator; manual duplicate review still needed.",
        },
        "notes": "Generated by deterministic pre-scan; treat as a scout queue, not a final merged example.",
    }


def write_report(path: Path, rows: list[dict[str, Any]]) -> None:
    by_tactic: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        by_tactic.setdefault(str(row["tactic"]), []).append(row)
    lines = [
        "# Purple Parry Gaming Tactic Candidate Pre-Scan",
        "",
        "This is a deterministic pre-scan over processed transcripts. It is not a",
        "human scout pass and should not be merged into the bank without audio",
        "verification and duplicate review.",
        "",
        f"- Candidate rows: {len(rows)}",
        "",
        "## Counts by Tactic",
        "",
        "| Tactic | Count |",
        "|---|---:|",
    ]
    for tactic, tactic_rows in sorted(by_tactic.items(), key=lambda item: (-len(item[1]), item[0])):
        lines.append(f"| {tactic} | {len(tactic_rows)} |")
    lines.extend(["", "## Top Candidates by Tactic", ""])
    for tactic, tactic_rows in sorted(by_tactic.items()):
        lines.extend([f"### {tactic}", ""])
        for row in tactic_rows[:8]:
            lines.extend(
                [
                    f"- `{row['candidate_id']}` score {row['score']} | {row['date']} | `{row['video_id']}` | {row['timestamp']} | {row['title']}",
                    f"  - {row['clip_url']}",
                    f"  - {row['quote']}",
                ]
            )
        lines.append("")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Heuristic tactic candidate pre-scan for processed transcripts.")
    parser.add_argument("--glob", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--report", required=True)
    parser.add_argument("--source-slug", default="purple-parry-20260604")
    parser.add_argument("--per-tactic-limit", type=int, default=25)
    args = parser.parse_args()

    paths = sorted(Path(path) for path in glob.glob(args.glob))
    if not paths:
        raise SystemExit(f"no files matched {args.glob!r}")
    candidates = extract(paths)
    selected: list[Candidate] = []
    for tactic in TACTIC_PATTERNS:
        tactic_candidates = [candidate for candidate in candidates if candidate.tactic == tactic]
        tactic_candidates.sort(key=lambda candidate: (-candidate.score, candidate.date, candidate.video_id, candidate.seconds))
        selected.extend(tactic_candidates[: args.per_tactic_limit])
    selected.sort(key=lambda candidate: (-candidate.score, candidate.tactic, candidate.date, candidate.video_id, candidate.seconds))
    rows = [to_json_row(candidate, index, args.source_slug) for index, candidate in enumerate(selected, start=1)]

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")
    write_report(Path(args.report), rows)
    print(f"wrote {len(rows)} candidate(s) to {out_path}")
    print(f"wrote report to {args.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
