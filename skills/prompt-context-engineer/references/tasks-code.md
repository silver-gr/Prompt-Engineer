# Code Tasks (March 2026)

## Code Generation

- Specify language, framework, and version
- Provide function signature or interface if known
- State error handling expectations
- Request tests alongside implementation when needed
- For Claude: "Keep solutions minimal" prevents over-engineering

### Pattern
```xml
<context>
[language/framework, project context, WHY this code is needed]
</context>

<task>
Implement [function/component] that [behavior].
</task>

<constraints>
- Language: [lang + version]
- Must handle: [edge cases]
- Return: [type/format]
</constraints>
```

## Code Review

- Specify review focus (bugs, security, performance, style)
- Provide surrounding context (what the code does, production vs prototype)
- Request structured output for programmatic processing

### Pattern
```
Review this [language] code for [focus areas].

<context>[purpose and environment]</context>
<code>[code block]</code>

Return JSON: {"issues": [{"type": "", "severity": "critical|warning|info", "line": 0, "description": "", "fix": ""}]}
```

## Code Explanation

- Specify audience level (junior dev, non-technical, expert)
- Ask for specific aspects (architecture, data flow, edge cases)
- Request diagrams or pseudocode for complex logic

## Refactoring

- Describe the problem with current code (not just "refactor this")
- Specify constraints (backward compatibility, performance requirements)
- Provide tests that must still pass

## Model Selection for Code

| Task | Best Model |
|------|-----------|
| Complex architecture | Opus 4.6 |
| Implementation | Sonnet 4.6 |
| Quick code completion | GPT-5.3 Instant / Haiku 4.5 |
| Budget coding | DeepSeek V3.2 |
| Code review | Opus 4.6 / GPT-5.2 Thinking |

## Avoid

- Step-by-step reasoning instructions (models reason internally)
- Overly verbose tool descriptions in coding agents
- Prescribing implementation approach (state WHAT, not HOW)
