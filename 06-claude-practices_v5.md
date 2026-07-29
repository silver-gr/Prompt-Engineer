# Claude Practices (Anthropic, July 2026)

This module documents Claude-specific prompting patterns for the **Claude 5 family** (Fable 5, Opus 5, Sonnet 5) and **Opus 4.8**. Canonical home for Claude agentic XML blocks, model-specific guidance, and migration patterns.

> **Model specs**: 03-model-catalog_v5.md for full pricing/specs.
> **Anti-patterns**: 02-techniques-patterns_v5.md (canonical).
> **Agentic patterns**: 10-agentic-patterns_v5.md for general agent design.

---

## 1. General Principles

### 1.1 Be Clear and Direct

Claude 5-family models follow instructions precisely. Being specific about desired output enhances results. "Above and beyond" behavior requires explicit requests.

**Less effective**: `Create an analytics dashboard`

**More effective**: `Create an analytics dashboard. Include as many relevant features and interactions as possible. Go beyond the basics to create a fully-featured implementation.`

### 1.2 Explain WHY, Not Just WHAT

Claude generalizes from explanatory context. Providing motivation behind instructions significantly improves performance.

**Less effective**: `NEVER use ellipses`

**More effective**: `Your response will be read aloud by a text-to-speech engine, so never use ellipses since the engine will not know how to pronounce them.`

### 1.3 Use Examples Effectively

3-5 well-crafted examples in `<example>` tags improve accuracy. Make them relevant, diverse, and structured. Avoid unintended patterns from inconsistent examples.

### 1.4 Concise, Direct Communication

Claude 5-family models are more direct and conversational. Fact-based progress reports, less self-celebratory.

**Opus 5 exception**: Default responses run longer than prior models. Prompt explicitly for conciseness:
```
Keep responses focused, brief, and concise. Keep disclaimers and caveats short,
and spend most of the response on the main answer.
```

For long system prompts, pair with a reminder near the end:
```xml
<tone_preference>
Keep outputs reasonably concise.
</tone_preference>
```

### 1.5 Literal Instruction Following (Sonnet 5)

Sonnet 5 interprets prompts literally, especially at lower effort levels. It does not silently generalize instructions. If you need an instruction applied broadly, state the scope explicitly:

```
Apply this formatting to every section, not just the first one.
```

---

## 2. Thinking Modes (July 2026)

### Per-Model Thinking Defaults

| Model | Default | Turn Off | Config |
|-------|---------|----------|--------|
| **Fable 5** | Always-on | Cannot (`disabled` → 400) | `thinking:{type:"adaptive"}` only |
| **Opus 5** | On by default | `disabled` (only at effort ≤high) | `thinking:{type:"adaptive"}` |
| **Opus 4.8** | Off unless set | N/A (already off) | Set `thinking:{type:"adaptive"}` |
| **Sonnet 5** | On by default | `thinking:{type:"disabled"}` | `thinking:{type:"adaptive"}` |
| **Haiku 4.5** | Manual budget | N/A | `thinking:{type:"enabled",budget_tokens:N}` |

### Effort Parameter

`output_config: {effort: "..."}` controls how much the model thinks, not how much it says. It is **soft behavioral guidance, not a hard cap** -- `max_tokens` remains the only strict ceiling.

| Level | Use For |
|-------|---------|
| `low` | Short, scoped tasks, latency-sensitive |
| `medium` | Cost-sensitive, still strong (Sonnet 5 medium ≈ 4.6 high) |
| `high` | Default. Most tasks. |
| `xhigh` | Hardest coding and agentic work |
| `max` | Absolute maximum capability, no token constraints |

**Key insight**: effort levels do not transfer across models. Anthropic documents Sonnet 5 `medium` ≈ Sonnet 4.6 `high` and Sonnet 5 `high` ≈ Sonnet 4.6 `max`; treat that as a Sonnet-specific mapping, not a family-wide "low/medium beats prior xhigh" rule. Start at default, sweep your evals per model.

### Steering Adaptive Thinking

When model thinks more than needed (large/complex system prompts):
```
Thinking adds latency and should only be used when it will meaningfully improve
answer quality -- typically for problems that require multistep reasoning.
When in doubt, respond directly.
```

When running hard workloads at `medium` and seeing under-thinking, raise effort first. If finer control needed:
```
This task involves multistep reasoning. Think carefully through the problem
before responding.
```

### Interleaved Thinking

Guide reflection after tool use:
```
After receiving tool results, carefully reflect on their quality and determine
optimal next steps before proceeding. Use your reasoning to plan and iterate
based on new information, then take the best next action.
```

---

## 3. Long-Horizon Reasoning & State Tracking

### 3.1 Context Awareness

Context awareness -- tracking remaining token budget -- is documented for Sonnet 5, Sonnet 4.6, Sonnet 4.5, and Haiku 4.5. Do not assume it on every Claude model. For agent harnesses with context compaction:

```xml
<context_management>
Your context window will be automatically compacted as it approaches its limit,
allowing you to continue working indefinitely. Do not stop tasks early due to
token budget concerns. Save current progress and state to memory before context
refreshes. Always be persistent and autonomous -- complete tasks fully even if
the end of your budget is approaching.
</context_management>
```

**Fable 5 context-budget concern**: In very long sessions, Fable 5 can occasionally suggest a new session or offer to summarize. Avoid surfacing explicit context-budget counts. If the harness must show them:
```
You have ample context remaining. Do not stop, summarize, or suggest a new
session on account of context limits. Continue the work.
```

### 3.2 Multi-Context Window Workflows

1. **First window**: Set up framework (write tests, create setup scripts, define success criteria)
2. **Subsequent windows**: Iterate on todo-list structured state files
3. **Fresh context**: Start with prescriptive discovery instructions:

```
Call pwd; you can only read and write files in this directory.
Review progress.txt, tests.json, and the git logs.
Manually run through a fundamental integration test before moving on.
```

4. **Encourage full context usage**:
```
This is a very long task, so plan your work clearly. It's encouraged to spend
your entire output context working on the task -- just make sure you don't run
out of context with significant uncommitted work.
```

### 3.3 State Management

| Format | Use For |
|--------|---------|
| **Structured (JSON)** | Test results, task status, schema-dependent data |
| **Unstructured (text)** | Progress notes, general context |
| **Git** | State tracking, checkpoints, session history |

### 3.4 Memory Systems (Fable 5)

Fable 5 performs notably better with a persistent memory file:
```
Store one lesson per file with a one-line summary at the top. Record corrections
and confirmed approaches alike, including why they mattered. Don't save what the
repo or chat history already records; update an existing note rather than creating
a duplicate; delete notes that turn out to be wrong.
```

Bootstrap from history:
```
Reflect on the previous sessions we've had together. Use subagents to identify
core themes and lessons, and store them in [X]. Make sure you know to reference
[X] for future use.
```

---

## 4. Tool Usage Patterns

### 4.1 Proactive vs Conservative Action

**Proactive** (default -- implement changes):
```xml
<default_to_action>
By default, implement changes rather than only suggesting them. If the user's
intent is unclear, infer the most useful likely action and proceed, using tools
to discover missing details instead of guessing.
</default_to_action>
```

**Conservative** (suggest first):
```xml
<do_not_act_before_instructions>
Do not jump into implementation unless clearly instructed. Default to providing
information and recommendations rather than taking action.
</do_not_act_before_instructions>
```

### 4.2 Tool Triggering

Claude 5-family models are highly responsive to system prompts. Over-aggressive language causes overtriggering:

| Overtriggers | Balanced |
|--------------|----------|
| `CRITICAL: You MUST use tool when...` | `Use tool when...` |
| `ALWAYS call function` | `Call this function when appropriate` |
| `If in doubt, use [tool]` | Remove (triggers appropriately now) |

**Sonnet 5 with thinking off**: Less likely to reach for tools. Add explicit nudge if you rely on tool calls with thinking disabled.

### 4.3 Parallel Tool Calling

All Claude 5-family models run independent tool calls in parallel:

```xml
<use_parallel_tool_calls>
If you intend to call multiple tools and there are no dependencies between the
calls, make all independent calls in parallel. Maximize use of parallel tool
calls for speed and efficiency. If some calls depend on previous results, call
them sequentially. Never use placeholders or guess missing parameters.
</use_parallel_tool_calls>
```

**Reduce parallelization** (for stability):
```
Execute operations sequentially with brief pauses between each step.
```

---

## 5. Agentic Coding Patterns

### 5.1 Minimize Hallucinations

```xml
<investigate_before_answering>
Never speculate about code you have not opened. If the user references a
specific file, you MUST read the file before answering. Never make claims
about code before investigating -- give grounded, hallucination-free answers.
</investigate_before_answering>
```

### 5.2 Prevent Overengineering

```xml
<scope_control>
Don't add features, refactor, or introduce abstractions beyond what the task
requires. A bug fix doesn't need surrounding cleanup; a one-shot operation
doesn't need a helper. Don't design for hypothetical future requirements.
Don't add error handling, fallbacks, or validation for scenarios that can't
happen. Trust internal code and framework guarantees. Only validate at system
boundaries (user input, external APIs).
</scope_control>
```

### 5.3 Self-Verification (Opus 5 / Fable 5)

**Remove *redundant* verification instructions.** Opus 5 and Fable 5 self-verify without prompting, so carrying over "double-check your answer" or "include a final verification step" from prior-model prompts causes over-verification -- extra cost with no quality gain.

This is **not** a blanket ban. Anthropic explicitly recommends making periodic self-verification explicit for *long-running* Fable 5 tasks, where the model cannot otherwise know when to checkpoint:

Pattern for that case:
```
Establish a method for checking your own work at an interval of [X] as you
build. Run this every [X interval], verifying your work with subagents against
the specification.
```

### 5.4 Progress Grounding (Fable 5)

Ground progress claims against tool results to prevent fabricated status reports:
```
Before reporting progress, audit each claim against a tool result from this
session. Only report work you can point to evidence for; if something is not
yet verified, say so explicitly. Report outcomes faithfully: if tests fail,
say so with the output; if a step was skipped, say that.
```

### 5.5 Action Boundaries (Fable 5)

Fable 5 can take unrequested actions (drafting emails, creating git backups). Define explicit boundaries:
```
When the user is describing a problem, asking a question, or thinking out loud
rather than requesting a change, the deliverable is your assessment. Report
your findings and stop. Don't apply a fix until they ask for one.
```

### 5.6 General-Purpose Solutions

```
Write a high-quality, general-purpose solution using standard tools. Do not
create helper scripts or workarounds. Implement a solution that works correctly
for all valid inputs, not just the test cases. Do not hard-code values.
```

### 5.7 File Cleanup

```
If you create any temporary files, scripts, or helper files for iteration,
clean up by removing them at the end of the task.
```

---

## 6. Output Format Control

### Tell Claude What TO DO (not what not to do)

Instead of: `"Do not use markdown"`

Use: `"Write in smoothly flowing prose paragraphs."`

### XML Format Indicators

```
Write prose sections in <smoothly_flowing_prose_paragraphs> tags.
```

### Detailed Formatting

```xml
<avoid_excessive_markdown_and_bullet_points>
When writing long-form content, write in clear, flowing prose using complete
paragraphs and sentences. Reserve markdown primarily for inline code, code
blocks, and simple headings.

DO NOT use ordered/unordered lists unless:
a) presenting truly discrete items where list format is optimal, or
b) the user explicitly requests a list

Instead of listing items with bullets, incorporate them naturally into sentences.
</avoid_excessive_markdown_and_bullet_points>
```

### Written Deliverable Length (Opus 5)

Files written to disk by Opus 5 (reports, documents) are often longer than prior models:
```
Match the length of written documents to what the task needs: cover the
substance, but do not pad with filler sections, redundant summaries, or
boilerplate.
```

### LaTeX Output

Current models default to LaTeX for math. For plain text:
```
Format your response in plain text only. Do not use LaTeX, MathJax, or any
markup notation. Write all math expressions using standard text characters.
```

### Prompt Style Matching

The formatting style in your prompt influences response style. Removing markdown from your prompt reduces markdown in output.

---

## 7. Claude Research Tool

### Core Functionality

Claude Research tool conducts multi-step investigations via 5-20+ web searches, synthesizing findings into citation-backed reports.

### Activation Requirements
- Available in Claude.ai web/desktop/mobile interfaces only (NOT via API)
- Requires paid plan (Pro, Max, Team, Enterprise)
- Manual toggle: enable web search, then click "Research" button

### Effective Research Patterns

**Research + Analysis**:
```xml
<context>
We're evaluating whether to migrate from Postgres to a NewSQL database.
</context>

<task>
Research CockroachDB and TiDB.
</task>

<requirements>
1. Migration complexity from Postgres
2. Performance for OLTP workloads
3. Cost comparison for 5TB dataset
4. Production incident reports and reliability track record
</requirements>
```

**Quote-First Method**: For long documents, ask Claude to extract direct quotes first, then analyze using only quotes. Grounds responses in actual text.

### Research Tool Comparison

| Feature | Claude Research | Gemini Deep Research | ChatGPT Deep Research |
|---------|----------------|---------------------|-----------------------|
| Sources per query | 5-20+ | 40-250+ | 10-50+ |
| Context window | 1M | 1M | 128K |
| Strength | Document analysis, uncertainty | Breadth, cost | Polished reports |

---

## 8. Subagent Orchestration

### Per-Model Delegation Behavior

| Model | Delegation Style |
|-------|-----------------|
| **Fable 5** | Most aggressive; dispatches parallel subagents readily; supports long-lived agents |
| **Opus 5** | Delegates readily; effective writer-verifier patterns; few overwrite conflicts |
| **Opus 4.8** | Dynamic workflows; hundreds of parallel subagents in one session |
| **Sonnet 5** | More agentic than Sonnet 4.6; higher tool usage at high/xhigh effort |

### Controlling Delegation

**Damping** (prevent excessive subagent use):
```
Delegate to a subagent only for large tasks that are genuinely independent and
parallelizable. Do not delegate work you can finish yourself in a handful of
tool calls, and do not use subagents to verify or double-check your own work.
If one subagent can complete the task, use one rather than several.
```

**Encouraging** (Fable 5 long runs):
```
Delegate independent subtasks to subagents and keep working while they run.
Intervene if a subagent goes off track or is missing relevant context.
```

### send-to-user Tool (Fable 5)

For long async agents, a tool that delivers messages verbatim mid-turn without ending it:
```json
{
  "name": "send_to_user",
  "description": "Display a message directly to the user. Use for progress updates, partial results, or content the user must see exactly as written before the task finishes.",
  "input_schema": {
    "type": "object",
    "properties": {
      "message": { "type": "string", "description": "Content to display." }
    },
    "required": ["message"]
  }
}
```

Pair with system prompt guidance:
```
Between tool calls, when you have content the user must read verbatim (a partial
deliverable, a direct answer to their question), call send_to_user. Use it only
for user-facing content, not for narration or reasoning.
```

### Cost Pattern: Orchestrator + Executor

Dominant 2026 pattern: **Fable 5 as orchestrator, Sonnet 5/Opus 4.8 as executor**. Long-lived subagents save time through cache-read savings and avoid bottlenecking on the slowest agent.

---

## 9. Frontend Design

Without guidance, Claude models can default to generic "AI slop" aesthetics. Sonnet 5 may settle into a consistent default visual style.

```xml
<frontend_aesthetics>
NEVER use generic AI-generated aesthetics like overused font families (Inter,
Roboto, Arial, system fonts), cliched color schemes (particularly purple
gradients on white or dark backgrounds), predictable layouts and component
patterns, and cookie-cutter design. Use unique fonts, cohesive colors and
themes, and animations for effects and micro-interactions.
</frontend_aesthetics>
```

**Two reliable approaches for Sonnet 5**:

1. **Specify a concrete alternative** -- the model follows explicit visual specs precisely (provide hex colors, font names, spacing, radius values)

2. **Have the model propose options before building**:
```
Before building, propose 4 distinct visual directions tailored to this brief
(each as: bg hex / accent hex / typeface, plus a one-line rationale). Ask the
user to pick one, then implement only that direction.
```

---

## 10. Vision Capabilities

Claude Opus 5 and Fable 5 have substantially improved vision:
- Strong on chart, document, diagram understanding
- UI and frontend visual replication
- Vision performance strongest with tools to iteratively analyze, crop, and verify
- Tool use is a more cost-effective lever for vision than thinking alone

**Performance boost**: Give Claude a crop tool to "zoom" in on relevant regions. Consistent uplift on image evaluations.

**Computer use** (Sonnet 5): `computer_20251124` tool version. Up to 2576px / 3.75MP max resolution. 1080p = good balance of performance and cost. 720p/1366x768 for cost-sensitive workloads.

---

## 11. Model Self-Knowledge

```
The assistant is Claude, created by Anthropic. The current model is Claude Opus 5.
```

For API strings:
```
When an LLM is needed, default to Claude Opus 5 unless the user requests
otherwise. The exact model string for Claude Opus 5 is claude-opus-5.
```

Current model IDs:
- `claude-fable-5` -- Fable 5
- `claude-opus-5` -- Opus 5
- `claude-opus-4-8` -- Opus 4.8
- `claude-sonnet-5` -- Sonnet 5
- `claude-haiku-4-5-20251001` -- Haiku 4.5

---

## 12. Claude Cheat Sheet (July 2026)

```
DO:
- output_config.effort (high default; xhigh for coding; low/medium for cost)
- Adaptive thinking (on by default for Opus 5, Sonnet 5; always-on Fable 5)
- Brief steering for Fable 5 (one instruction > enumeration)
- 3-5 examples in <example> tags, XML tags for structure
- Explain WHY, not just WHAT
- Role in system prompt, longform data at top
- Keep Opus 4.8 fallback wired for Fable 5
- Recount tokens on Sonnet 4.6→5 migration (+30% tokenizer)
- send_to_user tool for long async agents
- Memory file for Fable 5 (one lesson/file, dedupe)
- Ground Fable 5 progress claims against tool results

DON'T:
- Manual thinking budgets / non-default temperature / top_p / top_k / prefill (→ 400; Haiku 4.5 exempt)
- Over-prompt / CAPS tool cues (overtrigger on current models)
- Enumerate for Fable 5 (brief instruction beats lists)
- Tell Fable 5 to echo reasoning (reasoning_extraction refusal)
- Add verification/self-check instructions for Opus 5 (self-verifies)
- "Double-check your answer" / "re-verify" (cost, no quality gain)
- Expect old effort levels to transfer (re-sweep on each model)

TEMPLATE:
<context>[background + WHY this matters]</context>
<task>[direct instruction -- be EXPLICIT]</task>
<output_format>[JSON schema or format spec]</output_format>

EFFORT QUICK-MAP:
  Sonnet 5 medium ≈ Sonnet 4.6 high
  Sonnet 5 high ≈ Sonnet 4.6 max
  Start at high, sweep from there
```

---

## 13. Migration from Claude 4.6 to Claude 5 Family

### Breaking API Changes

**Haiku 4.5 is the exception to every row below** -- it keeps prefill, manual
`budget_tokens`, the old tokenizer, and sampling params (`temperature` *or*
`top_p`, not both). Do not apply this checklist to it.

- [ ] **Prefill removed**: No assistant-message on last turn (→ 400) on Fable 5, Opus 4.6+, Sonnet 4.6+. Use Structured Outputs or system instructions.
- [ ] **Manual thinking budgets removed**: `budget_tokens` → 400. Use the effort parameter.
- [ ] **Sampling params restricted**: **non-default** `temperature`/`top_p` → 400; `top_k` rejected outright. Omitting them (or passing the default) still works. Steer via prompt.
- [ ] **New tokenizer**: ~30% more tokens for the same text. Documented for Sonnet 5 vs Sonnet 4.6 -- verify per model rather than assuming family-wide. Recount and re-budget `max_tokens`.

### Behavioral Changes

- [ ] **Thinking on by default** for Opus 5 and Sonnet 5 (was off on 4.6). Budget `max_tokens` for thinking+text.
- [ ] **Remove verification instructions** for Opus 5 (self-verifies).
- [ ] **Remove "summarize every N calls"** scaffolding for Sonnet 5 (higher-quality native updates).
- [ ] **Remove anti-laziness prompting** ("be thorough", "use tools aggressively") -- may overtrigger.
- [ ] **Refactor old skills/prompts** for Fable 5 -- too-prescriptive instructions degrade output.
- [ ] **Add conciseness instruction** for Opus 5 (longer default responses).
- [ ] **Add scope constraints** for Opus 5 (can expand task scope).
- [ ] **Cap subagent delegation** for Opus 5 and Fable 5 (delegate more readily).
- [ ] **Code review harness**: If prompt says "only report high-severity" -- Sonnet 5/Opus 5 follow literally. Ask for everything, filter separately.
- [ ] **Mid-conversation system messages**: Accepted after a user turn in `messages[]` on **Opus 5 / Opus 4.8**. No beta header. **Sonnet 5 does not support this** -- do not assume it generalizes across the Claude 5 family.

### New Capabilities to Leverage

- [ ] **send-to-user tool** for long async Fable 5 agents
- [ ] **Memory system** for Fable 5 (persistent notes file)
- [ ] **Effort sweep** on your evals (effort recalibrated per model)
- [ ] **Refusal handling**: `stop_reason: "refusal"` is HTTP 200 -- handle in harness
- [ ] **Fallback configuration**: `fallbacks` param or SDK middleware for Fable 5 → Opus 4.8

---

## 14. Code Review Harnesses

Review prompts tuned for earlier models may show lower recall on Opus 5/Sonnet 5. This is a harness effect, not a capability regression. Models follow "only report high-severity" more faithfully.

**Recommended prompt**:
```
Report every issue you find, including ones you are uncertain about or consider
low-severity. Do not filter for importance or confidence at this stage -- a
separate verification step will do that. Your goal is coverage: it is better to
surface a finding that later gets filtered out than to silently drop a real bug.
For each finding, include your confidence level and an estimated severity.
```

If single-pass filtering needed:
```
Report any bugs that could cause incorrect behavior, a test failure, or a
misleading result; only omit nits like pure style or naming preferences.
```

---

## 15. Rare Edge Cases

### Fable 5 Early Stopping

Deep in long sessions, Fable 5 can end a turn with a statement of intent without issuing a tool call. For autonomous pipelines:
```
You are operating autonomously. The user is not watching in real time. For
reversible actions that follow from the original request, proceed without
asking. Before ending your turn, check your last paragraph. If it is a plan,
a list of next steps, or a promise, do that work now with tool calls.
```

### Opus 5 with Thinking Disabled

Two artifacts can appear with thinking off:
1. **Tool calls as text**: Model writes tool call in visible text instead of structured block
2. **Internal XML tags**: `<thinking>` tags leak into output

Mitigation (prefer keeping thinking on at lower effort instead):
```
When you use a tool, you may say a brief sentence first. If no tool can express
what the user asked for, say so instead of guessing. Do not include internal or
system XML tags in your response.
```

### Self-Correction Narration (Opus 5)

Opus 5 narrates corrections to earlier statements more than prior models:
```
Only correct an earlier statement when the error would change the user's code,
conclusions, or decisions. State corrections plainly and briefly, then continue.
```

---

## References

- [Prompting Claude Fable 5](https://docs.anthropic.com/en/build-with-claude/prompt-engineering/prompting-claude-fable-5)
- [Prompting Claude Opus 5](https://docs.anthropic.com/en/build-with-claude/prompt-engineering/prompting-claude-opus-5)
- [Prompting Claude Sonnet 5](https://docs.anthropic.com/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5)
- [Claude Prompting Best Practices](https://docs.anthropic.com/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)
- [Memory Tool](https://docs.anthropic.com/en/agents-and-tools/tool-use/memory-tool)
- [Effort Parameter](https://docs.anthropic.com/en/build-with-claude/effort)
- [Thinking](https://docs.anthropic.com/en/build-with-claude/thinking)
