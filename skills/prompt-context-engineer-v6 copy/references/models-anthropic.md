# Claude (Anthropic) Prompting Rules

*Source: 06-claude-practices_v5.md (all sections); model behavior context from 03-model-catalog_v5.md §1 Anthropic.*

Prompting current Claude is a **subtraction exercise**. Instructions tuned for prior models are the main defect: they overtrigger, over-verify, and over-expand scope. Cut first, add only what the per-model table below names.

## Per-model behavior

| Model | Prompt shape | Add | Remove | Watch for |
|---|---|---|---|---|
| **Fable 5** | One brief instruction beats enumeration. Give the reason, not only the request. | Memory file (one lesson per file, dedupe, delete wrong notes); progress grounded against tool results; action boundaries; `send_to_user` for long async runs | Prescriptive step lists carried from older prompts (AP-18) | Never ask it to echo/transcribe reasoning → refusal (AP-17). Takes unrequested actions (drafts, backups). Rare early stopping deep in sessions. Do not surface context-budget counts to it. |
| **Opus 5** | Shortest prompt that states the outcome and the scope. | Conciseness instruction; explicit scope fence; subagent cap ("do not use subagents to verify your own work"); length-matching rule for files written to disk | Verification / self-check instructions (AP-16, see below) | Expands scope with unrequested steps. Narrates corrections to its own earlier statements. With thinking off: tool calls leak as visible text and internal XML tags appear — prefer thinking on at lower effort. |
| **Sonnet 5** | Literal. State scope explicitly ("apply to every section, not just the first"). | Tool-use nudge when thinking is off; "report everything, filter in a separate pass" in review harnesses; concrete visual specs (or ask it to propose directions) for frontend | "Summarize every N calls" scaffolding — native updates are better | Follows narrowing instructions faithfully — "only report high-severity" really does suppress the rest. Settles into one default visual style. |
| **Opus 4.8** | Standard direct instruction. | Adaptive thinking **explicitly** — it is off unless set | — | Primary fallback target for Fable 5. Handles dynamic workflows with many parallel subagents. |
| **Haiku 4.5** | Legacy-shaped prompting is correct here. | Manual thinking budget when you want reasoning | Nothing from the 5-family checklist | **Exception to every other row.** Keeps prefill, manual budgets, sampling params, and the old tokenizer. Do not apply the migration checklist to it. |

## The Claude prompt template

```xml
<context>
[Background, and WHY it matters. State the reason behind each constraint, not
only the constraint — Claude generalizes from motivation.]
</context>

<task>
[One direct instruction. Be explicit about scope: what is in, what is out.]
</task>

<output_format>
[Section names, or a JSON schema, or a format spec.]
</output_format>
```

Supporting rules: a few consistent examples in `<example>` tags (inconsistent examples teach unintended patterns); role in the system prompt; longform data near the top; say what TO do rather than what not to do ("write in flowing prose" beats "do not use markdown"); the formatting style of your prompt leaks into the response style.

## AP-16 nuance: convert verification into an output contract

AP-16 removes *behavioral* verification instructions on Opus 5 and Fable 5 — they self-verify, so "double-check your answer" buys cost and no accuracy. Deleting the line also deletes the quality surface it was protecting. Preserve that surface by moving it into the output format, where it constrains shape rather than behavior.

```xml
<output_format>
Sources: each claim with the file, tool result, or citation it came from.
Limits: what could not be checked, and why.
Verdict: the single conclusion, stated once.
</output_format>
```

Two boundaries keep this from becoming AP-16 again:

| Boundary | Violation | Correct form |
|---|---|---|
| **No action verbs in the contract** | "Verify each claim, then list sources" — an instruction to re-run reasoning | "Sources:" — a section the answer must contain |
| **Task procedure is not self-verification** | Treating "run the suite and paste failing output" as an AP-16 hit | That is the task. AP-16 covers only re-checking work already produced. |

Exception: long-running Fable 5 builds. Anthropic recommends explicit periodic self-checks at a stated interval there, because the model cannot otherwise know when to checkpoint. AP-16 does not apply to that case.

Detection note: when scanning a prompt for literals such as "double-check", "verify your answer", or "re-verify", a match inside a quoted example, a negation, or a code fence is a **candidate, not a violation** — read the surrounding line before flagging.

## Delta: Claude 4.6 → Claude 5 family

Haiku 4.5 is exempt from all three tables.

### (a) Breaking changes — identical call, different outcome

| Field | On 4.6 | Same field on 5 | Passing form on 5 |
|---|---|---|---|
| Prefill | trailing `assistant` message in `messages[]` → accepted | same → HTTP 400 | remove it; use Structured Outputs, `output_config.format`, or a system instruction |
| Manual thinking budget | `"thinking":{"type":"enabled","budget_tokens":N}` → accepted | same → HTTP 400 | `"thinking":{"type":"adaptive"}` plus `output_config.effort` |
| Sampling | `"temperature":X` / `"top_p":X` → accepted | non-default value → HTTP 400 (omitting, or passing the default, still works) | omit; steer style in the prompt |
| `top_k` | `"top_k":X` → accepted | rejected outright → HTTP 400 | omit |
| Tokenizer | `max_tokens` sized against old counts | new tokenizer inflates counts for identical text → `stop_reason:"max_tokens"` truncation | recount and re-budget `max_tokens` (verify per model, not family-wide) |

### (b) What to add

| Add | To | Because |
|---|---|---|
| Conciseness instruction | Opus 5 | default responses run longer than prior Opus |
| Scope fence | Opus 5 | expands narrow tasks with unrequested steps |
| Subagent cap | Opus 5, Fable 5 | both delegate more readily |
| Explicit scope statement | Sonnet 5 | literal instruction following |
| Tool-use nudge | Sonnet 5 with thinking off | less likely to reach for tools |
| `"thinking":{"type":"adaptive"}` | Opus 4.8 | off unless set |
| `max_tokens` headroom | Opus 5, Sonnet 5, Fable 5 | thinking is on by default and shares the ceiling with text |
| "Report everything, filter separately" | review harnesses | literal following of severity filters lowers recall |
| Memory file + progress grounding + autonomy reminder | Fable 5 | performance uplift; prevents fabricated status and early stopping |

### (c) What became unsupported — and the fallback route

| Capability lost | Where | Fallback route |
|---|---|---|
| Prefilled assistant turn (forced output prefix) | all current except Haiku 4.5 | Structured Outputs or `output_config.format`; route prefix-critical calls to Haiku 4.5 |
| Sampling-level determinism control | all current except Haiku 4.5 | prompt-level style steering; send determinism-sensitive calls to Haiku 4.5 |
| Hard cap on thinking tokens | all current except Haiku 4.5 | effort is soft guidance only — `max_tokens` is the sole hard ceiling; Haiku 4.5 for a true budget |
| Turning thinking off at all | Fable 5 | route no-think work to another model |
| Turning thinking off cleanly | Opus 5 above its disable ceiling | keep thinking on at a lower effort instead of disabling |
| Mid-conversation system messages | Sonnet 5 (unsupported) | Opus 5 and Opus 4.8 accept them after a user turn, no beta header — route those flows there |
| Asking for exposed reasoning | Fable 5 | refusal; request a summarized rationale as an output-contract section instead |
| Availability and classifier refusals | Fable 5 | `fallbacks` param or SDK middleware → Opus 4.8; treat `stop_reason:"refusal"` as HTTP 200, not an error |

## [LEGACY] Claude 4.x-era prompting

Recognizable by: explicit chain-of-thought scaffolds, manual thinking budgets, prefill, sampling params, anti-laziness phrasing ("be thorough", "use tools aggressively"), and "summarize every N calls". Haiku 4.5 still lives in this era legitimately.

**A 4.x-era prompt that still works must not be force-migrated.** The delta tables above are an upgrade path taken when you move the model, not a deprecation notice. Migrate the prompt in the same change that swaps the model — not on a schedule, and not because the style looks dated.

## Settings

| Knob | Governs | Values |
|---|---|---|
| `output_config.effort` | how much the model thinks, not how much it says; soft behavioral guidance | references/specs-current.md |
| `thinking.type` | whether adaptive thinking runs; the default differs per model | references/specs-current.md |
| `max_tokens` | the only hard ceiling; shared by thinking and text | your budget |

Effort levels do not transfer across models or generations — re-sweep your evals per model rather than porting a level. Model settings are configuration, not prompt text.

```
DO: Cut before you add — start from the shortest prompt that states outcome and scope.
DO: Explain WHY behind each constraint, not just the constraint.
DO: Fence scope explicitly for Opus 5 and Sonnet 5.
DO: Convert removed verification instructions into Sources / Limits / Verdict output sections.
DO: Give Fable 5 a memory file, progress grounding, and action boundaries.
DO: Budget max_tokens for thinking plus text on every thinking-on model.
DO: Wire an Opus 4.8 fallback and handle stop_reason "refusal" as a success response.
DO: Re-sweep effort on your own evals after any model change.
DON'T: Add "double-check", "verify your answer", or a final verification step on Opus 5 or Fable 5.
DON'T: Enumerate step lists for Fable 5, or ask it to echo its reasoning.
DON'T: Send prefill, budget_tokens, non-default temperature/top_p, or top_k to current models.
DON'T: Use CAPS or "CRITICAL: you MUST" cues to push tool use — current models overtrigger on them. (This targets tool-invocation pressure only; a documented grounding contract such as the investigation block in tasks-code.md is not the same thing.)
DON'T: Keep "summarize every N calls" or anti-laziness phrasing from 4.6-era prompts.
DON'T: Apply the 5-family migration checklist to Haiku 4.5.
DON'T: Force-migrate a 4.x prompt that is still working.
DON'T: Assume Sonnet 5 accepts mid-conversation system messages.
```
