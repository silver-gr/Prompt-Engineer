# GPT-5 & GPT-6 Practices (OpenAI, September 2026)

This is the dedicated module for OpenAI GPT prompting guidance: the GPT-6 family (Astra, Sol, Luna) and the GPT-5.x generations that remain live (5.6, 5.5 and earlier).

> **Model specs**: See 03-model-catalog_v5.md for GPT-6 and GPT-5 family data.
> **Anti-patterns**: See 02-techniques-patterns_v5.md (canonical).

---

## 1. Core Philosophy: Less Is More

GPT-5 and GPT-6 models perform best with **minimal, direct prompts**. Adding unnecessary instructions, verbose descriptions, or elaborate frameworks actively reduces quality. This is the single most important principle for the GPT family. OpenAI's own runs show the payoff: leaner prompts gave +10-15% eval score, -41-66% tokens and -33-67% cost (internal, directional). GPT-6 Astra follows longer instructions better than earlier models, so the harm is instability from conflicting or excess rules, not length alone; recipe-style, over-specific guidance can now hinder results.

---

## 2. Reasoning Effort and Verbosity

### Current API Surface

The **Responses API** is the current recommended surface for GPT-5.x and GPT-6 (GPT-6 Astra function calling requires it). Chat Completions remains supported -- it is not deprecated, it just uses flat parameter names (`reasoning_effort`) where Responses uses nested ones (`reasoning.effort`). Reasoning depth and output length are controlled by two independent parameters: `reasoning.effort` and `text.verbosity`. `reasoning.mode` (`standard` | `pro`, Responses only, GPT-5.6 and GPT-6) is a third independent knob and replaces separate Pro model slugs for 5.6+.

### `reasoning.effort` Selection

| Effort | Latency | Use For |
|--------|---------|---------|
| `"minimal"` | Ultra-fast | Older models only (e.g. GPT-5 base) -- lowest reasoning tier there; migrate to `low` |
| `"none"` | Ultra-fast | Zero reasoning overhead, trivial/simple tasks. **HTTP 400 on GPT-6 Astra** (use `low`) |
| `"low"` | Fast | Simple queries, lookups, formatting |
| `"medium"` | Default | General tasks, standard reasoning |
| `"high"` | Slower | Complex analysis, multi-step problems |
| `"xhigh"` | Slower still | Deep research, hard agentic/multi-step tasks needing maximum depth |
| `"max"` | Slowest | GPT-5.6 and later (all GPT-6 tiers) -- top tier |

**The enum is model-specific -- do not assume one set across the family:**

| Model | Supported values | Default |
|-------|-----------------|---------|
| GPT-5 (base) | `minimal` / `low` / `medium` / `high` (not re-verified this cycle — Verify) | `medium` |
| GPT-5.2 | `none` / `low` / `medium` / `high` / `xhigh` (not re-verified this cycle — Verify) | `none` |
| GPT-5.5 | `none` / `low` / `medium` / `high` / `xhigh` | `medium` |
| GPT-5.5 Pro | `medium` / `high` / `xhigh` | `high` |
| GPT-5.6 Sol / Terra / Luna | `none` / `low` / `medium` / `high` / `xhigh` / `max` | `medium` |
| GPT-6 Astra | `low` / `medium` / `high` / `xhigh` / `max` (`none` -> HTTP 400) | not documented |
| GPT-6 Sol / Luna | `none` / `low` / `medium` / `high` / `xhigh` / `max` | `medium` |

Passing `xhigh` or `none` to GPT-5 (base) (not re-verified this cycle — Verify), `none` to GPT-6 Astra, or `max` to anything below 5.6, is an error. Effort values do not transfer across models: preserve your current *effective* effort where supported, and sweep per model.

> **Parameter naming**: `reasoning.effort` is the **Responses API** spelling.
> Chat Completions uses the flat `reasoning_effort`. Both surfaces are supported;
> Responses is the recommended one for new integrations.

### Related Config (Responses API)

| Knob | Governs |
|------|---------|
| `reasoning.mode` | `standard` (default) or `pro`; independent of effort; Pro bills aggregated tokens at standard rates |
| `reasoning.context` | Which prior-turn reasoning is kept: `auto` (= `all_turns`, the default on 5.6+), `all_turns`, `current_turn` (default on earlier models) |
| `configuration_update` (GPT-6) | Input item that changes effort mid-conversation and keeps the cache prefix. No adjacent updates; incompatible with auto-compaction |
| `prompt_cache_options.ttl` (5.6+) | `"30m"`; replaces `prompt_cache_retention`, which applies to 5.5 and earlier only |

### `text.verbosity` Selection

Independent of reasoning effort, `text.verbosity` controls output length and detail:

| Verbosity | Use For |
|-----------|---------|
| `"low"` | Terse answers, extraction, formatting |
| `"medium"` | Default. General responses |
| `"high"` | Detailed explanations, long-form writing |

Documented on `gpt-6-astra`; support on GPT-6 Sol/Luna is not stated (Verify). GPT-5.6+ is more concise by default than 5.5, so a blunt "be concise" over-truncates: use `text.verbosity`, and say what a short answer must keep.

### Implementation

```json
{
  "model": "gpt-5.6-sol",
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
- **High/xhigh (GPT-5.6 and earlier)**: Complex work. Concrete validation steps pay off: "List assumptions", "Check the answer against the contract".
- **GPT-6 Astra**: Verification is native and over-applied at every tier -- calibrate it down rather than adding scaffolds.
- **Before raising effort**: check the prompt for a missing success criterion, dependency rule, tool-routing rule or verification loop. Effort is a tuning knob, not the quality fix.

**Critical**: On GPT-5.x, agentic persistence reminders are essential at none/low/medium reasoning effort; the model may conclude tasks prematurely without them. On GPT-6 Astra, early stopping and approval-seeking is a model trait at every effort level (Section 7).

```
Continue working until the task is fully complete. Do not stop early.
```

> **Correction**: earlier editions of this guide described a `reasoning_profile: "light" | "balanced" | "deep"` parameter for GPT-5.2. **`reasoning_profile` does not exist** in any OpenAI model's API -- GPT-5.2 uses `reasoning.effort` (`none` default, plus `low`/`medium`/`high`/`xhigh`; not re-verified this cycle — Verify) like the rest of the family. Disregard any prompt or integration built against `reasoning_profile`.

---

## 3. Prompt Structure

### Recommended Format

OpenAI's suggested structure for GPT-5.5/5.6 and later is Role, Personality, Goal, Success criteria, Constraints, Tools, Output, Stop rules. Keep each section short, and use only the sections the task needs.

```markdown
## Role
## Personality
## Goal
## Success criteria
## Constraints
## Tools
## Output
## Stop rules
```

Section headers can be swapped for XML tags (`<role>`, `<goal>`, `<constraints>`, `<output>`) -- both work, and XML is preferred for agentic/tool-heavy prompts where section boundaries need to be unambiguous. Keep one convention per prompt.

Use ALWAYS/NEVER/must only for true invariants; for judgment calls prefer decision rules. GPT models follow prompt contracts closely, so conflicting rules create more instability than missing detail.

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
    model="gpt-5.6-sol",
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

Keep tool descriptions **concise and precise**. State what the tool does, **when to use it**, important return fields and error behavior. Expose only task-relevant tools.

**Good**:
```json
{
  "name": "search_database",
  "description": "Search customers by name or ID. Use before any customer-specific action. Returns customer details; errors if no match.",
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

Verbose or redundant descriptions, and irrelevant tools left exposed, degrade tool selection.

---

## 6. Coding Tasks

### Best Practices
- Specify language and target environment
- State success criteria clearly
- Avoid over-specification -- GPT-5 writes better code with less constraint
- Do not rely on sampling params: on GPT-6, remove `temperature`, `top_p`, `top_logprobs` and `logprobs` when effort is not `none` (whether they error or are ignored: Verify)
- GPT-5.6: keep explicit validation (targeted tests, type check, build, smoke test) -- OpenAI recommends it. GPT-6 Astra over-tests: calibrate down ("Do not write tests for reversible, low-impact changes that mirror the implementation")

### Pattern
```
Write a Python function that:
- Merges two sorted lists into one sorted list
- Handles empty inputs
- Includes type hints

Return the function with 3 test cases.
```

**Don't**: Prescribe algorithm, specify variable names, or dictate code structure. Let the model make those decisions.

---

## 7. Model Generations: GPT-6, GPT-5.6, GPT-5.5

### Naming (highest-risk item)

- **GPT-6 order: Astra (top) > Sol (middle) > Luna (bottom).**
- GPT-6 Sol/Luna are **successors to**, not the same models as, GPT-5.6 Sol/Luna (different IDs, prices, cutoffs and parameter rules).
- **"Sol" names a different tier per generation.** In GPT-5.6 Sol is the flagship (about the unsuffixed tier; Terra ~ mini, Luna ~ nano). In GPT-6, Astra is the flagship and Sol is the middle tier.
- **Terra has no GPT-6 successor**, and Astra is not a renamed Terra. All GPT-5.6 models (`gpt-5.6-sol`, `gpt-5.6-terra`, `gpt-5.6-luna`) remain live, with no deprecation notice.

### GPT-6 (Astra, Sol, Luna)

| Tier | ID | Released | $ in / cached / out per 1M | Positioning |
|------|----|----------|----------------------------|-------------|
| Astra | `gpt-6-astra` | Sep 3 2026 | $10 / $1.00 / $50 | Hardest end-to-end work: ambiguous problems, deep analysis, ambitious deliverables |
| Sol | `gpt-6-sol` | Sep 22 2026 | $2 / $0.20 / $10 | Everyday driver: writing, coding, work that needs judgment |
| Luna | `gpt-6-luna` | Sep 22 2026 | $0.10 / $0.01 / $0.50 | Scoped, high-volume tasks: triage, frequent automations |

All three: 1,050,000-token context, 128,000 max output. Choose the tier by representative evals rather than routing everything to the most capable model, and preserve the workload role when migrating.

**API rules**:
- Astra: `reasoning.effort: "none"` returns HTTP 400 (migrate `none` to `low`); function calling requires the Responses API.
- Sol/Luna: function calling on Chat Completions only with `reasoning_effort: "none"`; use Responses for reasoning with tools.
- Remove `temperature`, `top_p`, `top_logprobs`, `logprobs` when effort is not `none` (error vs ignored: Verify).
- New: async tool calling (`async: true`, result returned later by `call_id`), mid-turn steering over WebSocket, `configuration_update`, misalignment monitoring (can return `403 misalignment_policy_violation`: stop dispatching, do not auto-retry).
- There is no separate Sol/Luna prompting guide; the official guidance addresses behavior observed on Astra. Guidance that helps Sol/Luna may over-constrain Astra, so evaluate per model and audit repo skills and AGENTS.md.

**Five Astra behaviors and remedies**:

| Behavior | Remedy |
|----------|--------|
| **Initiative**: asks non-blocking questions, stops when it should assume and persist (any effort level) | Define completion before starting. "Persist until the user's intended goal is complete." Ask for approval only after preparing a concrete, reviewable result |
| **Instruction following**: more sensitive to skills and AGENTS.md; unclear or conflicting guidance makes it pause | Audit skills and AGENTS.md. State: "The user's instructions take precedence over guidelines provided in a skill." |
| **Writing style**: heavy Markdown, recurring phrases across sessions | Specify the style (plain paragraphs, lists only for parallel or sequential info). Blocklist: "delve", "foster", "leverage", "it's worth noting", "importantly", "genuinely", "Bottom Line:", "In short:", contrastive "X, not Y" framing |
| **Delegation**: under-delegates | Say when and how much to delegate (e.g. "if it could save time or improve quality") |
| **Testing**: over-tests small tasks | Calibrate: no tests for reversible, low-impact changes that mirror the implementation; broaden only when changes, failures or open concerns justify it |

**Migration from GPT-5.5/5.6**: replace `prompt_cache_retention` with `prompt_cache_options.ttl: "30m"`; drop `none` on Astra; audit "ask first / wait for approval" language written for older, over-eager models -- Astra can take it too seriously and stall.

### GPT-5.6 Sol / Terra / Luna (prior generation, still live)

`gpt-5.6` aliases to `gpt-5.6-sol`. All three share a 1,050,000-token context and 128,000 max output; they differ by capability/price tier. Multi-agent orchestration is beta (Responses API only). Effort: `none` to `max` (default `medium`); `reasoning.context` defaults to `all_turns`.

**Official prompting guidance**:
- **Lean prompts win.** OpenAI reports 10-15% eval score gains with 41-66% fewer tokens.
- **State each instruction once.** Repetition degrades performance.
- **Don't over-repeat caution phrases** ("ask first", "wait for approval") -- this triggers unnecessary approval prompts.
- **More concise by default than GPT-5.5.** Use `text.verbosity`, not a blunt "be concise".
- **Keep concrete validation steps** (tests, type check, build); OpenAI recommends them on 5.6.

**Billing (GPT-6 and GPT-5.6)**: input above 272K tokens bills **2x input and cache rates and 1.5x output for the entire request**, not just the overage. Cache writes bill at 1.25x input (GPT-5.5: no write charge); reads 0.1x. Prices per specs: GPT-5.6 Sol $4 / $0.40 / $20 (promo from Aug 21 2026, "at least through Nov 21 2026"), Terra $2 / $0.20 / $12, Luna $0.20 / $0.02 / $1.20.

### GPT-5.5 (Prior Generation)

GPT-5.5 (`gpt-5.5`, $5 / $0.50 / $30) and `gpt-5.5-pro` remain live in the API. GPT-5.5 leaves ChatGPT and Codex on Oct 14 2026 (API unaffected). GPT-5.3 Instant (`gpt-5.3-chat-latest`) was shut down Aug 10 2026; "Instant" is now a ChatGPT thinking level, and the API alias is the rolling `chat-latest` (not for production).

### Model Selection

| Scenario | Use |
|----------|-----|
| Hardest reasoning, ambiguous or ambitious work | GPT-6 Astra |
| Everyday coding, writing, judgment work | GPT-6 Sol |
| High-volume, cost-sensitive, scoped tasks | GPT-6 Luna |
| Existing GPT-5.6 integrations | Keep on GPT-5.6 until evals justify moving; mid-tier is Terra (no GPT-6 successor) |
| Previous-generation frontier | GPT-5.5 (`reasoning.effort: "high"`/`"xhigh"`) |

---

## 8. Common Pitfalls

### Over-Prompting
Adding more instructions makes GPT output worse. Resist the urge to add "be thorough", "consider all angles". The model does this naturally. On GPT-6 Astra also drop "double-check your work" (AP-16); on GPT-5.6 keep concrete validation steps.

### Thoroughness vs Persistence
These are different. Thoroughness phrasing ("be thorough") is still unneeded -- remove it; "double-check your work" is droppable on GPT-6 Astra only (AP-16), while GPT-5.6 keeps concrete validation steps. Persistence and completion phrasing ("persist until the goal is complete", a definition of done) is officially recommended for GPT-6 Astra, which stops early and asks for approval at any effort level.

### Over-Repeated Caution Phrases
Repeating "ask first", "do not mutate" or "wait for approval" causes unnecessary approval requests; carried over from older models, it makes Astra stall. Say it once, or not at all.

### Absolute-Rule Overuse
ALWAYS/NEVER on judgment calls creates instability. Reserve them for true invariants.

### Raising Effort Instead of Fixing the Prompt
Check for a missing success criterion, dependency rule, routing rule or verification loop before raising effort.

### Verbose System Prompts
Long system prompts dilute important instructions. Keep system messages focused on role, constraints, and format.

### Ignoring Reasoning Effort
Defaulting to `medium` for everything wastes latency on simple tasks and misses depth on complex ones. Match `reasoning.effort` to task, per model.

### Missing Persistence Reminders
On GPT-5.x at `none`, `low`, and `medium` reasoning effort, agentic tasks may terminate prematurely (on Astra at any effort). Add explicit continuation instructions, or use the `<tool_persistence_rules>` contract tag (Section 10).

---

## 9. GPT Cheat Sheet (GPT-5.x and GPT-6)

```
DO:
- Keep prompts MINIMAL
- Use reasoning.effort -- but check the per-model enum (Section 2); it is NOT uniform
- Use text.verbosity: "low" | "medium" | "high" to control output length
- Prefer the Responses API (current surface) over legacy Chat Completions params
- Use XML or Markdown structure (XML now recommended, not Markdown-only)
- Concise tool descriptions: what, when to use, returns, errors
- Use JSON mode for structured output
- System messages for role and constraints
- Specify language and success criteria for code
- Add persistence reminders, or `<tool_persistence_rules>`, for agentic tasks; for Astra add an initiative line and a completion definition
- Never send `reasoning.effort: none` to GPT-6 Astra; never use `reasoning_profile` (does not exist)
- Remove sampling params (`temperature`, `top_p`) on GPT-6
- Use the agentic contract tag set (Section 10) for tool-heavy tasks

DON'T:
- Over-prompt (reduces quality)
- Write verbose or redundant tool descriptions
- Repeat instructions or caution phrases for emphasis
- Reuse an effort value across models (enum is per-model)
- Force reasoning on simple tasks
- Use elaborate frameworks or CoT
- Add unnecessary "be thorough" instructions

TEMPLATE:
## Role
## Personality
## Goal
## Success criteria
## Constraints
## Tools
## Output
## Stop rules
```

---

## 10. Agentic Contract Tags (GPT-5.4 Guide Set)

For agentic and tool-heavy prompts, OpenAI's GPT-5.4 guide replaced the older ad-hoc `<persistence>` / `<dig_deeper_nudge>` style reminders with a structured set of contract tags. The 5.5, 5.6 and GPT-6 guides use plain labeled sections instead (Section 3), so treat these tags as a proven convention rather than the current official set; on 5.6+, `<tool_orchestration>` routes Programmatic Tool Calling. Use whichever are relevant to the task -- not every prompt needs all of them.

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

This guards against both premature stopping (the low-effort problem) and unnecessary over-searching.

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
- [OpenAI Latest Model Guide (GPT-6)](https://developers.openai.com/api/docs/guides/latest-model)
