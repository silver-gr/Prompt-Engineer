# Anthropic (Claude 4.x)

## Core Guidance
- Be explicit and direct; ask for "above and beyond" behavior if desired.
- Explain why the task matters; Claude generalizes from motivations.
- Use XML tags for structure.
- Use extended thinking only if you want visible reasoning.
- Avoid the word "think" when extended thinking is disabled; use "consider" or "evaluate".

## Opus 4.5 Notes
- Can overtrigger tools with aggressive language; keep tool cues calm.
- Supports `effort`: low | medium | high (config).
- Can overengineer; add "keep solutions minimal" if needed.

## Template
```xml
<context>
[background + why it matters]
</context>

<task>
[direct instruction]
</task>

<input>
[data]
</input>

<output_format>
[schema or format]
</output_format>
```
