# GPT-5 Practices (OpenAI, March 2026)

This is the dedicated module for GPT-5 family prompting guidance -- the first time GPT-5 gets its own reference (Claude and Gemini already had theirs).

> **Model specs**: See 03-model-catalog_v5.md for GPT-5 family data.
> **Anti-patterns**: See 02-techniques-patterns_v5.md (canonical).

---

## 1. Core Philosophy: Less Is More

GPT-5 models perform best with **minimal, direct prompts**. Adding unnecessary instructions, verbose descriptions, or elaborate frameworks actively reduces quality. This is the single most important principle for GPT-5.

---

## 2. Reasoning Profiles

### Profile Selection

| Profile | Latency | Use For |
|---------|---------|---------|
| `"light"` | Fastest | Simple queries, lookups, formatting |
| `"balanced"` | Default | General tasks, standard reasoning |
| `"deep"` | Slowest | Complex analysis, multi-step problems |
| `"none"` (5.1+) | Ultra-fast | Zero reasoning overhead, simple tasks |

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

### Profile Best Practices

- **Light**: Fast responses. Add persistence reminders for agentic tasks -- model may stop early.
- **Balanced**: Default. Good for most tasks. No special considerations.
- **Deep**: Complex work. Combine with verification scaffolds: "List assumptions", "Verify answer".
- **None** (5.1+): Pure speed. No internal reasoning. Best for trivial tasks.

**Critical**: Agentic persistence reminders are essential at light/balanced levels. The model may conclude tasks prematurely without them.

```
Continue working until the task is fully complete. Do not stop early.
```

---

## 3. Prompt Structure

### Recommended Format

GPT-5 works best with clean Markdown structure:

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

## 7. GPT-5.2 Thinking Mode

GPT-5.2 Thinking is the **SOTA model for chatbot use** as of March 2026.

Key characteristics:
- Deep reasoning mode produces highest-quality conversational responses
- Cleaner formatting and less verbosity than predecessors
- Strongest instruction adherence of any model
- Excellent tool grounding

### When to Use 5.2 Thinking vs 5.3 Instant

| Scenario | Use |
|----------|-----|
| Complex analysis, research | 5.2 Thinking |
| Multi-step reasoning | 5.2 Thinking |
| Real-time chat, simple queries | 5.3 Instant |
| High-volume, cost-sensitive | 5.3 Instant |
| Coding with edge cases | 5.2 Thinking |
| Data extraction, formatting | 5.3 Instant |

---

## 8. Common Pitfalls

### Over-Prompting
Adding more instructions makes GPT-5 output worse. Resist the urge to add "be thorough", "consider all angles", "double-check your work". The model does this naturally.

### Verbose System Prompts
Long system prompts dilute important instructions. Keep system messages focused on role, constraints, and format.

### Ignoring Reasoning Profiles
Defaulting to `balanced` for everything wastes latency on simple tasks and misses depth on complex ones. Match profile to task.

### Missing Persistence Reminders
At `light` and `balanced` profiles, agentic tasks may terminate prematurely. Add explicit continuation instructions.

---

## 9. GPT-5 Cheat Sheet

```
DO:
- Keep prompts MINIMAL
- Use reasoning_profile: "light" | "balanced" | "deep"
- Crisp tool descriptions (1-2 sentences)
- Use JSON mode for structured output
- System messages for role and constraints
- Specify language and success criteria for code
- Add persistence reminders for agentic tasks

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

## References

- [OpenAI GPT-5 Platform Documentation](https://platform.openai.com/docs)
- [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)
- [GPT-5 Best Practices](https://platform.openai.com/docs/guides/gpt-best-practices)
