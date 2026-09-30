# Claude Practices (Anthropic, September 2026)

This module documents Claude-specific prompting patterns for the **current models** (Fable 5.1, Opus 5.5, Sonnet 5.5, Haiku 4.5) and the **legacy-but-available** models (Fable 5, Opus 5, Sonnet 5, Opus 4.8; Mythos 5 / 5.1 = Fable 5 / 5.1 under Glasswing safeguards). Opus 5.5 at `medium` is Anthropic's stated starting model for most workloads. Canonical home for Claude agentic XML blocks, model-specific guidance, and migration patterns.

> **Model specs**: 03-model-catalog_v5.md for full pricing/specs.
> **Anti-patterns**: 02-techniques-patterns_v5.md (canonical).
> **Principle**: where a technique names a specific model, treat it as measured on that model and re-check it before applying it to another.
> **Agentic patterns**: 10-agentic-patterns_v5.md for general agent design.

---

## 1. General Principles

### 1.1 Be Clear and Direct

Claude 5.x models follow instructions precisely. Being specific about desired output enhances results. "Above and beyond" behavior requires explicit requests.

**Less effective**: `Create an analytics dashboard`

**More effective**: `Create an analytics dashboard. Include as many relevant features and interactions as possible. Go beyond the basics to create a fully-featured implementation.`

### 1.2 Explain WHY, Not Just WHAT

Claude generalizes from explanatory context. Providing motivation behind instructions significantly improves performance.

**Less effective**: `NEVER use ellipses`

**More effective**: `Your response will be read aloud by a text-to-speech engine, so never use ellipses since the engine will not know how to pronounce them.`

### 1.3 Use Examples Effectively

3-5 well-crafted examples in `<example>` tags improve accuracy. Make them relevant, diverse, and structured. Avoid unintended patterns from inconsistent examples.

### 1.4 Concise, Direct Communication

Claude 5.x models are more direct and conversational. Fact-based progress reports, less self-celebratory. Opus 5.5 communication is plain: it says what it did, what it found, and what it needs.

**Opus 5 exception (legacy)**: Default responses run longer than prior models. Prompt explicitly for conciseness:
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

**Fable 5.1 is the opposite**: it sends fewer user-facing progress updates and writes denser prose. Ask for progress text and remove any instruction telling it to keep that text brief (see `thinking.display` in §2, prose and formatting in §6, and silent-turn fixes in §8).

### 1.5 Literal Instruction Following (Sonnet 5 / 5.5)

Sonnet 5 and 5.5 interpret prompts literally, especially at lower effort levels. It does not silently generalize instructions. If you need an instruction applied broadly, state the scope explicitly:

```
Apply this formatting to every section, not just the first one.
```

---

## 2. Thinking Modes (September 2026)

### Per-Model Thinking Defaults

| Model | Default | Turn Off | Config |
|-------|---------|----------|--------|
| **Fable 5.1** | Always-on | Cannot (`disabled` → 400) | `thinking:{type:"adaptive"}` only |
| **Opus 5.5** | Always-on | Cannot (`disabled` → 400 at every effort) | `thinking:{type:"adaptive"}`; lower effort instead |
| **Sonnet 5.5** | On | `disabled` → 400; lowest is `thinking:{type:"between_tools"}` (≤`high` only, no other field) | `thinking:{type:"adaptive"}` |
| **Haiku 4.5** | Manual budget; off by default | N/A | `thinking:{type:"enabled",budget_tokens:N}` |
| *Legacy:* **Fable 5** | Always-on | Cannot (`disabled` → 400) | `thinking:{type:"adaptive"}` only |
| *Legacy:* **Opus 5** | On by default | `disabled` (only at effort ≤high) | `thinking:{type:"adaptive"}` |
| *Legacy:* **Sonnet 5** | On by default | `thinking:{type:"disabled"}` | `thinking:{type:"adaptive"}` |
| *Legacy:* **Opus 4.8** | Off unless set | N/A (already off) | Set `thinking:{type:"adaptive"}` |

`between_tools` (Sonnet 5.5 only) thinks only between tool calls: without tools it means no thinking, so use adaptive thinking for tool-less reasoning tasks. It accepts no other field (`display`, `budget_tokens`, `block_binding` → 400), and `xhigh`/`max` with `between_tools` → 400.

**History rules (Fable 5.1, Opus 5.5, Sonnet 5.5)**: thinking blocks are bound to the conversation prefix. Keep history append-only and pass `thinking` blocks back unchanged; editing `system`, `tools` or an earlier turn returns 400 (`The block is bound to a different conversation`) on accounts created on or after Aug 31 2026 00:00 UTC. Thinking blocks are also model-bound: Fable 5.1 reads Opus 5.5 blocks, not the reverse; unreadable blocks drop silently after a downward switch or fallback.

**`thinking.display`** (`omitted` | `summarized` | `updates`; default omitted): text written between tool calls now arrives as progress-update `thinking` blocks on Opus 5.5, Fable 5.1 and Sonnet 5.5, which are empty under the default. Set `"updates"` (beta header `thinking-display-updates-2026-08-18`) or `"summarized"` to keep the UI from going silent. To have less thinking, lower effort first; prompt instructions are less reliable.

### Effort Parameter

`output_config: {effort: "..."}` controls how much the model thinks, not how much it says. It is **soft behavioral guidance, not a hard cap** -- `max_tokens` remains the only strict ceiling. Enum on every 5.x model and Opus 4.8: `low` `medium` `high` `xhigh` `max`. Setting the default equals omitting it -- but set it explicitly.

| Level | Use For |
|-------|---------|
| `low` | Short, scoped tasks, latency-sensitive |
| `medium` | Default on Opus 5.5 (Anthropic's starting point for most workloads); cost-sensitive, still strong |
| `high` | Default on Fable 5.1 and Sonnet 5.5. Most tasks. |
| `xhigh` | Hardest coding and agentic work; reserve for measured gains |
| `max` | Absolute maximum capability, no token constraints; reserve for measured gains |

**Key insight**: effort levels do not transfer across models. Documented pairs only: Opus 5.5 `medium` ≥ Opus 5 `high` (Opus 5.5 `low` is close to Opus 5 `high` on several coding evals); Fable 5.1 `medium` ≈ Fable 5 at lower cost; Sonnet 5 `medium` ≈ Sonnet 4.6 `high`. Sonnet 5.5 levels were recalibrated with no published mapping. Opus 5.5 thinks **more per turn** than Opus 5 at the same level, so porting the Opus 5 value gives longer, costlier turns. Fable 5.1 at `low` is often competitive with Opus and Sonnet on cost per task while scoring higher, so include it where you would run a smaller model at higher effort. Start at each model's default, test all five levels on your evals.

**Per-message effort (beta, `mid-conversation-output-config-2026-07-01`)**: change effort per turn without breaking the cache. A top-level effort change invalidates the cache. Supported on Fable 5.1, Opus 5.5, Sonnet 5.5, Opus 5 (not Fable 5, Sonnet 5; Sonnet 5.5 not with `between_tools`).

**`max_tokens`**: thinking and text share it. Opus 5.5 and Sonnet 5.5 agentic coding worked well at 128,000 (stream on Sonnet 5.5).

### Steering Adaptive Thinking

When model thinks more than needed (large/complex system prompts):
```
Thinking adds latency and should only be used when it will meaningfully improve
answer quality -- typically for problems that require multistep reasoning.
When in doubt, respond directly.
```

When running hard workloads at `medium` and seeing under-thinking, raise effort first. Asking Sonnet 5.5 to think less in the system prompt does not reliably work either; lower effort instead. If finer control needed:
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

### Prompts Written for Thinking Disabled (Opus 5 → Opus 5.5 / Sonnet 5.5)

- Start at `low` effort and measure. If time-to-first-token still matters, add "Answer directly without deliberating." and re-measure quality.
- Remove "write out your reasoning in the response" instructions; read `display:"summarized"` thinking instead (otherwise you risk a `reasoning_extraction` refusal).
- Remove any "don't think" rule (on Sonnet 5.5 it causes internal XML tags in the output). Read the response by block type.
- Opus 5.5 chat prompts: remove "think carefully before answering" lines -- replies start sooner with no clear quality loss. Optionally add:
```
Once you have answered something, treat that answer as done. On later turns, focus
your thinking on what the user is asking now, and don't go back over an earlier
answer unless the user asks about it or points out a problem with it.
```
Skip that line for long analyses and agentic work; it may suppress self-correction.

---

## 3. Long-Horizon Reasoning & State Tracking

### 3.1 Context Awareness

Context awareness -- tracking remaining token budget -- is documented for Sonnet 5, Sonnet 4.6, Sonnet 4.5, and Haiku 4.5 only. Do not assume it on every Claude model. For agent harnesses with context compaction:

```xml
<context_management>
Your context window will be automatically compacted as it approaches its limit,
allowing you to continue working indefinitely. Do not stop tasks early due to
token budget concerns. Save current progress and state to memory before context
refreshes. Always be persistent and autonomous -- complete tasks fully even if
the end of your budget is approaching.
</context_management>
```

**Fable 5 context-budget concern (carry over to Fable 5.1)**: In very long sessions, Fable 5 can occasionally suggest a new session or offer to summarize. Avoid surfacing explicit context-budget counts. If the harness must show them:
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

### 3.4 Memory Systems (Fable 5 / 5.1)

Fable 5 performs notably better with a persistent memory file:
```
Store one lesson per file with a one-line summary at the top. Record corrections
and confirmed approaches alike, including why they mattered. Don't save what the
repo or chat history already records; update an existing note rather than creating
a duplicate; delete notes that turn out to be wrong.
```

Client-side compaction on Fable 5.1: replace the whole history with one summary plus the new turn (keeping history append-only); cache reads are cheaper, so try later compaction points. If compaction drops things, use a summarization prompt that lists what must be kept exactly and weights the user's voice and the agent's voice differently. Audit prefix changes with `thinking.block_binding.prefix_mismatch_behavior:"drop_block"` (beta `thinking-binding-controls-2026-08-01`) and log `input_transformations`.

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

Claude 5.x models are highly responsive to system prompts. Over-aggressive language causes overtriggering:

| Overtriggers | Balanced |
|--------------|----------|
| `CRITICAL: You MUST use tool when...` | `Use tool when...` |
| `ALWAYS call function` | `Call this function when appropriate` |
| `If in doubt, use [tool]` | Remove (triggers appropriately now) |

**Sonnet 5 with thinking off (legacy)**: Less likely to reach for tools. Add explicit nudge if you rely on tool calls with thinking disabled.

**Sonnet 5.5 answers from training when it should search**: remove "only use tools when strictly necessary" and "minimize tool calls", then add:
```
Use the search tool to check specifics that may have changed since your training, such as what is allowed, required or charged, even when you feel confident. For researched work such as a report or a comparison, gather current sources rather than writing from your training knowledge.
```
Sonnet 5.5 may also call tools with the wrong case or slightly wrong parameter names: have the harness accept unambiguous case mismatches, or return `is_error:true` naming the exact expected name. Opus 5.5 under-explores loosely specified multi-app tasks; add:
```
Before taking any action, explore broadly with tool calls: list and open the emails, documents, spreadsheet tabs and records across the available apps that could be relevant to this task, including ones the task does not explicitly mention, and use what you find.
```
Keep untrusted content out of the searched records.

**Forced `tool_choice` (`any` / `tool`) → 400 on Fable 5.1, Opus 5.5, Sonnet 5.5** (a forced call skips thinking, so the working-out leaks into the arguments). Use `auto` plus `strict:true`, or structured outputs, and say in the prompt when the tool applies.

### 4.3 Parallel Tool Calling

Claude 5.x models run independent tool calls in parallel:

```xml
<use_parallel_tool_calls>
If you intend to call multiple tools and there are no dependencies between the
calls, make all independent calls in parallel. Maximize use of parallel tool
calls for speed and efficiency. If some calls depend on previous results, call
them sequentially. Never use placeholders or guess missing parameters.
</use_parallel_tool_calls>
```

**Fable 5.1 serial calls**: in coding and computer-use loops where the next calls are implied, Fable 5.1 tends to make one call per turn. Send this as a turn-scoped system message after each tool-result turn, leaving earlier copies in place byte-for-byte (without the beta, put it in a text block after the `tool_result` blocks):
```
First privately list what you need next; then request every item that doesn't depend on another's result in this one response.
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

### 5.3 Self-Verification (Opus 5 only; Fable / Opus 5.5 / Sonnet 5.5 differ)

**Remove *redundant* verification instructions on Opus 5 (AP-16).** It self-verifies without prompting, so carrying over "double-check your answer" or "include a final verification step" from prior-model prompts causes over-verification -- extra cost with no quality gain. Opus 5 is the only model Anthropic names for this removal.

This is **not** a blanket ban:
- **Fable 5 / 5.1**: Anthropic recommends explicit periodic self-verification for *long-running* tasks, where the model cannot otherwise know when to checkpoint (AP-16 does not apply). Pattern:
```
Establish a method for checking your own work at an interval of [X] as you
build. Run this every [X interval], verifying your work with subagents against
the specification.
```
- **Opus 5.5**: no official statement on verification; the Opus 5 guidance "remains a reasonable starting point" (Verify).
- **Sonnet 5.5**: at `low` it may report done without running a check; at `xhigh`/`max` it starts self-initiated review rounds and reviewer subagents. It needs the *opposite* of AP-16 at high effort (see 5.8).

### 5.4 Progress Grounding (Fable 5 / 5.1)

Ground progress claims against tool results to prevent fabricated status reports:
```
Before reporting progress, audit each claim against a tool result from this
session. Only report work you can point to evidence for; if something is not
yet verified, say so explicitly. Report outcomes faithfully: if tests fail,
say so with the output; if a step was skipped, say that.
```

### 5.5 Action Boundaries (Fable 5 / 5.1)

Fable can take unrequested actions (drafting emails, creating git backups). Define explicit boundaries:
```
When the user is describing a problem, asking a question, or thinking out loud
rather than requesting a change, the deliverable is your assessment. Report
your findings and stop. Don't apply a fix until they ask for one.
```

Fable 5.1 also delivers extras (fixes nearby code, extends behavior, commits more test files than warranted). Use Anthropic's "extras only" paragraph: report nearby problems as a follow-up instead of fixing, optimizing or extending them; commit tests only where the task asks (roughly one focused test per stated behavior); implement every behavior the task asks for, completely. For whole-file rewrites on small edits:
```
The number of tokens used to edit files is best minimized, all else being equal. Therefore, when it will not affect the end result, try to surgically edit a file rather than rewrite the entire thing.
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

### 5.8 Sonnet 5.5 Scope and Stopping

Sonnet 5.5 adds unrequested tests, docs and small files at every effort (more at high effort), and on open-ended requests starts building when you wanted ideas. It also checks in before finishing at `low`/`medium`. Official additive lines (state scope; do not rely on it generalizing):

Checks in before done (try higher effort first; this raises cost at `low`/`medium`):
```
Keep working until everything the user asked for is done, and only stop to ask when you can't go on without the user or before a risky step.
```
Unrequested additions (add the second paragraph only):
```
When the work the user asked for is done and checked, stop and report. Don't add features, tests, files, docs or refactors that weren't asked for. If you think one would help, mention it at the end instead of doing it.
```
Over-thoroughness at `xhigh`/`max` (or run routine work at ≤`high`); at `max` this cut cost by about a third with no quality change:
```
When the work the user asked for is done and its checks pass, stop and report. Don't start extra rounds of review or hardening on your own, and don't launch reviewer sub-agents unless the user asked for a review. If you think a deeper review is worth doing, say so at the end.
```
Builds when you wanted ideas:
```
When the user asks for ideas, options or a plan, give them that and stop. Don't start building or changing anything until they say to go ahead.
```
Reports done without running a check (low effort): add Anthropic's verification paragraph -- run a real check that exercises the change before reporting it done, install declared dependencies with the project's own package manager and never with sudo, and if no real check can run, say which one was not run and why. This made skipped checks rare at slightly higher cost.

**JSON answers on multi-step reasoning**: use structured outputs where available, adaptive thinking (not `between_tools`), and end the system prompt with `Think the problem through before you answer.` At `high` this approaches `xhigh` accuracy. Treat `stop_reason:"max_tokens"` as a failure even if the JSON is valid. Without structured outputs, parse the last JSON value, not first `{` to last `}`.

### 5.9 Opus 5.5 Specifics

- Gets to work quickly and under-explores loosely specified multi-app tasks: use the "explore broadly" line in 4.2.
- More thinking per turn than Opus 5: lower effort first; size `max_tokens` for thinking plus reply.
- Pasted text carrying instructions: wrap each block in `<pasted_content id="ab12">…</pasted_content id="ab12">` with an app-generated random ID and the official system-prompt note (see 09-safety-guardrails_v5.md). One guardrail among several; the model may become slightly more cautious.

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

### Fable 5.1 Formatting and Prose

- **Too little formatting**: remove anti-formatting rules (the sample block above can suppress structure the content needs on Fable 5.1) and replace them with a "when to use lists" rule.
- **Dense prose** (longer sentences, fewer breaks): define "mannered prose" in the **user** message, or just say `Please remove all mannered prose.`
- **Unmarked quotations** (reproduces source text without quotation marks): add **one** complete example (request, response, rationale) in `<example>` tags, with tool lines templated.
- **Long deliverables at `xhigh`/`max`** (drafts the deliverable in thinking, then writes it again): prefer `high`; otherwise size `max_tokens` for thinking plus reply and tell it, in the user message, that one token limit covers both and not to compose the deliverable twice.

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

Claude Research tool conducts multi-step investigations via multiple web searches, synthesizing findings into citation-backed reports.

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

---

## 8. Subagent Orchestration

### Per-Model Delegation Behavior

| Model | Delegation Style |
|-------|-----------------|
| **Fable 5.1 / Fable 5** | Most aggressive; dispatches parallel subagents readily; supports long-lived agents. Use subagents frequently, with explicit guidance on when delegation is appropriate. The lead often waits idle: make the subagent-start tool return immediately, deliver results in a later user message, and offer a separate "wait" tool |
| **Opus 5.5** | Paces a multi-agent team to an advisory time budget (see below) |
| **Sonnet 5.5** | Launches reviewer subagents at `xhigh`/`max` (see 5.8) |
| *Legacy:* **Opus 5** | Delegates readily; effective writer-verifier patterns; few overwrite conflicts. Cap it |
| *Legacy:* **Opus 4.8** | Dynamic workflows; hundreds of parallel subagents in one session |
| *Legacy:* **Sonnet 5** | More agentic than Sonnet 4.6; higher tool usage at high/xhigh effort |

**Opus 5.5 time budget**: harness appends `elapsed 340s / 1200s` to each message. Set the budget somewhat above the target, because it is advisory; keep your own hard timeout. Without a budget: `Time matters here: do not spend time that can be avoided, and the earlier a correct result is obtained, the better.` A budget increases parallelism; lowering effort reduces work. Under time pressure the model may verify slightly less.

### Controlling Delegation

**Damping** (Opus 5; prevent excessive subagent use):
```
Delegate to a subagent only for large tasks that are genuinely independent and
parallelizable. Do not delegate work you can finish yourself in a handful of
tool calls, and do not use subagents to verify or double-check your own work.
If one subagent can complete the task, use one rather than several.
```

**Encouraging** (Fable 5 / 5.1 long runs):
```
Delegate independent subtasks to subagents and keep working while they run.
Intervene if a subagent goes off track or is missing relevant context.
```

### send-to-user Tool (Fable 5 / 5.1, Opus 5.5, Sonnet 5.5)

For long async agents (declare it from the **first** request; adding it mid-session breaks the cache), a tool that delivers messages verbatim mid-turn without ending it:
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

**Silent long turns (Opus 5.5, Sonnet 5.5, Fable 5.1)**: (1) `display:"updates"`; (2) the send-to-user tool above; (3) remove "hold all findings for the final response" and other narration-suppressing lines; (4) ask for a one-line intent before the first tool call and a recap at the end; (5) harness nudge: after about 5 silent tool steps, append a turn-scoped system message (`clear_at:"next_user_message"`, beta `mid-conversation-system-clear-at-2026-08-21`) and stop after 2-3 nudges (roughly halved long silent stretches at no measurable cost on Opus 5.5):
```
The user hasn't heard from you in a while — say in a few words what you're doing, then continue.
```
For Fable 5.1 a fuller version: `Before you start, say in a line what you're about to do; brief updates while you work help the user follow along. Close with a short recap that stands on its own — what you found, what you did, and what's next — so a reader who only sees the last message has the full picture.` On Sonnet 5.5, frequent harness text after tool results can look like an injection: keep harness notices in a **separate** mid-conversation system message, and never put user text inside `tool_result`; deliver genuine mid-turn user input as a text block after the last `tool_result`. No token-budget countdown after tool results in interactive sessions.

### Cost Pattern: Orchestrator + Executor

Dominant 2026 pattern: **Fable 5.1 as orchestrator, Sonnet 5.5/Opus 5.5 as executor**. Long-lived subagents save time through cache-read savings and avoid bottlenecking on the slowest agent. Variant: Opus 5.5 executor at `high` + Fable 5.1 advisor (+1.7 pts for about 2.1x the cost, at the edge of noise -- test on your workload). A Sonnet 5.5 executor accepts only a 5-series Opus, Fable or Mythos advisor (Opus 4.8, Opus 4.7 and Sonnet 5 advisors → 400).

---

## 9. Frontend Design

Without guidance, Claude models can default to generic "AI slop" aesthetics. Opus 5.5 falls back to a few default styles, and "avoid a generic AI look" just swaps one default for another: **name the specific patterns to avoid** (cream background, italic accent words, "01/02/03" labels, monospace labels, pill buttons) and iterate the list. Sonnet 5 may settle into a consistent default visual style. The general block below is Anthropic's older-model (Opus 4.5/4.6) form; use it as a base and add named patterns.

```xml
<frontend_aesthetics>
NEVER use generic AI-generated aesthetics like overused font families (Inter,
Roboto, Arial, system fonts), cliched color schemes (particularly purple
gradients on white or dark backgrounds), predictable layouts and component
patterns, and cookie-cutter design. Use unique fonts, cohesive colors and
themes, and animations for effects and micro-interactions.
</frontend_aesthetics>
```

**Two reliable approaches for Sonnet 5 / 5.5**:

1. **Specify a concrete alternative** -- the model follows explicit visual specs precisely (provide hex colors, font names, spacing, radius values)

2. **Have the model propose options before building**:
```
Before building, propose 4 distinct visual directions tailored to this brief
(each as: bg hex / accent hex / typeface, plus a one-line rationale). Ask the
user to pick one, then implement only that direction.
```

---

## 10. Vision Capabilities

Current models (Opus 5.5, Fable 5.1, Sonnet 5.5) and legacy Opus 5 / Fable 5 have substantially improved vision:
- Strong on chart, document, diagram understanding
- UI and frontend visual replication
- Vision performance strongest with tools to iteratively analyze, crop, and verify
- Tool use is a more cost-effective lever for vision than thinking alone

**Performance boost**: Give Claude a crop tool to "zoom" in on relevant regions (or a container with PIL/OpenCV). Consistent uplift on image evaluations.

- **Opus 5.5** reads dense charts much better without tools; for the densest inputs use higher resolution plus a container or crop tool, and re-test whether old vision scaffolding is still needed. Without tools, raising effort helps technical drawings but not charts.
- **Sonnet 5.5** needs crop, zoom or code tools. For charts, tools help at every effort and beat raising effort; for drawings, tools help only from `high` up.
- **Fable 5.1** is better out of the box; a crop tool gives most of the uplift.

**Computer use**: Opus 5.5 and Sonnet 5.5 reject `computer_20251124` on the Claude API and Google Cloud (Bedrock still accepts it) → use `computer_toolset_20260801`. On Sonnet 5 (legacy): `computer_20251124` tool version. Up to 2576px / 3.75MP max resolution. 1080p = good balance of performance and cost. 720p/1366x768 for cost-sensitive workloads.

---

## 11. Model Self-Knowledge

```
The assistant is Claude, created by Anthropic. The current model is Claude Opus 5.5.
```

For API strings:
```
When an LLM is needed, default to Claude Opus 5.5 unless the user requests
otherwise. The exact model string for Claude Opus 5.5 is claude-opus-5-5.
```

Current model IDs:
- `claude-fable-5-1` -- Fable 5.1
- `claude-opus-5-5` -- Opus 5.5
- `claude-sonnet-5-5` -- Sonnet 5.5
- `claude-haiku-4-5-20251001` -- Haiku 4.5 (alias `claude-haiku-4-5`)

Legacy (still available):
- `claude-fable-5` -- Fable 5
- `claude-opus-5` -- Opus 5
- `claude-sonnet-5` -- Sonnet 5
- `claude-opus-4-8` -- Opus 4.8

Mythos 5.1 (`claude-mythos-5-1`) is the same model as Fable 5.1, Glasswing participants only, with no prefix-binding check.

---

## 12. Claude Cheat Sheet (September 2026)

```
DO:
- Start at Opus 5.5 @ medium (set effort explicitly); escalate to Fable 5.1 when Opus 5.5 xhigh/max still falls short
- output_config.effort (Opus 5.5 medium default; Fable 5.1 / Sonnet 5.5 high default; xhigh/max only for measured gains)
- Adaptive thinking (always-on Fable 5.1, Opus 5.5; on for Sonnet 5.5, Opus 5, Sonnet 5)
- thinking.display "updates" or "summarized" so progress text is not empty
- Brief steering for Fable 5/5.1 (one instruction > enumeration)
- 3-5 examples in <example> tags (<thinking> inside examples allowed), XML tags for structure
- Explain WHY, not just WHAT
- Role in system prompt, longform data at top
- Keep history append-only; pass thinking blocks back unchanged (5.1/5.5)
- Wire fallbacks (Fable 5.1 -> Opus 4.8, Opus 5; Sonnet 5.5 -> Sonnet 5) and handle stop_reason "refusal" (HTTP 200)
- Recount tokens on any 4.6 -> 5.x migration (new tokenizer)
- send_to_user tool for long async agents, declared from the first request
- Memory file for Fable 5/5.1 (one lesson/file, dedupe)
- Ground Fable progress claims against tool results
- Name specific frontend patterns to avoid (Opus 5.5)

DON'T:
- Manual thinking budgets / non-default temperature / top_p / top_k / prefill (-> 400; Haiku 4.5 exempt)
- thinking:{type:"disabled"} on Fable 5.1, Opus 5.5, Sonnet 5.5 (-> 400)
- Forced tool_choice on Fable 5.1, Opus 5.5, Sonnet 5.5 (-> 400)
- Edit system/tools/earlier turns mid-conversation on 5.1/5.5 (-> 400 on newer accounts)
- Over-prompt / CAPS tool cues (overtrigger on current models)
- Enumerate for Fable 5/5.1 (brief instruction beats lists)
- Tell any 5.x model with a reasoning_extraction classifier to echo reasoning (billed refusal)
- Add verification/self-check instructions for Opus 5 (self-verifies; AP-16)
- "Double-check your answer" / "re-verify" on Opus 5 (cost, no quality gain)
- "Don't think" rules or "think carefully before answering" on Opus 5.5 / Sonnet 5.5
- Expect old effort levels to transfer (re-sweep on each model)

TEMPLATE:
<context>[background + WHY this matters]</context>
<task>[direct instruction -- be EXPLICIT]</task>
<output_format>[JSON schema or format spec]</output_format>

EFFORT QUICK-MAP (documented pairs only):
  Opus 5.5 medium >= Opus 5 high
  Fable 5.1 medium ~ Fable 5
  Sonnet 5 medium ~ Sonnet 4.6 high
  Sonnet 5.5: recalibrated, no published mapping
  Start at the model default, sweep from there
```

---

## 13. Migration from Claude 4.6 to Claude 5 Family (legacy path)

A 4.x-era prompt that still works must not be force-migrated; migrate the prompt in the same change that swaps the model. This section is the upgrade path to the Claude 5 generation; the 5 → 5.5 / 5.1 delta follows it.

### Breaking API Changes

**Haiku 4.5 is the exception to every row below** -- it keeps prefill, manual
`budget_tokens`, the old tokenizer, and sampling params (`temperature` *or*
`top_p`, not both). Do not apply this checklist to it.

- [ ] **Prefill removed**: No assistant-message on last turn (→ 400) on the Claude 5.x family and Opus 4.8 (Haiku 4.5 accepts it). Use Structured Outputs or system instructions.
- [ ] **Manual thinking budgets removed**: `budget_tokens` → 400. Use the effort parameter.
- [ ] **Sampling params restricted**: **non-default** `temperature`/`top_p` → 400; `top_k` rejected outright. Omitting them (or passing the default) still works. Steer via prompt.
- [ ] **New tokenizer**: ~30% more tokens for the same text. Documented for Sonnet 5 vs Sonnet 4.6 -- verify per model rather than assuming family-wide. Recount and re-budget `max_tokens`.

### Behavioral Changes

- [ ] **Thinking on by default** for Opus 5 and Sonnet 5 (was off on 4.6; always-on for Fable 5/5.1 and Opus 5.5). Budget `max_tokens` for thinking+text.
- [ ] **Remove verification instructions** for Opus 5 (self-verifies).
- [ ] **Remove "summarize every N calls"** scaffolding for Sonnet 5 (higher-quality native updates).
- [ ] **Remove anti-laziness prompting** ("be thorough", "use tools aggressively") -- may overtrigger.
- [ ] **Refactor old skills/prompts** for Fable 5 -- too-prescriptive instructions degrade output.
- [ ] **Add conciseness instruction** for Opus 5 (longer default responses).
- [ ] **Add scope constraints** for Opus 5 (can expand task scope).
- [ ] **Cap subagent delegation** for Opus 5 and Fable 5 (delegate more readily).
- [ ] **Code review harness**: If prompt says "only report high-severity" -- Sonnet 5/5.5 and Opus 5 follow literally. Ask for everything, filter separately.
- [ ] **Mid-conversation system messages**: Accepted after a user turn in `messages[]` on **Opus 5 / Opus 4.8**. No beta header. **Sonnet 5 does not support this** (Sonnet 5.5, Opus 5.5 and Fable 5.1 do) -- do not assume it generalizes across the Claude 5 family.

### New Capabilities to Leverage

- [ ] **send-to-user tool** for long async Fable agents
- [ ] **Memory system** for Fable 5/5.1 (persistent notes file)
- [ ] **Effort sweep** on your evals (effort recalibrated per model)
- [ ] **Refusal handling**: `stop_reason: "refusal"` is HTTP 200 -- handle in harness
- [ ] **Fallback configuration**: `fallbacks` param or SDK middleware (Fable 5.1 → Opus 4.8, Opus 5)

### Migration from Claude 5 to 5.5 / 5.1 (Fable 5.1, Opus 5.5, Sonnet 5.5)

Official line: existing Opus 5, Sonnet 5 and Fable 5 prompts should perform well without changes -- carry them over, then apply only the deltas below. Haiku 4.5 is exempt.

**Breaking (same call, different outcome):**
- [ ] **`thinking:{type:"disabled"}` → 400** on Opus 5.5 (at every effort) and Sonnet 5.5. Opus 5.5: lower effort. Sonnet 5.5: `between_tools` (≤`high`, no extra fields).
- [ ] **Forced `tool_choice` → 400** on all three. Use `auto` + `strict:true` or structured outputs.
- [ ] **Editing history → 400** on accounts created on or after Aug 31 2026 (older accounts log only). Append-only history; turn-scoped or mid-conversation system messages; server-side compaction.
- [ ] **Legacy computer-use tool → 400** on Opus 5.5 / Sonnet 5.5 (Claude API, Google Cloud). Use `computer_toolset_20260801`.
- [ ] **Per-message effort** (beta) is supported on Fable 5.1, Opus 5.5, Sonnet 5.5; a top-level effort change invalidates the cache.
- [ ] **Priority Tier** not supported on Opus 5.5.

**Silent behavior changes:**
- [ ] Text between tool calls arrives as progress-update `thinking` blocks (empty under default `display`) -- set `display:"updates"` or `"summarized"`.
- [ ] Downward model switch or fallback drops thinking blocks silently (Fable 5.1 reads Opus 5.5 blocks, not the reverse); Sonnet 5.5 blocks are also account-bound.
- [ ] Opus 5.5 default effort is `medium`: a request that omits effort runs one level lower than on Opus 5. Set it explicitly. It also thinks more per turn at the same level.
- [ ] Fable 5.1: fewer progress updates, serial tool calls in loops, denser prose, less formatting, unmarked quotations, whole-file rewrites (see sections 4-6).
- [ ] Sonnet 5.5: unrequested tests/docs, builds when asked for ideas, reviewer subagents at `xhigh`/`max`, mid-turn user text misread as injection (see 5.8, 8).
- [ ] Opus 5.5 unattended loops can stop on a text-only `end_turn` (see 15).

**Carry over:** the Opus 5 / Sonnet 5 / Fable 5 prompt. Do not rewrite what works.

---

## 14. Code Review Harnesses

Review prompts tuned for earlier models may show lower recall on Opus 5 / Sonnet 5 / Sonnet 5.5. This is a harness effect, not a capability regression. Models follow "only report high-severity" more faithfully.

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

### Fable 5 / 5.1 Early Stopping

Deep in long sessions, Fable can end a turn with a statement of intent without issuing a tool call. For autonomous pipelines:
```
You are operating autonomously. The user is not watching in real time. For
reversible actions that follow from the original request, proceed without
asking. Before ending your turn, check your last paragraph. If it is a plan,
a list of next steps, or a promise, do that work now with tool calls.
```

Anthropic's full autonomy block also carries an exception for describe-only or ask-only requests, a last-paragraph self-check, and an evidence check before state-changing commands. Keep the opening sentence verbatim. Pair it with the "# Delivering work" scope block; if you must cut length, use the autonomy block alone. It may reduce clarifying questions on ambiguous requests.

### Opus 5.5 Early Stopping

Unattended agents can stop on a text-only `end_turn` progress report. Treat it as a report, not completion: keep a checklist or to-do; auto-continue with a message that names the open items (or use a smaller judge model against a stated completion condition); **cap continuations at 2-3**; wait for background jobs and subagents to finish. Append Anthropic's unattended-run standing instruction (four banned stop types; status goes in the same message as the next tool call) **at the end of the system prompt from the first request** -- adding it mid-session invalidates thinking. Leave it out of human-in-the-loop apps and keep confirmation for destructive actions. Expect more tool calls.

### Opus 5 with Thinking Disabled (legacy; not possible on Opus 5.5)

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

### Refusals, Fallbacks, and Billing

- `stop_reason: "refusal"` arrives as HTTP 200; handle it in the harness.
- Classifier categories differ per model (specs in 03-model-catalog_v5.md): Opus 5.5 = cyber (vulnerability-finding in source code is allowed), bio, `reasoning_extraction`; Sonnet 5.5 = five categories including `frontier_llm` and `general_harms`; Fable 5.1 = classifiers on.
- Reasoning echo is refused on the 5.x models with a `reasoning_extraction` classifier: remove reasoning-in-response instructions and read summarized thinking (`display:"summarized"`). Fallbacks never retry `reasoning_extraction`.
- **Server-side fallbacks** (`fallbacks:"default"` or up to 3 models; beta `server-side-fallback-2026-07-01`): Fable 5.1 → Opus 4.8, Opus 5; Sonnet 5.5 → Sonnet 5 (cyber, `frontier_llm` only); Opus 5.5 cyber tasks re-route to Opus 4.8.
- Pre-output refusals in `bio`, `frontier_llm` and `reasoning_extraction` are **billed from Sep 24 2026** -- AP-17 now costs money.
- Fable 5.1 benign-coding refusals: ask "Are there any bugs...?" rather than "Does this compile...?", give context for obscure languages, and remove tools that return base64 into context.

---

## References

- [Prompting Claude Fable 5.1](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1)
- [Prompting Claude Opus 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5)
- [Prompting Claude Sonnet 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5)
- [Prompting Claude Fable 5](https://docs.anthropic.com/en/build-with-claude/prompt-engineering/prompting-claude-fable-5)
- [Prompting Claude Opus 5](https://docs.anthropic.com/en/build-with-claude/prompt-engineering/prompting-claude-opus-5)
- [Prompting Claude Sonnet 5](https://docs.anthropic.com/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5)
- [Claude Prompting Best Practices](https://docs.anthropic.com/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)
- [Memory Tool](https://docs.anthropic.com/en/agents-and-tools/tool-use/memory-tool)
- [Effort Parameter](https://docs.anthropic.com/en/build-with-claude/effort)
- [Thinking](https://docs.anthropic.com/en/build-with-claude/thinking)
