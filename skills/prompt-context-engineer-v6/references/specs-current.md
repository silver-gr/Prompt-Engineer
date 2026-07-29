# Current Model Specs

*Verified: July 2026 — this is the only dated file in this skill; re-check it first.*

*Source: 03-model-catalog_v5.md (all sections); Claude thinking defaults, effort enum and model IDs cross-checked against 06-claude-practices_v5.md §2 and §11.*

Every price, context window, max output, model ID, effort enum, thinking default, release date and availability fact used anywhere in this skill lives here and only here. `—` means the fact is not stated in the KB: leave it blank, do not guess, see 03-model-catalog_v5.md.

## Anthropic

| Model | Model ID | Context | Max out | $ in/out per 1M | Thinking default | Effort enum | Released |
|---|---|---|---|---|---|---|---|
| Fable 5 | `claude-fable-5` | 1M | 128K | $10/$50 ($5/$25 batch) | Always-on; `disabled` → 400 | `low` `medium` `high`(def) `xhigh` `max` | Jun 9 2026 |
| Mythos 5 | `claude-mythos-5` | 1M | 128K | Same as Fable 5 | Same as Fable 5 | Same | Jun 9 2026 |
| Opus 5 | `claude-opus-5` | 1M | 128K | $5/$25 | On; `disabled` only at effort ≤`high` | `low` `medium` `high`(def) `xhigh` `max` | Jul 2026 |
| Opus 4.8 | `claude-opus-4-8` | 1M | 128K | $5/$25 (fast $10/$50) | Off unless `type:"adaptive"` set | Same range | May 28 2026 |
| Sonnet 5 | `claude-sonnet-5` | 1M | 128K | $3/$15 (intro $2/$10 to Aug 31 2026) | On; `type:"disabled"` turns off | `low` `medium` `high`(def) `xhigh` `max` | Jun 30 2026 |
| Haiku 4.5 | `claude-haiku-4-5-20251001` | 200K | 64K | $1/$5 | Manual `budget_tokens` | N/A (no effort param) | Oct 2025 |

Verified parameter names: `output_config: {effort}`, `thinking: {type:"adaptive"|"disabled"|"enabled", budget_tokens}`, `speed:"fast"` (Opus 4.8 only), `max_tokens`, `cache_control`.

| API-surface fact | Fable 5 | Opus 5 | Opus 4.8 | Sonnet 5 | Haiku 4.5 |
|---|---|---|---|---|---|
| `temperature`/`top_p`/`top_k` | → 400 | → 400 | → 400 | → 400 | Accepted |
| Assistant prefill | → 400 | → 400 | → 400 | → 400 | Accepted |
| `budget_tokens` | → 400 | → 400 | → 400 | → 400 | Required |
| Tokenizer | New (+30% vs Sonnet 4.6) | New | New | New | Old |
| Fast mode | No | No | Yes | No | No |
| Safety classifiers | Yes | No | No | Yes (cyber) | No |

Effort does not transfer across models. The one documented mapping: Sonnet 5 `medium` ≈ Sonnet 4.6 `high`; Sonnet 5 `high` ≈ Sonnet 4.6 `max`. Sonnet-specific — re-sweep evals per model.
Prompt-cache minimum on Opus 4.8: 1,024 tokens (was 2,048).
Availability: Fable 5 was suspended Jun 12–Jul 1 2026 — keep an Opus 4.8 fallback wired.

## OpenAI

| Model | Model ID | Context | Max out | $ in/cached/out per 1M | Reasoning default | Released |
|---|---|---|---|---|---|---|
| GPT-5.6 Sol | `gpt-5.6-sol` (alias `gpt-5.6`) | 1,050,000 (max input 922,000) | 128,000 | $5 / $0.50 / $30 | `reasoning.effort` = `medium` | Jul 9 2026 |
| GPT-5.6 Terra | `gpt-5.6-terra` | 1,050,000 | 128,000 | — | `medium` | Jul 9 2026 |
| GPT-5.6 Luna | `gpt-5.6-luna` | 1,050,000 | 128,000 | — | `medium` | Jul 9 2026 |
| GPT-5.5 | — | 1,050,000 | 128,000 | — | `reasoning.effort`; Responses API | 2026 |
| GPT-5.3 Instant | — | 128K | — | — | — | Mar 3 2026 |
| GPT-5.2 Thinking (legacy) | — | 400K | — | — | `reasoning.effort` = `none` | Dec 2025 |
| GPT-5.1 | — | 400K | — | — | `none` mode available | Nov 13 2025 |
| GPT-5 base | — | 400K | — | — | — | Aug 2025 |

Effort enum: GPT-5.6 = `none` `low` `medium` `high` `xhigh` `max` (`max` new in 5.6). GPT-5.5 and 5.2 = `none` `low` `medium` `high` `xhigh` (no `max`).
Verbosity: `text.verbosity` = `low` `medium` `high`.
`reasoning_profile: light|balanced|deep` DOES NOT EXIST. It appeared in earlier editions of this KB and was retracted. Never emit it.
Billing: >272K input tokens bills 2x input / 1.5x output for the **entire** request, not the overage. Cache writes bill at 1.25x standard input.
GPT-5.6 GA on Responses, Chat Completions and Batch APIs; persisted reasoning across turns supported; multi-agent orchestration in beta on Responses API only.

## Google

| Model | Model ID | Context | Max out | Pricing | Thinking default | Released |
|---|---|---|---|---|---|---|
| Gemini 3.5 Flash | — | 1M | 64K | — | — | 2026 |
| Gemini 3.1 Pro (Preview) | `gemini-3.1-pro-preview` | 1M | 64K | — | `thinking_level` = `high` (other value: `low`) | Feb 19 2026 |
| Gemini 3.1 Flash-Lite | — | 1M | 64K | — | — | Preview Mar 3 2026, GA May 7 2026 |
| Gemini 2.5 Pro / Flash | — | 1M | — | — | Adaptive thinking budgets | Superseded |

OMIT `temperature`, `top_p`, `top_k` entirely — default 1.0 is the recommended setting; lowering causes loops and degraded performance.

## Grok / DeepSeek / GLM / Qwen / Kimi / MiniMax / Llama / Mistral / Mercury

| Model | Model ID | Context | Max out | Pricing per 1M | Reasoning default | License |
|---|---|---|---|---|---|---|
| Grok 4.5 | `grok-4.5` (aliases `grok-4.5-latest`, `grok-build-latest`) | 500K | — | <200K: $2.00 in / $0.30 cached / $6.00 out · ≥200K: $4.00 / $0.60 / $12.00 | `reasoning_effort` = `high`; `low` `medium` `high`; cannot be disabled | Closed, API-only |
| DeepSeek V4 | — | 1M | 384K | Flash $0.14/$0.28 · Pro $0.435/$0.87 | `reasoning_effort` = `high` (also `max`) | MIT, open weights |
| GLM-5.2 | — | 1M | 64K | — | `reasoning_effort`; High/Max modes | MIT, open weights |
| Qwen 3.7 | `qwen3.7-max` (snapshot `-2026-05-20`, US `qwen3.7-max-us`) · `qwen3.7-plus` | 1M | 32K | ~$1.48 in / $4.43 out (OpenRouter list, not Alibaba's) | `enable_thinking` toggle | Flagship closed/API-only; open option Qwen3.6-35B-A3B (Apache 2.0) |
| Qwen 3.8-Max-Preview | `qwen3.8-max-preview` (ID unconfirmed) | 1M | 65,536 | — | `enable_thinking` toggle | Preview, Token Plan subscribers only |
| Mercury 2 | `mercury-2` (sibling `mercury-edit-2`) | 128K | no published cap; docs example 8,192 | $0.25 in / $0.025 cached / $0.75 out | `reasoning_effort` — `instant` `low` `medium` `high` | Closed, API-only |
| Kimi K3 | — | 1,048,576 | — | $3.00 miss / $0.30 hit in · $15.00 out (flat, no tiering) | Always-on; `reasoning_effort` = `max`; `low` `high` `max` | Open weights, custom "Kimi K3 License" |
| Kimi K2.6 | — | 2M | 64K | — | Thinking + non-thinking modes; temp 1.0 thinking / 0.6 instant | — |
| MiniMax M3 | — | 512K guaranteed | 32K | ~$0.30/$1.20 | — | — |
| Llama 4 Scout | — | 10M | 32K | — | — | Open weights (frozen) |
| Llama 4 Maverick | — | 1M | — | — | — | Open weights, Apr 5 2025 |
| Mistral Large 3 | — | 256K | 32K | — | — | Open weights, Feb 2026 |

Grok 4.5: crossing 200K reprices the **entire** request. `presence_penalty`, `frequency_penalty` and `stop` are rejected as errors.
DeepSeek V4: enable thinking via `extra_body={"thinking":{"type":"enabled"}}` — not raw `<think>` tags. Must echo `reasoning_content` on tool-result turns or the API returns 400. Thinking mode ignores sampling params.
Kimi K3: preserved-thinking-history mode requires replaying full assistant messages (including `reasoning_content` and `tool_calls`) verbatim on later turns. GLM-5.2: preserved thinking blocks must match exactly when replayed.
Kimi K2.6 Agent Swarm v2: 300 sub-agents, 4,000 steps, ~13-hour runs. Variant K2.7-Code has thinking forced on.
Llama 4 Scout released Apr 5 2025; Meta frontier line is frozen.

## Select by need

| Need | Primary | Alternative | Why |
|---|---|---|---|
| Complex reasoning | Fable 5 | GPT-5.5, Opus 4.8 | Highest capability, long-horizon autonomy |
| Coding / software dev | Opus 5 at `xhigh` | Sonnet 5 | SOTA coding, self-verification, code review |
| Huge documents | Llama 4 Scout | 1M class: Claude 5 family, GPT-5.5, Gemini 3.5 | Context size |
| Low latency | Mercury 2 | Haiku 4.5, Gemini 3.5 Flash | >1000 tok/s (diffusion LLM) |
| High-volume / sub-agents | Haiku 4.5 | Sonnet 5 | Speed plus quality at low cost |
| Cost-sensitive | DeepSeek V4 Flash | MiniMax M3, GLM-5.2 free tiers | Frontier quality, lowest cost |
| Budget coding | DeepSeek V4 Pro | MiniMax M3 | Near-frontier at a fraction of cost |
| Multilingual | Qwen 3.7 (API) | Mistral Large 3 | Broadest coverage |
| Agent orchestration | Kimi K2.6 (Swarm v2) | Opus 5, Fable 5 | 300 agents, 4K steps |
| Self-hosted / open-weight | GLM-5.2 | DeepSeek V4 Pro, Kimi K2.7-Code | Top open-weight, MIT |
| EU compliance | Mistral Large 3 | — | European sovereignty |

Dominant cost pattern: frontier model as orchestrator, cheaper model as executor (Fable 5 orchestrating Sonnet 5 / Opus 4.8).
Capability is commoditizing — 5 models sit within 0.4 pts SWE-bench across a 5x price range; price and routing differentiate, not raw capability.

## Deprecated / retiring

| Model | API ID | Status |
|---|---|---|
| Opus 4.7 | `claude-opus-4-7` | Legacy; fast mode removed 2026-07-24 |
| Opus 4.6 | `claude-opus-4-6` | Fast mode disabled 2026-06-29 |
| Opus 4.5 | `claude-opus-4-5-20251101` | Last Opus with manual thinking budgets |
| Sonnet 4.6 | `claude-sonnet-4-6` | Superseded by Sonnet 5; old tokenizer |
| Sonnet 4.5 | `claude-sonnet-4-5-20250929` | 200K context |
| Opus 4.1 | `claude-opus-4-1-20250805` | Deprecated, retires 2026-08-05 |
| GPT-4o / GPT-4 | — | Removed 2025 → migrate to GPT-5.5+ |
| Gemini 2.x | — | Available but superseded → Gemini 3.5 Flash |
| DeepSeek V3.x | — | Available → DeepSeek V4 |
| Llama 3.x | — | Available → Llama 4 (frozen) |

Retired except on select clouds: Opus 4, Sonnet 4, Haiku 3.5.

Everything in this file is configuration you set on the API call. Model settings are configuration, not prompt text — never paste an effort level, a model ID or a thinking mode into the prompt body.

```
DO: Re-verify this file before trusting any number in this skill.
DO: Cite specs by pointing here; never restate a price or context size in another file.
DO: Leave a cell blank and point to 03-model-catalog_v5.md when the KB does not state the fact.
DO: Confirm every parameter name against the KB module before emitting it in code.
DO: Read Qwen 3.7 as 1M context — "128k-256k" in Alibaba's docs is task sizing advice, not the ceiling.
DO: Treat Qwen 3.8-Max-Preview specs as vendor-console-stated; they are not independently corroborated.
DO: Pick Qwen 3.8-Max-Preview over qwen3.7-max for multimodal — qwen3.7-max is text-only.
DON'T: Guess, interpolate, or round a price, context window, or max-output number.
DON'T: Emit reasoning_profile — it does not exist in any provider API.
DON'T: Carry an effort level across models; re-sweep evals per model.
DON'T: Set temperature, top_p, top_k, budget_tokens, or prefill on current Claude or Gemini models.
DON'T: Copy these tables into another reference file — link to this filename instead.
```
