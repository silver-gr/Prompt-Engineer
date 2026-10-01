# Agentic Patterns (September 2026 Edition)

This module is the **canonical home** for tool orchestration, sub-agent design, multi-context workflows, and IDE agent patterns. General agentic XML blocks for Claude are cross-referenced from 06-claude-practices_v5.md.

> **Model specs**: See 03-model-catalog_v5.md.
> **Anti-patterns**: See 02-techniques-patterns_v5.md (canonical).
> **Claude-specific agentic XML**: See 06-claude-practices_v5.md.

---

## 1. Agentic Architecture

### Agent Loop

```
+-------------------------------------------------------------+
|                      AGENT LOOP                              |
+-------------------------------------------------------------+
|  1. Observe    -> Receive task + context                     |
|  2. Think      -> Plan approach (native reasoning)           |
|  3. Act        -> Execute tool(s)                            |
|  4. Observe    -> Process results                            |
|  5. Iterate    -> Repeat until goal achieved                 |
+-------------------------------------------------------------+
```

**2026 Context**: Reasoning models excel at agentic workflows due to native planning, state tracking, and adaptive thinking. Agent coordination is now table stakes across providers.

---

## 2. Tool Description Patterns

### Optimal Format Is Provider-Specific

**There is no universal rule here -- vendors disagree, and following the wrong
one costs you accuracy:**

| Provider | Official guidance |
|----------|-------------------|
| OpenAI (GPT-5.x, GPT-6) | **Concise and precise**: what it does, **when to use it**, return fields, errors; expose only relevant tools. Verbose descriptions degrade quality |
| Anthropic | Describe **what the tool does *and* when to use it**; "when to use" text is recommended for resolving tool-selection ambiguity |
| Google (Gemini) | **No maximum**. Detailed descriptions with capabilities, usage conditions, and examples are recommended |

All three now want "when to use it" text. AP-7 targets **redundancy and irrelevant
tools**, not detail: a detailed Claude or Gemini description is not a violation.
Universal rules: one short line per parameter, enums where the value set is closed,
edge-case handling in code rather than in the description.

### Concise Format (OpenAI-style): 1-2 Sentences

```json
{
  "name": "tool_name",
  "description": "[What it does]. [When to use it].",
  "parameters": {
    "param1": {"type": "string", "description": "Brief description"}
  }
}
```

### Example

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

**Bad** (over-described):
```json
{
  "description": "This function allows you to search through the customer
  database. You should use this when the user asks about a customer. The
  function can search by name or ID. When searching by name, partial matches
  are returned. Make sure to validate input. If ambiguous, ask for
  clarification before searching..."
}
```

### Tool Description Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Multi-paragraph descriptions | Token waste, confuses models | 1-2 sentences |
| Restating the same usage rule across tools | Redundant text and irrelevant tools dilute selection (AP-7) | State once; expose only relevant tools |
| Edge case handling in description | Over-constrains | Handle in code |
| "Use this when..." | **Recommended by all three vendors** when tool choice is ambiguous | Keep it, concisely |

**MCP spec `2026-07-28`**: tool schemas may use full JSON Schema 2020-12; return
`tools/list` in a deterministic order to keep the prompt-cache prefix stable;
Sampling, Roots, and Logging are deprecated -- call provider APIs directly.

**Kimi K3 dynamic tool loading (optional)**: for large tool inventories, declare one
`search_tools` function plus a few core tools and advertise searchable domain tags in
the system prompt; force `tool_choice:"required"` on turn 1, then `auto`. Inject full
definitions mid-conversation via a `system` message carrying a `tools` field and no
`content`. Appending keeps the cached prefix; editing earlier declarations breaks it.

---

## 3. Goal-Oriented Prompting

### Pattern: State Goal, Provide Tools, Let Model Plan

```xml
<goal>
Deploy the updated API to production and verify it's working
</goal>

<available_tools>
- build: Compile and test the code
- deploy: Deploy to specified environment
- health_check: Verify service health
- rollback: Revert to previous version
</available_tools>

<constraints>
- Run tests before deploying
- Verify health after deploy
- Rollback if health check fails
</constraints>
```

The model determines the sequence (build -> deploy -> health_check -> conditional rollback) without explicit step prescription.

### State Tracking Pattern

For long-running tasks, maintain explicit state:

```xml
<task_state>
{
  "goal": "Migrate database schema",
  "completed": ["backup_created", "schema_validated"],
  "current": "applying_migration",
  "pending": ["verify_data", "update_app_config"],
  "blockers": []
}
</task_state>

Continue from current state. If blocked, update blockers and pause.
```

---

## 4. Parallel Tool Calling

### Enabling Parallel Execution

```
Research these topics in parallel:
1. Current market size for AI assistants
2. Top 5 competitors and their features
3. Regulatory landscape in US and EU

Synthesize findings into a comparison matrix.
```

Models launch parallel search/research calls, then synthesize.

**Fable 5.1 serial calls**: in coding and computer-use loops where the next calls are
implied, Fable 5.1 tends to issue one tool call per turn (and searches less at `low`
effort). Add a per-turn batching nudge as a turn-scoped system message from the harness
rather than prose in the base prompt. Official wording: `First privately list what you need next; then request every item that doesn't depend on another's result in this one response.` Leave earlier copies in place byte-for-byte.

**Gemini pre-tool text**: do not demand structured status text (XML/JSON) right before a
tool call -- it can cause `Malformed_Function_Call`. Declare an `update()` tool
(`previous_step`, `plan`, `next_step`) and tell the model to call it first, or use Markdown headers.

### Controlling Parallelization

**Enforce sequential** (dependencies):
```
Execute IN ORDER (each depends on previous):
1. Get current user permissions
2. Based on permissions, determine accessible resources
3. Query only accessible resources
```

**Allow parallel** (independent):
```
Gather this information (order doesn't matter):
- User profile
- Recent activity
- Notification settings
```

### Concurrency Limits (Claude)

Claude 5-family models (Fable 5.1, Opus 5.5, Sonnet 5.5 and legacy 5.x) emit multiple tool calls in one turn when beneficial. **Your application decides** whether to run them concurrently, sequentially, or mixed -- the model does not execute them. Concurrent execution is where the bottleneck risk lives. Effort level drives tool usage — `high`/`xhigh` show substantially more tool calls in agentic search and coding.

```xml
<execution_constraints>
Maximum 3 concurrent tool calls. Wait for results before next batch.
</execution_constraints>
```

Sonnet 5 / 5.5 is more agentic than Sonnet 4.6 by default. Legacy Sonnet 5 with thinking disabled is *less* likely to reach for tools -- add an explicit nudge if you rely on tool calls with thinking off. Sonnet 5.5 cannot run thinking off (`disabled` → 400; lowest is `between_tools`); it sometimes answers from training data instead of searching, so add a search-freshness line (e.g. "For anything that may have changed since your training data, search before answering"). Model settings (effort, thinking, concurrency) are configuration, not prompt text (AP-10).

---

## 5. Error Recovery

### Graceful Degradation

```xml
<error_handling>
- If primary data source fails: Use cached data with staleness warning
- If analysis tool errors: Retry once, then report partial results
- If output format fails: Return plain text with explanation
- Always: Report what succeeded and what failed
</error_handling>
```

### Retry with Backoff

```xml
<retry_policy>
- Max retries: 3
- On failure: Report error, attempt alternative approach
- After max retries: Summarize attempts and request human intervention
</retry_policy>
```

### Checkpoint Pattern

```xml
<checkpoint_policy>
After each major step:
1. Save current state to file
2. Report progress to user
3. If interrupted, resume from last checkpoint
</checkpoint_policy>
```

---

## 6. Multi-Context Window Workflows

### State Management Pattern

Use structured formats for schema data, unstructured for progress:

```json
// tests.json - Structured state
{
  "tests": [
    {"id": 1, "name": "auth_flow", "status": "passing"},
    {"id": 2, "name": "user_mgmt", "status": "failing"}
  ],
  "total": 200,
  "passing": 150,
  "failing": 25
}
```

```text
// progress.txt - Unstructured progress
Session 3 progress:
- Fixed token validation
- Updated user model
- Next: investigate test #2 failures
- Note: Do not remove tests
```

### First Context Window Setup

```xml
<first_window_setup>
1. Write tests before implementation (store in tests.json)
2. Create setup scripts (init.sh) for servers, linters, test suites
3. Establish git checkpoints for state recovery
4. Define success criteria
</first_window_setup>
```

### Context Continuation

When starting a fresh context:
```
Call pwd; you can only read and write files in this directory.
Review progress.txt, tests.json, and the git logs.
Run a fundamental integration test before implementing new features.
```

### Maximize Context Usage

```xml
<maximize_context>
This is a very long task. Plan your work clearly. Spend your entire output
context working on the task -- just don't run out of context with significant
uncommitted work. Continue working systematically until complete.
</maximize_context>
```

---

## 7. Sub-Agent Orchestration

### Orchestrator Pattern

```
You are the ORCHESTRATOR. You coordinate specialists but don't do detailed work.

Available specialists:
- researcher: Deep web research, citation gathering
- coder: Implementation, debugging, testing
- reviewer: Code review, security audit
- writer: Documentation, user-facing content

For each subtask:
1. Identify the right specialist
2. Provide focused context (not everything)
3. Collect and synthesize results
4. Decide next steps
```

### Context Minimization

Pass minimal context to sub-agents:

```python
def create_subagent_context(task, full_context):
    return {
        "task": task,
        "relevant_files": extract_relevant_files(task, full_context),
        "key_decisions": extract_decisions(full_context),
        # NOT: full_conversation_history
    }
```

### Handoff Protocol

```xml
<handoff_format>
When delegating:
1. TASK: Specific deliverable (1-2 sentences)
2. CONTEXT: Only what they need
3. POLICY FACTS: Facts that must survive the handoff, including exculpating
   ones, and who may use them
4. CONSTRAINTS: Quality requirements, boundaries
5. OUTPUT: Expected format

When receiving results:
1. Validate completeness
2. Integrate into main workflow
3. Decide next action
</handoff_format>
```

### Subagent Delegation Per Model

- **Opus 5** delegates more readily than prior generations: cap it (see Section 10).
- **Fable 5 / 5.1**: the opposite guidance -- use subagents frequently, with explicit guidance on when. For fan-out on a long run: `Delegate independent subtasks to subagents and keep working while they run. Intervene if a subagent goes off track or is missing relevant context.`
- **GPT-6 Astra** under-delegates: say when and how much to delegate.
- Uncapped delegation on an eager model is AP-13.

### Early Stopping in Long Autonomous Sessions

Deep into a long session, Fable 5 can end a turn with a statement of intent instead of a
tool call, and Opus 5.5 with a text-only `end_turn` progress report. **Neither is
completion.** Keep a checklist; auto-continue naming the open items, capped at 2-3
continuations. Put this block in the initial system prompt, never mid-session (it
invalidates thinking on 5.x):

```
You are operating autonomously. The user is not watching in real time. For
reversible actions that follow from the original request, proceed without
asking. Before ending your turn, check your last paragraph. If it is a plan,
a list of next steps, or a promise, do that work now with tool calls.
```

---

## 8. send-to-user Tool Pattern (Claude Fable 5 / 5.1, Opus 5.5, Sonnet 5.5)

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
Between tool calls, when you have content the user must read verbatim,
call send_to_user. Use only for user-facing content, not narration or reasoning.
```

Tool inputs are never summarized, so content arrives intact. Defining the tool alone is insufficient -- Fable 5 rarely calls it without explicit elicitation in the system prompt.

On Fable 5.1, Opus 5.5, and Sonnet 5.5, declare the tool from the **first** request. Silent-step nudge: after about 5 silent tool steps, the harness appends a turn-scoped system message ("The user hasn't heard from you in a while -- say in a few words what you're doing, then continue."), max 2-3 nudges. Frequent harness text after tool results can look like injection to Sonnet 5.5.

## 9. Memory Systems (Fable 5 / 5.1 / Long-Horizon)

Fable 5 and 5.1 perform notably better with persistent memory (the same file pattern is a cheap win on Opus 5.5 and Sonnet 5.5 long runs):

```
Store one lesson per file with a one-line summary at the top.
Record corrections and confirmed approaches alike, including why they mattered.
Don't save what the repo or chat history already records.
Update existing notes rather than creating duplicates.
Delete notes that turn out to be wrong.
```

Bootstrap from existing history:
```
Reflect on previous sessions. Use subagents to identify core themes
and lessons, and store them in [X]. Reference [X] for future use.
```

The memory tool pairs well with context awareness for managing context transitions.

## 10. Orchestrator + Executor Pattern (2026)

Dominant cost pattern: **frontier model as orchestrator, cheaper model as executor**.

- Fable 5.1 orchestrating Sonnet 5.5, or Opus 5.5 executor + Fable 5.1 advisor (+1.7 pts at ~2.1× cost — test on your workload)
- Long-lived subagents for cache-read savings (avoid bottlenecking on slowest)
- Asynchronous communication between orchestrator and subagents (don't block -- a non-blocking harness matters most on Fable 5.1)
- Separate verification from writing (fresh-context verifier subagents outperform self-critique)

For cost-sensitive workloads, cap delegation explicitly:
```
Delegate to a subagent only for large tasks that are genuinely independent.
Do not delegate work you can finish in a handful of tool calls.
Do not use subagents to verify your own work.
```

---

## 11. IDE Agent Patterns

### CLAUDE.md Best Practices

```markdown
# CLAUDE.md

## Project Context
[1-2 sentences: what this project does]

## Commands
[Essential build/test/run commands]

## Architecture
[Key patterns, not file listings]

## Conventions
[Only non-obvious rules]
```

**Anti-patterns for CLAUDE.md**:
- Listing every file and directory
- Generic advice ("write good tests")
- Obvious instructions ("don't commit secrets")
- Duplicating README content

### Skill/Command Design

```markdown
---
name: skill-name
description: [What]. USE WHEN [triggers].
---

## Context
[Minimal background]

## Process
[Clear steps or decision tree]

## Output Format
[Expected deliverable]
```

### Agentic Coding Pattern

```xml
<task>Implement user authentication</task>

<approach>
1. Explore existing patterns in codebase first
2. Follow established conventions
3. Implement incrementally with tests
4. Verify each step before proceeding
</approach>

<constraints>
- Don't over-engineer
- Match existing code style
- Ask before major architectural decisions
</constraints>
```

---

## 12. Model-Specific Agentic Guidance

### Claude 5 Family (Current: Fable 5.1, Opus 5.5, Sonnet 5.5; Legacy: Fable 5, Opus 5, Sonnet 5, Opus 4.8)

Per-model delegation behavior:

| Model | Delegation Style | Watch For |
|-------|-----------------|-----------|
| **Fable 5.1** | Frequent delegation with explicit guidance; long-lived subagents (Fable 5 carries over) | Serial one-call-per-turn tool use in loops (batching nudge); prefer async communication over blocking; rare early stopping; extras-only scope |
| **Opus 5.5** | Delegates readily (Opus 5 carries over); text-only `end_turn` progress reports stop unattended loops | Declare the unattended-run block from the first request; elapsed/time-budget line for multi-agent teams; "explore broadly" line for multi-app agents |
| **Sonnet 5.5** | More agentic than 4.6; tool usage scales with effort; literal | Sometimes answers from training instead of searching (add search-freshness line); unrequested tests/docs; mid-turn user text misread as injection; tool-name case drift |
| **Fable 5 (legacy)** | Most aggressive parallel dispatch; supports long-lived subagents | Prefer async communication over blocking on each return |
| **Opus 5 (legacy)** | Delegates readily; effective writer-verifier patterns, few overwrite conflicts | Cap delegation for cost; don't let it use subagents to verify its own work |
| **Opus 4.8 (legacy)** | Dynamic workflows: hundreds of parallel subagents in one session | Codebase-scale migrations; fallback target for Fable 5.1 |
| **Sonnet 5 (legacy)** | More agentic than 4.6; tool usage scales with effort | With thinking OFF, needs explicit tool nudge |

- **Strengths**: Long-horizon reasoning, native parallel tool calling, adaptive thinking, subagent delegation
- **Watch**: Opus 5 caps (cost); Fable 5/5.1 want *more* guided delegation, not less. Forced `tool_choice` returns 400 on Fable 5.1, Opus 5.5, Sonnet 5.5 -- use strict tools or structured outputs
- **Key XML blocks**: See 06-claude-practices_v5.md Section 4-5, 8

### GPT-6 (Astra / 6.1 Sol / Sol / Luna) and GPT-5.x
- **Strengths**: Clean instruction following, minimal verbosity; GPT-6 adds async tool calling (`async: true` on function/custom tools, result returned later under the original `call_id`), mid-turn steering over WebSocket Responses, and `configuration_update` (mid-conversation effort change that keeps the cache prefix; no adjacent updates; incompatible with auto-compaction)
- **Watch (Astra)**: early stopping and approval-seeking -- add an initiative line and a completion definition; under-delegates (say when and how much); over-tests (calibrate down); audit skills/AGENTS.md and strong "ask first" language carried from older models. `reasoning.effort: none` returns 400 on Astra
- **Watch (GPT-5.x)**: persistence at low/medium `reasoning_effort`
- **Misalignment monitoring (Astra)**: async monitoring can return `403 misalignment_policy_violation` -- stop dispatching actions and do not auto-retry
- **Key**: Use the GPT-5.4-guide tag set (`<output_contract>`, `<tool_persistence_rules>`, `<verification_loop>`) or plain labeled sections (the 5.5/5.6/6 guides use labeled sections) -- one convention per prompt; Astra and GPT-6.1 Sol function calling requires the Responses API

### Gemini 3.x
- **Strengths**: Massive context (1M), direct instruction execution
- **Watch**: OMIT sampling params; return thought signatures in stateless multi-turn function calling (unmodified, even across a model switch; resend built-in Search signatures too); exactly one function response per call, matched on both `id` and `name`; keep 10-20 active tools at most; no structured pre-tool text (use `update()`); if it over-uses tools, lower `thinking_level` first, then set an action budget
- **Stateful mode**: Interactions API (`store: true` + `previous_interaction_id`) manages history server-side; stateless multi-turn is where signatures matter
- **Key**: All constraints (behavioral AND formatting) in the system instruction at the TOP; context first, specific question last

### Kimi K3 / K2.6
- **K2.6 strengths**: Agent Swarm v2 (300 sub-agents, 4,000 steps, ~13-hour runs; carried over, not re-verified -- Verify)
- **K3**: long-horizon coding and knowledge work; optional dynamic tool loading (Section 2). Sampling keys are fixed server-side -- send none. Replay full assistant messages verbatim (including `reasoning_content` and `tool_calls`)
- **Key**: Models reach no external resources by default; wire tools explicitly

---

## 13. Agentic Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Prescribing exact tool sequence | Limits model's planning | State goal + constraints |
| Passing full context to sub-agents | Token waste, confusion | Minimal relevant context |
| No error handling | Failures cascade | Explicit recovery patterns |
| No state tracking | Can't resume, loses progress | Checkpoint pattern |
| Over-parallelization | System bottlenecks | Explicit concurrency limits |
| Micromanaging reasoning | Degrades native capabilities | Goal-oriented prompting |
| Redundant tool descriptions / irrelevant tools exposed (AP-7) | Dilutes selection | State each rule once; expose only relevant tools; detail is fine on all three vendors |
| Unbounded delegation (AP-13) | Cost blowup on eager delegators (Opus 5) | Explicit subagent cap; no self-verification subagents |
| No stop condition (AP-13) | Runaway or early-stopping loops | Completion criterion, retry ceiling, checkpoint cadence, escalation path |
| Steering effort/thinking/concurrency in prose (AP-10) | Ignored or overtriggers | Set it in API config |

---

## 14. Agentic Evaluation Metrics

| Metric | Definition | Target |
|--------|------------|--------|
| Task completion rate | % of goals achieved | >90% |
| Step efficiency | Actions vs optimal | <1.5x optimal |
| Error recovery rate | % errors handled | >80% |
| Tool accuracy | Correct tool selection | >95% |
| Parallelization efficiency | Time saved via parallel | >30% reduction |
| Context efficiency | Tokens used vs minimum | <2x minimum |

---

## References

- Anthropic "Building Effective Agents" (2025)
- Anthropic Claude Code Documentation (2025-2026)
- OpenAI GPT-5 / GPT-6 Agentic Workflows Guides (2025-2026)
- Model Context Protocol specification `2026-07-28`
- Yao, S., et al. (2022). "ReAct: Synergizing Reasoning and Acting." [arXiv:2210.03629](https://arxiv.org/abs/2210.03629)
