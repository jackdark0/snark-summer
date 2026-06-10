from __future__ import annotations

import argparse
import glob
import re
from pathlib import Path


DEFAULT_OUT_DIR = Path("agentic/packets")
DEFAULT_BANK = Path("docs/tactic-example-bank.md")
DEFAULT_TAXONOMY = Path("docs/counter-tactics-guide.md")
DEFAULT_ACTORS = Path("docs/actor-aliases.md")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def safe_stem(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9._-]+", "-", value).strip(".-")
    return value[:120] or "packet"


def parse_header(text: str) -> tuple[str, str]:
    lines = text.splitlines()
    header_lines: list[str] = []
    body_start = 0
    for index, line in enumerate(lines):
        if index < 20 and (":" in line or not line.strip()):
            header_lines.append(line)
            body_start = index + 1
            continue
        break
    header = "\n".join(header_lines).strip()
    body = "\n".join(lines[body_start:]).strip()
    if not body:
        body = text.strip()
    return header, body


def chunk_lines(text: str, max_lines: int) -> list[str]:
    lines = text.splitlines()
    return ["\n".join(lines[i : i + max_lines]) for i in range(0, len(lines), max_lines)]


def bank_summary(bank_text: str) -> str:
    headings = re.findall(r"^### (EX-\d{4}) \| (.+)$", bank_text, flags=re.MULTILINE)
    recent = headings[-30:]
    return "\n".join(f"- {ex_id}: {tactic}" for ex_id, tactic in recent)


def build_packet(
    *,
    source_path: Path,
    part: int,
    total: int,
    header: str,
    chunk: str,
    bank_text: str,
    actor_text: str,
) -> str:
    return f"""# Transcript Scout Packet

Source file: `{source_path.as_posix()}`
Part: {part} / {total}

## Agent Role

Use `agentic/roles/scout.md`.

## Instructions

- Scan only this packet.
- Identify candidate tactic examples using `docs/counter-tactics-guide.md`.
- Check likely duplicates against the existing examples summary below.
- Use the actor/entity register below for canonical names and classifications.
- If a new or ambiguous actor/entity appears and its role matters, include an
  `actor_classification_requests` array in the candidate JSON object rather than
  assigning a role silently.
- Return JSONL only, following `docs/agentic-workflow.md`.
- Do not edit files.

## Existing Example Summary

{bank_summary(bank_text)}

## Actor and Entity Register

```markdown
{actor_text}
```

## Transcript Header

```text
{header or "No parsed header."}
```

## Transcript Chunk

```text
{chunk}
```
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate transcript packets for scout agents.")
    parser.add_argument("--glob", required=True, help="Glob for processed transcript files.")
    parser.add_argument("--out-dir", default=str(DEFAULT_OUT_DIR), help="Directory for generated packets.")
    parser.add_argument("--max-lines", type=int, default=450, help="Maximum transcript lines per packet.")
    parser.add_argument("--bank", default=str(DEFAULT_BANK), help="Example bank path.")
    parser.add_argument("--actors", default=str(DEFAULT_ACTORS), help="Actor/entity register path.")
    args = parser.parse_args()

    paths = sorted(Path(path) for path in glob.glob(args.glob, recursive=True))
    if not paths:
        raise SystemExit(f"no files matched {args.glob!r}")

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    bank_text = read_text(Path(args.bank))
    actor_text = read_text(Path(args.actors))

    written = 0
    for source_path in paths:
        text = read_text(source_path)
        header, body = parse_header(text)
        chunks = chunk_lines(body, args.max_lines)
        total = len(chunks)
        source_stem = safe_stem(source_path.with_suffix("").as_posix())
        for index, chunk in enumerate(chunks, start=1):
            packet = build_packet(
                source_path=source_path,
                part=index,
                total=total,
                header=header,
                chunk=chunk,
                bank_text=bank_text,
                actor_text=actor_text,
            )
            out_path = out_dir / f"{source_stem}.part-{index:03d}-of-{total:03d}.md"
            out_path.write_text(packet, encoding="utf-8")
            written += 1

    print(f"wrote {written} packet(s) to {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
