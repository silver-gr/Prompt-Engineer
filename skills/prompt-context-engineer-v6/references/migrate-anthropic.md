# Claude Migration Deltas

*Source: 06-claude-practices_v5.md (delta and legacy sections); 5 → 5.5 / 5.1 delta from official Claude prompting guidance (refresh research). Per-model Add/Remove lists live in `models-anthropic.md`; values (effort/display enums, IDs, betas) in `references/specs-current.md`.*

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

Apply each target model's **Add** column in `models-anthropic.md` (Opus 5: conciseness, scope fence, subagent cap; Sonnet 5: explicit scope, tool-use nudge with thinking off; Opus 4.8: adaptive thinking explicitly; Fable 5: memory file and progress grounding). Migration-only addition: `max_tokens` headroom on every thinking-on model — thinking shares the ceiling with text.

### (c) What became unsupported — and the fallback route

| Capability lost | Where | Fallback route |
|---|---|---|
| Prefilled assistant turn (forced output prefix) | all current except Haiku 4.5 | Structured Outputs or `output_config.format`; route prefix-critical calls to Haiku 4.5 |
| Sampling-level determinism control | all current except Haiku 4.5 | prompt-level style steering; send determinism-sensitive calls to Haiku 4.5 |
| Hard cap on thinking tokens | all current except Haiku 4.5 | effort is soft guidance only — `max_tokens` is the sole hard ceiling; Haiku 4.5 for a true budget |
| Turning thinking off at all | Fable 5/5.1, Opus 5.5 | lower effort, or route no-think work to another model; Sonnet 5.5: `between_tools` at ≤`high` |
| Turning thinking off cleanly | Opus 5 above its disable ceiling | keep thinking on at a lower effort instead of disabling |
| Mid-conversation system messages | Sonnet 5 (unsupported; Sonnet 5.5 supports them) | Opus 5 and Opus 4.8 accept them after a user turn, no beta header — route Sonnet 5 flows there |
| Asking for exposed reasoning | Fable 5/5.1, Opus 5.5, Sonnet 5.5 | billed refusal; request a summarized rationale as an output-contract section instead |
| Availability and classifier refusals | Fable 5/5.1 | `fallbacks` param or SDK middleware (targets in `references/specs-current.md`); `reasoning_extraction` is never retried; treat `stop_reason:"refusal"` as HTTP 200, not an error |

## Delta: Claude 5 → 5.5 / 5.1

Applies to Fable 5.1, Opus 5.5, Sonnet 5.5. Official line: existing Opus 5 / Sonnet 5 / Fable 5 prompts should perform well without changes — then apply the per-model Add/Remove lists in `models-anthropic.md`.

### (a) Breaking — identical call, different outcome

| Field | Same call on 5.5 / 5.1 | Passing form |
|---|---|---|
| `thinking: disabled` | Opus 5.5 (any effort) and Sonnet 5.5 → HTTP 400 | Opus 5.5: lower effort. Sonnet 5.5: `between_tools` (≤`high`, no extra fields) |
| Forced `tool_choice` (`any` / `tool`) | HTTP 400 (all three) | `auto` + `strict:true` or structured outputs; say in the prompt when the tool applies |
| Editing history (system, tools, earlier turns, deleting injected reminders) | HTTP 400 on newer accounts (thinking blocks are bound to the prefix) | append-only history; mid-conversation or turn-scoped system messages; server-side compaction |
| Legacy computer-use tool version | HTTP 400 (Opus 5.5, Sonnet 5.5) | new toolset (IDs in `references/specs-current.md`) |
| Default effort | Opus 5.5 runs one level lower than Opus 5 when omitted | set effort explicitly |

### (b) Silent behavior changes

| Change | Effect | Fix |
|---|---|---|
| Text between tool calls arrives as progress-update `thinking` blocks | empty under default `display` — UI goes silent | `display:"updates"` or `"summarized"` |
| Downward model switch or fallback | thinking blocks dropped silently (Fable 5.1 reads Opus 5.5 blocks, not the reverse) | route upward when reasoning continuity matters |
| Opus 5.5 thinks more per turn at the same effort | cost and latency creep | lower effort first; prompt instructions are less reliable |
| Top-level effort change | invalidates the cache | per-message effort |

### (c) What to carry over

Keep the Opus 5 / Sonnet 5 / Fable 5 prompt. Apply only the 5.5 / 5.1 rows in `models-anthropic.md`; do not rewrite what works.

## [LEGACY] Claude 4.x-era prompting

Recognizable by: explicit chain-of-thought scaffolds, manual thinking budgets, prefill, sampling params, anti-laziness phrasing ("be thorough", "use tools aggressively"), and "summarize every N calls". Haiku 4.5 still lives in this era legitimately.

**A 4.x-era prompt that still works must not be force-migrated.** The delta tables above are an upgrade path taken when you move the model, not a deprecation notice. Migrate the prompt in the same change that swaps the model — not on a schedule, and not because the style looks dated.
