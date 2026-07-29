# Minimal Templates

## Context Pack Format
```
Context Pack
- references/core-principles.md
- references/models-<model>.md
- references/tasks-<task>.md
```

## GPT-5 Family
```
## Task
[direct instruction]

## Input
[data]

## Output Format
[schema]
```

## Claude 4.x
```xml
<context>
[background + why]
</context>
<task>
[direct instruction]
</task>
<input>
[data]
</input>
<output_format>
[schema]
</output_format>
```

## Gemini 3.x
```xml
<context>
[all material]
</context>
<task>
[direct instruction]
</task>
<constraints>
[format/limits last]
</constraints>
```
