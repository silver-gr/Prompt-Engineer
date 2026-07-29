#!/usr/bin/env python3
"""Basic lint for reference files (length and TOC checks)."""

from pathlib import Path


def has_toc(text):
    lowered = text.lower()
    return "table of contents" in lowered or "## contents" in lowered


def main():
    base_dir = Path(__file__).resolve().parent.parent / "references"
    failures = []
    for path in sorted(base_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        line_count = text.count("\n") + 1
        if line_count > 100 and not has_toc(text):
            failures.append(f"{path.name}: {line_count} lines, missing TOC")

    if failures:
        raise SystemExit("\n".join(failures))

    print("Reference lint passed")


if __name__ == "__main__":
    main()
