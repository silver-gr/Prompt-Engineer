# OpenAI (GPT-5 Family)

## Core Guidance
- Keep prompts minimal and direct.
- Use `reasoning_profile`: light | balanced | deep (config, not prompt text).
- Use native JSON mode for structured output when available.
- Tool descriptions should be 1-2 crisp sentences.
- Avoid overprompting; extra instructions reduce quality.

## Default Settings (suggested)
- reasoning_profile: balanced (deep for complex reasoning)
- temperature: task-dependent (code low; creativity higher)

## Template
```
## Task
[direct instruction]

## Input
[data]

## Output Format
[schema or format]
```
