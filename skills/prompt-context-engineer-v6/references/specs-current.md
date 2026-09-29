# Current Model Specs

*Verified: September 2026 — the only dated file in this skill; the stamp also covers specs-other.md. Re-check it first.*

*Source: `-HQ/docs-reference/2026-09-29-prompting-research-*.md` (R1 Anthropic, R2 OpenAI, R3 Google, R4 xAI/Meta/Mistral, R5 China OSS, R6 papers, R7 landscape).*

Every price, context window, max output, model ID, effort enum, thinking default, release date and availability fact used anywhere in this skill lives here and in specs-other.md, and nowhere else. `—` = not stated: leave it blank, do not guess.

## Anthropic — current

| Model | Model ID | Context | Max out | $ in/out per 1M | Batch · cache read | Thinking default | Default effort | Released | Retires ≥ |
|---|---|---|---|---|---|---|---|---|---|
| Fable 5.1 | `claude-fable-5-1` | 1M | 128K | $10/$50 | $5/$25 · $0.25 | Always-on; `disabled` → 400 | `high` | Sep 1 2026 | Sep 1 2027 |
| Opus 5.5 | `claude-opus-5-5` | 1M | 128K | $4/$20 (fast $8/$40) | $2/$10 · $0.20 | Always-on; `disabled` → 400 at every effort | `medium` | Sep 22 2026 | Sep 22 2027 |
| Sonnet 5.5 | `claude-sonnet-5-5` | 1M | 128K | $2/$10 | $1/$5 · $0.20 | On; `disabled` → 400; lowest is `between_tools` (≤`high` only) | `high` | Sep 28 2026 | Sep 28 2027 |
| Haiku 4.5 | `claude-haiku-4-5-20251001` (alias `claude-haiku-4-5`) | 200K | 64K | $1/$5 | $0.50/$2.50 · $0.10 | Manual `budget_tokens`; off by default | N/A (no effort param) | Oct 2025 | Oct 15 2026 |

Effort enum on every 5.x model and Opus 4.8: `low` `medium` `high` `xhigh` `max`. Setting the default equals omitting it.
Mythos 5.1 `claude-mythos-5-1` = same model as Fable 5.1, Glasswing participants only, no prefix-binding check. Haiku 5.5 is announced with no specs — do not table it.
Batch max output 300K on Opus 5.5 / Sonnet 5.5 with header `output-300k-2026-03-24`.

## Anthropic — legacy (still available)

All 1M context / 128K out.

| Model | Model ID | $ in/out per 1M | Thinking default | Notes |
|---|---|---|---|---|
| Fable 5 | `claude-fable-5` | $10/$50 (batch $5/$25; cache read $1) | Always-on; `disabled` → 400 | Released Jun 9 2026; retires ≥ Jun 9 2027 |
| Mythos 5 | `claude-mythos-5` | same as Fable 5 | same as Fable 5 | Glasswing only; retires ≥ Jun 9 2027 |
| Opus 5 | `claude-opus-5` | $5/$25 (fast $10/$50) | On; `disabled` only at effort ≤`high` | Released Jul 24 2026; retires ≥ Jul 24 2027 |
| Sonnet 5 | `claude-sonnet-5` | **$2/$10 — permanent since Aug 10 2026** (the $3/$15 increase was cancelled); cache read $0.20 | On; `type:"disabled"` turns off | Released Jun 30 2026 |
| Opus 4.8 | `claude-opus-4-8` | $5/$25 (fast $10/$50) | Off unless `type:"adaptive"` | Released May 28 2026; retires ≥ May 28 2027 |

| API-surface fact | Fable 5.1 | Opus 5.5 | Sonnet 5.5 | Fable 5 | Opus 5 | Sonnet 5 | Opus 4.8 | Haiku 4.5 |
|---|---|---|---|---|---|---|---|---|
| Non-default `temperature`/`top_p`; any `top_k` | 400 | 400 | 400 | 400 | 400 | 400 | 400 | Accepted by the API (Python SDK v1.0 removed the typed params) |
| Assistant prefill | 400 | 400 | 400 | 400 | 400 | 400 | 400 | Accepted |
| `budget_tokens` | 400 | 400 | 400 | 400 | 400 | 400 | 400 | Required |
| `thinking:{type:"disabled"}` | 400 | 400 | 400 (use `between_tools`) | 400 | Only at effort ≤`high` | Accepted | Accepted | Accepted |
| Forced `tool_choice` (`any`/`tool`) | 400 | 400 | 400 | Accepted | Accepted | Accepted | Accepted | Accepted |
| Thinking bound to conversation prefix | Yes | Yes | Yes | No | No | No | No | No |
| Per-message effort (beta) | Yes | Yes | Yes (not with `between_tools`) | 400 | Yes | No | — | No |
| Mid-conversation system messages | Yes | Yes | Yes | — | Yes | No | Yes | — |
| Tokenizer | New | New | New | New | New | New | New | Old |
| Fast mode | No | Yes | No | No | Yes | No | Yes | No |
| Safety classifiers | Yes | cyber, bio, reasoning_extraction | cyber, bio, frontier_llm, reasoning_extraction, general_harms | Yes | cyber | bio; cyber (Verify — official pages conflict) | No | No |
| Min cacheable prompt (tokens) | 512 | 512 | 512 | 512 | — | 1,024 | 1,024 | 4,096 |

Prefix binding: editing `system`, `tools` or an earlier turn invalidates later thinking blocks → 400 `The block is bound to a different conversation` for accounts created on or after Aug 31 2026 00:00 UTC; older accounts log only. Thinking blocks are also model-bound: Fable 5.1 reads Opus 5.5 blocks, not the reverse; unreadable blocks drop silently.
Opus 5.5 / Sonnet 5.5 reject `computer_20251124` on the Claude API and Google Cloud (Bedrock still accepts) → use `computer_toolset_20260801`.
Verified parameter names: `output_config: {effort}`; `thinking: {type:"adaptive"|"disabled"|"enabled"|"between_tools", display:"omitted"|"summarized"|"updates", budget_tokens}`; `thinking.block_binding.prefix_mismatch_behavior:"drop_block"`; turn-scoped system message `clear_at:"next_user_message"`; `fallbacks:"default"` (or up to 3 models); `speed:"fast"` (Opus 5.5, Opus 5, Opus 4.8); `max_tokens`; `cache_control`. Beta headers: `thinking-display-updates-2026-08-18`, `thinking-binding-controls-2026-08-01`, `mid-conversation-system-clear-at-2026-08-21`, `mid-conversation-output-config-2026-07-01`, `server-side-fallback-2026-07-01`, `inline-tools-2026-09-15`, `compact-2026-09-04`, `fast-mode-2026-02-01`.
Effort does not transfer across models. Documented pairs only: Opus 5.5 `medium` ≥ Opus 5 `high` (Opus 5.5 `low` close to Opus 5 `high` on several coding evals); Fable 5.1 `medium` ≈ Fable 5 at lower cost; Sonnet 5 `medium` ≈ Sonnet 4.6 `high`. Sonnet 5.5 levels were recalibrated with no published mapping. Opus 5.5 thinks more per turn than Opus 5 at the same level.
Availability: server-side fallback targets: Fable 5.1 → Opus 4.8, Opus 5; Sonnet 5.5 → Sonnet 5 (cyber, frontier_llm only); Opus 5.5 cyber tasks re-route to Opus 4.8. `reasoning_extraction` refusals are never retried. Pre-output refusals in bio, frontier_llm and reasoning_extraction are billed from Sep 24 2026. Fable 5 was suspended Jun 12–Jul 1 2026.

## OpenAI

| Model | Model ID | Context | Max out | $ in / cached / out per 1M (cache write) | Effort enum (default) | Released |
|---|---|---|---|---|---|---|
| GPT-6 Astra | `gpt-6-astra` | 1,050,000 | 128,000 | $10 / $1.00 / $50 ($12.50) | `low` `medium` `high` `xhigh` `max`; `none` → 400; default not documented | Sep 3 2026 |
| GPT-6 Sol | `gpt-6-sol` | 1,050,000 | 128,000 | $2 / $0.20 / $10 ($2.50) | `none`…`max` (`medium`) | Sep 22 2026 |
| GPT-6 Luna | `gpt-6-luna` | 1,050,000 | 128,000 | $0.10 / $0.01 / $0.50 ($0.125) | `none`…`max` (`medium`) | Sep 22 2026 |
| GPT-5.6 Sol | `gpt-5.6-sol` (alias `gpt-5.6`) | 1,050,000 | 128,000 | $4 / $0.40 / $20 ($5) — promo from Aug 21 2026, "at least through Nov 21 2026" | `none`…`max` (`medium`) | Jul 9 2026 |
| GPT-5.6 Terra | `gpt-5.6-terra` | 1,050,000 | 128,000 | $2 / $0.20 / $12 ($2.50) | same | Jul 9 2026 |
| GPT-5.6 Luna | `gpt-5.6-luna` | 1,050,000 | 128,000 | $0.20 / $0.02 / $1.20 ($0.25) | same | Jul 9 2026 |
| GPT-5.5 | `gpt-5.5` (snapshot `gpt-5.5-2026-04-23`) | 1,050,000 | 128,000 | $5 / $0.50 / $30 (no write charge) | `none`…`xhigh` (`medium`) | Apr 24 2026 |
| GPT-5.5 Pro | `gpt-5.5-pro` | 1,050,000 | 128,000 | $30 / — / $180 | `medium` `high`(def) `xhigh` | Apr 24 2026 |
| GPT-5.3-Codex | `gpt-5.3-codex` | 400,000 | 128,000 | $1.75 / $0.175 / $14 | `low`…`xhigh` | Feb 24 2026 |
| chat-latest | `chat-latest` | 400,000 (page as stated) | 128,000 | $5 / $0.50 / $30 | — | rolling alias = ChatGPT Instant; not for production |
| GPT-5.2 / 5.1 / 5 | `gpt-5.2`, `gpt-5.1`, `gpt-5` | 400K | — | $1.75/$0.175/$14 · $1.25/$0.125/$10 · $1.25/$0.125/$10 | — | Dec 2025 · Nov 13 2025 · Aug 2025 |

GPT-6 order: Astra › Sol › Luna. In GPT-5.6, Sol was the flagship (≈ unsuffixed), Terra ≈ mini, Luna ≈ nano. "Sol" names a different tier per generation; Terra has no GPT-6 successor; Astra is not a renamed Terra. All GPT-5.6 models remain live (no deprecation notice).
Effort: GPT-6 Astra `none` → HTTP 400 (migrate to `low`). `minimal` still exists on some older models (migrate to `low`). `max` exists on GPT-5.6+ only.
`reasoning.mode: "standard"|"pro"` on GPT-5.6 and GPT-6 (Responses only), independent of effort; replaces separate Pro slugs for 5.6+; no `gpt-6-*-pro` IDs. `reasoning.context` (5.6+): `auto` (= `all_turns`, default) · `all_turns` · `current_turn`; earlier models default `current_turn`.
Verbosity: `text.verbosity` = `low` `medium` `high`; documented on `gpt-6-astra`; Sol/Luna support (Verify).
`reasoning_profile: light|balanced|deep` DOES NOT EXIST. It appeared in earlier editions of this KB and was retracted. Never emit it.
Billing: >272K input bills 2× input **and cache** rates and 1.5× output for the entire request (GPT-6 and 5.6). Cache writes 1.25× input on GPT-5.6+ (GPT-5.5: no write charge); reads 0.1×. Batch/Flex 50%. Priority renamed **Fast mode** Jul 30 2026 (`service_tier:"fast"` or `"priority"`, 2× price).
Caching params: `prompt_cache_options.ttl:"30m"` (+ `mode:"explicit"`, `prompt_cache_breakpoint`) on 5.6+; `prompt_cache_retention` only ≤5.5.
Surface: GPT-6 Astra function calling requires the Responses API; GPT-6 Sol/Luna function calling on Chat Completions only with `reasoning_effort:"none"`. GPT-6 adds `configuration_update` (mid-conversation effort change), async tool calling, mid-turn steering.

## Google

All current rows: 1M in / 65,536 out.

| Model | Model ID | Thinking levels (default) | $ in/out per 1M | Released | Status |
|---|---|---|---|---|---|
| Gemini 3.8 Flash | `gemini-3.8-flash` | `low` `medium` `high` (`medium`); `minimal` → error | $0.75/$3.75 intro to Dec 31 2026, then $1.50/$7.50 | Sep 2 2026 | GA — top text model |
| Gemini 3.7 Flash | `gemini-3.7-flash` | same as 3.8 | same as 3.8 | Aug 13 2026 | GA |
| Gemini 3.6 Flash | `gemini-3.6-flash` | `minimal` `low` `medium` `high` (`medium`) | same as 3.8 | Jul 21 2026 | GA |
| Gemini 3.5 Flash | `gemini-3.5-flash` | `minimal`…`high` (`medium`) | $1.50/$9.00 | May 19 2026 | GA (legacy Flash) |
| Gemini 3.5 Flash-Lite | `gemini-3.5-flash-lite` | `minimal`…`high` (`minimal`) | $0.30/$2.50 | Jul 21 2026 | GA |
| Gemini 3.1 Flash-Lite | `gemini-3.1-flash-lite` | `minimal`…`high` (`minimal`) | $0.25/$1.50 | GA May 7 2026 | Shuts down May 7 2027 |
| Gemini 3.1 Pro | `gemini-3.1-pro-preview` | `low` `medium` `high` (`high`) | $2/$12; >200K $4/$18 | Feb 19 2026 | Preview |
| Gemini 3 Flash | `gemini-3-flash-preview` | `minimal`…`high` (`high`) | $0.50/$3.00 | Dec 17 2025 | Preview |

OMIT `temperature`, `top_p`, `top_k` entirely — sampling params were **deprecated Jul 21 2026**: ignored on 3.6+ and 3.5 Flash-Lite, 400 on "future model generations", still honored (looping risk) on 3.5 Flash, 3.1 Pro, 3 Flash. Default 1.0 is the recommended setting.
Prefilled model turn → 400 on 3.6+. `candidate_count`/`frequency_penalty`/`presence_penalty` → error on 3.8. `thinking_budget` + `thinking_level` → 400; `thinking_budget` alone kept for backward compatibility (acceptance on 3.7/3.8: Verify). Interactions API GA (Jun 2026) and recommended; `generateContent` legacy but supported.
Status: 3.5 Pro unreleased ("coming soon"); Gemini 4 in training, no release. Knowledge cutoff Jan 2025 for 3.5 Flash and 3 Flash; not published for 3.6–3.8. `gemini-flash-latest` target since May 19: Verify.

## Select by need

| Need | Primary | Alternative | Why |
|---|---|---|---|
| Complex reasoning | Fable 5.1 | GPT-6 Astra, Opus 5.5 at `xhigh` | Official escalation when Opus 5.5 falls short |
| Default / most workloads | Opus 5.5 at `medium` | Sonnet 5.5 | Anthropic's stated starting model |
| Coding / software dev | Opus 5.5 | Sonnet 5.5, Gemini 3.8 Flash | Opus 5.5 `medium` ≥ Opus 5 `high` |
| Huge documents | 1M class: Claude 5.x, GPT-6 / 5.6, Gemini 3.8 Flash | Llama 4 Scout (self-host only) | Scout has no first-party API; hosts are retiring it |
| Low latency | Mercury 2.5 | Haiku 4.5, Gemini 3.5 Flash-Lite, Gemini 3.8 Flash at `low` | Diffusion LLM |
| High-volume / sub-agents | Haiku 4.5 | Sonnet 5.5, GPT-6 Luna | Speed and cost |
| Cost-sensitive | DeepSeek V4.1-Flash | GPT-6 Luna, GLM-5.3-Flash, MiMo-V2.6-Flash | Lowest cost per task |
| Multilingual | Qwen 3.8-Max | Mistral Medium 3.5 | Broadest coverage |
| Agent orchestration | Opus 5.5 | Fable 5.1, Kimi K2.6 Swarm (Verify) | Paces multi-agent teams to a time budget |
| Self-hosted / open-weight | MiMo-V2.6-Pro (MIT) | GLM-5.3-Flash (MIT), DeepSeek V4.1-Flash (MIT), Muse Glimmer (Apache 2.0) | Top open-weights model; GLM-5.3, Kimi K3, Qwen 3.8, MiniMax M3 weights are custom licenses |
| EU compliance | Mistral Medium 3.5 | Mistral Large 3 | European sovereignty; in-region endpoints |

Cost pattern: Opus 5.5 executor + Fable 5.1 advisor (+1.7 pts at ~2.1× cost — test on your workload), or Fable 5.1 orchestrating Sonnet 5.5.
Capability is commoditizing — the open-weights leader scores 46 vs the closed leader's 58 on Artificial Analysis at roughly 1/45 the cost per task; price and routing differentiate.

## Deprecated / retiring

| Group | Status |
|---|---|
| Claude retired / imminent | Opus 4.1 **retired Aug 5 2026** (errors). Sonnet 4.5 `claude-sonnet-4-5-20250929` (200K context) retires ≥ Sep 29 2026 (imminent). Mythos Preview `claude-mythos-preview` deprecated Jun 9 2026, retirement TBA. Retired except on select clouds: Opus 4, Sonnet 4, Haiku 3.5 |
| Claude active (older) | Opus 4.5 `claude-opus-4-5-20251101` (last Opus with manual budgets) ≥ Nov 24 2026; Opus 4.7 ≥ Apr 16 2027 (fast mode removed Jul 24 2026); Opus 4.6 ≥ Feb 5 2027 (fast mode disabled Jun 29 2026); Sonnet 4.6 ≥ Feb 17 2027 (superseded by Sonnet 5; old tokenizer) |
| GPT retired | GPT-5.3 Instant `gpt-5.3-chat-latest` **Aug 10 2026** ("Instant" is now a ChatGPT thinking level on GPT-5.6 Sol/Luna). `gpt-5-codex`, `gpt-5.1-codex*`, `gpt-5.2-codex`, `gpt-5-chat-latest`, `gpt-5.1-chat-latest`, `computer-use-preview` Jul 23 2026; `gpt-5.2-chat-latest` Aug 10 2026 → `gpt-5.6-sol`/`-terra` |
| GPT retiring | `gpt-5-2025-08-07`, mini, nano, `gpt-5-pro`, `o3`, `o3-pro` Dec 11 2026 → `gpt-5.6-*` (Pro → `gpt-5.6-sol` + `reasoning.mode:"pro"`). GPT-5.5 leaves ChatGPT / Codex Oct 14 2026 (API unaffected). Specific GPT-4 / 4o snapshots Oct 23 2026 (`gpt-4o`, `gpt-4o-mini`, `gpt-4.1*` still priced) |
| OpenAI platform | Assistants API shut down Aug 26 2026 → Responses + Conversations. `v1/prompts` Nov 30 2026. Evals platform read-only Oct 31 2026 |
| Gemini | 2.0 Flash / Flash-Lite shut down Jun 1 2026. 2.5 — new users blocked since Sep 18 2026 (existing keep access; "not deprecated"). `gemini-3-pro-preview` shut down Mar 9 2026 → 3.1 Pro. `gemini-3.1-flash-lite-preview` shut down May 25 2026 |

Everything in this file is configuration you set on the API call. Model settings are configuration, not prompt text — never paste an effort level, a model ID or a thinking mode into the prompt body.

```
DO: Re-verify this file before trusting any number in this skill.
DO: Cite specs by pointing here or to specs-other.md; never restate a price or context size elsewhere.
DO: Leave a cell blank when the research docs do not state the fact.
DO: Confirm every parameter name here before emitting it in code.
DON'T: Guess, interpolate, or round a price, context window, or max-output number.
DON'T: Emit reasoning_profile — it does not exist in any provider API.
DON'T: Carry an effort level across models; read "Sol" as the same tier across GPT-5.6 and GPT-6.
DON'T: Set temperature, top_p, top_k, budget_tokens, or prefill on current Claude models; sampling keys or prefill on Gemini 3.6+.
```
