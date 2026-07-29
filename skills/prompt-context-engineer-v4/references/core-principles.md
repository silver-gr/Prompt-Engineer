# Core Principles (2025+)

## Paradigm Shift
- Context engineering beats prompt cleverness.
- Simpler prompts often win with reasoning models.
- Default to zero-shot; add examples only if format requires it.
- Avoid explicit chain-of-thought instructions unless the user needs to see reasoning.

## Instruction Hygiene
- State the task once, clearly, without persuasive fluff.
- Provide only the context needed for the task.
- Specify output format explicitly.
- Avoid over-constraining how the model should think.

## Context Priorities
1. Task definition (clear, direct)
2. Relevant background (concise)
3. Input data (structured)
4. Output format (schema/template)
5. Reasoning guidance (low priority; usually omit)

## Output Control
- Prefer native JSON mode when supported.
- Provide exact schema or table columns.
- Include constraints only when they change output behavior.

## Long Context Handling
- Use headers and clear sectioning.
- Place critical instructions near both start and end.
- Add a transition line before the task ("Based on the context above...").

## Minimal Model-Agnostic Template
```
## Task
[one sentence]

## Context
[only what is needed]

## Input
[data]

## Output Format
[schema or table columns]
```
