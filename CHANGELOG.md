# Changelog

All notable changes to the Prompt Engineering Knowledge Base are documented in this file.

## [6.0.1] - 2026-07-29 — Accuracy Audit

Every file was fact-checked against official vendor documentation by an independent
reviewer (Codex, `gpt-5.6-sol`, high reasoning effort), one file per pass. Findings
were triaged into hard factual errors, rubric conflicts, and editorial guidance;
each category is listed below.

### Fabricated APIs Removed

These did not exist in any vendor's documentation. Anyone copying them got a runtime error.

- **`model.generate(prompt=..., prefix=...)`** (07-gemini) — no such method or parameter
  in the Google GenAI SDK. Replaced with `client.models.generate_content()` using
  `response_mime_type` + `response_schema`.
- **`reasoning_profile: light|balanced|deep`** (08-gpt5, 03-catalog) — not an OpenAI
  parameter. The prior edition compounded the error by advising migration *away* from it,
  which legitimized it. Replaced with the real per-model `reasoning.effort` enum table.
- **Gemini generation config with `temperature`/`top_p`** (04-evaluation) — replaced with
  the nested `thinking.thinking_level` form and an explicit note to omit sampling params.

### Factual Corrections

- **Effort is soft guidance, not a hard cap** — `output_config.effort` steers behavior;
  `max_tokens` remains the only strict ceiling (06-claude, 02-techniques).
- **Effort mappings are Sonnet-specific** — the documented `medium` ≈ prior-`high`
  equivalence applies to Sonnet 5, not the family. Sweep per model (00, 06).
- **Sampling params: non-default values reject** — defaults are still accepted; only
  non-default `temperature`/`top_p` return 400, and `top_k` is rejected outright.
  Corrected from the blanket "MUST be 1.0" claim in 00/02/03/07/09/10.
- **Gemini sampling is discouraged, not rejected** — accepted by the API; sub-1.0
  temperature may cause looping. Downgraded from "→ 400" to "discouraged / may cause".
- **Gemini `thinking` config is nested** — `{"thinking": {"thinking_level": "medium"}}`,
  values lowercase; `minimal` is Gemini 3.5 Flash only (01, 07).
- **`thinking.display` defaults to `"omitted"` on Fable 5** — must be set to
  `"summarized"` to receive anything back (01, 09).
- **Mid-conversation system messages are Opus-only** — Opus 5 and Opus 4.8 support them;
  Sonnet 5 does not (06).
- **Context awareness is model-scoped** — token-budget tracking is documented for
  Sonnet 5, Sonnet 4.6, Sonnet 4.5, and Haiku 4.5 only (06).
- **Chat Completions is not deprecated** — corrected in 08.
- **GPT-5.6 Sol is the current flagship** — 08 still named GPT-5.5.
- **Cache savings are ~90%**, not 50%/75%, for both OpenAI and Google at current
  prices (01, 03).
- **Haiku 4.5 is the standing exception** to every Claude 5 breaking change — keeps
  prefill, `budget_tokens`, the old tokenizer, and sampling params. Noted inline
  rather than only in the migration section (06).

### Guidance Realigned to Vendor Docs

- **Few-shot threshold raised from >2 to >5.** Anthropic recommends **3-5 diverse,
  relevant examples** in `<example>` tags. The old rubric flagged vendor-recommended
  practice as a lint error. AP-3 now targets *redundant* and *reasoning-trace* examples
  rather than count in the 3-5 range (00, 01, 02, 03, 04, CLAUDE.md).
- **CoT penalty scoped to thinking-enabled models.** Manual CoT is a documented fallback
  when extended thinking is off (Opus 4.8 default, Haiku 4.5, legacy/open-weight models).
  AP-2, the eval rubric, the lint stage, and the quality score are now gated on
  `thinking_enabled` (00, 01, 02, 04, CLAUDE.md).
- **Gemini constraint ordering flipped to match Google.** Essential constraints and
  output-format requirements belong in the **system instruction at the beginning**;
  only the specific question goes last, to avoid burial under long context. The prior
  "constraints LAST" guidance contradicted Google's documentation (00, 02, 03, 07, 10,
  CLAUDE.md).
- **Tool-description length is provider-specific.** "1-2 sentences" is OpenAI's position.
  Anthropic and Google both recommend detail, including when-to-use conditions. AP-7
  now carries a per-provider table (10).
- **Gemini Deep Research** — `collaborative_planning=true` is opt-in (default `false`),
  and access is via the Gemini Interactions API, not Vertex Discovery Engine (07).

### Notes on Scope

Findings marked UNVERIFIABLE by the reviewer were largely artifacts of the per-pass
web-fetch cap rather than unsupported claims, and were not treated as errors. Disputed
items where vendor documentation was ambiguous were left unchanged.

## [6.0] - 2026-07-29

### Claude 5 Family Update

Major update covering the Claude 5 generation (Fable 5, Opus 5, Sonnet 5) alongside Opus 4.8, plus refreshed specs across all providers. Sourced from official Anthropic prompting guides and evidence-based research.

### Model Updates
| Provider | v5.0 (Mar 2026) | v6.0 (Jul 2026) |
|----------|-----------------|-----------------|
| Anthropic | Opus 4.6, Sonnet 4.6, Haiku 4.5 | **Fable 5 / Mythos 5, Opus 5, Opus 4.8, Sonnet 5**, Haiku 4.5 |
| OpenAI | GPT-5.2 Thinking, 5.3 Instant | GPT-5.5, GPT-5.6 Sol/Terra/Luna (preview) |
| Google | Gemini 3.1 Pro, 3.1 Flash-Lite | Gemini 3.5 Flash, 3.1 Pro |
| xAI | Grok 4.20 Beta 2 | Grok 4.x |
| DeepSeek | V3.2 | **V4** (MIT, 1M ctx, Flash/Pro tiers) |
| Zhipu | GLM-5 | **GLM-5.2** (MIT, top open-weight) |
| Alibaba | Qwen 3.5 | **Qwen 3.7** (flagship now closed/API-only) |
| Moonshot | Kimi K2.5 | **Kimi K3** (open weights, 2.8T MoE), K2.6 (Agent Swarm v2) |
| MiniMax | (missing) | **M3** (budget frontier + multimodal) |
| Meta | Llama 4 Scout/Maverick | Llama 4 (frozen — Meta frontier went closed) |

### Breaking API Changes Documented
- **Prefill removed** — assistant-message on last turn → 400 on Claude 4.6+ / Mythos
- **Manual thinking budgets removed** — `budget_tokens` → 400 (except Haiku 4.5)
- **Sampling params removed** — `temperature`/`top_p`/`top_k` → 400 on current Claude gen (now includes Sonnet 5)
- **New tokenizer** — ~30% more tokens on all current models except Haiku 4.5
- **Thinking defaults differ per model** — always-on (Fable 5), on-by-default (Opus 5, Sonnet 5), off-unless-set (Opus 4.8)
- **`output_config.effort`** — effort moved to top-level config; low/medium/high/xhigh/max

### New Content
- **Effort parameter as primary cost lever** — low/medium on current models often exceed prior xhigh; effort cross-mapping tables
- **Opus 5 subtraction principle** — remove verification instructions, scope constraints, subagent caps, correction-narration limits
- **Fable 5 patterns** — brief-instruction steering, memory systems, progress grounding, action boundaries, early-stopping mitigation, context-budget reassurance
- **send-to-user tool pattern** (10) — verbatim mid-turn delivery for long async agents
- **Memory systems** (10) — one-lesson-per-file, dedupe, bootstrap-from-history
- **Orchestrator + executor pattern** (10) — frontier orchestrates, cheaper model executes
- **Safety classifiers** (09) — Fable 5 cyber/bio/`reasoning_extraction` domains, refusal-as-HTTP-200, fallback configuration
- **Compaction as safety surface** (09) — constraint eviction and re-pinning mitigation
- **Code review harness guidance** (06) — coverage-first prompting to counter literal severity filtering

### Corrections
- **Gemini sampling params** — removed incorrect "`temperature = 1.0` REQUIRED" guidance from 02, 07, 09, 10 and 00 cheat sheet; current official guidance is to OMIT sampling params entirely
- **Model tier ordering** — Fable 5 sits above Opus; Opus 5 added between Fable 5 and Opus 4.8

### New Anti-Patterns
- **AP-11** Persona on accuracy/explanatory tasks (MMLU 71.6%→66.3%)
- **AP-12** "Never hallucinate" instruction (no mechanism)
- **AP-13** Agentic over-eagerness unmanaged (no stop conditions)
- **AP-14** "Think harder/keep going" (overthinking corrupts correct answers; stop-early = +21%, arXiv:2606.02835)
- **AP-15** Offset-from-end references (Position Curse, arXiv:2605.07127)
- **AP-16** Verification instructions on Opus 5 / Fable 5 (self-verify natively)
- **AP-17** Fable 5 reasoning echo (triggers `reasoning_extraction` refusal)
- **AP-18** Over-prescriptive Fable 5 prompts (enumeration degrades output)
- **AP-19** Overthinking DoS (adversarial runaway CoT, ICML 2026)

### Cost Gotchas Newly Documented

Several 2026 models reprice the **entire request** once an input threshold is crossed — not just the tokens above it. Budgeting per-token averages will understate cost:

| Model | Threshold | Effect |
|-------|-----------|--------|
| Grok 4.5 | ≥200K prompt | $2/$6 → $4/$12 per 1M, whole request |
| GPT-5.6 | >272K input | 2x input / 1.5x output, whole request |
| GPT-5.6 | Cache writes | 1.25x standard input rate |
| Claude 5-gen | New tokenizer | ~30% more tokens for identical text |

### Verified Model Additions (direct official-docs fetch)

- **Grok 4.5** — 500K ctx, closed API, reasoning cannot be disabled, `reasoning_effort` low/med/high (default high). `presence_penalty`/`frequency_penalty`/`stop` rejected as errors. No official prompting guide published.
- **Kimi K3** — 1M ctx, **open weights** (custom Kimi K3 License), $3/$15 ($0.30 cache hit), always-on thinking, `reasoning_effort` low/high/max (default max). 2.8T MoE / 104B activated, MoonViT-V2 vision. Preserved-thinking mode requires verbatim replay of `reasoning_content` + `tool_calls`.
- **GPT-5.6 Sol / Terra / Luna** — GA July 9, 2026. 1.05M ctx (922K max input) / 128K out, identical across tiers. `reasoning.effort` gains a new `max` level. Official guidance: lean prompts (10-15% eval gain at 41-66% fewer tokens), state each instruction once, avoid repeated caution phrases, use `text.verbosity` rather than "be concise".
- **Qwen 3.8 Max Preview** — **not found**. Alibaba Cloud Model Studio's current top Max-tier model is `qwen3.7-max`; no 3.8 designation exists in official listings or on HuggingFace. Not added to the catalog.

### Research Citations
- arXiv:2606.22528 — compaction/governance decay (tool-call violations 0%→30-59%)
- arXiv:2606.02835 — overthinking harm, early-stop benefit
- arXiv:2606.13603 — CoT commitment boundary, epiphenomenal reasoning
- arXiv:2605.07127 — Position Curse (positional retrieval failure)
- arXiv:2605.12922 — multi-turn goal drift as attention-reachability failure
- ICML 2026 (Zhejiang/Alibaba) — adversarial overthinking DoS

## [5.1] - 2026-03-05

### Claude Code Skill Package

Packaged the knowledge base as an installable Claude Code skill using progressive disclosure — a single entry file routes by intent and loads only the references a given task needs. Documented retroactively; shipped the same day as 5.0.

### Added
- **`skills/prompt-context-engineer/SKILL.md`** — four operating modes (CRAFT / OPTIMIZE / REVIEW / ADAPT), technique decision tree, model-specific prompt templates, and a model selection guide
- **Anti-pattern scanner (AP-1 – AP-10)** — severity-rated detection signals run against every prompt in all four modes
- **16 progressive-disclosure reference files** — per-provider deep dives (Anthropic, OpenAI, Gemini, xAI, China labs), task patterns (code, analysis, content, data), cross-cutting patterns (agentic, safety, evaluation), the full template collection, and research-tool guides
- **`scripts/build_context.py`** — context pack assembler with `--model` / `--task` shorthand
- **`scripts/lint_refs.py`** — frontmatter and outdated-term validation across reference files

### Note
The packaged skill targets the 4.6-era model set (Claude 4.6, GPT-5.x, Gemini 3.1). The knowledge base modules moved on in 6.0; the skill has not yet been resynced.

## [5.0] - 2026-03-05

### Major Rewrite

Complete rewrite consolidating 12 files to 11, eliminating ~1,800 lines of redundancy while preserving all unique content. Updated all models to March 2026 data.

### New Modules
- **03-model-catalog_v5.md** -- Centralized model specs, pricing, and selection guide (previously scattered across 00, 01, 03)
- **08-gpt5-practices_v5.md** -- Dedicated GPT-5 module (Claude and Gemini already had theirs)

### Merges
- **06-claude-practices_v5.md** -- Merged v4 07 (Claude Research) + v4 11 (Claude Best Practices) into single source
- **07-gemini-practices_v5.md** -- Merged v4 06 (Gemini Deep Research, 49 lines) + v4 08 (Gemini 3 Pro) into single source

### Model Updates
| Provider | v4.2 (Jan 2026) | v5.0 (Mar 2026) |
|----------|-----------------|-----------------|
| Anthropic | Claude 4.5 family | Opus 4.6, Sonnet 4.6, Haiku 4.5 |
| OpenAI | GPT-5.2 flagship | GPT-5.2 Thinking (SOTA), GPT-5.3 Instant |
| Google | Gemini 3 Pro | Gemini 3.1 Pro (#1 benchmarks), 3.1 Flash-Lite |
| xAI | Grok 4.1 Fast | Grok 4.20 Beta 2 |
| DeepSeek | V3.2 | V3.2 (V4 imminent) |
| Zhipu | GLM 4.6 | GLM-5 (744B params) |
| Alibaba | Qwen 3 Max | Qwen 3.5 (201 languages) |
| Moonshot | Kimi K2 | Kimi K2.5 (Agent Swarm) |
| Meta | (missing) | Llama 4 Scout/Maverick |
| Mistral | (missing) | Mistral Large 3 |

### New Content
- **Adaptive thinking** (Claude 4.6) -- model decides when/how much to reason
- **Context compaction** -- server-side summarization for infinite conversations
- **Agent coordination as table stakes** -- multi-agent standard across providers
- **Prompt caching** section (01) -- cache-friendly prompt structure
- **Structured outputs / constrained decoding** (01) -- JSON mode across providers
- **Cost optimization / token economics** (03) -- pricing tiers, batch API, caching savings
- **Multimodal prompt injection** (09) -- image-based injection, cross-modal attacks
- **Llama 4 Scout/Maverick** entries (03)
- **Mistral Large 3** entry (03)

### Removed
- **GPT-5 Mini** -- does not exist, removed
- **~1,800 lines of duplicated content** -- each topic has ONE canonical home
- **Old v4 files** -- replaced by v5 equivalents

### Redundancy Elimination (Single Source of Truth)
| Topic | Canonical Home | Previously Duplicated In |
|-------|---------------|-------------------------|
| Model specs/pricing | 03 | 00, 01, 03 |
| Anti-patterns | 02 | 00, 01, 02, 03, 05 |
| Thinking modes | 01 | 01, 02, 03 |
| Context engineering | 01 | 01, 03 |
| Tool descriptions | 10 | 03, 05, 09 |
| Claude comparison table | 06 | 00, 07, 11 |
| Few-shot guidance | 02 | 01, 02, 03 |
| Conversational fluff | 02 | 00, 02, 03 |

### Fixed
- GLM model version inconsistency (was 4.5 in one place, 4.6 in another)
- DeepSeek description inconsistency
- Few-shot count recommendations inconsistency (now consistent: 0-1 for most, 2-3 for Gemini)

---

## [4.2] - 2026-01-17

### Added

#### New Module
- **11-Claude-4.x-Best-Practices_v4.md** - Official Anthropic guidelines for Claude 4.x models
  - Long-horizon reasoning and state tracking patterns
  - Context awareness and multi-window workflows
  - State management best practices (JSON vs unstructured)
  - Communication style guidance (more direct, less verbose)
  - Tool usage patterns (proactive vs conservative)
  - Tool triggering fixes for Opus 4.5 overtriggering
  - Output format control techniques
  - Thinking sensitivity guidance ("think" word avoidance)
  - Interleaved thinking patterns
  - Agentic coding patterns (code exploration, hallucination minimization)
  - Overengineering prevention for Opus 4.5
  - Frontend design aesthetics (avoiding "AI slop")
  - Research and information gathering patterns
  - Native subagent orchestration
  - Vision capabilities improvements
  - Migration checklist

#### Enhanced Documentation
- **00-prompt-engineer.md** - Expanded Claude 4.x Cheat Sheet
- **09-agentic-prompting-patterns_v4.md** - Multi-Context Window Workflows
- **07-Sonnet-4.5-Research_v4.md** - Agentic Coding Patterns
- **08-Gemini-3.0-Pro-Preview_v4.md** - Official Google Guidelines (January 2026)

### Changed
- Version bumped from 4.1 to 4.2

---

## [4.1] - 2026-01-07

### Added

#### New Modules
- **09-agentic-prompting-patterns_v4.md** - AI agent development
- **10-safety-guardrails_v4.md** - Production safety patterns

#### Enhanced Evaluation Framework (04)
- Prompt Regression Testing, CI/CD Pipelines, LLM-as-Judge, Judge Calibration

#### Quick Reference Cards (00)
- Claude 4.x, Gemini 3.x, GPT-5.x cheat sheets, technique decision tree

---

## [4.0] - 2025-12

### Added
- Complete rewrite for 2025 reasoning models
- Context engineering paradigm documentation
- Model-specific optimization guides
- Thinking modes and reasoning traces documentation

### Changed
- Deprecated explicit CoT for reasoning models
- Reduced few-shot recommendations
- Updated all model specs to December 2025

### Removed
- Legacy prompting techniques superseded by native reasoning

---

## [3.0] - Previous

- Initial comprehensive prompt engineering guide
- Speculative model information (pre-release)
