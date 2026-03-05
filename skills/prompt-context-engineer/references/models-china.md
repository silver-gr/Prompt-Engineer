# Chinese Frontier Models (March 2026)

## Models

| Model | Provider | Context | Strengths | Use For |
|-------|----------|---------|-----------|---------|
| **DeepSeek V3.2** | DeepSeek | 128K | Cost-effective, strong coding, MoE | Budget coding, general tasks |
| **GLM-5** | Zhipu AI | 128K | 744B params, multilingual | Chinese-first, enterprise |
| **Qwen 3.5** | Alibaba | 128K | 201 languages, open weights | Multilingual, self-hosted |
| **Kimi K2.5** | Moonshot | 128K | Agent Swarm, long context | Agent orchestration, research |

## DeepSeek V3.2

Best cost-to-performance ratio among frontier models.
- Strong at code generation and mathematical reasoning
- MoE architecture (efficient inference)
- Markdown formatting preferred
- V4 imminent -- expect major capability jump

## Qwen 3.5

Best multilingual coverage (201 languages).
- Open weights available for self-hosting
- Strong reasoning capabilities
- Good for non-English content generation

## Kimi K2.5

Best for agent orchestration among Chinese models.
- Agent Swarm: native multi-agent coordination
- Strong long-context performance
- Good for research and analysis tasks

## GLM-5

Largest Chinese model (744B parameters).
- Strong bilingual (Chinese/English) performance
- Good for enterprise and finance tasks
- Define numeric assumptions explicitly for financial analysis

## General Guidance

- All support Markdown formatting
- Direct instructions work best (similar to GPT-5 approach)
- Most support function/tool calling
- JSON mode available on most
- For bilingual output, include a glossary for key terms
- Test zero-shot first, add examples only if needed
