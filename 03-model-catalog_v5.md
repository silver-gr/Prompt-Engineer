# Model Catalog & Selection Guide (September 2026)

This is the **single source of truth** for all model specifications, capabilities, and selection guidance. Other modules reference this catalog but do not duplicate model data. Numbers below are verified against the September 2026 specs (skill `references/specs-current.md`, `specs-other.md`) and research docs; benchmark figures are vendor-reported unless stated.

---

## Frontier Landscape (September 2026)

| Provider | Model | Context | Output | Release | Key Strength |
|----------|-------|---------|--------|---------|--------------|
| Anthropic | Fable 5.1 | 1M | 128K | Sep 1 2026 | Highest capability, long-horizon autonomy |
| Anthropic | Opus 5.5 | 1M | 128K | Sep 22 2026 | Anthropic's default starting model; agentic coding |
| Anthropic | Sonnet 5.5 | 1M | 128K | Sep 28 2026 | Cost-efficient, literal instruction following |
| Anthropic | Haiku 4.5 | 200K | 64K | Oct 2025 | Speed + quality, sub-agents |
| OpenAI | GPT-6 Astra | 1.05M | 128K | Sep 3 2026 | OpenAI top tier; no `none` effort |
| OpenAI | GPT-6.1 Sol | 1.05M | 128K | Sep 29 2026 | Middle tier (recommended Sol); no `none` effort |
| OpenAI | GPT-6 Sol / Luna | 1.05M | 128K | Sep 22 2026 | Middle (superseded by 6.1 Sol, still live) / efficient tiers |
| OpenAI | GPT-5.6 Sol / Terra / Luna | 1.05M | 128K | Jul 9 2026 | Prior generation, still live; `max` effort tier |
| OpenAI | GPT-5.5 | 1.05M | 128K | Apr 24 2026 | Prior flagship |
| Google | Gemini 3.8 Flash | 1M | 64K | Sep 2 2026 | Top Gemini text model (GA) |
| Google | Gemini 3.7 / 3.6 Flash | 1M | 64K | Aug 13 / Jul 21 2026 | GA; same pricing as 3.8 |
| Google | Gemini 3.1 Pro | 1M | 64K | Feb 19 2026 | Preview; deep reasoning |
| xAI | Grok 4.7 | 500K | — | Sep 21 2026 | Always-on reasoning, tiered pricing |
| DeepSeek | V4.1-Flash | 1M | 384K | Sep 10 2026 | MIT, lowest cost per task |
| Xiaomi | MiMo-V2.6-Pro | 1M | — | Sep 21-22 2026 | Top open-weights model (MIT) |
| Zhipu | GLM-5.3 / 5.3-Flash | 1M | 128K | Aug 18 / Aug 26 2026 | Forced thinking; Flash is MIT |
| Alibaba | Qwen 3.8-Max | 1M | 131K | GA Aug 3 2026 | Multimodal (text/image/video), multilingual |
| Moonshot | Kimi K3 | 1M | 131K default | Jul 2026 | Open weights, always-on thinking, 2.8T MoE |
| MiniMax | M3 | 1M | 524K | 2026 | Budget frontier coding + multimodal |
| Meta | Muse Spark 1.3 | 1M | — | Sep 2 2026 | Closed API; Meta's current line |
| Mistral | Medium 3.5 | 256K | — | Apr 28 2026 | EU compliance, open weights |
| Inception | Mercury 2.5 | 260K | 65K | Sep 2026 | Diffusion LLM, lowest latency |

---

## 1. Anthropic (Claude 5.x Family)

> **Tier order:** Fable 5.1 / Mythos 5.1 (top) > Opus 5.5 > Sonnet 5.5 > Haiku 4.5
> Start with: **Opus 5.5 at `medium`** (Anthropic's stated starting model) · **Fable 5.1** when Opus 5.5 falls short · **Sonnet 5.5** for cost
> Legacy but still available: Fable 5, Mythos 5, Opus 5, Sonnet 5, Opus 4.8 (see Legacy subsection)

### Claude Fable 5.1

**Released**: September 1, 2026 | **Model ID**: `claude-fable-5-1` | Retires no sooner than Sep 1 2027

- **Context Window**: 1M tokens | **Max Output**: 128K tokens | **Knowledge cutoff**: Jun 2026
- **Pricing**: $10 / $50 per 1M tokens ($5/$25 batch; cache read $0.25)
- **Key Feature**: Long-horizon autonomy -- sustained multiday, goal-directed runs with strong instruction retention
- **Thinking**: **Always-on** (`disabled` → 400)
- **Effort**: `low` | `medium` | `high` (default) | `xhigh` | `max`. Fable 5.1 `medium` ≈ Fable 5 at lower cost
- Data retention: 30-day, no ZDR unless authorized ("Covered Model")

**Prompting Quick-Reference**:
- One brief instruction beats enumeration -- Fable 5 prompts carry over; over-prescriptive prompts DEGRADE it
- Give the reason, not only the request
- Ground progress claims: "audit each claim against a tool result from this session"
- Provide a memory file (one lesson/file, dedupe, delete wrong notes) -- notable performance boost
- `send_to_user` tool for long async runs; `display:"updates"` + an explicit progress-update line
- Add a per-turn batching nudge (turn-scoped system message) if it makes serial one-call-per-turn tool calls in loops
- Use subagents freely, with explicit guidance on when

**Watch For**:
- **Never instruct to echo/transcribe reasoning** → `reasoning_extraction` refusal
- Pre-output refusals are billed from Sep 24 2026; `reasoning_extraction` refusals are never retried by fallbacks
- Server-side fallback targets: Opus 4.8, Opus 5 (`fallbacks:"default"`)
- `stop_reason: "refusal"` is HTTP 200 success, not an error -- handle in harness
- Serial tool calls in loops; less search at `low`; drafts long deliverables twice at `xhigh`/`max`; may reproduce source text without quotation marks
- Rare early-stopping deep in sessions; can take unrequested actions (email drafts, git backups) → define explicit boundaries

### Claude Mythos 5.1

**Model ID**: `claude-mythos-5-1` | Glasswing participants only

Same model as Fable 5.1, but **no prefix-binding check**. Use when Fable 5.1 refuses legitimate work.

### Claude Opus 5.5

**Released**: September 22, 2026 | **Model ID**: `claude-opus-5-5` | Retires no sooner than Sep 22 2027

- **Context Window**: 1M tokens | **Max Output**: 128K tokens (batch 300K with header `output-300k-2026-03-24`) | **Knowledge cutoff**: Jun 2026
- **Pricing**: $4 / $20 per 1M tokens (fast mode $8/$40 via `speed:"fast"`; batch $2/$10; cache read $0.20)
- **Thinking**: **Always-on**; `disabled` → 400 at every effort
- **Effort**: `low` | `medium` (default) | `high` | `xhigh` | `max`. Opus 5.5 `medium` ≥ Opus 5 `high`; `low` is close to Opus 5 `high` on several coding evals
- Thinks more per turn than Opus 5 at the same level

**Prompting Quick-Reference**:
- Shortest outcome + scope prompt; Opus 5 prompts carry over
- Set effort explicitly; add an "explore broadly" line for multi-app agents and an elapsed/time-budget line for multi-agent teams
- Name the frontend patterns to avoid rather than "avoid a generic AI look"
- Wrap pasted content in an ID-tagged wrapper (see `09-safety-guardrails_v5.md`)
- Unattended runs: official standing instruction at the end of the system prompt from the first request

**Watch For**:
- Text-only `end_turn` progress reports stop unattended loops; progress notes arrive as empty thinking blocks
- Remove "think carefully" / "write out your reasoning" lines and "don't think" rules carried from thinking-off Opus 5
- Safety classifiers: cyber, bio, reasoning_extraction; cyber tasks re-route to Opus 4.8
- `computer_20251124` rejected on the Claude API and Google Cloud (Bedrock still accepts) → use `computer_toolset_20260801`

### Claude Sonnet 5.5

**Released**: September 28, 2026 | **Model ID**: `claude-sonnet-5-5` | Retires no sooner than Sep 28 2027

- **Context Window**: 1M tokens | **Max Output**: 128K tokens (batch 300K, same header) | **Knowledge cutoff**: Jun 2026
- **Pricing**: $2 / $10 per 1M tokens (batch $1/$5; cache read $0.20)
- **Thinking**: On; `disabled` → 400. Lowest setting is `between_tools` (≤`high` effort only; not combinable with per-message effort)
- **Effort**: `low` | `medium` | `high` (default) | `xhigh` | `max`. Levels were recalibrated; no published mapping to Sonnet 5

**Prompting Quick-Reference**:
- Literal instruction following -- state scope explicitly
- Add the "keep working until done / stop when done and checked; no unrequested features, tests, files, docs" pair
- Add a real-check verification paragraph at low effort; at `xhigh`/`max` add "no extra review rounds or reviewer sub-agents unless asked"
- Remove "minimize tool calls" / "only use tools when strictly necessary" and per-step countdowns

**Watch For**:
- Unrequested tests/docs; builds when asked for ideas; tool-name case drift
- Mid-turn user text misread as injection
- "Don't think" rules under `between_tools` leak internal XML tags
- Safety classifiers: cyber, bio, frontier_llm, reasoning_extraction, general_harms; fallback to Sonnet 5 (cyber, frontier_llm only)

### Claude Haiku 4.5

**Released**: October 2025 | **Model ID**: `claude-haiku-4-5-20251001` (alias `claude-haiku-4-5`) | Retires no sooner than Oct 15 2026

- **Context Window**: 200K tokens | **Max Output**: 64K tokens | **Pricing**: $1 / $5 (batch $0.50/$2.50; cache read $0.10) | **Knowledge cutoff**: Feb 2025
- Manual extended thinking (`budget_tokens`, required); off by default; no effort parameter. Old tokenizer. Min cacheable prompt 4,096 tokens.
- Haiku 5.5 is announced with no specs.

**Best For**: Sub-agents, high-volume tasks, cost-sensitive deployments, routing. Exception to every 5.x rule: keeps prefill, manual budgets, sampling params.

### Claude 5.x Family Comparison (Current)

| Feature | Fable 5.1 | Opus 5.5 | Sonnet 5.5 | Haiku 4.5 |
|---------|-----------|----------|------------|-----------|
| Context | 1M | 1M | 1M | 200K |
| Max Output | 128K | 128K | 128K | 64K |
| Thinking default | Always-on | Always-on | On (`between_tools` lowest) | Manual budget, off |
| Default effort | `high` | `medium` | `high` | N/A |
| Sampling params | → 400 | → 400 | → 400 | Accepted |
| Prefill | → 400 | → 400 | → 400 | Accepted |
| `budget_tokens` | → 400 | → 400 | → 400 | Required |
| Forced `tool_choice` (`any`/`tool`) | → 400 | → 400 | → 400 | Accepted |
| Thinking bound to conversation prefix | Yes | Yes | Yes | No |
| Mid-conversation system messages | Yes | Yes | Yes | -- |
| Tokenizer | New | New | New | Old |
| Fast mode | No | Yes | No | No |
| Min cacheable prompt | 512 | 512 | 512 | 4,096 |
| Price in/out | $10/$50 | $4/$20 | $2/$10 | $1/$5 |

### Claude Legacy (Still Available)

All 1M context / 128K output. Guidance for these models stays valid; prefer the current tier for new work.

| Model | Model ID | Price in/out | Thinking default | Notes |
|-------|----------|--------------|------------------|-------|
| Fable 5 | `claude-fable-5` | $10/$50 (batch $5/$25; cache read $1) | Always-on; `disabled` → 400 | Released Jun 9 2026; retires ≥ Jun 9 2027; forced `tool_choice` accepted; per-message effort → 400 |
| Mythos 5 | `claude-mythos-5` | same as Fable 5 | same | Glasswing only; retires ≥ Jun 9 2027 |
| Opus 5 | `claude-opus-5` | $5/$25 (fast $10/$50) | On; `disabled` only at effort ≤`high` | Released Jul 24 2026; retires ≥ Jul 24 2027; classifier: cyber |
| Sonnet 5 | `claude-sonnet-5` | **$2/$10 -- permanent since Aug 10 2026** (the $3/$15 increase was cancelled); cache read $0.20 | On; `type:"disabled"` accepted | Released Jun 30 2026; min cacheable 1,024; no mid-conversation system messages |
| Opus 4.8 | `claude-opus-4-8` | $5/$25 (fast $10/$50) | Off unless `type:"adaptive"` | Released May 28 2026; retires ≥ May 28 2027; fallback target for Fable 5.1 and cyber re-route for Opus 5.5 |

**Opus 5 prompting** (AP-16 scope): self-verifies -- remove verification instructions; ask explicitly for conciseness; constrain scope; cap subagent delegation ("Do not use subagents to verify your own work"); limit correction narration. With thinking off: tool-call-as-text leakage and internal XML tags. Anthropic cut >80% of Claude Code's system prompt for Opus 5 with no eval loss.
**Sonnet 5 prompting**: literal -- state scope ("Apply to every section, not just the first"); nudge tool use when thinking is off; remove "summarize every N calls"; follows "only report high-severity" literally. Sonnet 5 `medium` ≈ Sonnet 4.6 `high`. New tokenizer (~30% more tokens vs 4.6). Computer use `computer_20251124`.
**Opus 4.8 prompting**: set adaptive thinking explicitly; handles many parallel subagents; prompt-cache minimum 1,024 tokens.

### API-Surface Facts (Claude 5.x)

- **Effort enum** on every 5.x model and Opus 4.8: `low` `medium` `high` `xhigh` `max`; setting the default equals omitting it. **Effort does not transfer across models** -- documented pairs only (above); Opus 5.5 thinks more per turn than Opus 5 at the same level.
- **Prefix binding**: editing `system`, `tools` or an earlier turn invalidates later thinking blocks → 400 `The block is bound to a different conversation` for accounts created on/after Aug 31 2026 00:00 UTC (older accounts log only). Keep history append-only. Thinking blocks are model-bound: Fable 5.1 reads Opus 5.5 blocks, not the reverse; unreadable blocks drop silently (`thinking.block_binding.prefix_mismatch_behavior:"drop_block"`).
- **Parameters**: `output_config: {effort}`; `thinking: {type:"adaptive"|"disabled"|"enabled"|"between_tools", display:"omitted"|"summarized"|"updates", budget_tokens}`; `fallbacks:"default"` (or up to 3 models); `speed:"fast"`; per-message effort (beta) on Fable 5.1, Opus 5.5, Sonnet 5.5.
- **Beta headers**: `thinking-display-updates-2026-08-18`, `thinking-binding-controls-2026-08-01`, `mid-conversation-system-clear-at-2026-08-21`, `mid-conversation-output-config-2026-07-01`, `server-side-fallback-2026-07-01`, `inline-tools-2026-09-15`, `compact-2026-09-04`, `fast-mode-2026-02-01`.
- **Fallbacks & refusals**: Fable 5.1 → Opus 4.8, Opus 5; Sonnet 5.5 → Sonnet 5 (cyber, frontier_llm only); Opus 5.5 cyber → Opus 4.8. Pre-output refusals in bio, frontier_llm and reasoning_extraction are billed from Sep 24 2026. Fable 5 was suspended Jun 12-Jul 1 2026 -- keep fallbacks wired.

### Key Claude Insight (September 2026)

**Prompting current Claude is a subtraction exercise.** The 5.x family requires:
- **Remove verification/self-check instructions on Opus 5** -- it self-verifies natively; Fable 5/5.1 are the opposite (Anthropic recommends periodic self-checks on long runs)
- **Brief instructions beat enumeration** -- Fable follows one brief instruction better than itemized lists
- **Effort is the primary cost lever** -- and does not transfer across models; re-sweep per model
- **No sampling params, no prefill, no manual budgets, no forced `tool_choice`** on Fable 5.1 / Opus 5.5 / Sonnet 5.5 (except Haiku 4.5 for the first three)
- **Thinking on by default** on the current 5.x models (always-on for Fable, Opus 5.5); Haiku 4.5 and Opus 4.8 are off by default -- budget `max_tokens` for thinking+text
- **New tokenizer** on all except Haiku 4.5 -- recount tokens when migrating from 4.6-era
- **Memory file + send-to-user tool** for long async agents
- **Cost patterns**: Opus 5.5 executor + Fable 5.1 advisor (+1.7 pts at ~2.1x cost -- test on your workload), or Fable 5.1 orchestrating Sonnet 5.5

---

## 2. OpenAI (GPT-6 and GPT-5.x)

> **GPT-6 tier order: Astra > Sol > Luna.** In GPT-5.6, Sol was the flagship (~unsuffixed), Terra ~ mini, Luna ~ nano. **"Sol" names a different tier per generation** -- GPT-6 Sol/Luna are not GPT-5.6 Sol/Luna (different IDs, prices, cutoffs, parameter rules). Terra has no GPT-6 successor; Astra is not a renamed Terra.
>
> **GPT-6.1 Sol** (Sep 29 2026) is OpenAI's recommended Sol: the featured trio is `gpt-6-astra` / `gpt-6.1-sol` / `gpt-6-luna`. There is no GPT-6.1 Astra (not released, on safety grounds) and no GPT-6.1 Luna. `gpt-6-sol` stays live with no deprecation notice.

### GPT-6 Astra / 6.1 Sol / Sol / Luna

| Variant | Model ID | Released | Knowledge cutoff | $ in / cached / out per 1M (cache write) | Effort enum (default) |
|---------|----------|----------|------------------|-------------------------------------------|-----------------------|
| **Astra** | `gpt-6-astra` | Sep 3 2026 | Apr 30 2026 | $10 / $1.00 / $50 ($12.50) | `low` `medium` `high` `xhigh` `max`; **`none` → 400**; default not documented |
| **6.1 Sol** | `gpt-6.1-sol` | Sep 29 2026 | Apr 30 2026 | $2 / $0.10 / $10 ($2.50) | `low` `medium` `high` `xhigh` `max` (`medium`); no `none` or `minimal` (error code not documented) |
| **Sol** | `gpt-6-sol` | Sep 22 2026 | Apr 20 2026 | $2 / $0.20 / $10 ($2.50) | `none`…`max` (`medium`) |
| **Luna** | `gpt-6-luna` | Sep 22 2026 | May 18 2026 | $0.10 / $0.01 / $0.50 ($0.125) | `none`…`max` (`medium`) |

- **Context Window**: 1,050,000 tokens | **Max Output**: 128,000 tokens (all four)
- `reasoning.mode: "standard"|"pro"` (Responses only; replaces separate Pro slugs on 5.6+; no `gpt-6-*-pro` IDs). `reasoning.context`: `auto` (= `all_turns`, default on 5.6+) | `all_turns` | `current_turn` (GPT-6.1 Sol supports `all_turns`; its default is not documented)
- `text.verbosity` = `low`/`medium`/`high` (documented on Astra; Sol/Luna support (Verify))
- Function calling: Astra and 6.1 Sol require the Responses API (Chat Completions works without tools); Sol/Luna on Chat Completions only with `reasoning_effort:"none"`
- GPT-6.1 Sol: cached input bills at 0.05x input (most other GPT-5.6+ models: 0.1x); in ChatGPT it is in Work and Codex only, not Chat; multi-agent beta (`OpenAI-Beta: responses_multi_agent=v1`) is listed for 6.1 Sol and GPT-5.6
- GPT-6 adds `configuration_update` (mid-conversation effort change), async tool calling, mid-turn steering
- Sep 25 2026 fix for an image-encoding bug in Sol/Luna: re-run image evals from before Sep 25

**Astra behavior and remedies** (no separate 6.1 Sol, Sol or Luna guide; evaluate there):
- Initiative: asks non-blocking questions, stops early → "persist until the goal is complete", define completion
- Sensitive to skills/AGENTS.md → audit them; state that user instructions take precedence
- Heavy Markdown, recurring phrases → specify style
- Under-delegates → say when and how much to delegate
- Over-tests → calibrate testing down
- Remove `temperature`, `top_p`, `logprobs` when effort is not `none` (error vs ignored: Verify)

### GPT-5.6 Sol / Terra / Luna (Prior Generation, Still Live)

**Released**: July 9, 2026 | No deprecation notice | Knowledge cutoff Feb 16 2026

| Variant | Model ID | $ in / cached / out per 1M (cache write) |
|---------|----------|-------------------------------------------|
| **Sol** | `gpt-5.6-sol` (alias `gpt-5.6`) | $4 / $0.40 / $20 ($5) -- promo from Aug 21 2026, "at least through Nov 21 2026" |
| **Terra** | `gpt-5.6-terra` | $2 / $0.20 / $12 ($2.50) |
| **Luna** | `gpt-5.6-luna` | $0.20 / $0.02 / $1.20 ($0.25) |

- **Context Window**: 1,050,000 tokens | **Max Output**: 128,000 tokens
- **Reasoning**: `none`/`low`/`medium` (default)/`high`/`xhigh`/`max` -- `max` exists on 5.6+ only
- Multi-agent orchestration in beta (Responses API only)

**Prompting Quick-Reference** (official guidance):
- **Lean prompts win**: OpenAI reports 10-15% eval score gains with 41-66% fewer tokens (directional)
- **State each instruction once** -- repetition degrades performance
- **Don't over-repeat caution phrases** ("ask first", "wait for approval")
- Concise by default -- blunt "be concise" can over-truncate; use `text.verbosity` and say what a short answer must keep

### Billing (GPT-6 and 5.6)

- >272K input tokens bills 2x input **and cache** rates and 1.5x output for the **entire request**
- Cache writes 1.25x input on 5.6+ (GPT-5.5: no write charge); reads 0.1x. Batch/Flex 50%
- Priority renamed **Fast mode** Jul 30 2026 (`service_tier:"fast"` or `"priority"`, 2x price)
- Caching: `prompt_cache_options.ttl:"30m"` (+ `mode:"explicit"`, `prompt_cache_breakpoint`) on 5.6+; `prompt_cache_retention` only ≤5.5

### GPT-5.5 and 5.5 Pro

- **GPT-5.5**: `gpt-5.5` (snapshot `gpt-5.5-2026-04-23`) | Released Apr 24 2026 | cutoff Dec 1 2025 | 1,050,000 ctx / 128,000 out | $5 / $0.50 / $30 (no cache-write charge)
- **Reasoning**: `none`/`low`/`medium` (default)/`high`/`xhigh` | **Verbosity**: `text.verbosity`
- Leaves ChatGPT, Work and Codex Oct 14 2026 (API unaffected)
- **GPT-5.5 Pro**: `gpt-5.5-pro` | $30 / -- / $180 | effort `medium`/`high` (default)/`xhigh` | Responses and Batch only

### GPT-5.3-Codex

`gpt-5.3-codex` | Released Feb 24 2026 | 400,000 ctx / 128,000 out | $1.75 / $0.175 / $14 | effort `low`…`xhigh` | The only Codex-branded API model still live. Older Codex slugs retired (see §10).

### chat-latest

`chat-latest` | rolling alias = ChatGPT Instant | 400,000 ctx (page as stated) / 128,000 out | $5 / $0.50 / $30 | **Not for production** (the target changes).

### GPT-5.2 / 5.1 / 5 (Legacy)

| Model | ID | Released | Price in / cached / out | Context |
|-------|----|----------|-------------------------|---------|
| GPT-5.2 | `gpt-5.2` | Dec 2025 | $1.75 / $0.175 / $14 | 400K |
| GPT-5.1 | `gpt-5.1` | Nov 13 2025 | $1.25 / $0.125 / $10 | 400K |
| GPT-5 | `gpt-5` | Aug 2025 | $1.25 / $0.125 / $10 | 400K |

Effort enums for these were not re-verified in September 2026. GPT-5.1 introduced `none` reasoning; `minimal` still exists on some older models (migrate to `low`). `gpt-5-2025-08-07` shuts down Dec 11 2026 → `gpt-5.6-*`. The `reasoning_profile: light|balanced|deep` parameter **does not exist** -- it appeared in earlier editions of this catalog and was retracted; never emit it (see `08-gpt5-practices_v5.md`).

### Key GPT Insight

Less is more. State the outcome once; effort is a per-model enum that does not transfer (Astra `none` → 400). Agentic persistence reminders matter at low effort and on Astra. Avoid over-specification -- outcome-first prompts win on both score and cost. Never emit `reasoning_profile`.

---

## 3. Google (Gemini 3.x Family)

All current rows: 1M context in / 65,536 out. Interactions API is GA (Jun 2026) and recommended; `generateContent` is legacy but supported.

| Model | Model ID | Thinking levels (default) | $ in/out per 1M | Released | Status |
|-------|----------|---------------------------|-----------------|----------|--------|
| **Gemini 3.8 Flash** | `gemini-3.8-flash` | `low` `medium` `high` (`medium`); `minimal` → error | $0.75/$3.75 intro to Dec 31 2026, then $1.50/$7.50 | Sep 2 2026 | GA -- top text model |
| Gemini 3.7 Flash | `gemini-3.7-flash` | same as 3.8 | same as 3.8 | Aug 13 2026 | GA |
| Gemini 3.6 Flash | `gemini-3.6-flash` | `minimal` `low` `medium` `high` (`medium`) | same as 3.8 | Jul 21 2026 | GA |
| Gemini 3.5 Flash | `gemini-3.5-flash` | `minimal`…`high` (`medium`) | $1.50/$9.00 | May 19 2026 | GA (legacy Flash) |
| Gemini 3.5 Flash-Lite | `gemini-3.5-flash-lite` | `minimal`…`high` (`minimal`) | $0.30/$2.50 | Jul 21 2026 | GA |
| Gemini 3.1 Flash-Lite | `gemini-3.1-flash-lite` | `minimal`…`high` (`minimal`) | $0.25/$1.50 | GA May 7 2026 | Shuts down May 7 2027 |
| Gemini 3.1 Pro | `gemini-3.1-pro-preview` | `low` `medium` `high` (`high`) | $2/$12; >200K $4/$18 | Feb 19 2026 | Preview |
| Gemini 3 Flash | `gemini-3-flash-preview` | `minimal`…`high` (`high`) | $0.50/$3.00 | Dec 17 2025 | Preview |

**Status**: Gemini 3.5 Pro is unreleased ("coming soon"); Gemini 4 is in training with no release. Knowledge cutoff Jan 2025 for 3.5 Flash and 3 Flash; not published for 3.6-3.8. Whether `gemini-flash-latest` has pointed to a new target since May 19: (Verify).

### API-Surface Block

- **Sampling**: OMIT `temperature`, `top_p`, `top_k` entirely. **Deprecated Jul 21 2026**: ignored on 3.6+ and 3.5 Flash-Lite; 400 on "future model generations"; still honored (looping risk when lowered) on 3.5 Flash, 3.1 Pro, 3 Flash. Default 1.0 is recommended.
- Prefilled model turn → 400 on 3.6+. `candidate_count` / `frequency_penalty` / `presence_penalty` → error on 3.8.
- `thinking_budget` + `thinking_level` together → 400; `thinking_budget` alone kept for backward compatibility (acceptance on 3.7/3.8: Verify). `minimal` is unavailable on 3.7/3.8 Flash and 3.1 Pro.

### Gemini 3.8 Flash

- **Key Feature**: Top Gemini text model; spends more tokens by design (smaller steps, iterative tools, self-verification) -- use `low` for everyday tasks or stay on 3.7 Flash
- Intro pricing expires Dec 31 2026 (price doubles) -- budget for the post-intro rate

### Gemini 3.1 Pro (Preview)

**Released**: February 19, 2026 | Model ID `gemini-3.1-pro-preview`

- **Thinking**: `thinking_level`: `low` | `medium` | `high` (default)
- Deep reasoning with massive context; still Preview

### Gemini 3.5 Flash-Lite / 3.1 Flash-Lite

Latency-optimized, near-Flash quality at a fraction of the cost; default `thinking_level` `minimal`. 3.1 Flash-Lite shuts down May 7 2027.

**Prompting Quick-Reference** (all Gemini 3.x):
- **OMIT `temperature`/`top_p`/`top_k`** -- lowering causes loops/degraded performance on older 3.x
- Favor DIRECTNESS over persuasion (treats prompts as executable instructions)
- NO conversational fluff ("please", "kindly", "if you could")
- Persona, behavioral constraints and output-format rules at the TOP (system instruction); context next; the specific question LAST; an optional recap of limits at the end
- Use `thinking_level` `low` for latency ("Think silently"); `medium` for most tasks; `high` for deep reasoning
- Always include a few few-shot examples with identical formatting (Google recommendation)
- Anchor transitions: "Based on the above..."; explicit labels for multimodal inputs

**Watch For**:
- Conversational language actively degrades instruction-following
- Constraints stranded at the end of a long context compete with the data for attention
- Personas are taken very seriously -- may override other instructions
- Gemini 3.x is terse by default -- request detail explicitly

### Gemini 2.x and 3.x Legacy

Gemini 2.5: new users blocked since Sep 18 2026 (existing keep access; "not deprecated"). Gemini 2.0 Flash / Flash-Lite shut down Jun 1 2026. See §10.

### Key Gemini Insight

Gemini 3.x treats prompts as executable instructions, not conversation. DO NOT use 2.x-era prompt engineering. Use `thinking_level` for reasoning control; leave sampling keys out. Be direct, never persuasive.

---

## 4. xAI (Grok Family)

Docs are now branded "SpaceXAI"; the API is still `api.x.ai`. Closed, API-only.

| Model | Model ID | Context | $ in / cached / out per 1M (<200K · ≥200K) | Reasoning | Released |
|-------|----------|---------|---------------------------------------------|-----------|----------|
| **Grok 4.7** (flagship) | `grok-4.7` | 500K | $2.00 / $0.50 / $6.00 · $4.00 / $1.00 / $12.00 | `reasoning_effort` `low` `medium` `high` (default) `xhigh`; **cannot be disabled** | Sep 21 2026 (cutoff May 2026) |
| Grok 4.6 | `grok-4.6` | 500K | same as 4.7 | same as 4.7 | Aug 12 2026 |
| Grok 4.5 | `grok-4.5` (aliases `grok-4.5-latest`, `grok-build-latest`) | 500K | $2.00 / $0.30 / $6.00 · $4.00 / $0.60 / $12.00 | `low` `medium` `high` (default); `xhigh` silently treated as `high`; cannot be disabled | API Jul 8 2026 |
| Grok 4.3 | `grok-4.3` | 1M | $1.25 / $0.20 / $2.50 · $2.50 / $0.40 / $5.00 | Default `low`; `none` supported; effort enum: xAI pages conflict (Verify) | Redirect target for retired Grok 4 / 4.1-fast / 3 |

**Watch For**:
- **Crossing 200K reprices the entire request**, not just the overage -- budget accordingly
- `presence_penalty`, `frequency_penalty`, and `stop` are **rejected as errors**; `logprobs` silently ignored on grok-4.20+
- Grok 4.5-4.7 reasoning cannot be turned off; Grok 4.3 can (`none`)
- Replay `reasoning.encrypted_content` unchanged; set `prompt_cache_key` / `x-grok-conv-id` for reliable cache hits; US regional endpoint +10%
- No official xAI text prompting guide

**Prompting Quick-Reference**:
- Structure large contexts with hierarchical headings
- Clear, direct tool instructions
- Request verification steps for quantitative reasoning

---

## 5. Chinese Frontier Models

### DeepSeek V4.1-Flash / V4-Pro

| Model | Model ID | Context / max out | $ in/out per 1M (peak · off-peak) | Notes |
|-------|----------|-------------------|-------------------------------------|-------|
| V4.1-Flash | `deepseek-flash` (`deepseek-v4-flash` is now an alias) | 1M / 384K | $0.30/$1.20 · $0.15/$0.60 | MIT; native image input; Sep 10 2026 |
| V4-Pro | `deepseek-v4-pro` | 1M / 384K | $1.32/$3.96 · $0.66/$1.98 | MIT open weights |

- **License**: MIT (open weights) | **Key Feature**: Frontier-level reasoning at lowest cost tier
- **Reasoning**: effort `low` `high` `max` (default `high`); `medium`/`xhigh` silently coerced to `high`. Responses API `reasoning.effort:"none"` disables thinking
- **Peak hours** 01-04 and 06-10 UTC Mon-Fri since Aug 16 2026; off-peak = half price

**Prompting**: Clear, structured prompts. Enable thinking via `extra_body={"thinking":{"type":"enabled"}}` -- NOT raw `<think>` tags. **Gotcha**: any request carrying `tools` must include `reasoning_content` from all prior turns or the API returns 400. Thinking mode ignores temperature and penalties; `top_p` is honored but clamped 0.95-1.0.

### GLM-5.3 / GLM-5.3-Flash / GLM-5.2 (Zhipu / Z.ai)

| Model | Model ID | Context / max out | Pricing per 1M | License / released |
|-------|----------|-------------------|----------------|--------------------|
| GLM-5.3 | `glm-5.3` | 1M / 128K | $1.40 / $0.26 cached / $4.40 | Custom GLM-5.3 License; Aug 18 2026 |
| GLM-5.3-Flash | `glm-5.3-flash` | 1M / 128K | $0.15 / $0.03 / $0.50 | 320B/18B MoE, multimodal; MIT; Aug 26 2026 |
| GLM-5.2 | -- | 1M / 128K | $1.40/$4.40 | MIT, open weights |

- **Reasoning**: GLM-5.3 has forced thinking (`thinking.type:"disabled"` → error); effort `low` `high` `max` (default `max`). GLM-5.2: `reasoning_effort`, High/Max modes

**Prompting**: Provide bilingual glossaries for multilingual output. Define explicit function-calling payloads. **Gotcha**: preserved thinking blocks must match exactly when replayed.

### Qwen 3.8-Max / 3.7 (Alibaba)

| Model | Model ID | Context / max out | Pricing per 1M |
|-------|----------|-------------------|----------------|
| **Qwen 3.8-Max** | `qwen3.8-max` (snapshot `qwen3.8-max-0902`) | 1M / 131,072 | $2/$6 (Alibaba Singapore list) |
| Qwen 3.8-Flash | `qwen3.8-flash` | 1M / 131,072 | $0.15/$0.47 |
| Qwen 3.7-Max | `qwen3.7-max` (snapshot `qwen3.7-max-2026-06-08` adds vision) | 1M / 131,072 | $2.50/$7.50 (official list) |

- **Qwen 3.8-Max**: GA Aug 3 2026; text + image + video (multimodal); `enable_thinking` default on; `preserve_thinking`; effort `low` `medium` `xhigh` (default `xhigh`, **no `high`**); effort + `thinking_budget` together → error. Supersedes `qwen3.8-max-preview`.
- **Open weights**: Qwen3.8-2.4T-A95B (custom license; text-only, thinking-only); Qwen3.8-27B (Apache 2.0)
- **Qwen 3.7-Max**: closed/API; `enable_thinking` toggle; text-only unless you use the June snapshot (adds vision). Prefer 3.8-Max for multimodal.
- **Key Feature**: Broadest multilingual coverage

> **Do not read "256K" as the Qwen 3.7 ceiling.** Alibaba's sizing-guidance prose says *"for standard tasks, 128k-256k tokens is typically sufficient"* -- advice about task sizing, not a spec. The max context is 1M.

**Prompting**: Direct, clear instructions with structured context. Always name the target output language explicitly.

### Kimi K3 / K2.7-Code / K2.6 (Moonshot AI)

| Model | Model ID | Context / max out | Pricing per 1M | Reasoning |
|-------|----------|-------------------|----------------|-----------|
| **Kimi K3** | `kimi-k3` | 1,048,576 / 131,072 default, 1,048,576 max | $3.00 miss / $0.30 hit / $15.00 out; cache write $3.00 (5-min) / $6.00 (1-h) | Always-on; `reasoning_effort` `low` `high` `max` (default `max`) |
| Kimi K2.7-Code | `kimi-k2.7-code` | 262,144 | $0.95 / $0.19 / $4.00 (highspeed $1.90 / $0.38 / $8.00) | Thinking forced on |
| Kimi K2.6 | -- | 262,144 | $0.95 / $0.16 cached / $4.00 | Thinking + non-thinking modes |

- **K3**: open weights under the custom Kimi K3 License (weights on HF Jul 26-27 2026); MoE 2.8T total / 104B activated, 93 layers (69 KDA + 24 Gated MLA attention), 896 experts, MoonViT-V2 vision encoder, MXFP4/MXFP8 quantization-aware training. Key feature: long-horizon coding, end-to-end knowledge work, native vision.
- **Sampling is fixed server-side on K3, K2.7 and K2.6 -- sending temperature, top_p, n or penalties errors.**
- **Watch For**: K3 preserved-thinking-history mode requires replaying full assistant messages (including `reasoning_content` and `tool_calls`) **verbatim**.
- **K2.6 Agent Swarm v2**: 300 sub-agents, 4,000 steps, ~13-hour runs (carried over, not re-verified -- Verify).

**Prompting**: Designed for extended coding sessions and multi-step knowledge tasks; native vision. Models do not access external resources by default -- wire tools explicitly.

### MiniMax M3

- **Context Window**: 1M (512K is a pricing-tier boundary, not a guarantee) | **Max Output**: 524,288 (recommended 131,072)
- **Pricing**: ≤512K $0.30/$1.20; >512K $0.60/$2.40 per 1M
- **License**: `minimax-community` (custom, not MIT); `thinking.type` adaptive/disabled
- **Key Feature**: Budget frontier coding + native multimodal
- **M3.1-Flash-Preview**: Token Plan / MiniMax Code only; always thinks (`disabled`/`none` → 400); 5-level effort, default `max`

**Prompting**: Plan against the real context ceiling, not the tier boundary. Standard structured prompting.

---

## 6. Open-Source / Open-Weight Models

### Muse (Meta -- Current Line)

Meta's current line is Muse: Spark = closed API, Glimmer = open weights. Llama is frozen at Llama 4.

| Model | Model ID | Context | Pricing per 1M | Reasoning | License / released |
|-------|----------|---------|----------------|-----------|--------------------|
| Muse Spark 1.3 | `muse-spark-1.3` | 1,048,576 | Standard $1.25 in / $0.15 cached / $4.25 out; Contributor tier (`-contributor`, trains on your data) $0.10 / $0.002 / $0.20; no long-context premium | `reasoning_effort` `minimal`…`xhigh` + `max`; `none` → 400 | Closed, API-only; Sep 2 2026 |
| **Muse Glimmer** | -- | 128K default (text+image in) | -- | `reasoning_strength` `low` `medium` `high` (default) `xhigh` | 30B dense; **Apache 2.0** open weights; Aug 10 2026 |

**Prompting**: Spark: `developer` role outranks `user`; keep temperature 1.0 (Meta injects a hidden steering prompt); `stop`, `n>1`, `logprobs`, `top_p:0`, `reasoning_effort:"none"` → 400. Glimmer: native reasoning, needs `apply_chat_template`, no parallel tool calls.

### Llama 4 (Meta -- Frozen)

Open weights only. Meta-hosted Llama API retired Jul 6 2026; third-party hosts are retiring Llama 4.

- **Maverick**: 1M context | MoE | Released Apr 5 2025 | Customizable, self-hosted
- **Scout**: 10M context | max out 32K | Released Apr 5 2025 | MoE, smaller expert count than Maverick; no first-party API -- self-host only

**Prompting**: Standard direct instruction patterns; benefits from structured context like Claude/GPT approaches. Explicit CoT and few-shot remain valid here (no documented native reasoning control).

### Mistral

| Model | Model ID | Context | $ in/out per 1M | Notes | Released |
|-------|----------|---------|-----------------|-------|----------|
| **Mistral Medium 3.5** | `mistral-medium-3-5` | 256K | $1.50/$7.50 | Current flagship; `reasoning_effort` (`high` / `none` documented); Modified MIT open weights | Apr 28 2026 |
| Mistral Small 4 | `mistral-small-2603` | 256K | $0.15/$0.60 | `reasoning_effort`; Apache 2.0 | Mar 16 2026 |
| Mistral Large 3 | `mistral-large-2512` | 256K | $0.50/$1.50 | Apache 2.0; max out 32K (carried, not re-verified) | Dec 2 2025 |

**Prompting**: Lead with explicit function schemas; use structured outputs for format enforcement; avoid asking the model to count words/characters. Response content becomes a chunk list when thinking is on. Pin major-minor IDs -- `-latest` aliases switch silently.

### Xiaomi MiMo

- **MiMo-V2.6-Pro**: 1M context | 1.02T/42B MoE | MIT open weights | Sep 21-22 2026 | top open-weights model on Artificial Analysis | ~$0.43/$0.87 (Arena price column)
- **MiMo-V2.6-Flash**: 1M context | 309B/15B | MIT

---

## 7. Specialized Architectures (Diffusion LLMs)

Not autoregressive. Tokens are generated in parallel by diffusion rather than one at a time, which is where the order-of-magnitude speed difference comes from -- it is an architecture change, not a smaller model.

### Mercury 2.5 (Inception Labs)

**Model ID**: `mercury-2.5` | GA Sep 8 2026 (press release) or Sep 24 2026 (launch blog) -- sources disagree (Verify)

- **Context Window**: 260K tokens | **Max Output**: 65,536 tokens
- **Pricing**: List $0.20 in / $0.02 cached / $0.75 out per 1M; promo $0.04 / $0.004 / $0.15
- **Reasoning**: `reasoning_effort` `instant` | `low` | `medium` (default) | `high`
- **API**: OpenAI-compatible, `https://api.inceptionlabs.ai/v1/chat/completions`; text only

### Mercury 2 (Inception Labs)

**Model ID**: `mercury-2` (sibling `mercury-edit-2`, coding-focused, FIM 32K / NextEdit 32K) | Released ~March 2026 | Closed, API-only

- **Context Window**: 128K tokens | **Max Output**: 50,000 tokens
- **Pricing**: $0.25 / $0.025 cached / $0.75 per 1M
- **Speed**: >1,000 tokens/sec on standard NVIDIA GPUs (vendor-reported)
- **Reasoning**: same effort enum as Mercury 2.5

**Best for**: latency-bound work where time-to-first-token dominates quality margin -- voice agents and phone calls, multi-step agentic tool loops, real-time search and RAG.

**Prompting**: Standard markdown; no special dialect; XML tags for multi-section prompts with critical rules placed last. Tune `reasoning_effort` first (vendor benchmarks put Mercury 2 `medium` ahead of GPT-4.1 on IFBench and Tau3Bench Telecom -- vendor-reported). Two architecture-specific gotchas: streaming semantics differ because tokens do not arrive strictly left-to-right, so UI code that assumes sequential append may need reworking; and the context window is small for this generation, so it is the wrong pick for large-document work regardless of speed.

---

## 8. Model Selection Guide

### By Use Case

| Use Case | Primary Pick | Alternative | Why |
|----------|-------------|-------------|-----|
| **Complex reasoning** | Fable 5.1 | GPT-6 Astra, Opus 5.5 at `xhigh` | Official escalation when Opus 5.5 falls short |
| **Default / most workloads** | Opus 5.5 at `medium` | Sonnet 5.5 | Anthropic's stated starting model |
| **Coding / software dev** | Opus 5.5 | Sonnet 5.5, Gemini 3.8 Flash | Opus 5.5 `medium` ≥ Opus 5 `high` |
| **Huge documents** | 1M class: Claude 5.x, GPT-6 / 5.6, Gemini 3.8 Flash | Llama 4 Scout (self-host only) | Scout has no first-party API; hosts are retiring it |
| **Low latency** | Mercury 2.5 | Haiku 4.5, Gemini 3.5 Flash-Lite, Gemini 3.8 Flash at `low` | Diffusion LLM |
| **High-volume / sub-agents** | Haiku 4.5 | Sonnet 5.5, GPT-6 Luna | Speed and cost |
| **Cost-sensitive** | DeepSeek V4.1-Flash | GPT-6 Luna, GLM-5.3-Flash, MiMo-V2.6-Flash | Lowest cost per task |
| **Multilingual** | Qwen 3.8-Max | Mistral Medium 3.5 | Broadest coverage |
| **Agent orchestration** | Opus 5.5 | Fable 5.1, Kimi K2.6 Swarm (Verify) | Paces multi-agent teams to a time budget |
| **Self-hosted / open-weight** | MiMo-V2.6-Pro (MIT) | GLM-5.3-Flash (MIT), DeepSeek V4.1-Flash (MIT), Muse Glimmer (Apache 2.0) | Top open-weights model; GLM-5.3, Kimi K3, Qwen 3.8, MiniMax M3 weights are custom licenses |
| **EU compliance** | Mistral Medium 3.5 | Mistral Large 3 | European sovereignty; in-region endpoints |

> Capability is commoditizing: the open-weights leader scores 46 vs the closed leader's 58 on the Artificial Analysis Intelligence Index (fetched Sep 29 2026) at roughly 1/45 the cost per task -- price and routing now differentiate.

### By Budget

| Tier | Models | When to Use |
|------|--------|-------------|
| **Frontier** | Fable 5.1 ($10/$50), GPT-6 Astra ($10/$50) | Hardest problems, multiday autonomous runs |
| **Premium** | Opus 5.5 ($4/$20), GPT-6.1 Sol ($2/$10) | Agentic coding, enterprise, complex tasks |
| **Standard** | Sonnet 5.5 ($2/$10), Gemini 3.8 Flash ($0.75/$3.75 intro) | Production workloads, daily coding |
| **Economy** | Haiku 4.5 ($1/$5), GPT-6 Luna ($0.10/$0.50), Gemini 3.5 Flash-Lite | High-volume, latency-critical |
| **Budget** | DeepSeek V4.1-Flash, GLM-5.3-Flash, MiMo-V2.6-Flash | Cost-optimized, self-hosted |

---

## 9. Cost Optimization & Token Economics

### Prompt Caching

Most providers offer prompt caching for repeated prefixes:

| Provider | Feature | Savings | How |
|----------|---------|---------|-----|
| Anthropic | Prompt caching | Reads at 0.05x-0.1x of input on current models (e.g. Opus 5.5 $0.20 vs $4) | `cache_control` breakpoints; min cacheable 512 tokens on Fable 5.1 / Opus 5.5 / Sonnet 5.5 (4,096 on Haiku 4.5); top-level effort changes break the cache -- use per-message effort |
| OpenAI | Prompt caching | Reads 0.1x input; writes 1.25x on 5.6+ | Automatic; on 5.6+ `prompt_cache_options` (`ttl:"30m"`, `mode:"explicit"`, `prompt_cache_breakpoint`); `prompt_cache_retention` only ≤5.5 |
| Google | Context caching | Up to 90% on cached tokens (excl. storage) | Explicit cache creation via API |

**Cache-Friendly Prompt Structure**:
```
[STATIC SYSTEM PROMPT]     <-- Cached (place first, rarely changes)
[REFERENCE DOCUMENTS]      <-- Cached (stable across requests)
[DYNAMIC USER QUERY]       <-- Not cached (changes per request)
```

### Token Optimization Strategies

1. **Right-size your model**: Use Haiku/Luna for simple tasks, Premium for complex ones
2. **Leverage caching**: Structure prompts with stable prefixes first
3. **Right-size few-shot**: 3-5 diverse examples is the vendor-recommended range; past ~5 you pay tokens for redundancy
4. **Use structured outputs**: JSON mode reduces output tokens vs verbose prose
5. **Batch processing**: Anthropic and OpenAI (Batch/Flex) offer 50% discounts for async batch calls
6. **Context window awareness**: Don't send 200K tokens when 10K suffices -- GPT-6/5.6 reprice the whole request above 272K, Grok above 200K, Gemini 3.1 Pro above 200K
7. **Time-of-day pricing**: DeepSeek off-peak (outside 01-04 and 06-10 UTC Mon-Fri) is half price
8. **Intro pricing expiry**: Gemini 3.8/3.7/3.6 Flash intro rate ($0.75/$3.75) ends Dec 31 2026; GPT-5.6 Sol promo runs "at least through Nov 21 2026"

### Cost Per Task Estimation

| Task Type | Typical Tokens | Recommended Tier | Est. Cost Range |
|-----------|---------------|------------------|-----------------|
| Simple Q&A | 1K-5K | Economy | $0.001-0.01 |
| Code generation | 5K-20K | Standard | $0.01-0.10 |
| Document analysis | 20K-200K | Standard/Premium | $0.05-1.00 |
| Deep research | 50K-500K | Premium | $0.50-5.00 |
| Agent workflow | 100K-1M+ | Standard | $0.10-10.00 |

---

## 10. Deprecated & Legacy Models

### Claude

| Model | API ID | Status |
|-------|--------|--------|
| **Opus 4.1** | `claude-opus-4-1-20250805` | **Retired Aug 5 2026** (errors) |
| Sonnet 4.5 | `claude-sonnet-4-5-20250929` | 200K context; retires ≥ Sep 29 2026 (imminent) |
| Mythos Preview | `claude-mythos-preview` | Deprecated Jun 9 2026, retirement TBA |
| Opus 4.5 | `claude-opus-4-5-20251101` | Last Opus with manual thinking budgets; ≥ Nov 24 2026 |
| Opus 4.6 | `claude-opus-4-6` | ≥ Feb 5 2027; fast mode disabled Jun 29 2026 |
| Opus 4.7 | `claude-opus-4-7` | ≥ Apr 16 2027; fast mode removed Jul 24 2026 |
| Sonnet 4.6 | `claude-sonnet-4-6` | ≥ Feb 17 2027; superseded by Sonnet 5; old tokenizer |

Retired except on select clouds: Opus 4, Sonnet 4, Haiku 3.5. Claude 5-generation legacy models (Fable 5, Mythos 5, Opus 5, Sonnet 5, Opus 4.8) are still available -- see §1.

### OpenAI

| Model / group | Status |
|---------------|--------|
| GPT-5.3 Instant `gpt-5.3-chat-latest` | **Retired Aug 10 2026** ("Instant" is now a ChatGPT thinking level on GPT-5.6 Sol/Luna) |
| `gpt-5-codex`, `gpt-5.1-codex*`, `gpt-5.2-codex`, `gpt-5-chat-latest`, `gpt-5.1-chat-latest`, `computer-use-preview` | Retired Jul 23 2026 |
| `gpt-5.2-chat-latest` | Retired Aug 10 2026 → `gpt-5.6-sol` / `-terra` |
| `gpt-5-2025-08-07`, mini, nano, `gpt-5-pro`, `o3`, `o3-pro` | Retire Dec 11 2026 → `gpt-5.6-*` (Pro → `gpt-5.6-sol` + `reasoning.mode:"pro"`) |
| GPT-5.5 in ChatGPT / Codex | Leaves Oct 14 2026 (API unaffected) |
| Specific GPT-4 / 4o snapshots | Oct 23 2026 (`gpt-4o`, `gpt-4o-mini`, `gpt-4.1*` still priced) |
| Assistants API | Shut down Aug 26 2026 → Responses + Conversations |
| Platform | `v1/prompts` shuts down Nov 30 2026; Evals platform read-only Oct 31 2026 |

### Google

| Model | Status |
|-------|--------|
| Gemini 2.0 Flash / Flash-Lite | Shut down Jun 1 2026 |
| Gemini 2.5 | New users blocked since Sep 18 2026 (existing keep access; "not deprecated") |
| `gemini-3-pro-preview` | Shut down Mar 9 2026 → 3.1 Pro |
| `gemini-3.1-flash-lite-preview` | Shut down May 25 2026 |

### Other Vendors

| Vendor | Status |
|--------|--------|
| xAI | `grok-4-0709`, `grok-4-fast-*`, `grok-4-1-fast-*`, `grok-3` retired May 15 2026 → redirect to `grok-4.3` (billed at 4.3 rates). `grok-code-fast-1` → `grok-build-0.1` |
| Meta | Meta-hosted Llama API retired Jul 6 2026. Llama 3.x → Llama 4 (frozen) or Muse |
| Mistral | `magistral-medium/small-2509`, `devstral-2512`, `mistral-small-2506` retired Jul 31 2026; `mistral-medium-2505/2508` retired Aug 31 2026. Retired IDs return 404 |
| DeepSeek | `deepseek-chat` / `deepseek-reasoner` discontinued Jul 24 2026. `deepseek-v4-flash` aliased to V4.1-Flash Sep 10 2026. V3.x → `deepseek-flash` |
| Kimi / Qwen | `kimi-k2.5`, `moonshot-v1-*` retired Aug 31 2026 (404); `kimi-k2-*` retired May 25 2026. `qwen3.8-max-preview` superseded by GA `qwen3.8-max` |

---

## 11. 2026 Paradigm Updates (September 2026)

### Adaptive Thinking Is Universal, Defaults Differ

All current Claude models (except Haiku 4.5) use adaptive thinking. Manual `budget_tokens` → 400 on all 5.x and Opus 4.8. Defaults differ per model: always-on (Fable 5/5.1, Opus 5.5), on-by-default (Opus 5, Sonnet 5, Sonnet 5.5 with `between_tools` as the lowest setting), off-unless-set (Opus 4.8). Cross-provider convergence: OpenAI `reasoning.effort`, Gemini `thinking_level`, DeepSeek `reasoning_effort`.

### Effort as Primary Cost Lever -- and It Does Not Transfer

`output_config: {effort: "..."}` is the main knob for intelligence vs cost/latency. Only documented pairwise mappings exist (Opus 5.5 `medium` ≥ Opus 5 `high`; Fable 5.1 `medium` ≈ Fable 5; Sonnet 5 `medium` ≈ Sonnet 4.6 `high`). Match effort to task difficulty, re-sweep per model, and never port effort across models or generations (GPT-6 Astra has no `none`; Qwen 3.8 has no `high`).

### Context Compaction Is a Safety Surface

Compaction silently evicts standing rules (tool-call violations 0%→30-59%, arXiv:2606.22528). **Re-pin governance rules/permissions after every compaction.** LLM summarizers are lossy and ignore volume instructions. Prefer file-backed state + git checkpoints over long conversation memory.

### Sampling Params Are Dying

`temperature`/`top_p`/`top_k` → 400 on Claude current-gen and legacy 5.x/Opus 4.8. Gemini sampling params were deprecated Jul 21 2026 (ignored on 3.6+, 400 on future generations). DeepSeek thinking ignores them; Kimi rejects them. Steer style via prompt, not sampling.

### Prefill Removed

Prefilled assistant responses (last turn) → 400 on the Claude 5.x family and Opus 4.8 (Haiku 4.5 accepts it), Mythos, and Gemini 3.6+. Migrate to Structured Outputs, `output_config.format`, or system instructions.

### Forced Tool Choice Removed on Newest Claude

Forced `tool_choice` (`any`/`tool`) → 400 on Fable 5.1, Opus 5.5, Sonnet 5.5. Use strict tools / structured outputs.

### Agent Coordination as Table Stakes

Multi-agent orchestration is standard:
- **Fable 5/5.1**: Orchestrator role, frequent subagent delegation, long-lived agents for cache savings
- **Opus 5.5**: Multi-agent teams paced to a time budget; **Opus 5**: capped subagent delegation
- **Kimi K2.6**: Agent Swarm v2 (300 agents, 4,000 steps, ~13-hr runs; Verify)
- **GPT-6 Astra**: Under-delegates -- say when and how much; async tool calling and mid-turn steering
- Dominant pattern: **frontier model as orchestrator/advisor, cheaper model as executor**

### Overthinking DoS

Adversarial logically-inconsistent prompts can force reasoning models into runaway chain-of-thought -- a denial-of-service vector via inflated compute/cost (ICML 2026, Zhejiang/Alibaba). Cap thinking budgets in production.

---

## References

- [Anthropic Claude Documentation](https://docs.anthropic.com)
- [Claude Prompting Best Practices](https://docs.anthropic.com/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)
- [OpenAI Platform Documentation](https://platform.openai.com/docs)
- [Google Gemini API Documentation](https://ai.google.dev/gemini-api/docs)
- [xAI Documentation](https://docs.x.ai)
- [Meta Llama / Muse](https://llama.meta.com)
- [Mistral Documentation](https://docs.mistral.ai)
- [Artificial Analysis Leaderboard](https://artificialanalysis.ai/leaderboards/models)
