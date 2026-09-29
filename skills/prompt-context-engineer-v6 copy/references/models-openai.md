# GPT (OpenAI) Prompting Rules

*Source: 08-gpt5-practices_v5.md (all sections) — core philosophy, effort/verbosity config, prompt structure, tool descriptions, agentic contract tags, pitfalls.*

## Core philosophy: outcome-first, minimal

State the outcome and stop. Adding instructions to a GPT prompt actively reduces quality — verbose descriptions, elaborate frameworks, and explicit reasoning scaffolds all cost tokens and eval score. Lean prompts win on both axes at once.

| Rule | Meaning |
|---|---|
| **Say it once** | Repeating an instruction degrades performance. One statement, in the right place. |
| **Outcome, not procedure** | Describe the result you want. Do not prescribe the algorithm, variable names, or code structure — the model chooses better than you specify. |
| **Trust the native behavior** | Thoroughness, angle-coverage, and self-checking happen without being asked. Asking for them adds tokens, not quality. |
| **System messages are load-bearing** | They are strongly prioritized. Put role, persistent constraints, and output requirements there — and nothing else. |
| **Steer length with config, not adjectives** | A blunt "be concise" over-truncates. Use the verbosity knob. |

## The GPT prompt template

```markdown
## Task
[concise instruction — the outcome]

## Context
[relevant background, kept minimal]

## Input
[data to process]

## Output Format
[JSON schema or format spec]
```

Section headers may be swapped for XML tags (`<task>`, `<context>`, `<input>`, `<output_format>`) when the surrounding system is tag-structured; keep one convention per prompt.

## Config knobs

Reasoning depth and output length are two **independent** parameters, set in the request, never described in prose inside the prompt.

| Knob | Governs | Surface | Values |
|---|---|---|---|
| `reasoning.effort` | how much the model reasons before answering | Responses API (recommended for new integrations) | references/specs-current.md |
| `reasoning_effort` | same thing, flat spelling | Chat Completions (supported, not deprecated) | references/specs-current.md |
| `text.verbosity` | length and detail of the final answer, independent of effort | Responses API | references/specs-current.md |

**The effort enum is per-model and does not transfer.** Tiers exist on some models and not others; passing a tier the target model does not support is a hard error, not a downgrade. Never port an effort value across models — confirm it against the roster in references/specs-current.md for the exact model you are calling.

`reasoning_profile` **does not exist.** Any prompt or wrapper referencing it produces a rejected call. There is no `"light" | "balanced" | "deep"` parameter on any GPT model.

Effort-dependent prompting:

| Effort band | What the prompt must carry |
|---|---|
| Lowest tiers | Agentic persistence is not native — the model may conclude a task early. Add a continuation rule or a `<tool_persistence_rules>` block. |
| Default band | Nothing extra. |
| Highest tiers | Verification scaffolds are worth their cost here ("list assumptions", "check the answer against the contract"). |

Large-input billing changes above a threshold, and cache writes bill above the standard input rate — thresholds and multipliers live in references/specs-current.md. Model settings are configuration, not prompt text.

## Tool descriptions

Crisp: one to two sentences, maximum. The model infers usage well from concise descriptions; verbose descriptions measurably degrade tool selection.

Describe what the tool does and what it returns. Do not describe when to call it, what not to do with it, or how it relates to other tools. For the worked tool-definition example and the per-provider comparison, see `patterns-agentic.md` — this brevity rule is GPT-scoped and does not apply to Claude or Gemini.

## Agentic contract tags

The official tag set for tool-heavy prompts. It replaces older ad-hoc `<persistence>` / `<dig_deeper_nudge>` reminders. Use only the tags the task needs — not all of them.

| Tag | Purpose |
|---|---|
| `<output_contract>` | exact shape the final answer must take |
| `<tool_persistence_rules>` | when to keep using tools versus stop |
| `<completeness_contract>` | what "done" means for this task |
| `<verification_loop>` | check output against the task before finishing |
| `<citation_rules>` | which claims need sources, and their format |
| `<research_mode>` | search budget and escalation rules |
| `<empty_result_recovery>` | what to do when a tool or search returns nothing |
| `<dependency_checks>` | confirm prerequisite state, files, or data before acting |
| `<instruction_priority>` | resolves system / developer / user conflicts |
| `<memo_mode>` | running progress memo for long sessions |

Search strategy inside `<research_mode>`: one broad pass first, targeted follow-ups only when the broad pass leaves facts missing or contradicted. Jumping straight to narrow repeated searches wastes calls and latency.

## JSON output

Include the literal word "JSON" in the system or user message whenever JSON mode is on. Supply the exact schema and types. Validate programmatically — JSON mode guarantees syntactic validity, not schema conformance.

## Common pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Over-prompting | Output quality drops as the prompt grows | Delete instructions until quality stops improving |
| Anti-laziness phrasing | "be thorough", "consider all angles", "double-check your work" | Remove — native behavior already covers it |
| Verbose system prompt | Important constraints get diluted | System message holds role, constraints, format. Nothing else. |
| Repeated instructions | Same rule stated in two places | State once, in the highest-priority location |
| Over-repeated caution phrases | Model asks for approval it was never meant to need | Say "ask first" once, or not at all |
| Effort left at default everywhere | Latency wasted on trivial tasks, depth missing on hard ones | Match effort to task; sweep per model |
| Missing persistence at low effort | Agentic runs terminate mid-task | `<tool_persistence_rules>` or an explicit continuation rule |
| Blunt "be concise" | Answers truncate below usefulness | Use the verbosity knob instead |
| Prescribed implementation | Worse code than an outcome-only prompt | State language, target environment, and success criteria only |

When scanning a prompt for these literals ("be thorough", "double-check", "ask first"), a match inside a quoted example, a negation, or a code fence is a **candidate, not a violation** — read the surrounding line before flagging it.

```
DO: State the outcome once and stop.
DO: Put role, persistent constraints, and format in the system message.
DO: Set reasoning effort and verbosity as request config, matched to the task.
DO: Confirm the effort value against the target model's own enum before every port.
DO: Keep tool descriptions to one or two sentences saying what they do and return.
DO: Use the official agentic contract tags for tool-heavy prompts.
DO: Add persistence rules when running agentic work at low reasoning effort.
DO: Run one broad search before any narrow follow-ups.
DO: Include the word "JSON" in the message when JSON mode is on, and validate the result.
DON'T: Add "be thorough", "consider all angles", or "double-check your work".
DON'T: Write elaborate frameworks or explicit chain-of-thought scaffolds.
DON'T: Repeat an instruction for emphasis.
DON'T: Write verbose tool descriptions or explain when to call a tool.
DON'T: Prescribe algorithms, variable names, or code structure.
DON'T: Use a blunt "be concise" in place of the verbosity knob.
DON'T: Reuse an effort value across models — the enum is per-model and errors when unsupported.
DON'T: Reference reasoning_profile. It does not exist.
```
