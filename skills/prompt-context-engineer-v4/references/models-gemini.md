# Google (Gemini 3.x)

## Core Guidance
- Be direct; treat the prompt as executable instructions.
- Keep temperature at 1.0 (config).
- Use `thinking_level`: low | high (config).
- Put context first, task after, constraints last.
- Avoid conversational padding.
- Use explicit labels for multimodal inputs.

## Few-Shot Policy
- Default: zero-shot.
- If you need a format example, use 1 example.
- Only use 2 examples if a non-standard format requires it.
- Never include reasoning steps in examples.

## Constraint Order (critical)
1. Context and source material
2. Main task
3. Negative/formatting/quantitative constraints (last)

## Template
```xml
<context>
[all relevant material]
</context>

<task>
[direct instruction]
</task>

<constraints>
[limits and formatting, last]
</constraints>
```
