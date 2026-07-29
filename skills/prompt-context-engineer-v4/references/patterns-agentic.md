# Agentic Patterns

## Tool Description Format
```
{"name": "tool", "description": "What it does. When to use it.", "parameters": {...}}
```

## Parallelization Control
- Allow parallel calls when tasks are independent.
- Enforce sequential steps when outputs depend on prior results.

## State Tracking (for long tasks)
```xml
<task_state>
{"goal": "...", "completed": [], "current": "...", "pending": []}
</task_state>
```

## Error Recovery
- Retry once for transient failures.
- Report partial results if tools fail.
- Include a brief recovery summary.
