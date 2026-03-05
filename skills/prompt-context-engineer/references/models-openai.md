# OpenAI (GPT-5 Family, March 2026)

## Models

| Model | Strengths | Use For |
|-------|-----------|---------|
| **GPT-5.2 Thinking** | SOTA chatbot reasoning | Complex analysis, multi-step problems |
| **GPT-5.3 Instant** | Ultra-fast, cheap | Routing, classification, simple tasks |
| **GPT-5.1** | Stable, well-tested | General production workloads |

## Core Philosophy: Less Is More

GPT-5 performs best with **minimal, direct prompts**. Adding unnecessary instructions, verbose descriptions, or elaborate frameworks **actively reduces quality**. This is the single most important principle.

## Reasoning Profiles

| Profile | Latency | Use For |
|---------|---------|---------|
| `"light"` | Fastest | Simple queries, lookups, formatting |
| `"balanced"` | Default | General tasks, standard reasoning |
| `"deep"` | Slowest | Complex analysis, multi-step problems |
| `"none"` (5.1+) | Ultra-fast | Zero reasoning overhead, trivial tasks |

### Implementation
```json
{
  "model": "gpt-5.2",
  "reasoning_profile": "deep",
  "messages": [
    {"role": "system", "content": "You are a code reviewer."},
    {"role": "user", "content": "Review this code for security issues:\n[code]"}
  ]
}
```

### Profile Tips
- **Light**: Add persistence reminders for agentic tasks -- model may stop early
- **Balanced**: Good default. No special considerations
- **Deep**: Combine with verification: "List assumptions", "Verify answer"
- **None**: Pure speed. No internal reasoning. Trivial tasks only

### Agentic Persistence
Critical at light/balanced levels:
```
Continue working until the task is fully complete. Do not stop early.
```

## System Messages

Strongly prioritized by GPT-5. Use for:
- Role definition
- Persistent constraints
- Output format requirements
- Keep system messages concise -- verbosity reduces effectiveness

## JSON Mode

```json
{
  "response_format": {"type": "json_object"},
  "messages": [{"role": "user", "content": "Extract entities as JSON..."}]
}
```

Always mention "JSON" in the prompt when using JSON mode.

## Tool Descriptions

1-2 crisp sentences. The model plans tool usage autonomously.

- Bad: 5-sentence description explaining when/how to use the tool
- Good: `"Search customers by name or ID. Returns customer details."`

## Template

```markdown
## Task
[concise instruction -- less is more]

## Input
[data]

## Output Format
[JSON schema]
```

**Settings:** `reasoning_profile: balanced`

## Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| Over-prompting (verbose instructions) | Cut to minimum. Trust the model. |
| Verbose system prompts | 2-4 sentences max for system |
| Missing persistence reminders | Add "Continue until complete" for agents |
| Forcing reasoning on simple tasks | Use profile: "none" or "light" |

## Cheat Sheet

```
DO: MINIMAL prompts, reasoning profiles, crisp tool descriptions,
    JSON mode, persistence reminders for agents
DON'T: over-prompt, verbose tool descriptions,
       force reasoning on simple tasks, elaborate frameworks
```
