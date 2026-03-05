#!/usr/bin/env python3
"""Assemble a minimal context pack from selected reference files.

Usage:
    python build_context.py --refs core-principles.md models-anthropic.md tasks-code.md
    python build_context.py --refs core-principles.md models-gemini.md --output pack.md
    python build_context.py --model claude --task code  # shorthand
"""

import argparse
from pathlib import Path

MODEL_MAP = {
    "claude": "models-anthropic.md",
    "anthropic": "models-anthropic.md",
    "gpt": "models-openai.md",
    "openai": "models-openai.md",
    "gemini": "models-gemini.md",
    "google": "models-gemini.md",
    "grok": "models-xai.md",
    "xai": "models-xai.md",
    "deepseek": "models-china.md",
    "qwen": "models-china.md",
    "glm": "models-china.md",
    "kimi": "models-china.md",
}

TASK_MAP = {
    "code": "tasks-code.md",
    "analysis": "tasks-analysis.md",
    "content": "tasks-content.md",
    "data": "tasks-data.md",
}


def parse_args():
    parser = argparse.ArgumentParser(
        description="Build a context pack from reference files"
    )
    parser.add_argument(
        "--refs", nargs="+",
        help="Reference filenames (relative to references/)"
    )
    parser.add_argument(
        "--model", choices=list(MODEL_MAP.keys()),
        help="Shorthand for model reference"
    )
    parser.add_argument(
        "--task", choices=list(TASK_MAP.keys()),
        help="Shorthand for task reference"
    )
    parser.add_argument(
        "--output", help="Optional output file path"
    )
    return parser.parse_args()


def main():
    args = parse_args()
    base_dir = Path(__file__).resolve().parent.parent / "references"

    # Build reference list
    refs = []
    refs.append("core-principles.md")  # Always included

    if args.model:
        refs.append(MODEL_MAP[args.model])
    if args.task:
        refs.append(TASK_MAP[args.task])
    if args.refs:
        refs.extend(args.refs)

    # Deduplicate while preserving order
    seen = set()
    unique_refs = []
    for r in refs:
        if r not in seen:
            seen.add(r)
            unique_refs.append(r)

    # Load files
    sections = []
    missing = []
    for ref in unique_refs:
        ref_path = base_dir / ref
        if not ref_path.exists():
            missing.append(ref)
            continue
        content = ref_path.read_text(encoding="utf-8")
        sections.append((ref, content))

    if missing:
        raise SystemExit(f"Missing references: {', '.join(missing)}")

    # Build output
    header_lines = ["# Context Pack", ""]
    header_lines.extend([f"- {name}" for name, _ in sections])
    header = "\n".join(header_lines)

    body_parts = [header]
    for name, content in sections:
        body_parts.append(f"\n---\n\n## {name}\n\n{content.strip()}\n")

    output = "\n".join(body_parts).strip() + "\n"

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"Context pack written to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
