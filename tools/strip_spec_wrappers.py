"""Remove leaked LLM wrapper tags from SPEC.md files.

Strips <Agent System Instructions> and <H11-...>...</H11-...> envelope tags
that were baked into generated specs. Leaves the specification body intact.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TAG_LINE = re.compile(r"^</?(?:Agent System Instructions|H11[-_][^>]+)\s*>\s*$")


def clean_spec(text: str) -> str:
    kept: list[str] = []
    for line in text.splitlines():
        if TAG_LINE.match(line.strip()):
            continue
        kept.append(line)
    cleaned = "\n".join(kept).strip()
    return cleaned + "\n" if cleaned else ""


def read_text(path: Path) -> str:
    raw = path.read_bytes()
    for enc in ("utf-8", "utf-8-sig", "cp1252", "latin-1"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


def main() -> int:
    changed = 0
    scanned = 0
    for path in ROOT.rglob("SPEC.md"):
        scanned += 1
        original = read_text(path)
        updated = clean_spec(original)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            changed += 1
    print(f"scanned={scanned} cleaned={changed}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
