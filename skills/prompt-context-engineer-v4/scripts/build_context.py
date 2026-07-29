#!/usr/bin/env python3
"""Assemble a minimal context pack from selected reference files."""

import argparse
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(
        description="Build a context pack from reference files"
    )
    parser.add_argument(
        "--refs",
        nargs="+",
        required=True,
        help="Reference filenames (relative to references/)"
    )
    parser.add_argument(
        "--output",
        help="Optional output file path"
    )
    return parser.parse_args()


def main():
    args = parse_args()
    base_dir = Path(__file__).resolve().parent.parent / "references"

    sections = []
    missing = []
    for ref in args.refs:
        ref_path = base_dir / ref
        if not ref_path.exists():
            missing.append(ref)
            continue
        content = ref_path.read_text(encoding="utf-8")
        sections.append((ref, content))

    if missing:
        raise SystemExit(f"Missing references: {', '.join(missing)}")

    header_lines = ["Context Pack", ""]
    header_lines.extend([f"- {name}" for name, _ in sections])
    header = "\n".join(header_lines)

    body_parts = [header]
    for name, content in sections:
        body_parts.append(f"\n---\n# {name}\n{content.strip()}\n")

    output = "\n".join(body_parts).strip() + "\n"

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
    else:
        print(output)


if __name__ == "__main__":
    main()
