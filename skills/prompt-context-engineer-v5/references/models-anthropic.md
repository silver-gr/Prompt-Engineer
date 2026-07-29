# Anthropic (Claude 4.6 Family, March 2026)

## Models

| Model | Context | Strengths | Use For |
|-------|---------|-----------|---------|
| **Opus 4.6** | 200K | Deepest reasoning, architecture | Complex analysis, planning |
| **Sonnet 4.6** | 200K (1M beta) | Best coding, most parallel tools | Software dev, agent orchestration |
| **Haiku 4.5** | 200K | Fastest, cheapest | Classification, extraction, routing |

## Core Principles

### 1. Be Explicit with Instructions
Claude 4.6 follows instructions precisely. "Above and beyond" behavior requires explicit requests.

- Less effective: `Create an analytics dashboard`
- More effective: `Create an analytics dashboard. Include as many relevant features and interactions as possible. Go beyond the basics.`

### 2. Explain WHY, Not Just WHAT
Claude generalizes from explanations. Providing context or motivation significantly improves output.

- Less effective: `NEVER use ellipses`
- More effective: `Your response will be read aloud by a text-to-speech engine, so never use ellipses since the engine won't know how to pronounce them.`

### 3. Be Vigilant with Examples
Claude pays close attention to example details. Inconsistent examples cause inconsistent outputs. Use 0-1 examples, format only.

### 4. Concise, Direct Communication
Claude 4.6 prefers direct, efficient communication. Skip persuasive language. The model is less verbose and more fact-based.

## Adaptive Thinking (New in 4.6)

The model autonomously decides when and how deeply to reason.

| Mode | Trigger | Use Case |
|------|---------|----------|
| **Adaptive** (default) | Automatic | Most tasks -- model decides depth |
| **Extended** | `/think`, `/megathink`, `/ultrathink` | Explicit deep reasoning |
| **Interleaved** | After tool results | Reflection on tool output |

### "Think" Word Sensitivity
When extended thinking is **disabled**, Opus is sensitive to the word "think":

| Avoid | Use Instead |
|-------|-------------|
| "think about" | "consider" |
| "think through" | "evaluate" |
| "think carefully" | "analyze" |
| "thinking" | "reasoning" |

## Tool Usage Patterns

- Opus can overtrigger tools with aggressive language. Keep tool cues calm.
- Sonnet supports most parallel tool calls in the family.
- Tool descriptions: 1-2 sentences max. Don't prescribe tool sequence.
- For proactive tool use: "Use tools proactively without asking for confirmation."
- For conservative: "Only use tools when explicitly requested."

## Agentic Coding Patterns

### Code Exploration
```
Before making changes, read and understand the relevant code.
Use Grep/Glob to search the codebase for related patterns.
```

### Hallucination Minimization
```
Never guess at API names, function signatures, or file paths.
Search the codebase to verify before using any identifier.
```

### Over-Engineering Prevention (Opus Specific)
```
Keep solutions minimal. Don't add features beyond what's requested.
A simple fix doesn't need surrounding code refactored.
```

## Template

```xml
<context>
[background + WHY this matters]
</context>

<task>
[direct instruction]
</task>

<output_format>
[JSON schema or format spec]
</output_format>
```

**Settings:** `adaptive thinking: auto` | `effort: auto`

## Cheat Sheet

```
DO: XML tags, explain WHY, be EXPLICIT, let adaptive thinking work,
    /think for explicit depth, parallel tool calls
DON'T: "think" word (thinking off), aggressive tool CAPS,
       over-engineer (Opus), expect above-and-beyond without asking
```
