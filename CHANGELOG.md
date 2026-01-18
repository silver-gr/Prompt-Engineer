# Changelog

All notable changes to the Prompt Engineering Knowledge Base are documented in this file.

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
  - Opus 4.5 specific guidance (effort parameter, overtriggering fixes)
  - Sonnet 4.5 specific guidance (aggressive parallel calling, 1M context)
  - Explicit behavior request patterns
  - Git state tracking recommendations

- **09-agentic-prompting-patterns_v4.md** - Multi-Context Window Workflows
  - State management patterns (structured vs unstructured)
  - First context window setup
  - Context continuation patterns
  - Complete context usage encouragement
  - Official Anthropic agentic prompt patterns

- **07-Sonnet-4.5-Research_v4.md** - Agentic Coding Patterns
  - Code exploration encouragement
  - Hallucination minimization
  - Overengineering prevention
  - General solution patterns (anti-hardcoding)
  - Tool triggering guidance

### Changed
- Version bumped from 4.1 to 4.2
- Updated module references to include 11-Claude-4.x-Best-Practices_v4.md

---

## [4.1] - 2026-01-07

### Added

#### New Modules
- **09-agentic-prompting-patterns_v4.md** - Comprehensive guide for AI agent development
  - Tool description patterns (crisp 1-2 sentence format)
  - Multi-step planning with goal-oriented prompting
  - Parallel tool calling patterns and concurrency control
  - Error recovery and checkpoint patterns
  - Sub-agent orchestration with context minimization
  - IDE agent patterns (Claude Code, Cursor) including CLAUDE.md best practices
  - Model-specific agentic guidance

- **10-safety-guardrails_v4.md** - Production safety and security patterns
  - Defense-in-depth architecture (5 layers)
  - Prompt injection defense with input isolation
  - Jailbreak resistance patterns (role lock, capability boundaries)
  - Output filtering and format validation
  - PII protection and confidentiality
  - Hallucination guardrails with citation requirements
  - Agentic safety (action confirmation, blast radius limiting)
  - Monitoring and alerting patterns

#### Enhanced Evaluation Framework (04)
- **Prompt Regression Testing** - Golden examples, threshold management, consistency checks
- **Automated CI/CD Pipelines** - Lint, unit test, regression, A/B test, LLM judge stages
- **LLM-as-Judge Patterns** - Judge templates, evaluation criteria sets, multi-judge consensus
- **Judge Calibration** - Bias detection and reliability scoring

#### Quick Reference Cards (00)
- Claude 4.x cheat sheet with XML templates
- Gemini 3.x cheat sheet with temperature requirements
- GPT-5.x cheat sheet with reasoning profiles
- Technique decision tree for model selection

#### Documentation Improvements
- Instruction hierarchy pattern with token allocation table (02)
- Conversational overhead quantification with model-specific impact (03)
- Before/after examples for instruction engineering (01)
- Before/after examples for structured prompts (02)

### Changed
- Version bumped from 4.0 to 4.1
- Updated module references in main file to include 09 and 10
- Updated CLAUDE.md with new architecture overview

---

## [4.0] - 2025-12

### Added
- Complete rewrite for 2025 reasoning models (GPT-5.x, Claude 4.x, Gemini 3.x)
- Context engineering paradigm documentation
- Model-specific optimization guides
- Thinking modes and reasoning traces documentation
- 2025 anti-patterns section

### Changed
- Deprecated explicit CoT for reasoning models
- Reduced few-shot recommendations (max 1-2 examples)
- Updated all model specifications to December 2025

### Removed
- Legacy prompting techniques superseded by native reasoning

---

## [3.0] - Previous

- Initial comprehensive prompt engineering guide
- Speculative model information (pre-release)
