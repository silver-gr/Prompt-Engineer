# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a **Prompt Engineering Knowledge Base v4.2** (January 2026 edition) - a comprehensive reference guide documenting modern prompt engineering techniques for frontier AI models (GPT-5.x, Claude 4.x, Gemini 3.x).

## Architecture

The repository follows a modular documentation structure with a main entry point and supporting modules:

```
00-prompt-engineer.md           # Main entry point (APEX prompt engineer persona)
                                # Auto-loads 01, 02; references 03-11 on demand
01-core-concepts-terminology    # Technical definitions, context windows, thinking modes
02-prompt-types-techniques      # Zero-shot, few-shot, role prompting, ReAct, RAG
03-implementation-patterns      # Context engineering, anti-patterns, model-specific patterns
04-advanced-optimization        # Evaluation, regression testing, CI/CD pipelines, LLM-as-judge
05-technical-applications       # Domain-specific patterns (content, analysis, code)
06-Gemini_Deep_Research         # Gemini Deep Research tool reference
07-Sonnet-4.5-Research          # Claude Research tool and 4.x best practices
08-Gemini-3.0-Pro-Preview       # Gemini 3.0 Pro specific guidance
09-agentic-prompting-patterns   # Tool orchestration, sub-agents, multi-context workflows
10-safety-guardrails            # Injection defense, jailbreak resistance, output filtering
11-Claude-4.x-Best-Practices    # Official Anthropic guidelines (NEW v4.2)
```

## 2025 Paradigm Shift (Critical Context)

This knowledge base reflects the fundamental shift in prompt engineering for reasoning models:

- **Context engineering > prompt engineering** - Focus on WHAT information you provide, not clever phrasing
- **Simpler prompts often work BETTER** - Reasoning models have native CoT; explicit step-by-step can REDUCE performance
- **Few-shot can HINDER** - Max 1-2 examples for format only, not reasoning demonstration
- **Zero-shot is preferred** - Start here, add complexity only if measured improvement

## Model-Specific Key Points

| Model | Critical Setting | Key Technique |
|-------|-----------------|---------------|
| **Claude 4.x** | Extended thinking (`<thinking>` tags) | XML structure, explain WHY not just WHAT |
| **Gemini 3.x** | `temperature = 1.0` (REQUIRED) | Direct instructions, NO conversational fluff |
| **GPT-5.x** | Reasoning profiles (light/balanced/deep) | Minimal prompts, crisp tool descriptions |

## Anti-Patterns to Avoid

- Explicit CoT ("Let's think step by step") with reasoning models
- Excessive few-shot examples (>2)
- Conversational padding ("please", "kindly") - especially harmful for Gemini 3.x
- Over-specifying reasoning steps
- Lowering temperature on Gemini 3.x

## File Relationships

The main prompt (`00-prompt-engineer.md`) uses `@` syntax to auto-load core modules:
```
@~/.claude/commands/01-core-concepts-terminology_v4.md
@~/.claude/commands/02-prompt-types-techniques_v4.md
```

This suggests the files may be used as Claude Code custom commands when placed in `~/.claude/commands/`.
