# Agentic Patterns (March 2026)

## Agent Loop Architecture

```
Goal -> Plan -> Execute (tool calls) -> Observe -> Reflect -> Repeat
```

Models manage this loop internally with native tool calling. Don't prescribe the loop.

## Tool Description Format

1-2 crisp sentences per tool. Include WHAT it does and WHAT it returns.

Good:
```json
{"name": "search_customers", "description": "Search customers by name or ID. Returns customer details including email and account status."}
```

Bad:
```json
{"name": "search_customers", "description": "This function allows you to search through the customer database. You should use this when the user asks about a customer. It can search by name or ID. When searching by name, partial matches are returned. Make sure to validate input first..."}
```

## Goal-Oriented Prompting

State the end goal, not the steps to get there:

- Bad: "First search for X, then use tool Y to process, then format with Z"
- Good: "Find customer details for [name] and return their account summary"

## Parallel Tool Calling

- Allow parallel calls when tasks are independent
- Claude: Sonnet 4.6 supports most parallel calls; Opus may need encouragement
- GPT-5: Naturally parallelizes well
- Enforce sequential only when outputs depend on prior results

## State Tracking (Long Tasks)

```xml
<task_state>
{"goal": "...", "completed": [], "current": "...", "pending": [], "blockers": []}
</task_state>
```

For Claude: use git or files for state persistence across sessions.

## Error Recovery

- Retry once for transient failures
- Graceful degradation: report partial results if tools fail
- Checkpoint progress for long-running tasks
- Don't retry the exact same failing call -- vary approach

## Persistence Reminders

Critical for GPT-5 at light/balanced reasoning profiles:
```
Continue working until the task is fully complete. Do not stop early.
Check your work before reporting completion.
```

## Sub-Agent Orchestration

- Minimize context passed to sub-agents (need-to-know basis)
- Use handoff protocols: clear input/output contracts
- Orchestrator pattern: one coordinator delegates to specialists

## Multi-Context Window Workflows

For tasks spanning multiple sessions:
1. First window: establish goal, explore, create plan
2. Save state to files (not just conversation memory)
3. Subsequent windows: load state, continue execution
4. Context compaction handles long conversations automatically

## Model Selection for Agents

| Task | Best Model |
|------|-----------|
| Complex orchestration | Sonnet 4.6 / Kimi K2.5 |
| Simple tool routing | Haiku 4.5 / GPT-5.3 Instant |
| Deep planning + execution | Opus 4.6 |
| Budget agents | DeepSeek V3.2 |

## Anti-Patterns

| Pattern | Why It Fails |
|---------|-------------|
| Prescribing tool sequence | Models plan better autonomously |
| Verbose tool descriptions | Confuses model, wastes tokens |
| No persistence reminders | GPT-5 may stop early |
| Passing full context to sub-agents | Overwhelms, reduces accuracy |
