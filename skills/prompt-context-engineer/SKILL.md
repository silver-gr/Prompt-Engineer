---
name: prompt-context-engineer
description: Craft, optimize, review, and adapt AI prompts for frontier models (Claude 4.6, GPT-5.x, Gemini 3.1, Grok, DeepSeek, Llama 4). Use when writing prompts, system prompts, optimizing existing prompts, reviewing prompt quality, adapting prompts between models, or discussing prompt engineering. Triggers on "write a prompt", "optimize prompt", "system prompt", "review my prompt", "adapt for Claude/GPT/Gemini", "prompt engineering".
---

# Prompt & Context Engineer (March 2026)

Expert prompt engineering using the 2026 context engineering paradigm. Craft minimal, model-specific prompts for any frontier model.

## Core Paradigm

**Context engineering > prompt engineering.** WHAT you provide matters more than HOW you phrase it.

| Principle | Rule |
|-----------|------|
| Zero-shot first | Always start without examples |
| Simpler wins | Reasoning models work best with direct prompts |
| No explicit CoT | "Let's think step by step" HURTS reasoning model performance |
| Context quality | Rich, structured context > clever phrasing |
| Native features | Use thinking modes, JSON mode, caching -- not prompt hacks |
| Explain WHY | Motivation helps models generalize (especially Claude) |

## Workflow

### Step 1: Detect Mode

| User Intent | Mode |
|-------------|------|
| "Write/create a prompt for..." | **CRAFT** |
| "Improve/optimize this prompt..." | **OPTIMIZE** |
| "Review/check this prompt..." | **REVIEW** |
| "Adapt/convert this prompt for [model]..." | **ADAPT** |

### Step 2: Identify Target Model

If not specified, ask or default to Claude 4.6 (Sonnet).

| Model | Key Constraint | Format |
|-------|---------------|--------|
| **Claude 4.6** | XML tags, explain WHY, avoid "think" (thinking off) | XML |
| **GPT-5.x** | Minimal prompts, reasoning profiles | Markdown |
| **Gemini 3.1** | `temp=1.0` REQUIRED, constraints LAST | XML or Markdown |
| **Grok 4.20** | Long context (512K), real-time data | Markdown |
| **DeepSeek V3.2** | Cost-effective, strong coding | Markdown |
| **Llama 4** | Self-hosted, open weights | Markdown |

### Step 3: Identify Task Type

Load deeper reference if needed:

| Task | Reference |
|------|-----------|
| Code | [tasks-code.md](references/tasks-code.md) |
| Analysis/research | [tasks-analysis.md](references/tasks-analysis.md) |
| Content generation | [tasks-content.md](references/tasks-content.md) |
| Data extraction/transform | [tasks-data.md](references/tasks-data.md) |
| Agentic/tools | [patterns-agentic.md](references/patterns-agentic.md) |
| Safety/guardrails | [patterns-safety.md](references/patterns-safety.md) |

### Step 4: Execute Mode

---

## CRAFT Mode

1. Understand the task requirement
2. Select technique (see Decision Tree below)
3. Apply model-specific template (see Templates below)
4. Run Anti-Pattern Scanner
5. Deliver: recommended prompt + model settings + rationale

**Output structure:**
```
## Requirement Analysis
[user goals, constraints, target model]

## Recommended Prompt
[the optimized prompt]

## Model Settings
[config parameters -- separate from prompt text]

## Rationale
[why this approach, which 2026 principles applied]

## Anti-Pattern Check
[issues found or "Clean"]
```

---

## OPTIMIZE Mode

1. Read the existing prompt carefully
2. Run Anti-Pattern Scanner -- flag all issues with AP codes
3. Identify the single highest-impact optimization:
   - Remove over-engineering / fluff? (AP-1, AP-4)
   - Add missing context or structure?
   - Fix model-specific issues? (AP-5, AP-6, AP-9)
   - Better output format specification?
4. Produce optimized version
5. Show before/after diff with rationale

---

## REVIEW Mode

Run the full Anti-Pattern Scanner. Report:

```
## Prompt Review

**Score:** [1-10] / 10
**Target Model:** [detected or assumed]

### Issues Found
| Code | Issue | Severity | Fix |
|------|-------|----------|-----|
| AP-X | ... | Critical/Warning/Info | ... |

### Strengths
[what the prompt does well]

### Recommendations
[ordered by impact]
```

---

## ADAPT Mode

Translate prompts between model families.

1. Identify source model and target model
2. Apply translation rules:

| From → To | Key Changes |
|-----------|-------------|
| Claude → GPT-5 | XML → Markdown, remove WHY context, minimize length |
| Claude → Gemini | Keep XML, move constraints to END, remove "think", set temp=1.0 |
| GPT-5 → Claude | Markdown → XML, add WHY context, can add more detail |
| GPT-5 → Gemini | Keep Markdown, constraints LAST, set temp=1.0 |
| Gemini → Claude | Keep XML or convert, add WHY, constraints can be inline |
| Gemini → GPT-5 | Keep Markdown, minimize, remove constraint ordering |

3. Run Anti-Pattern Scanner against target model
4. Deliver adapted prompt + target model settings

---

## Anti-Pattern Scanner

**Check every prompt against ALL of these. Flag any matches.**

| Code | Anti-Pattern | Detection Signal | Severity |
|------|-------------|-----------------|----------|
| **AP-1** | Over-engineering | Prompt >500 tokens for simple task; elaborate frameworks; multi-page instructions | Critical |
| **AP-2** | Explicit CoT | "step by step", "Step 1:", prescribed reasoning sequences | Critical |
| **AP-3** | Excessive few-shot | >2 examples (>1 for Claude/GPT-5); examples showing reasoning steps | Warning |
| **AP-4** | Conversational fluff | "please", "kindly", "I hope", "thank you", "when you have a moment" | Warning; **Critical for Gemini** |
| **AP-5** | Gemini temp ≠ 1.0 | Temperature set below 1.0 for any Gemini 3.x model | Critical |
| **AP-6** | "Think" sensitivity | "think about/through/carefully" with Claude extended thinking disabled | Warning |
| **AP-7** | Verbose tool descriptions | Tool descriptions >2 sentences | Warning |
| **AP-8** | Prescribed tool sequence | "First use tool A, then B, then C" | Warning |
| **AP-9** | Over-prompting GPT-5 | Elaborate framework, verbose system prompt, unnecessary instructions for GPT-5 | Critical |
| **AP-10** | Missing model params | No reasoning_profile / thinking_level / effort configured | Info |

### Fluff Token Table (AP-4 detail)

| Phrase | Tokens Wasted | Signal Value |
|--------|--------------|--------------|
| "Hello! I hope you're doing well" | 8-12 | Zero |
| "Could you please help me" | 5-7 | Zero |
| "Thank you so much!" | 4-5 | Zero |
| "I would really appreciate if" | 6-8 | Zero |
| "When you have a moment" | 5 | Zero (models are instant) |

---

## Technique Decision Tree

```
Is this a reasoning model (Claude 4.6, GPT-5.x, Gemini 3.1)?
│
├─ YES → Zero-shot first
│   ├─ Works? → Done
│   ├─ Need specific format? → Add 1 example (format only, no reasoning)
│   ├─ Need deeper reasoning? → Enable thinking mode
│   │   ├─ Claude: /think, /megathink, /ultrathink
│   │   ├─ GPT-5: reasoning_profile: "deep"
│   │   └─ Gemini: thinking_level: "high"
│   └─ Gemini specifically? → 2-3 examples OK (Google recommends it)
│
└─ NO → Legacy / open-source model
    ├─ Standard task? → Zero-shot + explicit CoT
    └─ Complex pattern? → Few-shot (2-3 examples with reasoning)
```

---

## Model Templates

### Claude 4.6

```xml
<context>
[background + WHY this matters]
</context>

<task>
[direct instruction]
</task>

<output_format>
[JSON schema or format spec]
</output_format>
```

**Settings:** adaptive thinking (default) · effort: auto
**Key rules:** Explain WHY · Be explicit · Avoid "think" (thinking off) · XML tags strongly preferred

### GPT-5.x

```markdown
## Task
[concise instruction -- less is more]

## Input
[data]

## Output Format
[JSON schema]
```

**Settings:** `reasoning_profile: balanced` (light | balanced | deep | none)
**Key rules:** Minimal prompts · Crisp tool descriptions · Add persistence reminders for agentic tasks

### Gemini 3.1

```xml
<context>
[all background FIRST]
</context>

<task>
[direct instruction -- no fluff]
</task>

<constraints>
[limits and formatting LAST -- this placement is CRITICAL]
</constraints>
```

**Settings:** `temperature: 1.0` (REQUIRED) · `thinking_level: high`
**Key rules:** Constraints LAST · No conversational padding · Be direct · 2-3 few-shot OK

---

## Model Selection Guide

| Need | Best Model |
|------|-----------|
| Complex reasoning | Opus 4.6 / GPT-5.2 Thinking |
| Software development | Sonnet 4.6 |
| Massive documents (1M+) | Gemini 3.1 Pro / Grok 4.20 |
| Low latency | GPT-5.3 Instant / Haiku 4.5 |
| Cost-sensitive | DeepSeek V3.2 / Haiku 4.5 |
| Multilingual (200+) | Qwen 3.5 |
| Agent orchestration | Sonnet 4.6 / Kimi K2.5 |
| Self-hosted | Llama 4 Maverick / Mistral Large 3 |
| EU compliance | Mistral Large 3 |

---

## Prompt Caching (Token Efficiency)

Structure prompts cache-friendly: stable content first, dynamic last.

```
[1. SYSTEM PROMPT]         ← Cached (rarely changes)
[2. REFERENCE DOCUMENTS]   ← Cached (stable across requests)
[3. FEW-SHOT EXAMPLES]     ← Cached (if used)
[4. USER QUERY]            ← Not cached (changes per request)
```

| Provider | Mechanism | Savings |
|----------|-----------|---------|
| Anthropic | Explicit `cache_control` breakpoints | ~90% on cached |
| OpenAI | Automatic prefix caching | ~50% on repeated |
| Google | Explicit cache creation via API | ~75% on cached |

---

## Deep Reference Files

Load these only when you need domain-specific depth:

| Reference | When to Load |
|-----------|-------------|
| [core-principles.md](references/core-principles.md) | Full 2026 paradigm detail |
| [models-anthropic.md](references/models-anthropic.md) | Claude 4.6 deep dive |
| [models-openai.md](references/models-openai.md) | GPT-5 family deep dive |
| [models-gemini.md](references/models-gemini.md) | Gemini 3.1 deep dive |
| [models-xai.md](references/models-xai.md) | Grok family |
| [models-china.md](references/models-china.md) | DeepSeek, GLM, Qwen, Kimi |
| [tasks-code.md](references/tasks-code.md) | Code generation/review patterns |
| [tasks-analysis.md](references/tasks-analysis.md) | Analytical reasoning patterns |
| [tasks-content.md](references/tasks-content.md) | Content generation patterns |
| [tasks-data.md](references/tasks-data.md) | Data extraction/transformation |
| [patterns-agentic.md](references/patterns-agentic.md) | Agent loops, tool patterns |
| [patterns-safety.md](references/patterns-safety.md) | Injection defense, guardrails |
| [patterns-eval.md](references/patterns-eval.md) | Evaluation, LLM-as-judge |
| [tools-claude-research.md](references/tools-claude-research.md) | Claude Research UI |
| [tools-gemini-research.md](references/tools-gemini-research.md) | Gemini Deep Research |
| [templates.md](references/templates.md) | Full template collection |
