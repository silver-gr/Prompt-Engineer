# Model-Specific Templates (March 2026)

## Claude 4.6

```xml
<context>
[background + WHY this matters]
</context>

<task>
[direct instruction]
</task>

<input>
[data to process]
</input>

<output_format>
[JSON schema or format spec]
</output_format>
```

Settings: `adaptive thinking: auto` | `effort: auto`

## GPT-5.x

```markdown
## Task
[concise instruction -- less is more]

## Context
[relevant background -- keep minimal]

## Input
[data]

## Output Format
[JSON schema]
```

Settings: `reasoning_profile: balanced` (light | balanced | deep | none)

## Gemini 3.1

```xml
<context>
[all material FIRST]
</context>

<task>
[direct instruction -- no fluff]
</task>

<constraints>
[format/limits LAST -- critical placement]
</constraints>
```

Settings: `temperature: 1.0` (REQUIRED) | `thinking_level: high`

## Model-Agnostic (Safe Default)

```markdown
## Task
[one clear sentence]

## Context
[only what is needed]

## Input
[data]

## Output Format
[schema or table columns]
```

## System Prompt Template

```markdown
You are a [role] specializing in [domain].

[1-2 sentences on approach/constraints]

[Output format requirement]
```

## Agentic Task Template

```markdown
## Goal
[end state to achieve]

## Available Tools
[tool list with 1-2 sentence descriptions each]

## Constraints
- [boundary 1]
- [boundary 2]

Continue working until the task is fully complete.
```

## Data Extraction Template

```markdown
## Task
Extract [entities] from the following [data type].

## Input
[data]

## Output Format
Return JSON matching this schema:
{
  "items": [
    {"field1": "type", "field2": "type"}
  ]
}
```

## Code Review Template

```xml
<context>
[language, framework, purpose of the code]
</context>

<code>
[code to review]
</code>

<task>
Review for [bugs | security | performance | all].
Return findings as JSON: {"issues": [{"type": "", "severity": "", "line": 0, "fix": ""}]}
</task>
```

## Content Generation Template

```markdown
## Task
Write [content type] about [topic].

## Audience
[who will read this]

## Tone
[formal | conversational | technical]

## Constraints
- Length: [word count or range]
- Format: [structure requirements]
- Include: [required elements]
```
