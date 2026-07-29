#!/usr/bin/env python3
"""Lint reference files for quality and consistency.

Checks:
- File length (warn if >100 lines without TOC)
- Required heading structure
- March 2026 currency (warn if outdated model names)
- SKILL.md frontmatter validation
"""

import re
import sys
from pathlib import Path

OUTDATED_TERMS = [
    "Opus 4.5", "Sonnet 4.5", "Claude 4.5",
    "Gemini 3.0", "Gemini 3 Pro",
    "GPT-5 Mini", "GPT-5.0",
    "GLM 4", "GLM-4", "Qwen 3 Max", "Kimi K2 ",
    "2025+", "2025 Edition",
]


def has_toc(text: str) -> bool:
    lowered = text.lower()
    return "table of contents" in lowered or "## contents" in lowered


def check_outdated(text: str, filename: str) -> list[str]:
    warnings = []
    for term in OUTDATED_TERMS:
        if term in text:
            warnings.append(f"  {filename}: outdated term '{term}'")
    return warnings


def check_heading(text: str, filename: str) -> list[str]:
    warnings = []
    if not text.startswith("#"):
        warnings.append(f"  {filename}: missing top-level heading")
    return warnings


def check_skill_frontmatter(text: str) -> list[str]:
    warnings = []
    if not text.startswith("---"):
        warnings.append("  SKILL.md: missing YAML frontmatter")
        return warnings

    parts = text.split("---", 2)
    if len(parts) < 3:
        warnings.append("  SKILL.md: incomplete frontmatter")
        return warnings

    fm = parts[1]
    if "name:" not in fm:
        warnings.append("  SKILL.md: missing 'name' in frontmatter")
    if "description:" not in fm:
        warnings.append("  SKILL.md: missing 'description' in frontmatter")

    # Check name format
    name_match = re.search(r"name:\s*(.+)", fm)
    if name_match:
        name = name_match.group(1).strip()
        if not re.match(r"^[a-z0-9-]+$", name):
            warnings.append(f"  SKILL.md: name '{name}' must be lowercase-hyphens only")
        if len(name) > 64:
            warnings.append(f"  SKILL.md: name too long ({len(name)} > 64 chars)")

    # Check description length
    desc_match = re.search(r"description:\s*(.+?)(?:\n[a-z]|\n---)", fm, re.DOTALL)
    if desc_match:
        desc = desc_match.group(1).strip()
        if len(desc) > 1024:
            warnings.append(f"  SKILL.md: description too long ({len(desc)} > 1024 chars)")

    return warnings


def main():
    base_dir = Path(__file__).resolve().parent.parent
    refs_dir = base_dir / "references"
    skill_path = base_dir / "SKILL.md"

    warnings = []
    errors = []

    # Check SKILL.md
    if skill_path.exists():
        text = skill_path.read_text(encoding="utf-8")
        errors.extend(check_skill_frontmatter(text))
        warnings.extend(check_outdated(text, "SKILL.md"))

    # Check reference files
    for path in sorted(refs_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        line_count = text.count("\n") + 1

        if line_count > 100 and not has_toc(text):
            warnings.append(f"  {path.name}: {line_count} lines (consider adding TOC)")

        warnings.extend(check_heading(text, path.name))
        warnings.extend(check_outdated(text, path.name))

    # Report
    if errors:
        print("ERRORS:")
        print("\n".join(errors))

    if warnings:
        print("WARNINGS:")
        print("\n".join(warnings))

    if not errors and not warnings:
        print("All checks passed")
        return 0

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
