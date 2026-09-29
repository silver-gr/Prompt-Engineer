# Current Model Specs — Other Vendors

*Covered by the Verified stamp in specs-current.md. Version-volatile facts for these vendors live here and nowhere else.*

## xAI / Grok

Docs are branded "SpaceXAI"; the API is still `api.x.ai`. Closed, API-only.

| Model | Model ID | Context | $ in / cached / out per 1M (<200K · ≥200K) | Reasoning | Released |
|---|---|---|---|---|---|
| Grok 4.7 | `grok-4.7` (flagship) | 500K | $2.00 / $0.50 / $6.00 · $4.00 / $1.00 / $12.00 | `reasoning_effort` `low` `medium` `high`(def) `xhigh`; cannot be disabled | Sep 21 2026 (cutoff May 2026) |
| Grok 4.6 | `grok-4.6` | 500K | same as 4.7 | same as 4.7 | Aug 12 2026 |
| Grok 4.5 | `grok-4.5` (aliases `grok-4.5-latest`, `grok-build-latest`) | 500K | $2.00 / $0.30 / $6.00 · $4.00 / $0.60 / $12.00 | `high` default; `low` `medium` `high`; `xhigh` silently treated as `high`; cannot be disabled | API Jul 8 2026 |
| Grok 4.3 | `grok-4.3` | 1M | $1.25 / $0.20 / $2.50 · $2.50 / $0.40 / $5.00 | Default `low`; `none` supported (can be disabled); effort enum: the two xAI pages conflict (Verify) | Redirect target for retired Grok 4 / 4.1-fast / 3 |

Crossing 200K reprices the **entire** request. `presence_penalty`, `frequency_penalty`, `stop` are rejected as errors. `logprobs` silently ignored on grok-4.20+. US regional endpoint +10%.

## Meta

| Model | Model ID | Context | Pricing per 1M | Reasoning | License / released |
|---|---|---|---|---|---|
| Muse Spark 1.3 | `muse-spark-1.3` | 1,048,576 | Standard $1.25 in / $0.15 cached / $4.25 out; Contributor tier (`-contributor`, trains on your data) $0.10 / $0.002 / $0.20; no long-context premium | `reasoning_effort` `minimal`…`xhigh` + `max`; `none` → 400 | Closed, API-only; Sep 2 2026 |
| Muse Glimmer | — | 128K default (text+image in) | — | `reasoning_strength` `low` `medium` `high`(def) `xhigh` | 30B dense; Apache 2.0 open weights; Aug 10 2026 |
| Llama 4 Scout | — | 10M | — | — | Open weights only |
| Llama 4 Maverick | — | 1M | — | — | Open weights only, Apr 5 2025 |

Llama is frozen at Llama 4; Meta's current line is Muse (Spark = closed API, Glimmer = open weights). Meta-hosted Llama API retired Jul 6 2026; third-party hosts are retiring Llama 4. Scout released Apr 5 2025, max out 32K.

## Mistral

| Model | Model ID | Context | $ in/out per 1M | Notes | Released |
|---|---|---|---|---|---|
| Mistral Medium 3.5 | `mistral-medium-3-5` | 256K | $1.50/$7.50 | Current flagship; `reasoning_effort` (`high` / `none` documented); Modified MIT open weights | Apr 28 2026 |
| Mistral Small 4 | `mistral-small-2603` | 256K | $0.15/$0.60 | `reasoning_effort`; Apache 2.0 | Mar 16 2026 |
| Mistral Large 3 | `mistral-large-2512` | 256K | $0.50/$1.50 | Apache 2.0; max out 32K (carried, not re-verified) | Dec 2 2025 |

## DeepSeek

| Model | Model ID | Context / max out | $ in/out per 1M (peak · off-peak) | Notes |
|---|---|---|---|---|
| V4.1-Flash | `deepseek-flash` (`deepseek-v4-flash` is now an alias) | 1M / 384K | $0.30/$1.20 · $0.15/$0.60 | MIT; native image input; Sep 10 2026 |
| V4-Pro | `deepseek-v4-pro` | 1M / 384K | $1.32/$3.96 · $0.66/$1.98 | MIT open weights |

Effort `low` `high` `max` (default `high`); `medium`/`xhigh` silently coerced to `high`. Responses API `reasoning.effort:"none"` disables thinking. Peak hours 01–04 and 06–10 UTC Mon–Fri since Aug 16 2026; off-peak = ½ price.
Enable thinking via `extra_body={"thinking":{"type":"enabled"}}`, not raw `<think>`. **Any request carrying `tools` must include `reasoning_content` from all prior turns or the API returns 400.** Thinking mode ignores temperature and penalties; `top_p` honored but clamped 0.95–1.0.

## Qwen

| Model | Model ID | Context / max out | Pricing per 1M | Reasoning | License / released |
|---|---|---|---|---|---|
| Qwen 3.8-Max | `qwen3.8-max` (snapshot `qwen3.8-max-0902`) | 1M / 131,072 | $2/$6 (Alibaba Singapore list) | `enable_thinking` default on; `preserve_thinking`; effort `low` `medium` `xhigh` (default `xhigh`, **no `high`**); effort + `thinking_budget` together → error | Text+image+video; GA Aug 3 2026 |
| Qwen 3.8-Flash | `qwen3.8-flash` | 1M / 131,072 | $0.15/$0.47 | — | — |
| Qwen 3.7-Max | `qwen3.7-max` (snapshot `qwen3.7-max-2026-06-08` adds vision) | 1M / 131,072 | $2.50/$7.50 (official list) | `enable_thinking` toggle | Closed/API |

Open weights: Qwen3.8-2.4T-A95B under a custom license (text-only, thinking-only); Qwen3.8-27B under Apache 2.0.
DO: Read Qwen 3.7 as 1M context — "128k-256k" in Alibaba's docs is task sizing advice, not the ceiling.
DO: Pick Qwen 3.8-Max over qwen3.7-max for multimodal — 3.8-Max is GA and multimodal; qwen3.7-max is text-only unless you use the June snapshot.

## Kimi (Moonshot)

| Model | Model ID | Context / max out | Pricing per 1M | Reasoning | License / released |
|---|---|---|---|---|---|
| Kimi K3 | `kimi-k3` | 1,048,576 / 131,072 default, 1,048,576 max | $3.00 miss / $0.30 hit / $15.00 out; cache write $3.00 (5-min) / $6.00 (1-h) | Always-on; `reasoning_effort` `low` `high` `max` (default `max`) | 2.8T/104B; Kimi K3 License; weights on HF Jul 26–27 2026 |
| Kimi K2.7-Code | `kimi-k2.7-code` | 262,144 | $0.95 / $0.19 / $4.00 (highspeed $1.90 / $0.38 / $8.00) | Thinking forced on | — |
| Kimi K2.6 | — | 262,144 | $0.95 / $0.16 cached / $4.00 | Thinking + non-thinking modes | — |

Temperature, top_p, n and penalties are **fixed server-side on K3, K2.7 and K2.6 — sending another value errors**. K3: preserved-thinking-history mode requires replaying full assistant messages (including `reasoning_content` and `tool_calls`) verbatim. K2.6 Agent Swarm v2: 300 sub-agents, 4,000 steps, ~13-hour runs (carried over, not re-verified — Verify).

## GLM (Z.ai)

| Model | Model ID | Context / max out | Pricing per 1M | Reasoning | License / released |
|---|---|---|---|---|---|
| GLM-5.3 | `glm-5.3` | 1M / 128K | $1.40 / $0.26 cached / $4.40 | Forced thinking (`thinking.type:"disabled"` → error); effort `low` `high` `max` (default `max`) | Custom GLM-5.3 License; Aug 18 2026 |
| GLM-5.3-Flash | `glm-5.3-flash` | 1M / 128K | $0.15 / $0.03 / $0.50 | — | 320B/18B MoE, multimodal; MIT; Aug 26 2026 |
| GLM-5.2 | — | 1M / 128K | $1.40/$4.40 | `reasoning_effort`; High/Max modes | MIT, open weights |

GLM-5.2: preserved thinking blocks must match exactly when replayed.

## MiniMax

| Model | Context / max out | Pricing per 1M | Notes |
|---|---|---|---|
| MiniMax M3 | 1M (512K is a pricing-tier boundary, not a guarantee) / 524,288 (recommended 131,072) | ≤512K $0.30/$1.20; >512K $0.60/$2.40 | License `minimax-community` (custom, not MIT); `thinking.type` adaptive/disabled |
| MiniMax M3.1-Flash-Preview | — | — | Token Plan / MiniMax Code only; always thinks (`disabled`/`none` → 400); 5-level effort, default `max` |

## Mercury (Inception) and Xiaomi MiMo

| Model | Model ID | Context / max out | Pricing per 1M | Notes |
|---|---|---|---|---|
| Mercury 2.5 | `mercury-2.5` | 260K / 65,536 | List $0.20 / $0.02 cached / $0.75; promo $0.04 / $0.004 / $0.15 | `reasoning_effort` `instant` `low` `medium`(def) `high`; GA Sep 8 2026 (press release) or Sep 24 2026 (launch blog) — sources disagree (Verify) |
| Mercury 2 | `mercury-2` (sibling `mercury-edit-2`) | 128K / 50,000 | $0.25 / $0.025 / $0.75 | Same effort enum; closed, API-only |
| MiMo-V2.6-Pro | — | 1M | ~$0.43/$0.87 (Arena price column) | 1.02T/42B MoE; MIT open weights; Sep 21–22 2026; top open-weights model on Artificial Analysis |
| MiMo-V2.6-Flash | — | 1M | — | 309B/15B; MIT |

## Deprecated / retiring (other vendors)

| Group | Status |
|---|---|
| xAI | `grok-4-0709`, `grok-4-fast-*`, `grok-4-1-fast-*`, `grok-3` retired May 15 2026 → redirect to `grok-4.3` (billed at 4.3 rates). `grok-code-fast-1` → `grok-build-0.1` |
| Meta | Meta-hosted Llama API retired Jul 6 2026. Llama 3.x → Llama 4 (frozen) or Muse |
| Mistral | `magistral-medium/small-2509`, `devstral-2512`, `mistral-small-2506` retired Jul 31 2026; `mistral-medium-2505/2508` retired Aug 31 2026. Retired IDs return 404 |
| DeepSeek | `deepseek-chat` / `deepseek-reasoner` discontinued Jul 24 2026. `deepseek-v4-flash` aliased to V4.1-Flash Sep 10 2026. DeepSeek V3.x → `deepseek-flash` |
| Kimi / Qwen | `kimi-k2.5`, `moonshot-v1-*` retired Aug 31 2026 (404); `kimi-k2-*` retired May 25 2026. `qwen3.8-max-preview` superseded by GA `qwen3.8-max` |
