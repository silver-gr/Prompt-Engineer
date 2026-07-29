# Agentic Patterns

*Source: 10-agentic-patterns_v5.md (tool descriptions, goal-oriented prompting, sub-agent orchestration, memory, send-to-user) plus 06-claude-practices_v5.md sections 4, 5, 8, 15*

The prompt's job in an agent loop is to state the goal, bound the blast radius, and define when to stop — not to script the tool sequence (AP-8) or micromanage reasoning the model does natively.

## Tool description discipline

No universal rule exists — vendors disagree, and following the wrong one costs accuracy.

| Provider | Guidance | "When to use it" text |
|---|---|---|
| OpenAI | Keep crisp; verbose descriptions degrade quality | Redundant — remove |
| Anthropic | Describe what the tool does *and* when to use it | Recommended when tool choice is ambiguous |
| Google | No maximum; capabilities, conditions, examples encouraged | Recommended |

AP-7 (tool description verbosity) is an OpenAI-scoped finding; a detailed Claude or Gemini description is not a violation. Universal rules: one short line per parameter, enums where the value set is closed, edge-case handling in code rather than in the description.

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

## Goal-oriented prompting

```xml
<goal>Deploy the updated API to production and verify it's working</goal>
<available_tools>build, deploy, health_check, rollback</available_tools>
<constraints>
- Run tests before deploying
- Verify health after deploy
- Rollback if health check fails
</constraints>
```

## Orchestrator + executor — the dominant pattern

Frontier model orchestrates, cheaper model executes.

| Rule | Why |
|---|---|
| Orchestrator coordinates, never does the detailed work | Keeps its context free for routing decisions |
| Hand over task, relevant files, key decisions — never the full conversation | Full-context handoff wastes tokens and confuses the executor |
| Prefer long-lived subagents | Cache reads amortize; avoids re-priming per subtask |
| Communicate asynchronously | Blocking on each return bottlenecks on the slowest agent |
| Verification is a separate lane with fresh context | Fresh-context verifiers outperform self-critique |

```xml
<handoff_format>
When delegating: TASK (specific deliverable, 1-2 sentences), CONTEXT (only what
they need), CONSTRAINTS (quality requirements, boundaries), OUTPUT (expected format).
When receiving results: validate completeness, integrate, decide next action.
</handoff_format>
```

## Subagent caps

Current Claude models delegate more readily than prior generations — Opus 5 and Fable 5 both dispatch subagents on work a single agent finishes faster. Uncapped delegation is AP-13.

```
Delegate to a subagent only for large tasks that are genuinely independent and
parallelizable. Do not delegate work you can finish yourself in a handful of
tool calls, and do not use subagents to verify or double-check your own work.
If one subagent can complete the task, use one rather than several.
```

Inverse case — a long Fable 5 run where you want fan-out: `Delegate independent subtasks to subagents and keep working while they run. Intervene if a subagent goes off track or is missing relevant context.`

Concurrency is your harness's decision, not the model's: the model emits several tool calls in one turn; you choose whether to run them at once. Bound it with `<execution_constraints>Maximum N concurrent tool calls. Wait for results before next batch.</execution_constraints>`. Tool-call volume scales with reasoning effort, and Sonnet 5 with thinking off reaches for tools less — nudge explicitly if you depend on tool calls in that configuration. Model settings are configuration, not prompt text.

## Stop conditions

An autonomous run without a stop condition is AP-13. Specify all four: completion criterion, retry ceiling, checkpoint cadence, escalation path.

```xml
<retry_policy>
Max retries: 3. On failure, report the error and attempt an alternative approach. After max retries, summarize attempts and request human intervention.
</retry_policy>
<checkpoint_policy>
After each major step: save state to file, report progress, and on interruption resume from the last checkpoint.
</checkpoint_policy>
```

## Early stopping in long autonomous sessions

Deep into a long session, Fable 5 can end a turn with a statement of intent instead of a tool call — the plan is stated, the work is not done. Mitigation for unattended pipelines:

```
You are operating autonomously. The user is not watching in real time. For
reversible actions that follow from the original request, proceed without
asking. Before ending your turn, check your last paragraph. If it is a plan,
a list of next steps, or a promise, do that work now with tool calls.
```

## send-to-user tool for long async runs

Delivers content verbatim mid-turn without ending it; tool inputs are never summarized, so the message arrives intact.

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

Defining the tool is not enough — Fable 5 rarely calls it without elicitation: `Between tool calls, when you have content the user must read verbatim, call send_to_user. Use only for user-facing content, not narration or reasoning.`

## Memory files and cross-window state

Fable 5 performs notably better with a persistent memory file. Rules govern the file, not the model:

```
Store one lesson per file with a one-line summary at the top.
Record corrections and confirmed approaches alike, including why they mattered.
Don't save what the repo or chat history already records.
Update existing notes rather than creating duplicates.
Delete notes that turn out to be wrong.
```

Bootstrap from history with `Reflect on previous sessions. Use subagents to identify core themes and lessons, and store them in [X]. Reference [X] for future use.` Use structured JSON for schema data (test status, task lists), unstructured text for progress notes, git for checkpoints. Open a fresh context window with prescriptive discovery: pin the working directory, read the state files and git log, run one integration check before new work.

```
DO: State the goal and constraints; let the model choose the tool sequence.
DO: Match tool-description verbosity to the target provider, not a universal rule.
DO: Cap subagent delegation explicitly on current Claude models.
DO: Give every autonomous run a completion criterion, retry ceiling, and checkpoint cadence.
DO: Verify in a separate lane with fresh context.
DO: Add the last-paragraph check to unattended long-running prompts.
DO: Elicit send_to_user in the system prompt, not just in the tool schema.
DO: Hand subagents the task, relevant files, and key decisions only.
DON'T: Prescribe "first call X, then Y" when dependencies can be stated instead (AP-8).
DON'T: Let a model use subagents to verify its own work.
DON'T: Pass full conversation history to a subagent.
DON'T: Flag a detailed Claude or Gemini tool description under AP-7.
DON'T: Steer effort, thinking, or concurrency in prose when the API exposes them (AP-10).
DON'T: Ship an agent loop with no stop condition or scope bound (AP-13).
```
