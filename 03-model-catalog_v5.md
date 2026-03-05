# Model Catalog & Selection Guide (March 2026)

This is the **single source of truth** for all model specifications, capabilities, and selection guidance. Other modules reference this catalog but do not duplicate model data.

---

## Frontier Landscape (March 2026)

| Provider | Model | Context | Output | Release | Key Strength |
|----------|-------|---------|--------|---------|--------------|
| Anthropic | Opus 4.6 | 200K | 32K | Feb 2026 | Adaptive thinking, peak reasoning |
| Anthropic | Sonnet 4.6 | 200K / 1M (beta) | 32K | Feb 2026 | Best coding, aggressive parallelism |
| Anthropic | Haiku 4.5 | 200K | 16K | Sep 2025 | Speed + quality, sub-agents |
| OpenAI | GPT-5.2 Thinking | 128K | 32K | Dec 2025 | SOTA chatbot, deep reasoning |
| OpenAI | GPT-5.3 Instant | 128K | 16K | Mar 2026 | Ultra-low latency, cost-efficient |
| OpenAI | GPT-5.1 | 128K | 16K | Oct 2025 | Flexible reasoning modes |
| Google | Gemini 3.1 Pro | 1M | 64K | Feb 2026 | #1 benchmarks, massive context |
| Google | Gemini 3.1 Flash-Lite | 1M | 32K | Mar 2026 | Real-time, cost-optimized |
| Google | Gemini 2.5 Pro | 1M | 64K | 2025 | Multimodal, adaptive thinking |
| xAI | Grok 4.20 Beta 2 | 2M | 32K | Feb 2026 | Largest context, real-time data |
| DeepSeek | V3.2 | 512K | 32K | 2025 | Cost-effective reasoning |
| Zhipu | GLM-5 | 512K | 32K | Feb 2026 | 744B params, bilingual |
| Alibaba | Qwen 3.5 | 256K | 32K | Feb 2026 | 201 languages |
| Moonshot | Kimi K2.5 | 2M | 64K | Jan 2026 | Agent Swarm orchestration |
| Meta | Llama 4 Maverick | 1M | 32K | Mar 2026 | Open-weight, MoE architecture |
| Meta | Llama 4 Scout | 1M | 16K | Mar 2026 | Open-weight, efficient |
| Mistral | Large 3 | 256K | 32K | Feb 2026 | European sovereignty, multilingual |

---

## 1. Anthropic (Claude 4.6 Family)

### Claude Opus 4.6

**Released**: February 5, 2026 | **Model ID**: `claude-opus-4-6`

- **Context Window**: 200K tokens
- **Key Feature**: **Adaptive thinking** -- model autonomously decides when and how deeply to reason, eliminating the need for explicit thinking mode toggling
- **Strengths**: Peak reasoning, long-horizon task handling, exceptional state tracking, nuanced instruction following
- **Thinking**: Adaptive (automatic), extended thinking (explicit), interleaved thinking after tool use
- **Effort Parameter**: `"low"` | `"medium"` | `"high"` (unique to Opus)

**Prompting Quick-Reference**:
- Be EXPLICIT -- Opus follows instructions precisely, needs clear direction
- Explain WHY, not just WHAT -- Claude generalizes from explanatory context
- XML tags for structure (`<context>`, `<task>`, `<constraints>`, `<output_format>`)
- Use "consider", "evaluate", "analyze" instead of "think" when extended thinking disabled
- Dial back aggressive language -- Opus may overtrigger on tools with CAPS/emphasis
- Constrain scope explicitly -- tendency to overengineer ("Keep solutions minimal")

**Watch For**:
- Tool overtriggering with aggressive language ("CRITICAL: MUST use..." -> "Use when...")
- Overengineering (add "Don't add features beyond what was asked")
- Sensitive to "think" word when extended thinking disabled

### Claude Sonnet 4.6

**Released**: February 17, 2026 | **Model ID**: `claude-sonnet-4-6`

- **Context Window**: 200K tokens / 1M (beta)
- **Key Feature**: Best-in-class coding with adaptive thinking, most aggressive parallel tool calling
- **Strengths**: SOTA software development, agentic workflows, extended autonomous operation (hours of independent work)
- **Thinking**: Adaptive (automatic), extended thinking (explicit)

**Prompting Quick-Reference**:
- Same core principles as Opus -- explicit instructions, explain motivation, XML tags
- Design prompts assuming multiple simultaneous tool calls
- Enable extended thinking for best coding performance
- Monitor system resources at scale (parallel calls can overwhelm)
- Excellent for multi-phase agentic workflows needing sustained focus

**Watch For**:
- Most aggressive parallel tool calling (can bottleneck systems)
- May need explicit concurrency limits: "Maximum 3 concurrent tool calls"

### Claude Haiku 4.5

**Released**: September 2025 | **Model ID**: `claude-haiku-4-5-20251001`

- **Context Window**: 200K tokens
- **Key Feature**: First Haiku with extended thinking, near-frontier intelligence at lowest cost
- **Strengths**: Fastest in family, exceptional value, ideal for sub-agent architectures

**Prompting Quick-Reference**:
- Keep instructions concise but explicit
- Prioritize bulletized constraints for clarity
- Request explicit validation summaries
- Best for real-time applications requiring speed

### Claude 4.6 Family Comparison

| Feature | Haiku 4.5 | Sonnet 4.6 | Opus 4.6 |
|---------|-----------|------------|----------|
| **Adaptive thinking** | No | Yes | Yes |
| **Effort parameter** | No | No | Yes (only model) |
| **Thinking preservation** | No | Yes | Yes |
| **Programmatic tools** | No | Beta | Beta |
| **Tool search (100+)** | No | Beta | Beta |
| **Context window** | 200K | 200K / 1M (beta) | 200K |
| **Best for** | Sub-agents, high-volume | Coding, complex agents | Peak intelligence |
| **Relative cost** | $ | $$ | $$$$ |

### Key Claude Insight

Claude models excel when you explain WHY you want something, not just WHAT. They generalize from explanatory context. Native parallel tool calling is aggressive -- design prompts assuming multiple simultaneous actions.

**Adaptive thinking** (new in 4.6) means Opus and Sonnet now autonomously decide when to engage deep reasoning, making explicit `/think` commands optional for most tasks. The model allocates reasoning effort proportional to task complexity.

---

## 2. OpenAI (GPT-5.x Family)

### GPT-5.2 Thinking

**Released**: December 2025 | **SOTA for chatbot use**

- **Context Window**: 128K tokens
- **Key Feature**: Deep reasoning mode ("Thinking") that produces the highest-quality conversational responses of any model
- **Strengths**: Top-tier reasoning, cleaner formatting, less verbosity, strongest instruction adherence, excellent tool grounding
- **Reasoning Profiles**: `"light"` | `"balanced"` | `"deep"`

**Prompting Quick-Reference**:
- Keep prompts MINIMAL and direct -- less is more
- Crisp tool descriptions (1-2 sentences)
- Use `reasoning_profile: "deep"` with verification scaffolds for high-assurance tasks
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

**Released**: October 2025

- **Context Window**: 128K tokens
- **Key Feature**: `"none"` reasoning mode for ultra-low-latency; auto-calibrates reasoning depth
- **Strengths**: Flexible reasoning modes, calibrated to prompt difficulty

### GPT-5 (Base)

**Released**: August 2025

- **Context Window**: 128K tokens
- **Key Feature**: Unified flagship, enterprise-grade alignment
- **Strengths**: All benchmarks, video reasoning, biomedical analysis

### Key GPT-5 Insight

Less is more. Agentic persistence reminders are critical at minimal reasoning levels. For coding tasks, avoid over-specification -- the model performs better with cleaner, simpler instructions. Use reasoning profiles to match task complexity rather than prompt engineering tricks.

---

## 3. Google (Gemini 3.1 Family)

### Gemini 3.1 Pro

**Released**: February 19, 2026 | **#1 on major benchmarks**

- **Context Window**: 1M tokens
- **Output**: 64K tokens
- **Key Feature**: Top-ranked reasoning model with massive context, builds on Gemini 3 foundations
- **Thinking**: `thinking_level`: `"low"` | `"high"` (default)

**Prompting Quick-Reference**:
- **Temperature MUST be 1.0** -- lowering causes loops/degraded performance
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

**Released**: March 4, 2026

- **Context Window**: 1M tokens
- **Output**: 32K tokens
- **Key Feature**: Real-time optimized with near-Pro quality at fraction of cost
- **Strengths**: Latency-optimized, rapid iteration, streaming outputs

**Prompting Quick-Reference**:
- Concise task briefs with optional enrichment sections
- Define response schemas to maintain structure at high speed
- Same temperature=1.0 requirement

### Gemini 2.5 Pro / Flash

Still available for production workloads. Same 1M context, adaptive thinking budgets. Being superseded by 3.1 family.

### Key Gemini Insight

Gemini 3.x treats prompts as executable instructions, not conversation. DO NOT use complex prompt engineering from the 2.x era. Use `thinking_level` for reasoning control. Keep temperature at 1.0. Be direct, never persuasive.

**Critical constraint ordering**: Place negative/formatting constraints LAST or they get dropped.

---

## 4. xAI (Grok Family)

### Grok 4.20 Beta 2

**Released**: February 2026

- **Context Window**: 2M tokens (largest available)
- **Key Feature**: Massive context with real-time data integration
- **Strengths**: Live data workflows, tool-use reinforcement, long-context synthesis

**Prompting Quick-Reference**:
- Leverage massive 2M context with layered sectioning
- Clear, direct tool instructions
- Request verification steps for quantitative reasoning
- Structure large contexts with hierarchical headings

### Grok 4.1 Fast / Grok 4 Fast

Earlier iterations with same 2M context. Grok 4 Fast introduced unified reasoning/non-reasoning model.

---

## 5. Chinese Frontier Models

### DeepSeek V3.2

- **Context Window**: 512K tokens
- **Key Feature**: Cost-effective frontier-level reasoning
- **Strengths**: Advanced reasoning, strong coding, bilingual (EN/CN)
- **Status**: V4 release imminent

**Prompting**: Clear, structured prompts. Specify language requirements explicitly.

### GLM-5 (Zhipu AI)

**Released**: February 2026

- **Context Window**: 512K tokens
- **Parameters**: 744B (one of the largest dense models)
- **Key Feature**: Enterprise-grade bilingual reasoning
- **Strengths**: Financial analysis, tool-use reliability, compliance

**Prompting**: Provide bilingual glossaries for multilingual output. Enumerate numerical assumptions for quantitative tasks. Define explicit function-calling payloads.

### Qwen 3.5 (Alibaba)

**Released**: February 2026

- **Context Window**: 256K tokens
- **Key Feature**: 201 language support (broadest multilingual coverage)
- **Strengths**: Strong general capabilities, competitive benchmarks

**Prompting**: Direct, clear instructions with structured context. Specify target language explicitly.

### Kimi K2.5 (Moonshot AI)

**Released**: January 2026

- **Context Window**: 2M tokens
- **Key Feature**: Agent Swarm -- native multi-agent orchestration
- **Strengths**: Exceptional long-context handling, information synthesis, agent coordination

**Prompting**: Leverage ultra-long context for document analysis. Structure information hierarchically. Agent Swarm capabilities enable native multi-agent task decomposition.

---

## 6. Open-Source / Open-Weight Models

### Llama 4 Maverick (Meta)

**Released**: March 2026

- **Context Window**: 1M tokens
- **Architecture**: Mixture of Experts (MoE)
- **Key Feature**: Open-weight model competitive with closed-source frontier
- **Strengths**: Customizable, self-hosted, strong reasoning

**Prompting**: Standard direct instruction patterns. Benefits from structured context similar to Claude/GPT approaches.

### Llama 4 Scout (Meta)

**Released**: March 2026

- **Context Window**: 1M tokens
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

## 7. Model Selection Guide

### By Use Case

| Use Case | Primary Pick | Alternative | Why |
|----------|-------------|-------------|-----|
| **Complex reasoning** | Opus 4.6 | GPT-5.2 Thinking | Peak intelligence, adaptive thinking |
| **Software development** | Sonnet 4.6 | GPT-5.2 Thinking | SOTA coding, extended autonomy |
| **Massive document analysis** | Gemini 3.1 Pro | Grok 4.20 | 1M-2M context windows |
| **Real-time / low latency** | GPT-5.3 Instant | Haiku 4.5 | Ultra-fast responses |
| **High-volume / sub-agents** | Haiku 4.5 | GPT-5.3 Instant | Speed + quality at low cost |
| **Multimodal (text+image+video)** | Gemini 3.1 Pro | Opus 4.6 | Native multimodal processing |
| **Cost-sensitive** | DeepSeek V3.2 | Haiku 4.5 | Frontier quality at low cost |
| **Multilingual (200+ langs)** | Qwen 3.5 | Gemini 3.1 Pro | Broadest language coverage |
| **Agent orchestration** | Sonnet 4.6 | Kimi K2.5 | Parallel tools, Agent Swarm |
| **Self-hosted / open-weight** | Llama 4 Maverick | Mistral Large 3 | Full control, customizable |
| **EU compliance** | Mistral Large 3 | Qwen 3.5 | European sovereignty |
| **Real-time data** | Grok 4.20 | Gemini 3.1 Pro | Live data integration |

### By Budget

| Tier | Models | When to Use |
|------|--------|-------------|
| **Premium** | Opus 4.6, GPT-5.2 Thinking | Maximum quality, complex tasks |
| **Standard** | Sonnet 4.6, Gemini 3.1 Pro | Production workloads, coding |
| **Economy** | Haiku 4.5, GPT-5.3 Instant, Flash-Lite | High-volume, latency-critical |
| **Budget** | DeepSeek V3.2, Llama 4, Mistral Large 3 | Cost-optimized, self-hosted |

---

## 8. Cost Optimization & Token Economics

### Prompt Caching

Most providers offer prompt caching for repeated prefixes:

| Provider | Feature | Savings | How |
|----------|---------|---------|-----|
| Anthropic | Prompt caching | Up to 90% on cached tokens | `cache_control` breakpoints in messages |
| OpenAI | Automatic caching | Up to 50% | Automatic for repeated prefixes |
| Google | Context caching | Up to 75% | Explicit cache creation via API |

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

## 9. Deprecated & Removed Models

| Model | Status | Replacement |
|-------|--------|-------------|
| GPT-4o | Removed from ChatGPT (Aug 2025) | GPT-5.x family |
| GPT-4 | Removed 2025 | GPT-5.x family |
| Claude 4.5 family | Superseded (still available) | Claude 4.6 family |
| Gemini 3.0 Pro | Superseded | Gemini 3.1 Pro |
| Gemini 2.5 Flash | Available but superseded | Gemini 3.1 Flash-Lite |

**Notable removal**: GPT-5 Mini does not exist and was erroneously included in previous versions.

---

## 10. 2026 Paradigm Updates

### Adaptive Thinking (Claude 4.6)

The 4.6 models introduce **adaptive thinking**: the model autonomously decides when and how much to reason, allocating compute proportional to task complexity. This eliminates the need for explicit thinking mode toggling in most cases. Extended thinking (`/think`, `/megathink`, `/ultrathink`) remains available for explicit control.

### Context Compaction

Server-side context summarization enables effectively infinite conversations. When context approaches limits, the system automatically compresses prior messages while preserving key information. Design prompts assuming this capability:
- Save critical state to files/memory before context refreshes
- Don't stop tasks early due to token budget concerns
- Use structured state files (JSON) for data that must survive compaction

### Agent Coordination as Table Stakes

Multi-agent orchestration is now standard across providers:
- **Claude 4.6**: Native parallel tool calling, subagent delegation
- **GPT-5.x**: Tool orchestration with reasoning profiles
- **Gemini 3.1**: Agent-ready with massive context
- **Kimi K2.5**: Native Agent Swarm architecture
- **Llama 4**: Open-weight agent framework support

Design agentic systems assuming the model can coordinate multiple tools and subtasks without explicit orchestration prompts.

---

## References

- [Anthropic Claude 4.6 Documentation](https://docs.anthropic.com)
- [OpenAI GPT-5 Platform Documentation](https://platform.openai.com/docs)
- [Google Gemini 3.1 Prompting Guide](https://ai.google.dev/gemini-api/docs)
- [xAI Grok Documentation](https://docs.x.ai)
- [Meta Llama 4 Model Card](https://llama.meta.com)
- [Mistral Large 3 Documentation](https://docs.mistral.ai)
