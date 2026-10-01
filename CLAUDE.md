# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a **Prompt Engineering Knowledge Base v6.1** (September 2026 edition) - a comprehensive reference guide documenting modern prompt engineering techniques for frontier AI models (Claude Fable 5.1/Opus 5.5/Sonnet 5.5, GPT-6 Astra/6.1 Sol/Luna, Gemini 3.8 Flash, and 10+ other frontier models).

## Architecture

The repository follows a modular documentation structure (11 files, ~6,200 lines) with a main entry point and supporting modules:

```
00-prompt-engineer.md           # Main entry point (APEX persona, compressed cheat sheets)
                                # Auto-loads 01, 02; references 03-10 on demand
01-foundations_v5               # Context engineering, thinking modes, hallucination mgmt, caching
02-techniques-patterns_v5       # All techniques + ALL anti-patterns (canonical home)
03-model-catalog_v5             # All model specs, pricing, selection guide (single source)
04-evaluation-optimization_v5   # Evaluation, regression testing, CI/CD pipelines, LLM-as-judge
05-domain-applications_v5       # Domain-specific patterns (content, analysis, code, data)
06-claude-practices_v5          # MERGED: Claude Research + Best Practices + agentic coding
07-gemini-practices_v5          # MERGED: Deep Research + Gemini 3.x (3.8 Flash) guidance
08-gpt5-practices_v5            # GPT-5.x + GPT-6 module (reasoning effort, tiers, tools)
09-safety-guardrails_v5         # Injection defense, jailbreak resistance, multimodal injection
10-agentic-patterns_v5          # Tool orchestration, sub-agents, IDE patterns
```

## 2026 Paradigm (Critical Context)

- **Context engineering > prompt engineering** - Focus on WHAT information you provide, not clever phrasing
- **Simpler prompts work BETTER** - Reasoning models have native CoT; explicit step-by-step REDUCES performance
- **Effort parameter** is primary cost lever - defaults differ per model (Opus 5.5 `medium`, most others `high`); mappings are pairwise only (e.g. Opus 5.5 `medium` ≥ Opus 5 `high`) — never port a level across models
- **Adaptive thinking** defaults differ per model (Fable 5/5.1 and Opus 5.5 always-on; Opus 5, Sonnet 5/5.5 on; Opus 4.8 off)
- **Agent coordination is table stakes** - Orchestrator+executor is dominant pattern
- **Compaction is a safety surface** - Silently evicts constraints; re-pin after every compaction
- **Sampling params are dying** - temp/top_p/top_k → 400 on Claude current-gen; formally deprecated on Gemini (ignored on 3.6+, 400 on future generations)

## Model-Specific Key Points

| Model | Critical Setting | Key Technique |
|-------|-----------------|---------------|
| **Claude Opus 5.5** | Thinking always-on (`disabled` → 400), default effort `medium` | Default starting model; shortest outcome + scope prompt; set effort explicitly |
| **Claude Fable 5.1** | Thinking always-on, effort | Escalation model; brief instructions > enumeration; ask for progress updates; no forced `tool_choice` |
| **Claude Sonnet 5.5** | Thinking on, lowest `between_tools` (≤`high`) | Literal instruction following, state scope, add "stop when done" line |
| **Claude 5.1/5.5 (all)** | No prefill, sampling, `budget_tokens`, forced `tool_choice` | Keep history append-only; pass thinking blocks back unchanged |
| **Gemini 3.x** (3.8 Flash top) | OMIT temp/top_p/top_k; no prefill (3.6+) | Direct instructions; persona + output format at top, question last |
| **GPT-6** (Astra › 6.1 Sol › Luna) | `reasoning.effort` (enum is PER-MODEL; Astra and 6.1 Sol reject `none`) | Outcome-first prompts; Astra: define completion, calibrate testing |
| **GPT-5.x** | `reasoning.effort` (enum is PER-MODEL) | Outcome-first minimal prompts, XML tags recommended |

## Anti-Patterns to Avoid

- Explicit CoT ("Let's think step by step") with reasoning models **when thinking is enabled** (still valid as a fallback when thinking is off)
- "Think harder"/"keep going" - overthinking corrupts correct answers
- Verification instructions for Opus 5/GPT-6 Astra (self-verify; cost, no gain) — not Fable 5/5.1, whose guidance asks for periodic self-checks on long runs
- Asking Fable 5/5.1, Opus 5.5 or Sonnet 5.5 to echo reasoning (triggers a billed reasoning_extraction refusal)
- Excessive few-shot examples (>5 = warning; Anthropic recommends 3-5 diverse examples in `<example>` tags) or examples that demo reasoning rather than output format
- Conversational padding ("please", "kindly") - especially harmful for Gemini
- Over-prompting GPT-5.x/GPT-6/Fable 5.x (less is more)
- Setting temperature/top_p/top_k on Claude current-gen (→ 400) or Gemini (ignored on 3.6+, looping on older 3.x)
- Offset-from-end references ("second-to-last") - Position Curse

## File Relationships

The main prompt (`00-prompt-engineer.md`) uses `@` syntax to auto-load core modules:
```
@~/.claude/commands/01-foundations_v5.md
@~/.claude/commands/02-techniques-patterns_v5.md
```

Files are designed as Claude Code custom commands when placed in `~/.claude/commands/`.

<!-- rtk-instructions v2 -->
# RTK (Rust Token Killer) - Token-Optimized Commands

## Golden Rule

**Always prefix commands with `rtk`**. If RTK has a dedicated filter, it uses it. If not, it passes through unchanged. This means RTK is always safe to use.

**Important**: Even in command chains with `&&`, use `rtk`:
```bash
# ❌ Wrong
git add . && git commit -m "msg" && git push

# ✅ Correct
rtk git add . && rtk git commit -m "msg" && rtk git push
```

## RTK Commands by Workflow

### Build & Compile (80-90% savings)
```bash
rtk cargo build         # Cargo build output
rtk cargo check         # Cargo check output
rtk cargo clippy        # Clippy warnings grouped by file (80%)
rtk tsc                 # TypeScript errors grouped by file/code (83%)
rtk lint                # ESLint/Biome violations grouped (84%)
rtk prettier --check    # Files needing format only (70%)
rtk next build          # Next.js build with route metrics (87%)
```

### Test (90-99% savings)
```bash
rtk cargo test          # Cargo test failures only (90%)
rtk vitest run          # Vitest failures only (99.5%)
rtk playwright test     # Playwright failures only (94%)
rtk test <cmd>          # Generic test wrapper - failures only
```

### Git (59-80% savings)
```bash
rtk git status          # Compact status
rtk git log             # Compact log (works with all git flags)
rtk git diff            # Compact diff (80%)
rtk git show            # Compact show (80%)
rtk git add             # Ultra-compact confirmations (59%)
rtk git commit          # Ultra-compact confirmations (59%)
rtk git push            # Ultra-compact confirmations
rtk git pull            # Ultra-compact confirmations
rtk git branch          # Compact branch list
rtk git fetch           # Compact fetch
rtk git stash           # Compact stash
rtk git worktree        # Compact worktree
```

Note: Git passthrough works for ALL subcommands, even those not explicitly listed.

### GitHub (26-87% savings)
```bash
rtk gh pr view <num>    # Compact PR view (87%)
rtk gh pr checks        # Compact PR checks (79%)
rtk gh run list         # Compact workflow runs (82%)
rtk gh issue list       # Compact issue list (80%)
rtk gh api              # Compact API responses (26%)
```

### JavaScript/TypeScript Tooling (70-90% savings)
```bash
rtk pnpm list           # Compact dependency tree (70%)
rtk pnpm outdated       # Compact outdated packages (80%)
rtk pnpm install        # Compact install output (90%)
rtk npm run <script>    # Compact npm script output
rtk npx <cmd>           # Compact npx command output
rtk prisma              # Prisma without ASCII art (88%)
```

### Files & Search (60-75% savings)
```bash
rtk ls <path>           # Tree format, compact (65%)
rtk read <file>         # Code reading with filtering (60%)
rtk grep <pattern>      # Search grouped by file (75%)
rtk find <pattern>      # Find grouped by directory (70%)
```

### Analysis & Debug (70-90% savings)
```bash
rtk err <cmd>           # Filter errors only from any command
rtk log <file>          # Deduplicated logs with counts
rtk json <file>         # JSON structure without values
rtk deps                # Dependency overview
rtk env                 # Environment variables compact
rtk summary <cmd>       # Smart summary of command output
rtk diff                # Ultra-compact diffs
```

### Infrastructure (85% savings)
```bash
rtk docker ps           # Compact container list
rtk docker images       # Compact image list
rtk docker logs <c>     # Deduplicated logs
rtk kubectl get         # Compact resource list
rtk kubectl logs        # Deduplicated pod logs
```

### Network (65-70% savings)
```bash
rtk curl <url>          # Compact HTTP responses (70%)
rtk wget <url>          # Compact download output (65%)
```

### Meta Commands
```bash
rtk gain                # View token savings statistics
rtk gain --history      # View command history with savings
rtk discover            # Analyze Claude Code sessions for missed RTK usage
rtk proxy <cmd>         # Run command without filtering (for debugging)
rtk init                # Add RTK instructions to CLAUDE.md
rtk init --global       # Add RTK to ~/.claude/CLAUDE.md
```

## Token Savings Overview

| Category | Commands | Typical Savings |
|----------|----------|-----------------|
| Tests | vitest, playwright, cargo test | 90-99% |
| Build | next, tsc, lint, prettier | 70-87% |
| Git | status, log, diff, add, commit | 59-80% |
| GitHub | gh pr, gh run, gh issue | 26-87% |
| Package Managers | pnpm, npm, npx | 70-90% |
| Files | ls, read, grep, find | 60-75% |
| Infrastructure | docker, kubectl | 85% |
| Network | curl, wget | 65-70% |

Overall average: **60-90% token reduction** on common development operations.
<!-- /rtk-instructions -->