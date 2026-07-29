# Agentic Patterns (2026 Edition)

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
| OpenAI (GPT-5.x) | Keep descriptions **crisp**; verbose descriptions degrade quality |
| Anthropic | Describe **what the tool does *and* when to use it**; "when to use" text is recommended for resolving tool-selection ambiguity |
| Google (Gemini) | **No maximum**. Detailed descriptions with capabilities, usage conditions, and examples are recommended |

The guidance below (brevity-first) reflects OpenAI's stance. On Claude and
Gemini, prefer describing selection conditions explicitly.

### Brevity-First Format (OpenAI): 1-2 Sentences

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
| Usage instructions in description | Redundant on GPT-5.x; **recommended by Anthropic and Google** | Remove for OpenAI; keep elsewhere |
| Edge case handling in description | Over-constrains | Handle in code |
| "You should use this when..." | Redundant on GPT-5.x; **Anthropic recommends it** when tool choice is ambiguous | Judge per provider |

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

Claude 5-family models emit multiple tool calls in one turn when beneficial. **Your application decides** whether to run them concurrently, sequentially, or mixed -- the model does not execute them. Concurrent execution is where the bottleneck risk lives. Effort level drives tool usage — `high`/`xhigh` show substantially more tool calls in agentic search and coding.

```xml
<execution_constraints>
Maximum 3 concurrent tool calls. Wait for results before next batch.
</execution_constraints>
```

Sonnet 5 is more agentic than Sonnet 4.6 by default. With thinking disabled it is *less* likely to reach for tools — add an explicit nudge if you rely on tool calls with thinking off.

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
3. CONSTRAINTS: Quality requirements, boundaries
4. OUTPUT: Expected format

When receiving results:
1. Validate completeness
2. Integrate into main workflow
3. Decide next action
</handoff_format>
```

---

## 8. send-to-user Tool Pattern (Claude Fable 5)

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

## 9. Memory Systems (Fable 5 / Long-Horizon)

Fable 5 performs notably better with persistent memory:

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

- Fable 5 orchestrates, Sonnet 5/Opus 4.8 executes
- Long-lived subagents for cache-read savings (avoid bottlenecking on slowest)
- Asynchronous communication between orchestrator and subagents (don't block)
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

### Claude 5 Family

Per-model delegation behavior:

| Model | Delegation Style | Watch For |
|-------|-----------------|-----------|
| **Fable 5** | Most aggressive parallel dispatch; supports long-lived subagents | Prefer async communication over blocking on each return |
| **Opus 5** | Delegates readily; effective writer-verifier patterns, few overwrite conflicts | Cap delegation for cost; don't let it use subagents to verify its own work |
| **Opus 4.8** | Dynamic workflows: hundreds of parallel subagents in one session | Codebase-scale migrations |
| **Sonnet 5** | More agentic than 4.6; tool usage scales with effort | With thinking OFF, needs explicit tool nudge |

- **Strengths**: Long-horizon reasoning, native parallel tool calling, adaptive thinking, subagent delegation
- **Watch**: Opus 5 and Fable 5 both delegate more readily than prior models
- **Key XML blocks**: See 06-claude-practices_v5.md Section 4-5, 8

### GPT-5.x
- **Strengths**: Clean instruction following, minimal verbosity
- **Watch**: Persistence at low/medium `reasoning_effort`
- **Key**: Use official agentic contract tags (`<output_contract>`, `<tool_persistence_rules>`, `<verification_loop>`)

### Gemini 3.x
- **Strengths**: Massive context (1M), direct instruction execution
- **Watch**: OMIT sampling params; return thought signatures in stateless multi-turn function calling
- **Key**: Context first, questions last; behavioral constraints TOP, formatting END

### Kimi K2.6
- **Strengths**: Agent Swarm v2 (300 sub-agents, 4,000 steps, ~13-hour runs), 2M context
- **Key**: Built-in multi-agent orchestration at a scale unmatched elsewhere

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
| Verbose tool descriptions | Reduces performance **on GPT-5.x only** | 1-2 sentences for OpenAI; detail is fine on Claude/Gemini |

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
- OpenAI GPT-5 Agentic Workflows Guide (2025-2026)
- Yao, S., et al. (2022). "ReAct: Synergizing Reasoning and Acting." [arXiv:2210.03629](https://arxiv.org/abs/2210.03629)
