# Google (Gemini 3.1 Family, March 2026)

## Models

| Model | Context | Strengths | Use For |
|-------|---------|-----------|---------|
| **3.1 Pro** | 2M | #1 benchmarks, deepest reasoning | Complex analysis, research |
| **3.1 Flash-Lite** | 1M | Fast, cheap, large context | Extraction, summarization |

## Core Principles

### 1. Be Precise and Direct
Gemini treats prompts as executable instructions. Directness over persuasion.

- Avoid: "Could you please help me understand..."
- Use: "Explain the differences between..."

### 2. Simplify Prompts
Gemini 3.x has native advanced reasoning. Stop using complex CoT.

- Old (2.x): "Let's approach this step-by-step: First, identify..."
- New (3.x): "Solve this problem: [problem]. Show your reasoning."

### 3. Temperature = 1.0 (REQUIRED)
**CRITICAL**: Gemini 3.x is calibrated for `temperature = 1.0`. Do NOT change.

- Lowering causes loops and degraded reasoning
- Exception: Creative tasks can try 1.1-1.2
- If safety filters trigger, try increasing slightly

### 4. Use thinking_level Parameter

| Level | Latency | Cost | Use For |
|-------|---------|------|---------|
| `"low"` | Fast | Lower | Simple queries, extraction, formatting |
| `"high"` (default) | Slower | Higher | Research, planning, complex problems |

### 5. Consistent Structure
Choose XML or Markdown and stick with it throughout a single prompt.

## Constraint Ordering (CRITICAL)

**Gemini 3.x drops negative/formatting constraints placed before context.**

Correct order:
1. Context and source material (FIRST)
2. Main task instruction
3. Negative/formatting/quantitative constraints (LAST)

Bad:
```
Do not use bullet points. Keep under 200 words.
Here is the context: [data]
Summarize this.
```

Good:
```xml
<context>[data]</context>
<task>Summarize this.</task>
<constraints>
- No bullet points
- Maximum 200 words
</constraints>
```

## Few-Shot Policy

Google recommends 2-3 examples with consistent formatting for Gemini. This is the exception to the "zero-shot first" rule.

- Default: zero-shot is fine for most tasks
- Format demos: 1-2 examples
- Complex patterns: 2-3 examples OK
- Never include reasoning steps in examples

## Multimodal Labels

Label each modality explicitly:
```
Image 1: [photo of product packaging]
Image 2: [screenshot of competitor site]

Compare the design approaches shown in both images.
```

## Response Prefixes

Anchor output format by starting the response:
```
Start your response with: {"analysis":
```

## Persona Caution

Gemini takes personas very seriously and may ignore instructions that conflict with the assigned role. Be explicit about persona boundaries:
```
You are a data analyst. Despite your analytical focus, also provide
plain-language summaries accessible to non-technical readers.
```

## Template

```xml
<context>
[all relevant material FIRST]
</context>

<task>
[direct instruction -- no fluff]
</task>

<constraints>
[limits and formatting LAST -- critical placement]
</constraints>
```

**Settings:** `temperature: 1.0` (REQUIRED) | `thinking_level: high`

## Cheat Sheet

```
DO: temperature=1.0, thinking_level, be direct, context FIRST,
    constraints LAST, 2-3 few-shot OK, label multimodal inputs
DON'T: lower temperature, constraints before context,
       conversational fluff, complex CoT, broad "do not infer"
```
