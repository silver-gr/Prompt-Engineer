# Model Catalog & Selection Guide (July 2026)

This is the **single source of truth** for all model specifications, capabilities, and selection guidance. Other modules reference this catalog but do not duplicate model data.

---

## Frontier Landscape (July 2026)

| Provider | Model | Context | Output | Release | Key Strength |
|----------|-------|---------|--------|---------|--------------|
| Anthropic | Fable 5 | 1M | 128K | Jun 2026 | Highest capability, long-horizon autonomy |
| Anthropic | Opus 5 | 1M | 128K | Jul 2026 | Agentic coding, code review, self-verification |
| Anthropic | Opus 4.8 | 1M | 128K | May 2026 | Enterprise coding, dynamic workflows |
| Anthropic | Sonnet 5 | 1M | 128K | Jun 2026 | Default model, strong coding, cost-efficient |
| Anthropic | Haiku 4.5 | 200K | 64K | Oct 2025 | Speed + quality, sub-agents |
| OpenAI | GPT-5.6 Sol | 1.05M | 128K | Jul 2026 | Frontier; `max` effort tier new |
| OpenAI | GPT-5.6 Terra / Luna | 1.05M | 128K | Jul 2026 | Balanced / high-volume tiers |
| OpenAI | GPT-5.5 | 1.05M | 128K | 2026 | Prior flagship, Responses API |
| Google | Gemini 3.5 Flash | 1M | 64K | 2026 | Fast reasoning, cost-optimized |
| Google | Gemini 3.1 Pro | 1M | 64K | Feb 2026 | Deep reasoning, massive context |
| xAI | Grok 4.5 | 500K | — | 2026 | Reasoning always-on, tiered pricing |
| DeepSeek | V4 | 1M | 384K | 2026 | MIT, cost-effective frontier |
| Zhipu | GLM-5.2 | 1M | 64K | 2026 | Top open-weight, MIT license |
| Alibaba | Qwen 3.7 | 1M | 32K | May 2026 | Flagship closed API, multilingual, text-only |
| Alibaba | Qwen 3.8-Max-Preview | 1M | 64K | 2026 | Multimodal flagship (text/image/video), Token Plan only |
| Moonshot | Kimi K3 | 1M | — | Jul 2026 | Open weights, always-on thinking, 2.8T MoE |
| Moonshot | Kimi K2.6 | 2M | 64K | 2026 | Agent Swarm v2 (300 agents, 4K steps) |
| MiniMax | M3 | 512K | 32K | 2026 | Budget frontier coding + multimodal |
| Meta | Llama 4 Scout | 10M | 32K | Apr 2025 | Open-weight, largest context (frozen) |
| Mistral | Large 3 | 256K | 32K | Feb 2026 | EU compliance, open weights |
| Inception | Mercury 2 | 128K | — | Mar 2026 | Diffusion LLM, >1000 tok/s, lowest latency |

---

## 1. Anthropic (Claude 5 Family + Opus 4.8)

> **Tier order:** Fable 5 / Mythos 5 (top) > Opus 5 > Opus 4.8 > Sonnet 5 > Haiku 4.5
> Start with: **Opus 5** for agentic coding · **Fable 5** for highest capability · **Sonnet 5** = default

### Claude Fable 5

**Released**: June 9, 2026 | **Model ID**: `claude-fable-5`

- **Context Window**: 1M tokens | **Max Output**: 128K tokens
- **Pricing**: $10 / $50 per 1M tokens ($5/$25 batch)
- **Key Feature**: Long-horizon autonomy -- sustained multiday, goal-directed runs with strong instruction retention
- **Thinking**: Adaptive **always-on** (`disabled` → 400). Output: summarized-only (never raw CoT)
- **Effort**: `low` | `medium` | `high` (default) | `xhigh` | `max`

**Prompting Quick-Reference**:
- One brief instruction beats enumeration -- over-prescriptive prompts DEGRADE Fable 5
- Give the reason, not only the request -- context helps it connect tasks to relevant info
- Ground progress claims: "audit each claim against a tool result from this session"
- Provide a memory file (one lesson/file, dedupe, delete wrong notes) -- notable performance boost
- Use `send_to_user` tool for long async runs (delivers messages verbatim mid-turn)
- Refactor old skills/prompts -- instructions tuned for prior models are often too prescriptive

**Watch For**:
- **Never instruct to echo/transcribe reasoning** → triggers `reasoning_extraction` refusal
- Safety classifiers target offensive cyber, bio/life-sciences -- configure fallback to Opus 4.8
- `stop_reason: "refusal"` is HTTP 200 success, not an error -- handle in harness
- Rare early-stopping deep in sessions → add "You are operating autonomously" reminder
- Can take unrequested actions (email drafts, git backups) → define explicit boundaries
- Availability volatile (suspended Jun 12-Jul 1 2026) -- keep Opus 4.8 fallback wired

### Claude Mythos 5

**Released**: June 9, 2026 | **Model ID**: `claude-mythos-5` | Invite-only (Glasswing)

Same specs/pricing as Fable 5 but **no safety classifiers**. Use when Fable 5 refuses legitimate work.

### Claude Opus 5

**Released**: July 2026 | **Model ID**: `claude-opus-5`

- **Context Window**: 1M tokens (default and maximum) | **Max Output**: 128K tokens
- **Pricing**: $5 / $25 per 1M tokens
- **Key Feature**: Strongest on difficult agentic coding, code review with high precision+recall
- **Thinking**: On by default; can disable only at effort `high` or below
- **Effort**: `low` | `medium` | `high` (default) | `xhigh` | `max`

**Prompting Quick-Reference**:
- **Remove verification instructions** -- self-verifies without prompting; explicit checks cause over-verification (cost, no quality gain)
- Prompt explicitly for conciseness -- default responses run longer than prior Opus
- Constrain scope for narrow tasks -- can expand scope, adding unrequested steps
- Cap subagent delegation for cost-sensitive work
- Limit correction narration: "Only correct when the error would change code/conclusions/decisions"
- Vision: strong on charts, docs, UI replication; iterative crop tool boosts further
- `low`/`medium` effort produce strong quality at fraction of tokens -- start at default, sweep

**Watch For**:
- Delegates to subagents more readily -- add "Do not use subagents to verify your own work"
- With thinking disabled: rare tool-call-as-text leakage + internal XML tags in output
- Anthropic cut >80% of Claude Code's system prompt for Opus 5 with no eval loss -- less is more

### Claude Opus 4.8

**Released**: May 28, 2026 | **Model ID**: `claude-opus-4-8`

- **Context Window**: 1M tokens | **Max Output**: 128K tokens
- **Pricing**: $5 / $25 per 1M tokens (fast mode: $10/$50 via `speed:"fast"`)
- **Thinking**: Adaptive **off unless `type:"adaptive"` set** | **Effort**: same range
- ~4× less likely to let own code flaws pass vs 4.7
- Dynamic workflows: plans + hundreds of parallel subagents in one session
- Prompt-cache min lowered to 1,024 tokens (was 2,048)

**Best For**: Enterprise coding, fast-mode agentic work, primary Fable 5 fallback target

### Claude Sonnet 5

**Released**: June 30, 2026 | **Model ID**: `claude-sonnet-5`

- **Context Window**: 1M tokens | **Max Output**: 128K tokens
- **Pricing**: $3 / $15 per 1M tokens (intro: $2/$10 until Aug 31, 2026)
- **Thinking**: Adaptive **on by default** (`disabled` to turn off)
- **Effort**: `low` | `medium` | `high` (default) | `xhigh` | `max`
- New tokenizer: ~30% more tokens for same text vs Sonnet 4.6

**Effort cross-mapping**: Sonnet 5 `medium` ≈ 4.6 `high` · Sonnet 5 `high` ≈ 4.6 `max`

**Prompting Quick-Reference**:
- More literal instruction following -- state scope explicitly ("Apply to every section, not just the first")
- Calibrates response length to task complexity (shorter on simple, longer on complex)
- With thinking off: less likely to reach for tools -- nudge explicitly
- Higher-quality progress updates -- remove "summarize every N calls" scaffolding
- Frontend/design may settle into default style -- specify concrete alternatives or ask for options first
- Computer use: `computer_20251124`, up to 2576px / 3.75MP; 1080p = good balance

**Watch For**:
- `budget_tokens` → 400 | `temperature`/`top_p`/`top_k` → 400 | prefill → 400
- `max_tokens` shared by thinking+text -- risk `stop_reason:"max_tokens"` truncation
- Code review: follows "only report high-severity" literally -- ask for everything, filter separately

### Claude Haiku 4.5

**Released**: October 2025 | **Model ID**: `claude-haiku-4-5-20251001`

- **Context Window**: 200K tokens | **Max Output**: 64K tokens | **Pricing**: $1 / $5
- **NO CHANGE** from prior version. Manual extended thinking (budget_tokens). Old tokenizer.

**Best For**: Sub-agents, high-volume tasks, cost-sensitive deployments, routing

### Claude 5 Family Comparison

| Feature | Fable 5 | Opus 5 | Opus 4.8 | Sonnet 5 | Haiku 4.5 |
|---------|---------|--------|----------|----------|-----------|
| Context | 1M | 1M | 1M | 1M | 200K |
| Max Output | 128K | 128K | 128K | 128K | 64K |
| Thinking default | Always-on | On (off ≤high) | Off unless set | On by default | Manual budget |
| Effort range | low→max | low→max | low→max | low→max | N/A |
| Sampling params | → 400 | → 400 | → 400 | → 400 | Accepted |
| Prefill | → 400 | → 400 | → 400 | → 400 | Accepted |
| Tokenizer | New (+30%) | New (+30%) | New (+30%) | New (+30%) | Old |
| Fast mode | No | No | Yes | No | No |
| Safety classifiers | Yes | No | No | Yes (cyber) | No |
| Price in/out | $10/$50 | $5/$25 | $5/$25 | $3/$15 | $1/$5 |

### Key Claude Insight (July 2026)

**"Prompting Opus 5 is a subtraction exercise"** (Anthropic cut >80% of Claude Code's system prompt with no eval loss). The Claude 5 family requires:
- **Remove verification/self-check instructions** -- Opus 5 and Fable 5 self-verify natively
- **Brief instructions beat enumeration** -- Fable 5 follows one brief instruction better than itemized lists
- **Effort is the primary cost lever** -- `low`/`medium` on current models often exceed `xhigh` on prior
- **No sampling params, no prefill, no manual budgets** on any current model (except Haiku 4.5)
- **Thinking on by default** for Fable 5 (always), Opus 5, Sonnet 5 -- budget `max_tokens` for thinking+text
- **New tokenizer** on all except Haiku 4.5 -- recount tokens when migrating from 4.6-era
- **Fable 5 memory system** -- provide a notes file; notable performance boost
- **send-to-user tool** -- for long async agents, deliver messages verbatim mid-turn
- **Fable 5 as orchestrator, Sonnet 5/Opus 4.8 as executor** -- dominant 2026 cost pattern

---

## 2. OpenAI (GPT-5.x Family)

### GPT-5.6 Sol / Terra / Luna

**Released**: July 9, 2026 | **GA** on Responses, Chat Completions, and Batch APIs

| Variant | Model ID | Tier |
|---------|----------|------|
| **Sol** | `gpt-5.6-sol` (default alias `gpt-5.6`) | Frontier capability |
| **Terra** | `gpt-5.6-terra` | Balanced capability/cost |
| **Luna** | `gpt-5.6-luna` | High-volume |

- **Context Window**: 1,050,000 tokens (max input 922,000) — same across all three
- **Max Output**: 128,000 tokens
- **Pricing (Sol)**: $5 in / $0.50 cached / $30 out per 1M
- **Reasoning**: `reasoning.effort` = `none`/`low`/`medium` (default)/`high`/`xhigh`/`max` — **`max` is new in this release**
- Persisted reasoning across turns supported
- Multi-agent orchestration in beta (Responses API only)

**Prompting Quick-Reference** (official guidance):
- **Lean prompts win**: OpenAI reports 10-15% eval score gains with 41-66% fewer tokens
- **State each instruction once** — repetition degrades performance
- **Don't over-repeat caution phrases** ("ask first", "wait for approval") — triggers unnecessary approval prompts
- **Model is more concise by default than 5.5** — blunt "be concise" instructions can over-truncate; use `text.verbosity` instead

**Watch For**:
- **Long-context repricing**: >272K input tokens bills **2x input / 1.5x output for the entire request**, not just the overage
- Cache writes bill at 1.25x standard input rate

### GPT-5.5

**Current widely-deployed flagship** prior to 5.6.

- **Context Window**: 1,050,000 tokens | **Max Output**: 128,000
- **Reasoning**: `reasoning.effort` = `none`/`low`/`medium`/`high`/`xhigh`
- **Verbosity**: `text.verbosity` = `low`/`medium`/`high`
- **API**: Responses API is the current recommended surface

### GPT-5.2 Thinking (Legacy)

**Released**: December 2025 | Superseded by GPT-5.5 / 5.6

- **Context Window**: 400K tokens
- **Reasoning**: `reasoning.effort` = `none` (default) / `low` / `medium` / `high` / `xhigh`
- **Note**: earlier editions of this catalog listed a `reasoning_profile: light|balanced|deep` parameter here. No such parameter exists in OpenAI's GPT-5.2 docs -- see 08-gpt5-practices_v5.md.

**Prompting Quick-Reference**:
- Keep prompts MINIMAL and direct -- less is more
- Crisp tool descriptions (1-2 sentences)
- Use `reasoning.effort: "high"` or `"xhigh"` with verification scaffolds for high-assurance tasks
- Avoid over-prompting (reduces quality)
- System messages for role definition
- JSON mode for structured outputs
- For coding: specify languages and success criteria, avoid over-specification

**Watch For**:
- Agentic persistence reminders needed at light/balanced reasoning levels
- Over-specification reduces quality

### GPT-5.3 Instant

**Released**: March 3, 2026

- **Context Window**: 128K tokens
- **Key Feature**: Ultra-low latency responses with strong capability retention
- **Strengths**: Cost-efficient, fast, maintains core GPT-5 capabilities
- **Best For**: Real-time applications, high-volume deployments, latency-critical tasks

**Prompting Quick-Reference**:
- Same principles as GPT-5.2 -- simple, direct prompts
- Optimized for speed; avoid requesting deep reasoning on simple tasks
- Ideal for streaming, interactive use cases

### GPT-5.1

**Released**: November 13, 2025

- **Context Window**: 400K tokens
- **Key Feature**: `"none"` reasoning mode for ultra-low-latency; auto-calibrates reasoning depth
- **Strengths**: Flexible reasoning modes, calibrated to prompt difficulty

### GPT-5 (Base)

**Released**: August 2025

- **Context Window**: 400K tokens
- **Key Feature**: Unified flagship, enterprise-grade alignment
- **Strengths**: All benchmarks, video reasoning, biomedical analysis

### Key GPT-5 Insight

Less is more. Agentic persistence reminders are critical at minimal reasoning levels. For coding tasks, avoid over-specification -- the model performs better with cleaner, simpler instructions. Use reasoning profiles to match task complexity rather than prompt engineering tricks.

---

## 3. Google (Gemini 3.1 Family)

### Gemini 3.1 Pro (Preview)

**Released**: February 19, 2026 as Preview | Model ID `gemini-3.1-pro-preview` | **#1 on major benchmarks**

- **Context Window**: 1M tokens
- **Output**: 64K tokens
- **Key Feature**: Top-ranked reasoning model with massive context, builds on Gemini 3 foundations
- **Thinking**: `thinking_level`: `"low"` | `"high"` (default)

**Prompting Quick-Reference**:
- **OMIT `temperature`/`top_p`/`top_k`** -- default 1.0 is the recommended setting; lowering causes loops/degraded performance
- Favor DIRECTNESS over persuasion (treats prompts as executable instructions)
- NO conversational fluff ("please", "kindly", "if you could")
- Context FIRST, questions LAST for long contexts
- Constraints at END (negative/formatting constraints dropped if placed early)
- Use `thinking_level: "low"` for fast mode + "Think silently"
- 2-3 few-shot examples with consistent formatting (Google recommendation)
- Anchor transitions: "Based on the above..."
- Explicit labels for multimodal inputs ("Image 1..., Video 2...")

**Watch For**:
- Conversational language actively degrades instruction-following
- Constraints placed before context may be dropped
- Personas taken very seriously -- may override other instructions

### Gemini 3.1 Flash-Lite

**Released**: Preview March 3, 2026 | Stable GA May 7, 2026

- **Context Window**: 1M tokens
- **Output**: 64K tokens
- **Key Feature**: Real-time optimized with near-Pro quality at fraction of cost
- **Strengths**: Latency-optimized, rapid iteration, streaming outputs

**Prompting Quick-Reference**:
- Concise task briefs with optional enrichment sections
- Define response schemas to maintain structure at high speed
- Same guidance: OMIT temperature/top_p/top_k (use defaults)

### Gemini 2.5 Pro / Flash

Still available for production workloads. Same 1M context, adaptive thinking budgets. Being superseded by 3.1 family.

### Key Gemini Insight

Gemini 3.x treats prompts as executable instructions, not conversation. DO NOT use complex prompt engineering from the 2.x era. Use `thinking_level` for reasoning control. Keep temperature at 1.0. Be direct, never persuasive.

**Critical constraint ordering**: Place negative/formatting constraints LAST or they get dropped.

---

## 4. xAI (Grok Family)

### Grok 4.5

**Model ID**: `grok-4.5` (aliases `grok-4.5-latest`, `grok-build-latest`)

- **Context Window**: 500,000 tokens
- **License**: Closed, API-only. Available on API, Grok Build, Cursor
- **Reasoning**: `reasoning_effort` = `low`/`medium`/`high` (default `high`). **Reasoning cannot be disabled.**

**Pricing (tiered by prompt size)**:

| Prompt size | Input | Cached | Output |
|-------------|-------|--------|--------|
| <200K | $2.00 | $0.30 | $6.00 |
| ≥200K | $4.00 | $0.60 | $12.00 |

**Watch For**:
- **Crossing 200K reprices the entire request**, not just the overage — budget accordingly
- `presence_penalty`, `frequency_penalty`, and `stop` are **rejected as errors**
- No official prompting guide published

**Prompting Quick-Reference**:
- Structure large contexts with hierarchical headings
- Clear, direct tool instructions
- Request verification steps for quantitative reasoning

### Grok 4.x Earlier / Fast Variants

Earlier iterations. Grok 4 Fast introduced the unified reasoning/non-reasoning model.

---

## 5. Chinese Frontier Models

### DeepSeek V4

- **Context Window**: 1M tokens
- **Pricing**: V4 Flash $0.14/$0.28 · V4 Pro $0.435/$0.87 per 1M
- **License**: MIT (open weights)
- **Key Feature**: Frontier-level reasoning at lowest cost tier
- **Reasoning**: `reasoning_effort`: high (default) / max

**Prompting**: Clear, structured prompts. Enable thinking via `extra_body={"thinking":{"type":"enabled"}}` -- NOT raw `<think>` tags. **Gotcha**: must echo `reasoning_content` on tool-result turns or the API returns 400. Thinking mode ignores sampling params.

### GLM-5.2 (Zhipu AI)

- **Context Window**: 1M tokens
- **License**: MIT (top open-weight model)
- **Key Feature**: Best open-weight option; High/Max reasoning modes
- **Reasoning**: `reasoning_effort`

**Prompting**: Provide bilingual glossaries for multilingual output. Define explicit function-calling payloads. **Gotcha**: preserved thinking blocks must match exactly when replayed.

### Qwen 3.7 (Alibaba)

**Released**: `qwen3.7-max` May 21, 2026 (snapshot `qwen3.7-max-2026-05-20`; US variant `qwen3.7-max-us` Jun 26, 2026) · `qwen3.7-plus` ~Jun 1, 2026 (snapshot `qwen3.7-plus-2026-05-26`)

- **Context Window**: **1M tokens** for both `qwen3.7-max` and `qwen3.7-plus` (Alibaba Model Studio docs, EN and ZH)
- **Availability**: Flagship is **closed/API-only**; open option is Qwen3.6-35B-A3B (Apache 2.0)
- **Key Feature**: Broadest multilingual coverage
- **Modality**: `qwen3.7-max` is **text-only** (no vision); `qwen3.7-plus` handles text and multimodal
- **Reasoning**: `enable_thinking` toggle

> **Do not read "256K" as this model's ceiling.** Alibaba's sizing-guidance prose says *"for standard tasks, 128k-256k tokens is typically sufficient"* — that is advice about how much context a task needs, not a spec. The max context is 1M.

**Prompting**: Direct, clear instructions with structured context. Specify target language explicitly.

### Qwen 3.8-Max-Preview (Alibaba)

- **Context Window**: 1,000,000 tokens
- **Max Output**: 65,536 tokens
- **Modality**: text, image, video
- **Availability**: Preview, gated to **Token Plan** subscribers on Alibaba Cloud Model Studio; likely model ID `qwen3.8-max-preview`
- **Key Feature**: Flagship of the Qwen3.8 series — state of the art across *both* language and vision, unlike text-only `qwen3.7-max`
- **Strengths**: Expert-level knowledge, complex logical reasoning, advanced mathematics, sophisticated coding; vision covers high-precision image understanding, visual reasoning, OCR, document and chart analysis, and fine-grained visual grounding
- **Pricing**: not published

> **Sourcing**: existence and Token Plan gating are confirmed in Alibaba's public docs, but the spec table above comes from the provider console, which sits behind a subscription login and could not be independently corroborated. Treat the numbers as vendor-stated, not third-party verified.

**Prompting**: Same dialect as Qwen 3.7. Prefer it over `qwen3.7-max` when the task is multimodal; `qwen3.7-max` cannot see images at all.

### Kimi K3 (Moonshot AI)

- **Context Window**: 1,048,576 tokens (1M)
- **Pricing**: Input $3.00 (cache miss) / $0.30 (cache hit) · Output $15.00 per 1M — flat, no tiering
- **License**: **Open weights** under custom "Kimi K3 License"
- **Architecture**: MoE, 2.8T total / 104B activated params, 93 layers (69 KDA + 24 Gated MLA attention), 896 experts, MoonViT-V2 vision encoder, MXFP4/MXFP8 quantization-aware training
- **Reasoning**: **Always-on thinking**; returns `reasoning_content`. `reasoning_effort` = `low`/`high`/`max` (default `max`)
- **Key Feature**: Long-horizon coding and end-to-end knowledge work, native visual understanding

**Watch For**: **Preserved thinking history mode** — full assistant messages (including `reasoning_content` and `tool_calls`) must be replayed **verbatim** on later turns.

**Prompting**: Designed for extended coding sessions and multi-step knowledge tasks. Native vision means no separate image pipeline needed.

### Kimi K2.6 (Moonshot AI)

- **Context Window**: 2M tokens
- **Key Feature**: **Agent Swarm v2** -- 300 sub-agents, 4,000 steps, ~13-hour runs
- **Input**: Text, image, and video; thinking and non-thinking modes
- **Variant**: K2.7-Code (thinking forced ON)
- **Sampling**: temp 1.0 for thinking mode / 0.6 for instant

**Prompting**: Leverage ultra-long context for document analysis. Agent Swarm enables native multi-agent task decomposition at scale unmatched by other providers. Models do not access external resources by default — extend via official tools or custom tool calls.

### MiniMax M3

- **Context Window**: 512K guaranteed
- **Pricing**: ~$0.30/$1.20 per 1M
- **Key Feature**: Budget frontier coding + native multimodal

**Prompting**: Plan against the 512K guaranteed context. Standard structured prompting.

---

## 6. Open-Source / Open-Weight Models

### Llama 4 Maverick (Meta)

**Released**: April 5, 2025

- **Context Window**: 1M tokens
- **Architecture**: Mixture of Experts (MoE)
- **Key Feature**: Open-weight model competitive with closed-source frontier
- **Strengths**: Customizable, self-hosted, strong reasoning

**Prompting**: Standard direct instruction patterns. Benefits from structured context similar to Claude/GPT approaches.

### Llama 4 Scout (Meta)

**Released**: April 5, 2025

- **Context Window**: 10M tokens
- **Architecture**: MoE, smaller expert count than Maverick
- **Key Feature**: Efficient open-weight model for deployment at scale
- **Strengths**: Lower compute requirements, strong performance per FLOP

### Mistral Large 3

**Released**: February 2026

- **Context Window**: 256K tokens
- **Key Feature**: European AI sovereignty, strong multilingual capabilities
- **Strengths**: EU compliance, function calling, multilingual reasoning

**Prompting**: Structured prompts with clear function schemas. Strong at JSON output generation.

---

## 7. Specialized Architectures (Diffusion LLMs)

Not autoregressive. Tokens are generated in parallel by diffusion rather than one at a time, which is where the order-of-magnitude speed difference comes from — it is an architecture change, not a smaller model.

### Mercury 2 (Inception Labs)

**Released**: ~March 2026

- **Context Window**: 128K tokens (vendor states this is a current constraint they are working to extend)
- **Max Output**: no published hard cap; docs use `max_tokens: 8192` in examples
- **Pricing**: Input $0.25 · Cached input $0.025 · Output $0.75 per 1M
- **Speed**: >1,000 tokens/sec on standard NVIDIA GPUs
- **Modality**: text only
- **API**: OpenAI-compatible, `https://api.inceptionlabs.ai/v1/chat/completions`; model ID `mercury-2`
- **Reasoning**: `reasoning_effort` with tiers `instant` | `low` | `medium` | `high`
- **Sibling**: Mercury Edit 2 (`mercury-edit-2`), coding-focused — FIM 32K / NextEdit 32K

**Best for**: latency-bound work where time-to-first-token dominates quality margin — voice agents and phone calls, multi-step agentic tool loops, real-time search and RAG.

**Prompting**: Standard markdown; no special dialect. Tune `reasoning_effort` first — vendor benchmarks put `medium` ahead of GPT-4.1 on IFBench and Tau3Bench Telecom while still decoding faster. Two architecture-specific gotchas: streaming semantics differ from autoregressive models because tokens do not arrive strictly left-to-right, so UI code that assumes sequential append may need reworking; and the 128K window is small for this generation, so it is the wrong pick for large-document work regardless of speed.

---

## 8. Model Selection Guide

### By Use Case

| Use Case | Primary Pick | Alternative | Why |
|----------|-------------|-------------|-----|
| **Complex reasoning** | Fable 5 | GPT-5.5, Opus 4.8 | Highest capability, long-horizon autonomy |
| **Software development** | Opus 5 (effort: xhigh) | Sonnet 5 | SOTA coding, self-verification, code review |
| **Massive document analysis** | Llama 4 Scout (10M) | 1M class: Claude 5-gen, GPT-5.5, Gemini 3.5 | Context size |
| **Real-time / low latency** | Mercury 2 | Haiku 4.5, Gemini 3.5 Flash | >1000 tok/s (diffusion LLM) |
| **High-volume / sub-agents** | Haiku 4.5 | Sonnet 5 | Speed + quality at low cost |
| **Cost-sensitive** | DeepSeek V4 Flash ($0.14/$0.28) | MiniMax M3, GLM-5.2 free tiers | Frontier quality at lowest cost |
| **Multilingual** | Qwen 3.7 (API) | Mistral Large 3 | Broadest coverage |
| **Agent orchestration** | Kimi K2.6 (Swarm v2) | Opus 5, Fable 5 | 300 agents, 4K steps |
| **Self-hosted / open-weight** | GLM-5.2 (MIT, 1M) | DeepSeek V4 Pro, Kimi K2.7-Code | Top open-weight |
| **EU compliance** | Mistral Large 3 | -- | European sovereignty |
| **Budget coding** | DeepSeek V4 Pro ($0.44/$0.87) | MiniMax M3 | Near-frontier at fraction of cost |

> Capability is commoditizing: 5 models within 0.4 pts SWE-bench across a 5x price range -- price/routing now differentiates.

### By Budget

| Tier | Models | When to Use |
|------|--------|-------------|
| **Frontier** | Fable 5 ($10/$50) | Hardest problems, multiday autonomous runs |
| **Premium** | Opus 5, Opus 4.8, GPT-5.5 | Agentic coding, enterprise, complex tasks |
| **Standard** | Sonnet 5, Gemini 3.1 Pro | Production workloads, daily coding |
| **Economy** | Haiku 4.5, Gemini 3.5 Flash | High-volume, latency-critical |
| **Budget** | DeepSeek V4 Flash, MiniMax M3, GLM-5.2 | Cost-optimized, self-hosted |

---

## 9. Cost Optimization & Token Economics

### Prompt Caching

Most providers offer prompt caching for repeated prefixes:

| Provider | Feature | Savings | How |
|----------|---------|---------|-----|
| Anthropic | Prompt caching | Up to 90% on cached tokens | `cache_control` breakpoints in messages |
| OpenAI | Automatic caching | Up to 90% on cached tokens | Automatic for repeated prefixes |
| Google | Context caching | Up to 90% on cached tokens (excl. storage) | Explicit cache creation via API |

**Cache-Friendly Prompt Structure**:
```
[STATIC SYSTEM PROMPT]     <-- Cached (place first, rarely changes)
[REFERENCE DOCUMENTS]      <-- Cached (stable across requests)
[DYNAMIC USER QUERY]       <-- Not cached (changes per request)
```

### Token Optimization Strategies

1. **Right-size your model**: Use Haiku/Instant for simple tasks, Premium for complex ones
2. **Leverage caching**: Structure prompts with stable prefixes first
3. **Minimize few-shot**: 0-1 examples for reasoning models (saves tokens, improves quality)
4. **Use structured outputs**: JSON mode reduces output tokens vs verbose prose
5. **Batch processing**: Many providers offer 50% discounts for async batch API calls
6. **Context window awareness**: Don't send 200K tokens when 10K suffices

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

### Claude Legacy

| Model | API ID | Notes |
|-------|--------|-------|
| Opus 4.7 | `claude-opus-4-7` | Legacy; fast mode removed 2026-07-24 |
| Opus 4.6 | `claude-opus-4-6` | Fast mode disabled 2026-06-29 |
| Opus 4.5 | `claude-opus-4-5-20251101` | Last Opus with manual thinking budgets |
| Sonnet 4.6 | `claude-sonnet-4-6` | Replaced by Sonnet 5; old tokenizer |
| Sonnet 4.5 | `claude-sonnet-4-5-20250929` | 200K context |
| **Opus 4.1** | `claude-opus-4-1-20250805` | **Deprecated, retires 2026-08-05** |

Retired (except select clouds): Opus 4, Sonnet 4, Haiku 3.5.

### Other Legacy

| Model | Status | Migration Target |
|-------|--------|-----------------|
| GPT-4o / GPT-4 | Removed 2025 | GPT-5.5+ |
| Claude 4.5 family | Superseded | Claude 5 family |
| Gemini 2.x | Available but superseded | Gemini 3.5 Flash |
| DeepSeek V3.x | Available | DeepSeek V4 |
| Llama 3.x | Available | Llama 4 (frozen -- Meta frontier went closed with Muse Spark) |

---

## 11. 2026 Paradigm Updates (July 2026)

### Adaptive Thinking Is Universal

All current Claude models (except Haiku 4.5) use adaptive thinking. Manual thinking budgets (`budget_tokens`) → 400 on all current models except Haiku 4.5. Thinking defaults now differ per model: always-on (Fable 5), on-by-default (Opus 5, Sonnet 5), off-unless-set (Opus 4.8). Cross-provider convergence: GPT-5.5 `reasoning.effort`, Gemini 3.x `thinking_level`, DeepSeek `reasoning_effort`.

### Effort as Primary Cost Lever

`output_config: {effort: "..."}` is the main knob for intelligence vs cost/latency. `low`/`medium` on current models often exceed `xhigh` on prior models. Match effort to task difficulty, not model tier.

### Context Compaction Is a Safety Surface

Compaction silently evicts standing rules (tool-call violations 0%→30-59%, arXiv:2606.22528). **Re-pin governance rules/permissions after every compaction.** LLM summarizers are lossy and ignore volume instructions. Prefer file-backed state + git checkpoints over long conversation memory.

### Sampling Params Are Dying

`temperature`/`top_p`/`top_k` → 400 on Claude current-gen and Sonnet 5. Gemini docs: remove them. DeepSeek thinking: ignores them. Steer style via prompt, not sampling.

### Prefill Removed

Prefilled assistant responses (last turn) → 400 on Claude 4.6+ and Mythos. Migrate to Structured Outputs, `output_config.format`, or system instructions.

### Agent Coordination as Table Stakes

Multi-agent orchestration is standard:
- **Fable 5**: Orchestrator role, parallel subagent dispatch, long-lived agents for cache savings
- **Opus 5**: Writer-verifier patterns, strong multi-agent coordination
- **Kimi K2.6**: Agent Swarm v2 (300 agents, 4,000 steps, ~13-hr runs)
- **GPT-5.5**: Tool orchestration with reasoning profiles
- Dominant pattern: **frontier model as orchestrator, cheaper model as executor**

### New Anti-Pattern: Overthinking DoS

Adversarial logically-inconsistent prompts can force reasoning models into runaway chain-of-thought -- a denial-of-service vector via inflated compute/cost (ICML 2026, Zhejiang/Alibaba). Cap thinking budgets in production.

---

## References

- [Anthropic Claude 5 Documentation](https://docs.anthropic.com)
- [Prompting Claude Fable 5](https://docs.anthropic.com/en/build-with-claude/prompt-engineering/prompting-claude-fable-5)
- [Prompting Claude Opus 5](https://docs.anthropic.com/en/build-with-claude/prompt-engineering/prompting-claude-opus-5)
- [Prompting Claude Sonnet 5](https://docs.anthropic.com/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5)
- [Claude Prompting Best Practices](https://docs.anthropic.com/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)
- [OpenAI GPT-5 Platform Documentation](https://platform.openai.com/docs)
- [Google Gemini 3.x Prompting Guide](https://ai.google.dev/gemini-api/docs)
- [xAI Grok Documentation](https://docs.x.ai)
- [Meta Llama 4 Model Card](https://llama.meta.com)
- [Mistral Large 3 Documentation](https://docs.mistral.ai)
