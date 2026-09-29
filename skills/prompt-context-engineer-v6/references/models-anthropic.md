# Claude (Anthropic) Prompting Rules

*Source: 06-claude-practices_v5.md (all sections); model behavior context from 03-model-catalog_v5.md §1 Anthropic.*

Prompting current Claude is a **subtraction exercise**. Instructions tuned for prior models are the main defect: they overtrigger, over-verify, and over-expand scope. Cut first, add only what the per-model table below names.

## Per-model behavior

| Model | Prompt shape | Add | Remove | Watch for |
|---|---|---|---|---|
| **Fable 5.1** | Brief instructions; Fable 5 prompts carry over. | `display:"updates"` + an explicit progress-update line; per-turn batching nudge as a turn-scoped system message; official autonomy block and "Delivering work" scope block; extras-only paragraph; surgical-edit line; one complete quoting example; memory file | Anti-formatting rules; narration-suppression lines; tools that return base64 | Serial one-call-per-turn tool use in loops; less search at `low`; drafting long deliverables twice at `xhigh`/`max`; source text reproduced without quotation marks. |
| **Opus 5.5** | Shortest outcome + scope prompt; Opus 5 prompts carry over. | Explicit effort; "explore broadly" line for multi-app agents; elapsed/time-budget line for multi-agent teams; ID-tagged pasted-content wrapper (see patterns-safety.md); named frontend patterns to avoid, not "avoid a generic AI look"; official unattended-run standing instruction at the end of the system prompt from the first request (autonomous harnesses only) | "Think carefully before answering" in chat prompts; "write out your reasoning" instructions; "don't think" rules carried from thinking-off Opus 5 | Text-only `end_turn` progress reports stop unattended loops. Progress notes arrive as empty thinking blocks. More thinking per level than Opus 5. |
| **Sonnet 5.5** | Literal. State scope. | "Keep working until done / stop when done and checked; no unrequested features, tests, files, docs" pair; ideas-only stop line; search-freshness line; real-check verification paragraph at low effort; at `xhigh`/`max`, "no extra review rounds or reviewer sub-agents unless asked"; closing think-through line for JSON reasoning with adaptive thinking (`tasks-data.md`) | "Minimize tool calls" / "only use tools when strictly necessary"; "hold all findings for the final response"; "don't think" rules under `between_tools` (they leak internal XML tags); per-step countdowns after tool results in interactive sessions | Unrequested tests/docs. Builds when asked for ideas. Mid-turn user text misread as injection. Tool-name case drift. |
| **Fable 5** | One brief instruction beats enumeration. Give the reason, not only the request. Use subagents freely with explicit guidance on when. | Memory file (one lesson per file, dedupe, delete wrong notes); progress grounded against tool results; action boundaries; `send_to_user` for long async runs | Prescriptive step lists carried from older prompts (AP-18) | Never ask it to echo/transcribe reasoning → refusal (AP-17). Takes unrequested actions (drafts, backups). Rare early stopping deep in sessions. Do not surface context-budget counts to it. |
| **Opus 5** | Shortest prompt that states the outcome and the scope. | Conciseness instruction; explicit scope fence; subagent cap ("do not use subagents to verify your own work"); length-matching rule for files written to disk | Verification / self-check instructions (AP-16, see below) | Expands scope with unrequested steps. Narrates corrections to its own earlier statements. With thinking off: tool calls leak as visible text and internal XML tags appear — prefer thinking on at lower effort. |
| **Sonnet 5** | Literal. State scope explicitly ("apply to every section, not just the first"). | Tool-use nudge when thinking is off; "report everything, filter in a separate pass" in review harnesses; concrete visual specs (or ask it to propose directions) for frontend | "Summarize every N calls" scaffolding — native updates are better | Follows narrowing instructions faithfully — "only report high-severity" really does suppress the rest. Settles into one default visual style. |
| **Opus 4.8** | Standard direct instruction. | Adaptive thinking **explicitly** — it is off unless set | — | Server-side fallback target for Fable 5.1 and cyber re-route target for Opus 5.5; handles many parallel subagents. |
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

Supporting rules: 3–5 relevant, diverse examples in `<example>` tags (`<thinking>` inside examples may demonstrate the reasoning pattern); role in the system prompt; longform data near the top; say what TO do rather than what not to do ("write in flowing prose" beats "do not use markdown"); the formatting style of your prompt leaks into the response style.

## AP-16 nuance: convert verification into an output contract

AP-16 removes *behavioral* verification instructions on Opus 5 — it self-verifies, so "double-check your answer" buys cost and no accuracy. Deleting the line also deletes the quality surface it was protecting. Preserve that surface by moving it into the output format, where it constrains shape rather than behavior.

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

Fable 5/5.1: Anthropic recommends explicit periodic self-checks on long runs — AP-16 does not apply. Opus 5.5: no official statement; Opus 5 guidance is only "a reasonable starting point" (Verify). Sonnet 5.5 at `xhigh`/`max` needs the *opposite*: an additive "stop and report when checks pass" line.

Detection note: when scanning a prompt for literals such as "double-check", "verify your answer", or "re-verify", a match inside a quoted example, a negation, or a code fence is a **candidate, not a violation** — read the surrounding line before flagging.

## Settings

| Knob | Governs | Values |
|---|---|---|
| `output_config.effort` | how much the model thinks, not how much it says; soft behavioral guidance | references/specs-current.md |
| `thinking.type` | whether adaptive thinking runs; the default differs per model | references/specs-current.md |
| `thinking.display` | whether thinking/progress text comes back; default omitted on 5.x | references/specs-current.md |
| per-message effort (beta) | change effort per turn without breaking the cache | references/specs-current.md |
| `max_tokens` | the only hard ceiling; shared by thinking and text | your budget |

Effort levels do not transfer across models or generations — re-sweep your evals per model rather than porting a level. Model settings are configuration, not prompt text.

```
DO: Cut before you add — start from the shortest prompt that states outcome and scope.
DO: Explain WHY behind each constraint, not just the constraint.
DO: Fence scope explicitly for Opus 5/5.5 and Sonnet 5/5.5.
DO: Convert removed verification instructions into Sources / Limits / Verdict output sections.
DO: Give Fable 5/5.1 a memory file, progress grounding, and action boundaries.
DO: Budget max_tokens for thinking plus text on every thinking-on model.
DO: Wire server-side fallbacks (targets in specs-current.md) and handle stop_reason "refusal" as a success response.
DO: Re-sweep effort on your own evals after any model change.
DO: Keep history append-only and pass thinking blocks back unchanged on Fable 5.1, Opus 5.5, Sonnet 5.5.
DON'T: Add "double-check", "verify your answer", or a final verification step on Opus 5.
DON'T: Enumerate step lists for Fable 5/5.1; never ask any 5.x model with a reasoning_extraction classifier to echo reasoning.
DON'T: Send prefill, budget_tokens, non-default temperature/top_p, or top_k to current models.
DON'T: Use CAPS or "CRITICAL: you MUST" cues to push tool use — current models overtrigger on them. (This targets tool-invocation pressure only; a documented grounding contract such as the investigation block in tasks-code.md is not the same thing.)
DON'T: Keep "summarize every N calls" or anti-laziness phrasing from 4.6-era prompts.
DON'T: Apply the 5-family migration checklist to Haiku 4.5.
DON'T: Force-migrate a 4.x prompt that is still working.
DON'T: Assume Sonnet 5 accepts mid-conversation system messages (5.5 does).
DON'T: Send forced tool_choice to Fable 5.1, Opus 5.5, or Sonnet 5.5.

Generation deltas and the legacy era: `migrate-anthropic.md`.
```
