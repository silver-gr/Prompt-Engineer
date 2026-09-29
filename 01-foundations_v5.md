# Foundations: Context Engineering & Core Concepts (2026 Edition)

This module covers the foundational principles of modern prompt engineering: context engineering, thinking modes, hallucination management, and structured outputs. Auto-loaded by the main entry point.

> **Model specifications**: See 03-model-catalog_v5.md for all model data.

---

## 1. The 2026 Paradigm: Context Engineering

**Core Principle**: The quality of WHAT information you provide matters far more than HOW you phrase requests. With reasoning models (Claude 5.x, GPT-5.x/GPT-6, Gemini 3.x), focus on context structure, not clever prompting tricks.

### What Changed

| Era | Focus | Key Technique |
|-----|-------|---------------|
| 2023 | Prompt engineering | Complex CoT, many-shot, elaborate frameworks |
| 2024 | Prompt optimization | Few-shot refinement, role engineering |
| 2025 | Context engineering | Simpler prompts, rich context, native reasoning |
| 2026 | Adaptive context | Model-selected reasoning depth, structured state, agent coordination |

### Context Engineering Checklist

```
PROVIDE (high impact):
- Clear problem statement
- Relevant background context
- Well-structured input data
- Desired output format
- Constraints and boundaries

AVOID (negative impact):
- Micromanaging reasoning steps
- Conversational padding ("please", "kindly")
- Over-specified step-by-step frameworks
- Excessive few-shot examples (AP-3: >2 format-only on GPT and other reasoning models; Claude 3-5 recommended; Gemini "a few")
- Prescriptive "think about X, then Y, then Z"
```

### Context Prioritization Matrix

| Component | Priority | Token Allocation | Notes |
|-----------|----------|------------------|-------|
| Task definition | Highest | 5-10% | Crystal clear, direct |
| Relevant background | High | 20-30% | Well-organized |
| Input data | High | 40-50% | Properly formatted |
| Output format | High | 5-10% | Explicit schema |
| Examples | Low | 0-10% | Format only; Claude 3-5, Gemini a few, others 0-2 |
| Reasoning guidance | **Avoid** | **0%** | Let model decide |

---

## 2. Prompt Structure

### Core Components

Every effective prompt contains some combination of:

- **Role/Identity**: System-level expertise assignment
- **Context**: Background information relevant to the task
- **Instruction**: The task directive
- **Input Data**: Content to process
- **Output Format**: Desired response structure
- **Constraints**: Boundaries and limitations

### Recommended Structure

```
[System Context / Role]     → WHO the model is
[Background / Context]      → WHAT it needs to know
[Task Instruction]          → WHAT to do
[Input Data]                → WITH what data
[Output Format]             → HOW to respond
[Constraints]               → WITHIN what limits
```

### Model-Specific Formatting

| Model Family | Preferred Format | Key Pattern |
|--------------|-----------------|-------------|
| Claude 5 family | XML tags | `<context>`, `<task>`, `<output_format>` |
| GPT-5.x / GPT-6 | Markdown or XML | XML tags now recommended |
| Gemini 3.x | XML or Markdown | Either works; be consistent within prompt |

### Delimiter Implementation

**Claude (XML -- strongly recommended)**:
```xml
<context>
Background information and relevant facts
</context>

<task>
Clear, direct instruction
</task>

<data>
Input data, well-structured
</data>

<output_format>
Desired format specification
</output_format>
```

**GPT-5 / Gemini (Markdown)**:
```markdown
## Context
Background information

## Task
Direct instruction

## Input
[data]

## Output Format
Specify format
```

---

## 3. Instruction Engineering

### 2026 Principle: Clarity Over Complexity

With reasoning models, simpler and more direct instructions outperform elaborate prompt engineering techniques.

**Before (over-engineered)**:
```
I need you to carefully analyze this code. Please follow these steps:
Step 1: First, read through the entire codebase
Step 2: Then, identify any potential bugs
Step 3: Next, think about security implications
Step 4: Consider performance issues
Step 5: Finally, provide your recommendations
Please be thorough and think step by step.
```

**After (2026 approach)**:
```
Analyze this code for bugs, security issues, and performance problems.

<code>
[code block]
</code>

Return findings as JSON: {"bugs": [], "security": [], "performance": []}
```

**Why**: Reasoning models decompose tasks internally. Explicit steps constrain their natural reasoning and waste tokens.

### Instruction Categories

| Category | Verbs | Use For |
|----------|-------|---------|
| Generative | create, write, develop, design | Content creation |
| Analytical | analyze, evaluate, compare, assess | Analysis tasks |
| Transformative | convert, translate, summarize, simplify | Data transformation |
| Classification | categorize, identify, label, sort | Categorization |
| Extraction | extract, find, parse, identify | Data extraction |

---

## 4. Thinking Modes & Reasoning

### 2026 Approach: Use Model-Native Thinking

Instead of prompt-based Chain-of-Thought, use each model's native reasoning capabilities.

> **Model-specific details**: See 06 (Claude), 07 (Gemini), 08 (GPT-5) for deep guidance.

### Overview by Model Family

**Claude 5 Family (Anthropic)** -- Adaptive Thinking + Effort:
```
Thinking defaults (per model):
- Fable 5.1 / Fable 5: always-on; type:"disabled" -> 400. Raw CoT never returned
- Opus 5.5: always-on; type:"disabled" -> 400 at every effort
- Sonnet 5.5: on; type:"disabled" -> 400. Lowest setting is
  type:"between_tools" (effort <=high only; accepts no display,
  budget_tokens or block_binding; no thinking on tool-less turns)
- Opus 5 (legacy): on; disabled only at effort <=high
- Sonnet 5 (legacy): on; type:"disabled" turns it off
- Opus 4.8 (legacy): off unless type:"adaptive" set
- Haiku 4.5: manual budget (budget_tokens:N); off by default

thinking.display: "omitted" (default on 5.x) | "summarized" | "updates" (beta).
On Fable 5.1 / Opus 5.5 / Sonnet 5.5, between-tool progress text arrives as
thinking blocks, empty under "omitted" -- set "updates" or "summarized" if
users need to see it.

Effort parameter (output_config.effort):
- low/medium/high/xhigh/max. Default differs per model (Opus 5.5: medium;
  Fable 5.1, Sonnet 5.5: high); setting the default equals omitting it
- Primary cost lever; controls thinking depth, NOT response length
- Does not transfer across models: only documented pairs hold
  (e.g. Opus 5.5 medium >= Opus 5 high). Re-sweep per model.

History: thinking blocks are bound to the conversation prefix on Fable 5.1 /
Opus 5.5 / Sonnet 5.5. Keep history append-only and pass thinking blocks back
unchanged; editing system, tools, or earlier turns -> 400 on newer accounts.

Best practice: Let model decide. Raise effort for depth, not "think harder".
```

**Gemini 3.x (Google)** -- Thinking Level:
```json
{
  "thinking": {"thinking_level": "medium"}  // nested, not top-level
  // low/medium/high; default differs per model (3.8/3.7 Flash: medium,
  // no `minimal`; 3.6 Flash: medium; 3.1 Pro: high). `minimal` exists on
  // 3.6 Flash, 3.5 Flash, Flash-Lite, 3 Flash -- and is an error on 3.7+
  // thinking_budget + thinking_level in one request -> 400
  // OMIT temperature/top_p/top_k entirely (deprecated Jul 2026: ignored on
  // 3.6+, sub-1.0 values can loop on older 3.x, 400 on future generations)
}
```

**GPT-5.x / GPT-6 (OpenAI)** -- Reasoning Effort:
```json
{
  "reasoning": {"effort": "medium"}  // Responses API. Enum is PER-MODEL:
                                     // GPT-5.5: none/low/medium/high/xhigh
                                     // GPT-5.6, GPT-6 Sol/Luna: none..max
                                     // GPT-6 Astra: low..max; "none" -> 400
                                     // Older GPT-5 base: minimal/low/medium/high
  // "mode": "standard"|"pro" is a separate reasoning field (5.6+, Responses only)
}
```
GPT-6 also adds `configuration_update`, an input item that changes effort mid-conversation without breaking the cache prefix (see 08).

### When Explicit CoT Still Works

- **Whenever extended thinking is OFF** -- Opus 4.8 (thinking off by default),
  Haiku 4.5, Sonnet 5 with `type:"disabled"`, and any legacy/open-weight model. Manual CoT is the documented
  fallback here, not an anti-pattern.
- For **output transparency** (showing work, not guiding reasoning)
- For **debugging/verification** (user needs to see the logic)
- **NOT** for telling a thinking-enabled model how to think -- there it duplicates
  native reasoning and costs tokens for no gain

---

## 5. Large Context Management

### Principles for 1M-class Token Windows (10M on Llama 4 Scout)

- **Structure over append**: Use clear markdown headers and sections, not raw text dumps
- **Strategic placement**: Critical information at beginning or end of context (high-recall zones)
- **Explicit retrieval**: Add instructions like "Scan the entire document before answering"
- **Hierarchical organization**: `# > ## > ### > ####` for navigable structure

### RAG vs Full Context

| Approach | When to Use | Context Size |
|----------|-------------|-------------|
| Full context | Document fits in window | <500K tokens |
| RAG (retrieval) | Knowledge base > context window | Any size |
| Hybrid | Large corpus, specific queries | Variable |

### Context Window Awareness

```
Signal to model:
"The following context contains [description]. Focus on [specific aspect]
relevant to the query at the end."

[Large context block]

"Based on the context above, [specific question]."
```

---

## 6. Hallucination Management

### Types

1. **Intrinsic**: Contradictions to provided context
2. **Extrinsic**: Unverifiable information outside provided context

### Mitigation Strategies

```xml
<grounding_rules>
- Only use information explicitly provided in the context
- For information not in context: "I don't have enough information"
- Cite specific parts of the context supporting each statement
- Distinguish between context-grounded and training-knowledge claims
</grounding_rules>
```

### Calibrated Uncertainty

| Phrase | Certainty | Use When |
|--------|-----------|----------|
| "Based on the provided context..." | Grounded | Citing context directly |
| "I'm confident that..." | >90% | Well-established facts |
| "I believe..." | 70-90% | Likely but not certain |
| "I'm not certain, but..." | 50-70% | Moderate uncertainty |
| "I don't have enough information" | <50% | Should not speculate |

### Knowledge Boundary Enforcement

```xml
<knowledge_boundaries>
You have access ONLY to:
1. Information in the provided context
2. Your training knowledge (with uncertainty acknowledged)

If asked about something not in context:
- Say "I don't have information about that in my current context"
- Do NOT make up facts, citations, or URLs
- Offer to help find the information if appropriate
</knowledge_boundaries>
```

---

## 7. Structured Outputs & Constrained Decoding

### JSON Mode

Most frontier models support native JSON output:

```python
# OpenAI
response = client.chat.completions.create(
    model="gpt-5.6-sol",
    response_format={"type": "json_object"},
    messages=[{"role": "user", "content": "Extract entities as JSON..."}]
)

# Anthropic
response = client.messages.create(
    model="claude-opus-5-5",
    messages=[...],
    # Structured outputs (output_config.format), or XML output tags / explicit
    # JSON instruction. No assistant prefill on 5.x (400).
)

# Google
response = model.generate_content(
    "Extract entities...",
    generation_config={"response_mime_type": "application/json"}
)
# generateContent only. On the Interactions API (GA, recommended) use
# response_format={"type": "text", "mime_type": "application/json", "schema": {...}}
```

### Schema Specification

Always provide the exact schema you expect:

```
Return JSON matching this schema exactly:
{
  "summary": "string",
  "key_findings": ["array of strings"],
  "metrics": {
    "score": "number (0.0-1.0)",
    "confidence": "number (0.0-1.0)"
  },
  "entities": [
    {"name": "string", "type": "person|org|location"}
  ]
}
```

### Output Format Best Practices

- Specify exact schema with types
- Use native JSON mode when available
- Validate output programmatically
- For Claude 5.x: prefill is a 400 and forced `tool_choice` (`any`/`tool`) is a 400 on Fable 5.1, Opus 5.5, Sonnet 5.5. Use structured outputs, or `tool_choice: auto` + `strict: true` tools; XML tags guide structure otherwise (Haiku 4.5 still accepts prefill)
- For Gemini: no prefill (a trailing model turn is a 400 on 3.6+); anchor format with `system_instruction` or a response schema
- Treat `stop_reason: "max_tokens"` as a failure even when the JSON parses

---

## 8. Prompt Caching & Token Efficiency

### Cache-Friendly Prompt Structure

Place stable content first, dynamic content last:

```
[1. SYSTEM PROMPT]         ← Cached (rarely changes)
[2. REFERENCE DOCUMENTS]   ← Cached (stable across requests)
[3. FEW-SHOT EXAMPLES]     ← Cached (if used)
[4. USER QUERY]            ← Not cached (changes per request)
```

### Provider-Specific Caching

| Provider | Mechanism | Max Savings |
|----------|-----------|-------------|
| Anthropic | Explicit `cache_control` breakpoints | ~90% on cached tokens |
| OpenAI | Automatic prefix caching; explicit `prompt_cache_options` (ttl, breakpoints) on GPT-5.6+ | ~90% on cached tokens |
| Google | Explicit cache creation via API | ~90% on cached tokens (excl. storage) |

Cache rules that bite:
- Minimum cacheable prompt is per model (Fable 5.1 / Opus 5.5 / Sonnet 5.5: 512 tokens; Sonnet 5 and Opus 4.8: 1,024; Haiku 4.5: 4,096) -- shorter prefixes silently don't cache
- Any edit to the stable prefix invalidates everything after it, including thinking blocks bound to it on current Claude
- Top-level effort changes break the cache on Claude 5.x: pick effort before the session, or use per-message effort (beta)
- Keep tool lists in a deterministic order; append-only history

### Token Efficiency Principles

1. **Zero-shot first**: Start without examples (saves tokens, often better quality)
2. **Minimal examples**: 1-2 for format on GPT and other reasoning models; Claude (3-5 diverse `<example>` tags) and Gemini (always a few, identically formatted) are the documented exceptions
3. **Structured output**: JSON is more token-efficient than verbose prose
4. **Remove fluff**: Every token of "please", "kindly" is waste
5. **Right-size models**: Use economy tier for simple tasks

---

## 9. What Still Works (2026)

| Technique | Status | Notes |
|-----------|--------|-------|
| Clear instructions | Essential | Foundation of all prompting |
| Rich context | Essential | Most impactful factor |
| Structured output | Essential | JSON/XML schemas |
| XML tags (Claude) | Essential | Primary structuring method |
| Role prompting | Effective | Keep concise |
| System instructions | Effective | Proper placement matters |
| 1 example for format | Effective | Format demo only |
| RAG | Essential | For knowledge > context window |

## 10. What's Deprecated (2026)

| Technique | Status | Why |
|-----------|--------|-----|
| Elaborate CoT | Deprecated | Models reason internally |
| Many-shot (>5 examples) | Deprecated | Can overwhelm native reasoning; 3-5 is the Claude range, and Gemini wants a few |
| "Let's think step by step" | Obsolete *when thinking is on* | Use thinking modes; still valid with thinking off |
| Complex prompt frameworks | Harmful | Simpler prompts work better |
| Conversational padding | Harmful | Especially bad for Gemini 3.x |
| Setting Gemini sampling params | Omit entirely (deprecated; ignored on 3.6+) | May cause loops/degradation |
| "Think" word (Claude, thinking off) | Harmful | Use "consider", "evaluate" |
| Sampling params on Claude 5.x / Gemini 3.6+ | Error or ignored | 400 on Claude 5.x; ignored on Gemini 3.6+. Omit |
| Assistant prefill, `budget_tokens` (Claude 5.x) | Removed | 400. Structured outputs / adaptive thinking (Haiku 4.5 exempt) |
| Carrying an effort level across models | Harmful | Enums and calibration are per model; re-sweep |

---

## Universal Principles (All Models, 2026)

1. **Clarity over cleverness**: Direct instructions outperform tricks
2. **Context quality > prompt phrasing**: Focus on WHAT you provide
3. **Simplicity wins**: Reasoning models work best with clear, minimal prompts
4. **Native features first**: Use thinking modes, structured outputs, caching; configure effort/thinking in the API call, not in prose
5. **Explain motivation**: WHY behind instructions helps models generalize
6. **Be direct**: Treat prompts as executable instructions
7. **Structure context**: Hierarchical organization, clear labels
8. **Specify constraints explicitly**: Models follow precise boundaries
9. **Let models reason**: Don't micromanage the thinking process
10. **Verify outputs**: Hallucination risk remains; always validate critical claims

---

This module is auto-loaded. For model-specific details, see:
- 03-model-catalog_v5.md (all model specs)
- 06-claude-practices_v5.md (Claude-specific)
- 07-gemini-practices_v5.md (Gemini-specific)
- 08-gpt5-practices_v5.md (GPT-5 and GPT-6-specific)
