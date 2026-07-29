# GPT-5 Practices (OpenAI, March 2026)

This is the dedicated module for GPT-5 family prompting guidance -- the first time GPT-5 gets its own reference (Claude and Gemini already had theirs).

> **Model specs**: See 03-model-catalog_v5.md for GPT-5 family data.
> **Anti-patterns**: See 02-techniques-patterns_v5.md (canonical).

---

## 1. Core Philosophy: Less Is More

GPT-5 models perform best with **minimal, direct prompts**. Adding unnecessary instructions, verbose descriptions, or elaborate frameworks actively reduces quality. This is the single most important principle for GPT-5.

---

## 2. Reasoning Effort and Verbosity

### Current API Surface

The **Responses API** is the current recommended surface for GPT-5.x. Chat Completions remains supported -- it is not deprecated, it just uses flat parameter names (`reasoning_effort`) where Responses uses nested ones (`reasoning.effort`). Reasoning depth and output length are controlled by two independent parameters: `reasoning.effort` and `text.verbosity`.

### `reasoning.effort` Selection

| Effort | Latency | Use For |
|--------|---------|---------|
| `"minimal"` | Ultra-fast | GPT-5 (base) only -- lowest reasoning tier on that model |
| `"none"` | Ultra-fast | Zero reasoning overhead, trivial/simple tasks |
| `"low"` | Fast | Simple queries, lookups, formatting |
| `"medium"` | Default | General tasks, standard reasoning |
| `"high"` | Slower | Complex analysis, multi-step problems |
| `"xhigh"` | Slower still | Deep research, hard agentic/multi-step tasks needing maximum depth |
| `"max"` | Slowest | GPT-5.6 only -- new top tier |

**The enum is model-specific -- do not assume one set across the family:**

| Model | Supported values | Default |
|-------|-----------------|---------|
| GPT-5 (base) | `minimal` / `low` / `medium` / `high` | `medium` |
| GPT-5.2 | `none` / `low` / `medium` / `high` / `xhigh` | `none` |
| GPT-5.5 | `none` / `low` / `medium` / `high` / `xhigh` | `medium` |
| GPT-5.6 Sol / Terra / Luna | `none` / `low` / `medium` / `high` / `xhigh` / `max` | `medium` |

Passing `xhigh` or `none` to GPT-5 (base), or `max` to anything below 5.6, is an error.

> **Parameter naming**: `reasoning.effort` is the **Responses API** spelling.
> Chat Completions uses the flat `reasoning_effort`. Both surfaces are supported;
> Responses is the recommended one for new integrations.

### `text.verbosity` Selection

Independent of reasoning effort, `text.verbosity` controls output length and detail:

| Verbosity | Use For |
|-----------|---------|
| `"low"` | Terse answers, extraction, formatting |
| `"medium"` | Default. General responses |
| `"high"` | Detailed explanations, long-form writing |

### Implementation

```json
{
  "model": "gpt-5.5",
  "reasoning": {"effort": "high"},
  "text": {"verbosity": "medium"},
  "input": [
    {"role": "system", "content": "You are a code reviewer."},
    {"role": "user", "content": "Review this code for security issues:\n[code]"}
  ]
}
```

### Effort Best Practices

- **None/Low**: Fast responses. Add persistence reminders for agentic tasks -- model may stop early.
- **Medium**: Default. Good for most tasks. No special considerations.
- **High/xhigh**: Complex work. Combine with verification scaffolds: "List assumptions", "Verify answer".

**Critical**: Agentic persistence reminders are essential at none/low/medium reasoning effort. The model may conclude tasks prematurely without them.

```
Continue working until the task is fully complete. Do not stop early.
```

> **Correction**: earlier editions of this guide described a `reasoning_profile: "light" | "balanced" | "deep"` parameter for GPT-5.2. **No such parameter appears in OpenAI's GPT-5.2 documentation** -- GPT-5.2 uses `reasoning.effort` (`none` default, plus `low`/`medium`/`high`/`xhigh`) like the rest of the family. Disregard any prompt or integration built against `reasoning_profile`.

---

## 3. Prompt Structure

### Recommended Format

Earlier GPT-5 guidance was Markdown-only. Current guidance now recommends **XML tags** for structuring prompts as well -- both work, but XML is preferred for agentic/tool-heavy prompts where section boundaries need to be unambiguous.

```markdown
## Task
[concise instruction]

## Context
[relevant background -- keep minimal]

## Input
[data to process]

## Output Format
[JSON schema or format spec]
```

```xml
<task>[concise instruction]</task>
<context>[relevant background -- keep minimal]</context>
<input>[data to process]</input>
<output_format>[JSON schema or format spec]</output_format>
```

### System Messages

System messages are strongly prioritized by GPT-5. Use them for:
- Role definition
- Persistent constraints
- Output format requirements

```json
{
  "messages": [
    {
      "role": "system",
      "content": "You are a data analyst. Return all responses as valid JSON."
    },
    {
      "role": "user",
      "content": "Analyze quarterly revenue trends from this data:\n[data]"
    }
  ]
}
```

---

## 4. JSON Mode & Structured Outputs

GPT-5 has excellent native JSON mode:

```python
response = client.chat.completions.create(
    model="gpt-5.2",
    response_format={"type": "json_object"},
    messages=[
        {"role": "system", "content": "Return valid JSON."},
        {"role": "user", "content": "Extract entities from: [text]"}
    ]
)
```

### Best Practices
- Always include "JSON" in the system or user message when using JSON mode
- Provide exact schema with types
- Validate output programmatically
- JSON mode ensures syntactically valid output

---

## 5. Tool Descriptions

Keep tool descriptions **crisp** -- 1-2 sentences maximum.

**Good**:
```json
{
  "name": "search_database",
  "description": "Search customers by name or ID. Returns customer details.",
  "parameters": {
    "query": {"type": "string", "description": "Name or customer ID"},
    "field": {"type": "string", "enum": ["name", "id"]}
  }
}
```

**Bad** (over-described, reduces quality):
```json
{
  "description": "This function allows you to search through the customer
  database. You should use this when the user asks about a customer. It can
  search by name or ID. When searching by name, partial matches are returned..."
}
```

GPT-5 infers tool usage well from concise descriptions. Verbose descriptions actually degrade performance.

---

## 6. Coding Tasks

### Best Practices
- Specify language and target environment
- State success criteria clearly
- Avoid over-specification -- GPT-5 writes better code with less constraint
- Lower temperature (0.1-0.3) for deterministic output

### Pattern
```
Write a Python function that:
- Merges two sorted lists into one sorted list
- Handles empty inputs
- Includes type hints

Return the function with 3 test cases.
```

**Don't**: Prescribe algorithm, specify variable names, or dictate code structure. Let GPT-5 make those decisions.

---

## 7. GPT-5.5 (Prior Flagship)

**GPT-5.6 Sol is the current flagship** -- the `gpt-5.6` alias routes to `gpt-5.6-sol`. GPT-5.5 is the prior flagship, still widely deployed and accessed via the Responses API. GPT-5.2 Thinking -- once "SOTA for chatbot use" -- is superseded for new integrations but remains supported.

Key characteristics:
- Frontier reasoning via `reasoning.effort` control (see Section 2)
- Cleaner formatting and less verbosity than predecessors
- Strong instruction adherence
- Excellent tool grounding

### When to Use GPT-5.5 vs GPT-5.3 Instant

| Scenario | Use |
|----------|-----|
| Complex analysis, research | GPT-5.5 (`reasoning.effort: "high"`/`"xhigh"`) |
| Frontier capability | GPT-5.6 Sol |
| Balanced capability/cost | GPT-5.6 Terra |
| High-volume, cost-sensitive | GPT-5.6 Luna |
| Multi-step reasoning | GPT-5.6 Sol / GPT-5.5 |
| Coding with edge cases | GPT-5.6 Sol |
| Real-time chat, simple queries | GPT-5.6 Luna / GPT-5.3 Instant |

### GPT-5.6 Sol / Terra / Luna (GA, July 9 2026)

All three share a 1,050,000-token context (max input 922,000) and 128,000 max output; they differ by capability/price tier, not context size. GA on Responses, Chat Completions, and Batch APIs; multi-agent orchestration is beta (Responses API only).

**`reasoning.effort`**: `none` | `low` | `medium` (default) | `high` | `xhigh` | `max` — the `max` tier is new in this release. Persisted reasoning across turns is supported.

**Official prompting guidance**:
- **Lean prompts win.** OpenAI reports 10-15% eval score gains with 41-66% fewer tokens.
- **State each instruction once.** Repetition degrades performance.
- **Don't over-repeat caution phrases** ("ask first", "wait for approval") — this triggers unnecessary approval prompts.
- **More concise by default than GPT-5.5.** A blunt "be concise" instruction can over-truncate; use `text.verbosity` instead.

**Cost gotchas**: input above 272K tokens bills **2x input / 1.5x output for the entire request**, not just the overage. Cache writes bill at 1.25x standard input rate.

---

## 8. Common Pitfalls

### Over-Prompting
Adding more instructions makes GPT-5 output worse. Resist the urge to add "be thorough", "consider all angles", "double-check your work". The model does this naturally.

### Verbose System Prompts
Long system prompts dilute important instructions. Keep system messages focused on role, constraints, and format.

### Ignoring Reasoning Effort
Defaulting to `medium` for everything wastes latency on simple tasks and misses depth on complex ones. Match `reasoning.effort` to task.

### Missing Persistence Reminders
At `none`, `low`, and `medium` reasoning effort, agentic tasks may terminate prematurely. Add explicit continuation instructions, or use the `<tool_persistence_rules>` contract tag (Section 10).

---

## 9. GPT-5 Cheat Sheet

```
DO:
- Keep prompts MINIMAL
- Use reasoning.effort -- but check the per-model enum (Section 2); it is NOT uniform
- Use text.verbosity: "low" | "medium" | "high" to control output length
- Prefer the Responses API (current surface) over legacy Chat Completions params
- Use XML or Markdown structure (XML now recommended, not Markdown-only)
- Crisp tool descriptions (1-2 sentences)
- Use JSON mode for structured output
- System messages for role and constraints
- Specify language and success criteria for code
- Add persistence reminders, or `<tool_persistence_rules>`, for agentic tasks
- Use the agentic contract tag set (Section 10) for tool-heavy tasks

DON'T:
- Over-prompt (reduces quality)
- Write verbose tool descriptions
- Force reasoning on simple tasks
- Use elaborate frameworks or CoT
- Add unnecessary "be thorough" instructions

TEMPLATE:
## Task
[concise instruction]

## Input
[data]

## Output Format
[JSON schema or format spec]
```

---

## 10. Agentic Contract Tags (GPT-5.5)

For agentic and tool-heavy prompts, current GPT-5.5 guidance replaces the older ad-hoc `<persistence>` / `<dig_deeper_nudge>` style reminders with a structured set of contract tags. Use whichever are relevant to the task -- not every prompt needs all of them.

| Tag | Purpose |
|-----|---------|
| `<output_contract>` | Defines the exact shape/format the final answer must take |
| `<tool_persistence_rules>` | States when to keep using tools vs. stop (replaces ad-hoc "keep going" reminders) |
| `<completeness_contract>` | States what "done" means for the task |
| `<verification_loop>` | Requires the model to check its own output against the task before finishing |
| `<citation_rules>` | Requires sources/evidence for claims, and how to format them |
| `<research_mode>` | Governs multi-step information-gathering behavior (search budget, escalation rules) |
| `<empty_result_recovery>` | What to do when a tool/search returns nothing -- retry strategy vs. give up |
| `<dependency_checks>` | Verify prerequisite state/files/data exist before acting |
| `<instruction_priority>` | Resolves conflicts between system, developer, and user instructions |
| `<memo_mode>` | Produces a running summary/memo of progress for long agentic sessions |

### Stop-Condition Guidance

Inside `<verification_loop>` or `<completeness_contract>`, state an explicit stop condition:

```
Use the minimum evidence sufficient to answer, cite it, then stop.
```

This guards against both premature stopping (the old light/low-effort problem) and unnecessary over-searching.

### Retrieval Budget Guidance

Inside `<research_mode>`, set an explicit search budget:

```
Run one broad search first. Only run additional searches if the broad
search leaves facts missing or contradicted.
```

Jumping straight to narrow, repeated searches wastes tool calls and latency. Prefer one broad pass first, then targeted follow-ups only if needed.

### Example Skeleton

```xml
<output_contract>
Return a markdown report with sections: Summary, Findings, Sources.
</output_contract>

<tool_persistence_rules>
Keep using tools until the task's stated goal is met. Do not stop after
the first partial result.
</tool_persistence_rules>

<research_mode>
Run one broad search first. Escalate to additional searches only if
facts are missing or contradicted.
</research_mode>

<verification_loop>
Before returning, check the output against <output_contract>. Use the
minimum evidence sufficient to answer, cite it, then stop.
</verification_loop>

<citation_rules>
Cite every factual claim with a source. No uncited claims.
</citation_rules>
```

---

## References

- [OpenAI GPT-5 Platform Documentation](https://platform.openai.com/docs)
- [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)
- [GPT-5 Best Practices](https://platform.openai.com/docs/guides/gpt-best-practices)
