# GPT (OpenAI) Prompting Rules

*Source: 08-gpt5-practices_v5.md (all sections) — core philosophy, effort/verbosity config, prompt structure, tool descriptions, agentic contract tags, pitfalls; OpenAI latest-model guide and GPT-5.6 prompt guidance (refresh research).*

## Core philosophy: outcome-first, minimal

State the outcome and stop. Adding instructions to a GPT prompt actively reduces quality — verbose descriptions, elaborate frameworks, and explicit reasoning scaffolds all cost tokens and eval score. Lean prompts win on both axes at once.

| Rule | Meaning |
|---|---|
| **Say it once** | Repeating an instruction degrades performance. One statement, in the right place. |
| **Outcome, not procedure** | Describe the result you want. Do not prescribe the algorithm, variable names, or code structure — the model chooses better than you specify. |
| **Trust the native behavior** | Thoroughness, angle-coverage, and self-checking happen without being asked. Asking for them adds tokens, not quality. GPT-6 Astra over-tests; calibrate testing down. |
| **ALWAYS/NEVER only for true invariants** | Use decision rules for judgment calls; conflicting rules create more instability than missing detail. |
| **Fix the prompt before raising effort** | Check for a missing success criterion, dependency rule, routing rule or verification loop; effort is a tuning knob, not the quality fix. |
| **System messages are load-bearing** | They are strongly prioritized. Put role, persistent constraints, and output requirements there — and nothing else. |
| **Steer length with config, not adjectives** | A blunt "be concise" over-truncates. Use the verbosity knob. |

## The GPT prompt template

```markdown
## Role
## Personality
## Goal
## Success criteria
## Constraints
## Tools
## Output
## Stop rules
```

OpenAI's suggested structure; keep each section short. Section headers may be swapped for XML tags (`<role>`, `<goal>`, `<constraints>`, `<output>`) when the surrounding system is tag-structured; keep one convention per prompt.

## Config knobs

Reasoning depth and output length are two **independent** parameters, set in the request, never described in prose inside the prompt.

| Knob | Governs | Surface | Values |
|---|---|---|---|
| `reasoning.effort` | how much the model reasons before answering | Responses API (recommended for new integrations) | references/specs-current.md |
| `reasoning_effort` | same thing, flat spelling | Chat Completions (supported, not deprecated) | references/specs-current.md |
| `reasoning.mode` | `standard` / `pro`; independent of effort | Responses API only | references/specs-current.md |
| `reasoning.context` | which prior-turn reasoning is kept; `all_turns` is the default on 5.6+ | Responses API | references/specs-current.md |
| `text.verbosity` | length and detail of the final answer, independent of effort | Responses API | references/specs-current.md |

**The effort enum is per-model and does not transfer.** Tiers exist on some models and not others; passing a tier the target model does not support is a hard error, not a downgrade. Never port an effort value across models — confirm it against the roster in references/specs-current.md for the exact model you are calling.

`configuration_update` (GPT-6): an input item that changes effort mid-conversation and keeps the cache prefix. No adjacent updates; incompatible with auto-compaction.

`reasoning_profile` **does not exist.** Any prompt or wrapper referencing it produces a rejected call. There is no `"light" | "balanced" | "deep"` parameter on any GPT model.

Effort-dependent prompting:

| Effort band | What the prompt must carry |
|---|---|
| Lowest tiers | Agentic persistence is not native — the model may conclude a task early. Add a continuation rule or a `<tool_persistence_rules>` block. |
| Default band | Nothing extra. |
| Highest tiers | GPT-5.6: concrete validation steps pay off ("list assumptions", "check the answer against the contract"). Astra already over-verifies; calibrate down. |
| Astra (any tier) | Early stopping and approval-seeking are a model trait: add an initiative prompt and a completion definition. |

Large-input billing changes above a threshold, and cache writes bill above the standard input rate — thresholds and multipliers live in references/specs-current.md. Model settings are configuration, not prompt text.

## Tool descriptions

Crisp and precise. State what the tool does, **when to use it**, important return fields and error behavior. Expose only task-relevant tools. Verbose descriptions measurably degrade tool selection.

For the worked tool-definition example and the per-provider comparison, see `patterns-agentic.md`.

## Agentic contract tags

Tag set from OpenAI's GPT-5.4 guide; the 5.5/5.6/6 guides use plain labeled sections instead. Use only the tags the task needs — not all of them. On 5.6+, `<tool_orchestration>` routes Programmatic Tool Calling.

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

## GPT-6 Astra behavior

Observed on Astra; evaluate on GPT-6 Sol/Luna (no separate Sol/Luna guide exists). Guidance that helps Sol/Luna may over-constrain Astra.

| Behavior | Remedy |
|---|---|
| Initiative: asks non-blocking questions, stops early | "Persist until the goal is complete; ask approval only after preparing a concrete, reviewable result." Define completion before starting. |
| Instruction following: sensitive to skills and AGENTS.md | Audit them. State "The user's instructions take precedence over guidelines provided in a skill." |
| Writing style: heavy Markdown, recurring phrases | Specify style; the anti-slop phrase list lives in `tasks-content.md`. |
| Delegation: under-delegates | Say when and how much to delegate. |
| Testing: over-tests | "No tests for reversible, low-impact changes that mirror the implementation." |

Sampling: remove `temperature`, `top_p`, `top_logprobs`, `logprobs` on GPT-6 when effort is not `none` (whether they error or are ignored: Verify). `reasoning.effort: none` returns 400 on Astra.

Evidence for AP-9: OpenAI internal runs show leaner prompts gave +10-15% eval score, -41-66% tokens, -33-67% cost (directional).

## JSON output

Include the literal word "JSON" in the system or user message whenever JSON mode is on. Supply the exact schema and types. Validate programmatically — JSON mode guarantees syntactic validity, not schema conformance.

## Common pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Over-prompting | Output quality drops as the prompt grows | Delete instructions until quality stops improving |
| Thoroughness phrasing | "be thorough", "consider all angles", "double-check your work" | Remove — native behavior already covers it |
| Missing completion/persistence phrasing on Astra | Stops early, asks non-blocking questions | Recommended: "persist until the goal is complete" plus a completion definition |
| Verbose system prompt | Important constraints get diluted | System message holds role, constraints, format. Nothing else. |
| Repeated instructions | Same rule stated in two places | State once, in the highest-priority location |
| Over-repeated caution phrases | Model asks for approval it was never meant to need | Say "ask first" once, or not at all. Strong "ask first / wait for approval" language carried from older models makes Astra stall; audit it on migration |
| Effort left at default everywhere | Latency wasted on trivial tasks, depth missing on hard ones | Match effort to task; sweep per model |
| Missing persistence at low effort | Agentic runs terminate mid-task | `<tool_persistence_rules>` or an explicit continuation rule |
| Blunt "be concise" | GPT-5.6+ is terser by default; answers truncate below usefulness | Use the verbosity knob; say what a short answer must keep |
| Prescribed implementation | Worse code than an outcome-only prompt | State language, target environment, and success criteria only |

When scanning a prompt for these literals ("be thorough", "double-check", "ask first"), a match inside a quoted example, a negation, or a code fence is a **candidate, not a violation** — read the surrounding line before flagging it.

```
DO: State the outcome once and stop.
DO: Put role, persistent constraints, and format in the system message.
DO: Set reasoning effort and verbosity as request config, matched to the task.
DO: Confirm the effort value against the target model's own enum before every port.
DO: Keep tool descriptions concise: what, when, returns, errors.
DO: Use contract tags or labeled sections — one convention per prompt.
DO: Add persistence rules when running agentic work at low reasoning effort.
DO: For Astra, define completion and add an initiative line.
DO: Run one broad search before any narrow follow-ups.
DO: Include the word "JSON" in the message when JSON mode is on, and validate the result.
DON'T: Add "be thorough", "consider all angles", or "double-check your work".
DON'T: Write elaborate frameworks or explicit chain-of-thought scaffolds.
DON'T: Repeat an instruction for emphasis.
DON'T: Write verbose tool descriptions.
DON'T: Prescribe algorithms, variable names, or code structure.
DON'T: Use a blunt "be concise" in place of the verbosity knob.
DON'T: Reuse an effort value across models — the enum is per-model and errors when unsupported.
DON'T: Reference reasoning_profile. It does not exist.
DON'T: Send `reasoning.effort: none` to GPT-6 Astra.
```
