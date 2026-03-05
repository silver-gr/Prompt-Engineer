# Changelog

All notable changes to the Prompt Engineering Knowledge Base are documented in this file.

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
