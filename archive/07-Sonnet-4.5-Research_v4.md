# Claude Sonnet 4.x Research Tool: Quick Reference (v4 - Updated 2025)

## Core Functionality
The Claude Research tool is an autonomous, user-facing feature that conducts multi-step investigations by performing 5-20+ progressive web searches. It synthesizes findings into comprehensive, citation-backed reports, transforming Claude from a simple chatbot into a research assistant. Claude 4.x models (Opus 4.5, Sonnet 4.5) bring significant improvements in reasoning, instruction-following, and native agentic capabilities.

## Activation Requirements
- **User-Facing Only:** Available exclusively in the Claude.ai web/desktop/mobile interfaces, **not accessible via API**.
- **Paid Plans:** Requires a Claude Pro, Max, Team, or Enterprise subscription. Not available on the free tier.
- **Manual Toggle:** Users must enable web search in settings, then click the "Research" button at the bottom left of the chat interface to activate it for a session.
- **Admin Approval:** For Team/Enterprise plans, an administrator must first enable web search at the organization level.

## Claude 4.x Best Practices for Research

### 1. Be Explicit with Instructions
- **Don't assume:** Claude 4.x follows instructions literally. Be precise about what you want.
- **Bad:** "Research React."
- **Good:** "Research React. Compare it to Vue and Svelte on: 1) Performance benchmarks from 2024-2025, 2) Developer experience metrics, 3) Ecosystem maturity. Present findings in a comparison table with citations."

### 2. Provide Context and Motivation
- **Explain why:** Sharing the goal or background behind your request helps Claude prioritize relevant information.
- **Example:** "I'm evaluating frontend frameworks for a new enterprise SaaS product. Research React, Vue, and Svelte. Focus on: performance, TypeScript support, enterprise adoption, and long-term maintenance. We need to make a decision by next week."

### 3. Use Concise Communication
- **Get to the point:** Claude 4.x prefers direct, efficient communication over verbose, persuasive language.
- **Avoid:** "I would really appreciate it if you could perhaps take a look at..."
- **Use:** "Research the following..."

### 4. Leverage Long-Horizon Reasoning
- **Multi-step tasks:** Claude 4.x excels at tasks requiring planning, state tracking, and sequential reasoning across many steps.
- **Example:** "Research cloud infrastructure providers. Phase 1: Identify top 5 providers. Phase 2: For each, find pricing for medium-scale deployments. Phase 3: Compare performance benchmarks. Phase 4: Synthesize into a recommendation matrix."

### 5. Structure with XML Tags
- **Use `<task>`, `<context>`, `<requirements>`, `<output_format>`:** This significantly improves instruction-following.
- **Example:**
  ```
  <context>
  I'm building a ML pipeline for real-time fraud detection. We need a vector database.
  </context>

  <task>
  Research vector databases: Pinecone, Weaviate, Milvus, Qdrant.
  </task>

  <requirements>
  - Focus on latency, throughput, and scalability for real-time use
  - Find pricing for 10M vectors, 512 dimensions
  - Include developer experience and Python SDK quality
  </requirements>

  <output_format>
  1. Executive summary (3-5 sentences)
  2. Comparison table
  3. Recommendation with rationale
  </output_format>
  ```

### 6. Parallel Tool Calling
- **Native capability:** Claude 4.x can make multiple tool calls simultaneously, speeding up research significantly.
- **Prompt for it:** "Research these topics in parallel: AI safety regulations in the EU, US AI policy landscape, and Chinese AI governance. Synthesize into a global comparison."

### 7. Extended Thinking
- **When to use:** For complex, nuanced topics that benefit from visible reasoning chains.
- **How to activate:** "Use extended thinking to research [topic]. Show your reasoning process."
- **Important:** Do NOT use phrases like "think step-by-step" when extended thinking is disabled—this can degrade performance. Only use when you specifically want the extended thinking feature.

### 8. Context Awareness for Multi-Window Workflows
- **Claude remembers:** In Claude.ai, the model has context awareness across Projects and long conversations.
- **Leverage it:** "Continue the research from our previous conversation about database options. Now focus on cost optimization strategies."

### 9. Steer Proactive vs. Conservative Action
- **You control it:** Claude 4.x can be steered to be more proactive or more conservative.
- **Proactive:** "Be proactive. If you need more information to answer comprehensively, search for it without asking me first."
- **Conservative:** "Ask me before making assumptions. If the research requires clarification, pause and ask questions."

### 10. Verify with the "Sources Method"
- **~17% hallucination rate:** Independent research shows Claude can still hallucinate facts, even with citations.
- **3-Layer Verification:**
  1. **Check source quality:** Authority, publication date, relevance.
  2. **Cross-reference claims:** Ask Claude to find multiple sources for the same claim.
  3. **Manual validation:** For critical numbers, dates, and names, click through to the original source and verify.
- **Quote-First Method:** For long documents, ask Claude to extract direct quotes first, then analyze using only those quotes.

### 11. Subagent Orchestration
- **Native capability:** Claude 4.x can naturally orchestrate multi-step workflows that feel like coordinating subagents.
- **Example:** "Research this topic in three phases. Phase 1: Identify key sources and create a reading list. Phase 2: Summarize each source. Phase 3: Synthesize findings into a cohesive report. Execute each phase sequentially and show me the output after each."

## Effective Prompt Patterns

### Pattern 1: Research + Analysis
```
<context>
We're evaluating whether to migrate from Postgres to a NewSQL database.
</context>

<task>
Research CockroachDB and TiDB.
</task>

<requirements>
1. Migration complexity from Postgres
2. Performance characteristics for OLTP workloads
3. Cost comparison for 5TB dataset
4. Production incident reports and reliability track record
</requirements>

<output_format>
- Migration feasibility section
- Performance comparison table
- Cost analysis
- Risk assessment
- Final recommendation
</output_format>
```

### Pattern 2: Iterative Refinement
```
Initial: "Research Rust web frameworks."
Follow-up 1: "Focus on Actix and Axum. Compare async runtime performance."
Follow-up 2: "Now find production case studies for each."
Follow-up 3: "Which one is better for a team familiar with Express.js?"
```

### Pattern 3: Parallel Investigation
```
Research these three topics in parallel:
1. Latest developments in quantized LLMs (2024-2025)
2. On-device inference frameworks for mobile
3. Regulatory requirements for AI in healthcare (EU, US)

After researching, identify connections between these topics and synthesize into a single strategic brief.
```

## Key Capabilities
- **Agentic Multi-Step Search:** Autonomously conducts multiple searches that build on each other, exploring topics from various angles to synthesize information rather than just aggregating it.
- **Real-Time Information:** Accesses current data beyond its training cutoff (January 2025) via web search.
- **Workspace & MCP Integration:** Connects to Google Workspace (Gmail, Docs) and a vast ecosystem of third-party apps (Jira, Zapier, Stripe, etc.) via the Model Context Protocol (MCP) for combined internal/external research.
- **Coding Synergy:** Integrates with Sonnet 4.5's SOTA coding abilities to research current API documentation and technical best practices while writing code.
- **Extended Thinking:** Can be prompted to use up to 64,000 tokens of visible reasoning for deeper analysis on complex topics, improving transparency and rigor.
- **Native Parallel Tool Calling:** Executes multiple tool calls simultaneously for faster research.
- **Subagent-Like Orchestration:** Naturally handles multi-phase workflows without explicit orchestration code.

## Critical Limitations
- **No API Access:** The agentic Research feature cannot be called programmatically; developers must build similar functionality manually using basic tool use.
- **Beta Status & Rate Limits:** The feature is in early beta, and each research session consumes usage limits much faster than standard chat.
- **Hallucination Risk:** Independent research shows ~17% hallucination rates on factual questions. Citations are a starting point for verification, not a guarantee of accuracy.
- **"Context Anxiety":** The model may take shortcuts or leave tasks incomplete when it believes it's approaching its context limit, even if it's not. (Less pronounced in Claude 4.x but still present.)
- **Niche Topics:** Struggles with highly specialized domains (legal, medical) and topics not well-represented in Wikipedia-like sources.

## Best Practices
- **Use Conversational Refinement:** Start with a focused prompt, then use follow-up questions to deepen or expand the research. Iteration is more effective than a single perfect prompt.
- **Chain Prompts for Complexity:** Break complex research into a sequence of smaller, interconnected prompts to prevent the model from dropping steps.
- **Verify with the "Quote-First" Method:** For long documents, first ask Claude to extract direct quotes relevant to your topic, then ask it to perform analysis using only those quotes. This grounds the response in actual text.
- **Implement a 3-Layer Verification:** 1) Check source quality (authority, date). 2) Cross-reference claims with follow-up questions. 3) Manually validate specific numbers, dates, and names against original sources.
- **Be explicit about reasoning needs:** If you want extended thinking, request it. If you don't, avoid phrases like "think step-by-step."
- **Provide motivation:** Share the "why" behind your research request to help Claude prioritize relevant information.

## Agentic Coding Patterns (Official Anthropic Guidelines - January 2026)

### Encourage Code Exploration
Opus 4.5 can be overly conservative. Add explicit instructions:

```xml
<code_exploration>
ALWAYS read and understand relevant files before proposing code edits. Do not speculate about code you have not inspected. If the user references a specific file/path, you MUST open and inspect it before explaining or proposing fixes. Be rigorous and persistent in searching code for key facts.
</code_exploration>
```

### Minimize Hallucinations

```xml
<investigate_before_answering>
Never speculate about code you have not opened. If the user references a specific file, you MUST read the file before answering. Make sure to investigate and read relevant files BEFORE answering questions about the codebase. Never make any claims about code before investigating.
</investigate_before_answering>
```

### Prevent Overengineering (Opus 4.5)

```xml
<avoid_overengineering>
Avoid over-engineering. Only make changes that are directly requested or clearly necessary. Keep solutions simple and focused. Don't add features, refactor code, or make "improvements" beyond what was asked. Don't create helpers or abstractions for one-time operations.
</avoid_overengineering>
```

### Avoid Hard-Coding & Test-Focused Solutions

```xml
<general_solutions>
Write high-quality, general-purpose solutions. Do not hard-code values or create solutions that only work for specific test inputs. Implement the actual logic that solves the problem generally. Tests verify correctness, not define the solution.
</general_solutions>
```

### Tool Triggering (Opus 4.5)
Dial back aggressive language to prevent overtriggering:

| Overtriggers | Balanced |
|--------------|----------|
| `CRITICAL: You MUST use...` | `Use this tool when...` |
| `ALWAYS call this function` | `Call when appropriate` |

## Quick Comparison
- **vs. Gemini Deep Research:** Claude is better at processing very long documents (200k token window) and shows a greater willingness to admit uncertainty. Gemini visits more sources (40-250+ vs. 5-20+) and is cheaper ($20/mo vs. Pro tier pricing).
- **vs. ChatGPT Deep Research:** Claude is often faster and more conversational. ChatGPT may produce more polished reports and asks clarifying questions before starting.
- **Overall:** Claude 4.x's strength lies in its large context window for document analysis, conversational refinement loop, native agentic capabilities, and explicit instruction-following, making it a powerful expert accelerant when combined with rigorous human verification.

## What's New in Claude 4.x (2025)
- **Opus 4.5 Released:** November 2025. Claude Opus 4.5 is the most advanced model, with superior reasoning and instruction-following.
- **Sonnet 4.5 Enhanced:** Improved long-horizon reasoning, state tracking, and parallel tool calling.
- **Native Agentic Workflows:** Subagent-like orchestration without explicit code.
- **Better Instruction-Following:** Requires more explicit, direct communication (less "please," more "do this").
- **Context Awareness:** Enhanced memory and state tracking across multi-turn conversations.
- **Knowledge Cutoff:** January 2025 for all Claude 4.x models.

## Model-Specific Guidance for Claude 4.5 Family

### Shared Across All 4.5 Models

All Claude 4.5 models (Haiku, Sonnet, Opus) share these core characteristics:
- **Be explicit with instructions** - These models follow instructions literally and precisely
- **Add context/motivation** - Claude generalizes from explanations; explaining WHY helps the model prioritize
- **Concise, direct communication style** - Skip persuasive language, get to the point
- **Context awareness & multi-window workflows** - Leverage Projects and conversation history
- **Extended thinking support** - Can be explicitly enabled for deeper reasoning (must request it)
- **Parallel tool execution** - Native capability to call multiple tools simultaneously
- **XML tags for structure** - `<context>`, `<task>`, `<requirements>`, `<output_format>` work exceptionally well

### Model-Specific Differences

| Feature | Haiku 4.5 | Sonnet 4.5 | Opus 4.5 |
|---------|-----------|------------|----------|
| **Effort parameter** | No | No | **YES** (only model with this feature) |
| **Thinking block preservation** | No | No | **YES** (automatic preservation) |
| **Programmatic tool calling** | No | Beta | Beta |
| **Tool search (100+ tools)** | No | Beta | Beta |
| **Context window** | 200K | 200K / **1M (beta)** | 200K |
| **Best use case** | High-volume, sub-agents | Coding, complex agents | Maximum intelligence tasks |

### Haiku 4.5 Specific Guidance

**Key Characteristics:**
- **FIRST Haiku model with extended thinking support** - A major capability upgrade
- **Near-frontier intelligence at fastest speed and lowest cost** - Exceptional value proposition
- **Ideal for sub-agent architectures and high-volume deployments** - When you need many parallel agents
- **Best for real-time applications requiring speed** - Lowest latency in the 4.5 family

**Prompting Tips:**
- Keep instructions concise but explicit
- Prioritize bulletized constraints for clarity
- Request explicit validation summaries to ensure accuracy
- Leverage for tasks where speed matters more than absolute peak intelligence

### Sonnet 4.5 Specific Guidance

**Key Characteristics:**
- **MOST AGGRESSIVE parallel tool calling** - Can bottleneck system performance if not managed
- **Extended autonomous operation capability** - Can work independently for hours
- **Best coding performance when extended thinking is enabled** - SOTA for software development
- **1M context window available in beta** - 5x larger than standard 200K

**Prompting Tips:**
- Design prompts assuming multiple simultaneous tool calls
- For coding tasks, explicitly enable extended thinking for best results
- Monitor system resources when deploying at scale (parallel calls can overwhelm)
- Leverage the 1M context window (beta) for massive document analysis
- Excellent for multi-phase agentic workflows that need sustained focus

### Opus 4.5 Specific Guidance

**Key Characteristics:**
- **Most sensitive to "think" when extended thinking disabled** - Use "consider", "evaluate", "analyze" instead
- **May OVERTRIGGER on tools** - Dial back aggressive language like "CRITICAL: You MUST use..." to normal "Use this tool when..."
- **Tendency to OVERENGINEER solutions** - Add explicit constraints like "Keep solutions minimal", "Don't add features beyond what was asked"
- **Supports effort parameter** - Unique feature: "low" (token-efficient), "medium" (balanced), "high" (thorough)

**Prompting Tips:**
- Avoid the word "think" unless extended thinking is enabled (use alternatives)
- Use measured, calm language for tool instructions - avoid ALL CAPS or excessive emphasis
- Explicitly constrain scope: "Provide a minimal solution", "Only implement what was requested"
- Leverage the effort parameter:
  - `effort: "low"` for quick, efficient responses
  - `effort: "medium"` for balanced quality/efficiency (default)
  - `effort: "high"` for maximum thoroughness and detail
- Best for tasks requiring absolute peak intelligence and reasoning depth
- Ideal for complex research, strategic analysis, and sophisticated problem-solving

### Choosing the Right Model

**Use Haiku 4.5 when:**
- You need fast responses at scale
- Cost optimization is critical
- Building sub-agent architectures
- Real-time applications

**Use Sonnet 4.5 when:**
- Coding is the primary task
- You need extended autonomous operation
- Parallel tool use is valuable
- Working with large documents (1M context beta)

**Use Opus 4.5 when:**
- Maximum intelligence is required
- Complex reasoning and analysis needed
- You need fine-grained control (effort parameter)
- Quality matters more than speed/cost

**For Research Tasks Specifically:**
- **Haiku 4.5**: Quick fact-finding, simple queries, high-volume research
- **Sonnet 4.5**: Standard research tasks, technical documentation, code-related research
- **Opus 4.5**: Deep analysis, strategic research, complex synthesis requiring maximum reasoning
