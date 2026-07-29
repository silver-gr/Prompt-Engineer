# Task Pattern: Code

## Code Analysis
- Specify the analysis type (bugs, security, performance, style).
- Provide the full code block with language tag.
- Require structured output (JSON or table).

## Code Generation
- Specify language, version, and constraints (deps, runtime).
- State required interfaces and edge cases.
- Request a single code block (plus tests only if asked).

## Minimal Template
```
Analyze this code for [issues].

<code>
[code block]
</code>

Return JSON with fields: issues[], severity, recommendation.
```

## Avoid
- Step-by-step reasoning instructions.
- Overly verbose tool descriptions.
