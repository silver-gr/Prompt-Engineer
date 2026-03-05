# Claude Practices (Anthropic, March 2026)

This module merges Claude Research tool guidance and official Anthropic best practices into a single reference. It is the **canonical home** for Claude-specific comparison tables, agentic XML blocks, and model-specific guidance.

> **Model specs**: See 03-model-catalog_v5.md for Claude 4.6 family data.
> **Anti-patterns**: See 02-techniques-patterns_v5.md (canonical).
> **Agentic patterns**: See 10-agentic-patterns_v5.md for general agent design.

---

## 1. General Principles

### 1.1 Be Explicit with Instructions

Claude 4.6 follows instructions precisely. "Above and beyond" behavior requires explicit requests.

**Less effective**: `Create an analytics dashboard`

**More effective**: `Create an analytics dashboard. Include as many relevant features and interactions as possible. Go beyond the basics to create a fully-featured implementation.`

### 1.2 Explain WHY, Not Just WHAT

Claude generalizes from explanations. Providing context or motivation behind instructions significantly improves performance.

**Less effective**: `NEVER use ellipses`

**More effective**: `Your response will be read aloud by a text-to-speech engine, so never use ellipses since the engine won't know how to pronounce them.`

### 1.3 Be Vigilant with Examples

Claude 4.6 pays close attention to details and examples. Ensure examples align with desired behaviors and minimize undesired ones. Inconsistent examples cause inconsistent outputs.

### 1.4 Concise, Direct Communication

Claude 4.6 prefers direct, efficient communication. Skip persuasive language, get to the point. The models are more direct and conversational themselves -- less verbose, fact-based progress reports, less self-celebratory.

If you want summaries during tool use:
```
After completing a task that involves tool use, provide a quick summary of the work you've done.
```

---

## 2. Adaptive Thinking (New in 4.6)

Claude 4.6 (Opus and Sonnet) introduces **adaptive thinking**: the model autonomously decides when and how deeply to reason, allocating compute proportional to task complexity.

### Thinking Modes

| Mode | Trigger | Use Case |
|------|---------|----------|
| **Adaptive** (default) | Automatic | Most tasks -- model decides depth |
| **Extended** | `/think`, `/megathink`, `/ultrathink` | Explicit deep reasoning request |
| **Interleaved** | After tool results | Reflection on tool output |

### Thinking Sensitivity (Opus 4.6)

When extended thinking is **disabled**, Opus is sensitive to the word "think":

| Avoid | Use Instead |
|-------|-------------|
| "think about" | "consider" |
| "think through" | "evaluate" |
| "think carefully" | "analyze" |
| "thinking" | "reasoning" |

### Interleaved Thinking

Guide reflection after tool use:
```
After receiving tool results, carefully reflect on their quality and determine
optimal next steps before proceeding. Use your reasoning to plan and iterate
based on this new information, then take the best next action.
```

---

## 3. Long-Horizon Reasoning & State Tracking

Claude 4.6 excels at long-horizon reasoning with exceptional state tracking across extended sessions.

### 3.1 Context Awareness

Claude tracks its remaining token budget. For agent harnesses with context compaction:

```xml
<context_management>
Your context window will be automatically compacted as it approaches its limit,
allowing you to continue working indefinitely. Do not stop tasks early due to
token budget concerns. Save current progress and state to memory before context
refreshes. Always be persistent and autonomous -- complete tasks fully even if
the end of your budget is approaching.
</context_management>
```

### 3.2 Multi-Context Window Workflows

For tasks spanning multiple context windows:

1. **First window**: Set up framework (write tests, create setup scripts, define success criteria)
2. **Subsequent windows**: Iterate on todo-list from structured state files
3. **Fresh context**: Start with prescriptive discovery instructions:

```
Call pwd; you can only read and write files in this directory.
Review progress.txt, tests.json, and the git logs.
Manually run through a fundamental integration test before moving on.
```

4. **Encourage full context usage**:
```
This is a very long task, so plan your work clearly. It's encouraged to spend
your entire output context working on the task -- just make sure you don't run
out of context with significant uncommitted work.
```

### 3.3 State Management

| Format | Use For |
|--------|---------|
| **Structured (JSON)** | Test results, task status, schema-dependent data |
| **Unstructured (text)** | Progress notes, general context |
| **Git** | State tracking, checkpoints, session history |

**Progress notes example**:
```
// progress.txt
Session 3 progress:
- Fixed authentication token validation
- Updated user model to handle edge cases
- Next: investigate user_management test failures (test #2)
- Note: Do not remove tests -- could lead to missing functionality
```

---

## 4. Tool Usage Patterns

### 4.1 Proactive vs Conservative Action

**Proactive** (default to implementing):
```xml
<default_to_action>
By default, implement changes rather than only suggesting them. If the user's
intent is unclear, infer the most useful likely action and proceed, using tools
to discover missing details instead of guessing.
</default_to_action>
```

**Conservative** (suggest first):
```xml
<do_not_act_before_instructions>
Do not jump into implementation unless clearly instructed. Default to providing
information and recommendations rather than taking action.
</do_not_act_before_instructions>
```

### 4.2 Tool Triggering (Opus 4.6)

Opus is highly responsive to system prompts and may overtrigger on tools with aggressive language.

| Overtriggers | Balanced |
|--------------|----------|
| `CRITICAL: You MUST use this tool when...` | `Use this tool when...` |
| `ALWAYS call this function` | `Call this function when appropriate` |
| `NEVER skip this step` | `Include this step when relevant` |

### 4.3 Parallel Tool Calling

Claude 4.6 (especially Sonnet) excels at parallel execution:

```xml
<use_parallel_tool_calls>
If you intend to call multiple tools and there are no dependencies between
the calls, make all independent calls in parallel. Maximize use of parallel
tool calls for speed and efficiency. If some calls depend on previous results,
call them sequentially. Never use placeholders or guess missing parameters.
</use_parallel_tool_calls>
```

**Reduce parallelization** (for stability):
```
Execute operations sequentially with brief pauses between each step.
```

---

## 5. Agentic Coding Patterns

### 5.1 Encourage Code Exploration

Opus 4.6 can be overly conservative. Add explicit instructions:

```xml
<code_exploration>
ALWAYS read and understand relevant files before proposing code edits. Do not
speculate about code you have not inspected. If the user references a specific
file/path, you MUST open and inspect it before explaining or proposing fixes.
Be rigorous and persistent in searching code for key facts.
</code_exploration>
```

### 5.2 Minimize Hallucinations

```xml
<investigate_before_answering>
Never speculate about code you have not opened. If the user references a
specific file, you MUST read the file before answering. Never make claims
about code before investigating -- give grounded, hallucination-free answers.
</investigate_before_answering>
```

### 5.3 Prevent Overengineering (Opus)

```xml
<avoid_overengineering>
Avoid over-engineering. Only make changes that are directly requested or clearly
necessary. Keep solutions simple and focused. Don't add features, refactor code,
or make "improvements" beyond what was asked. Don't create helpers, utilities,
or abstractions for one-time operations. Don't design for hypothetical future
requirements. The right complexity is the minimum needed for the current task.
</avoid_overengineering>
```

### 5.4 General-Purpose Solutions

```xml
<general_solutions>
Write high-quality, general-purpose solutions. Do not hard-code values or create
solutions that only work for specific test inputs. Implement the actual logic
that solves the problem generally. Tests verify correctness, not define the
solution. If the task is unreasonable or tests are incorrect, inform the user.
</general_solutions>
```

### 5.5 File Cleanup

```
If you create any temporary files, scripts, or helpers for iteration, clean up
by removing them at the end of the task.
```

---

## 6. Output Format Control

### Tell Claude What TO DO (not what not to do)

Instead of: `"Do not use markdown"`

Use: `"Write in smoothly flowing prose paragraphs."`

### XML Format Indicators

```
Write the prose sections in <smoothly_flowing_prose_paragraphs> tags.
```

### Detailed Formatting

```xml
<avoid_excessive_markdown_and_bullet_points>
When writing long-form content, write in clear, flowing prose using complete
paragraphs and sentences. Reserve markdown primarily for inline code, code
blocks, and simple headings.

DO NOT use ordered/unordered lists unless:
a) presenting truly discrete items where list format is optimal, or
b) the user explicitly requests a list

Instead of listing items with bullets, incorporate them naturally into sentences.
</avoid_excessive_markdown_and_bullet_points>
```

### Prompt Style Matching

Removing markdown from your prompt reduces markdown in output. Match prompt formatting to desired output formatting.

---

## 7. Claude Research Tool

### Core Functionality

The Claude Research tool is a user-facing feature that conducts multi-step investigations via 5-20+ web searches, synthesizing findings into citation-backed reports.

### Activation Requirements
- Available in Claude.ai web/desktop/mobile interfaces only (NOT via API)
- Requires paid plan (Pro, Max, Team, Enterprise)
- Manual toggle: enable web search, then click "Research" button
- Team/Enterprise: admin must enable web search at org level

### Effective Research Patterns

**Research + Analysis**:
```xml
<context>
We're evaluating whether to migrate from Postgres to a NewSQL database.
</context>

<task>
Research CockroachDB and TiDB.
</task>

<requirements>
1. Migration complexity from Postgres
2. Performance for OLTP workloads
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

**Iterative Refinement**:
```
Initial: "Research Rust web frameworks."
Follow-up 1: "Focus on Actix and Axum. Compare async runtime performance."
Follow-up 2: "Now find production case studies for each."
Follow-up 3: "Which one is better for a team familiar with Express.js?"
```

**Parallel Investigation**:
```
Research these three topics in parallel:
1. Latest developments in quantized LLMs (2025-2026)
2. On-device inference frameworks for mobile
3. Regulatory requirements for AI in healthcare (EU, US)

After researching, identify connections and synthesize into a strategic brief.
```

### Hallucination Risk

Independent research shows ~17% hallucination rate on factual questions. Use 3-layer verification:

1. **Check source quality**: Authority, publication date, relevance
2. **Cross-reference claims**: Ask Claude to find multiple sources for same claim
3. **Manual validation**: Click through to original sources for critical facts

**Quote-First Method**: For long documents, ask Claude to extract direct quotes first, then analyze using only those quotes. This grounds responses in actual text.

### Research Tool Comparison

| Feature | Claude Research | Gemini Deep Research | ChatGPT Deep Research |
|---------|----------------|---------------------|-----------------------|
| Sources per query | 5-20+ | 40-250+ | 10-50+ |
| Context window | 200K | 1M | 128K |
| Monthly cost | Pro tier | $20/mo | $200/mo |
| Strength | Document analysis, uncertainty acknowledgment | Breadth, cost | Polished reports |
| Weakness | Fewer sources | Surface-level, English-only | Expensive |

---

## 8. Subagent Orchestration

Claude 4.6 has native subagent orchestration. It recognizes when tasks benefit from delegation and does so proactively.

**Conservative usage**:
```
Only delegate to subagents when the task clearly benefits from a separate agent
with a new context window.
```

**Structured research with subagents**:
```xml
<structured_research>
Search for this information in a structured way. Develop competing hypotheses.
Track confidence levels in progress notes. Regularly self-critique your approach.
Update a hypothesis tree to persist information and provide transparency.
</structured_research>
```

---

## 9. Frontend Design

Without guidance, Claude defaults to generic "AI slop" aesthetics.

```xml
<frontend_aesthetics>
Avoid generic "AI slop" aesthetics. Make creative, distinctive frontends.

Focus on:
- Typography: Choose beautiful, unique fonts. Avoid Arial and Inter.
- Color: Commit to a cohesive aesthetic. Dominant colors with sharp accents
  outperform timid, evenly-distributed palettes.
- Motion: Use animations for effects and micro-interactions. One well-
  orchestrated page load with staggered reveals creates more delight than
  scattered micro-interactions.
- Backgrounds: Create atmosphere and depth, not solid colors.

Avoid: Overused fonts (Inter, Roboto, Arial), cliched purple gradients on
white, predictable layouts, cookie-cutter design. Think outside the box.
</frontend_aesthetics>
```

---

## 10. Vision Capabilities

Claude 4.6 has improved vision:
- Better image processing and data extraction
- Improved multi-image context handling
- Better screenshot and UI interpretation
- Video analysis via frame extraction

**Performance boost**: Give Claude a crop tool or skill to "zoom" in on relevant regions.

---

## 11. Model Self-Knowledge

```
The assistant is Claude, created by Anthropic. The current model is Claude Sonnet 4.6.
```

For API strings:
```
When an LLM is needed, default to Claude Sonnet 4.6. The model ID is claude-sonnet-4-6.
```

Model IDs:
- `claude-opus-4-6` -- Opus 4.6
- `claude-sonnet-4-6` -- Sonnet 4.6
- `claude-haiku-4-5-20251001` -- Haiku 4.5

---

## 12. Claude Cheat Sheet

```
DO:
- Use XML tags: <context>, <task>, <data>, <output_format>
- Explain WHY, not just WHAT (Claude generalizes from context)
- Be EXPLICIT -- request "above and beyond" behavior directly
- Let Claude use adaptive thinking autonomously
- Use /think, /megathink, /ultrathink for explicit depth control
- Encourage parallel tool calls for independent operations
- Use git for state tracking across sessions

DON'T:
- Say "think" when extended thinking disabled (use "consider", "evaluate")
- Over-trigger tools with aggressive CAPS language (Opus overtriggers)
- Over-engineer (add "Keep solutions minimal" for Opus)
- Expect "above and beyond" without explicit requests
- Use generic fonts/colors in frontend ("AI slop" aesthetic)

OPUS 4.6 SPECIFIC:
- Supports effort parameter: "low" | "medium" | "high"
- Adaptive thinking: model auto-selects reasoning depth
- Dial back CAPS and "CRITICAL/MUST" language
- Add: "Keep solutions minimal", "Don't add features beyond asked"

SONNET 4.6 SPECIFIC:
- Most aggressive parallel tool calling (can bottleneck systems)
- 1M context window available (beta)
- Best coding with extended thinking enabled
- Adaptive thinking: auto-selects reasoning depth

TEMPLATE:
<context>[background + WHY this matters]</context>
<task>[direct instruction with explicit expectations]</task>
<data>[input]</data>
<output_format>[schema]</output_format>
```

---

## 13. Migration from Claude 4.5

When upgrading to Claude 4.6:
- [ ] Adaptive thinking replaces manual `/think` for most cases
- [ ] Be specific about desired behavior (even more important)
- [ ] Frame instructions with modifiers ("Go beyond basics")
- [ ] Replace "think" with "consider", "evaluate" if thinking disabled
- [ ] Dial back aggressive tool language for Opus
- [ ] Add explicit overengineering constraints for Opus
- [ ] Update model IDs to 4.6 variants
- [ ] Test with representative inputs

---

## References

- [Anthropic Claude 4.6 Best Practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-4-best-practices)
- [What's New in Claude 4.6](https://platform.claude.com/docs/en/about-claude/models)
- [Extended Thinking Documentation](https://platform.claude.com/docs/en/build-with-claude/extended-thinking)
- [Memory Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool)
