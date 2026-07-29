# Core Principles (March 2026)

## The 2026 Paradigm: Context Engineering

**Context engineering > prompt engineering.** The quality of WHAT you provide matters far more than HOW you phrase it.

| Era | Focus | Key Technique |
|-----|-------|---------------|
| 2023 | Prompt engineering | Complex CoT, many-shot, elaborate frameworks |
| 2024 | Prompt optimization | Few-shot refinement, role engineering |
| 2025 | Context engineering | Simpler prompts, rich context, native reasoning |
| 2026 | Adaptive context | Model-selected reasoning depth, structured state, agent coordination |

## Context Engineering Checklist

**PROVIDE (high impact):**
- Clear problem statement
- Relevant background context
- Well-structured input data
- Desired output format (explicit schema)
- Constraints and boundaries

**AVOID (negative impact):**
- Micromanaging reasoning steps
- Conversational padding ("please", "kindly")
- Over-specified step-by-step frameworks
- Excessive few-shot examples (>2)
- Prescriptive "think about X, then Y, then Z"

## Context Prioritization

| Component | Priority | Token Budget | Notes |
|-----------|----------|-------------|-------|
| Task definition | Highest | 5-10% | Crystal clear, direct |
| Relevant background | High | 20-30% | Well-organized |
| Input data | High | 40-50% | Properly formatted |
| Output format | High | 5-10% | Explicit schema |
| Examples | Low | 0-10% | 0-1 for format only |
| Reasoning guidance | **Avoid** | **0%** | Let model decide |

## Instruction Engineering

Clarity over complexity. Direct instructions outperform tricks.

| Category | Verbs | Use For |
|----------|-------|---------|
| Generative | create, write, develop, design | Content creation |
| Analytical | analyze, evaluate, compare, assess | Analysis tasks |
| Transformative | convert, translate, summarize, simplify | Data transformation |
| Classification | categorize, identify, label, sort | Categorization |
| Extraction | extract, find, parse, identify | Data extraction |

## Prompt Structure (Universal)

```
[System Context / Role]     -> WHO the model is
[Background / Context]      -> WHAT it needs to know
[Task Instruction]          -> WHAT to do
[Input Data]                -> WITH what data
[Output Format]             -> HOW to respond
[Constraints]               -> WITHIN what limits
```

## Model-Specific Formatting

| Model Family | Preferred Format | Key Pattern |
|--------------|-----------------|-------------|
| Claude 4.6 | XML tags | `<context>`, `<task>`, `<output_format>` |
| GPT-5.x | Markdown headers | `## Context`, `## Task`, `## Output` |
| Gemini 3.1 | XML or Markdown | Either works; be consistent within prompt |

## Structured Outputs

- Specify exact schema with types
- Use native JSON mode when available (GPT-5, Gemini)
- For Claude: XML output tags guide structure effectively
- For Gemini: Use response prefixes to anchor format (start with `{"`)
- Validate output programmatically

## Prompt Caching (Token Efficiency)

Place stable content first, dynamic content last:

```
[1. SYSTEM PROMPT]         <- Cached (rarely changes)
[2. REFERENCE DOCUMENTS]   <- Cached (stable across requests)
[3. FEW-SHOT EXAMPLES]     <- Cached (if used)
[4. USER QUERY]            <- Not cached (changes per request)
```

| Provider | Mechanism | Savings |
|----------|-----------|---------|
| Anthropic | Explicit `cache_control` breakpoints | ~90% on cached |
| OpenAI | Automatic prefix caching | ~50% on repeated |
| Google | Explicit cache creation via API | ~75% on cached |

## Hallucination Management

- Ground claims in provided context
- Enforce knowledge boundaries explicitly
- Request calibrated uncertainty ("Based on the context..." vs "I believe...")
- Never fabricate citations, URLs, or specific data
- Distinguish context-grounded claims from training knowledge

## Universal Principles

1. **Clarity over cleverness**: Direct instructions outperform tricks
2. **Context quality > prompt phrasing**: Focus on WHAT you provide
3. **Simplicity wins**: Reasoning models work best with clear, minimal prompts
4. **Native features first**: Use thinking modes, JSON mode, caching
5. **Explain motivation**: WHY behind instructions helps models generalize
6. **Be direct**: Treat prompts as executable instructions
7. **Structure context**: Hierarchical organization, clear labels
8. **Specify constraints explicitly**: Models follow precise boundaries
9. **Let models reason**: Don't micromanage the thinking process
10. **Verify outputs**: Hallucination risk remains; validate critical claims
