# Claude 4.x Best Practices (Official Anthropic Guidelines - January 2026)

This technical reference documents official prompt engineering best practices for Claude 4.x models (Opus 4.5, Sonnet 4.5, Haiku 4.5) based on Anthropic's documentation.

> **Source**: [platform.claude.com/docs](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-4-best-practices)

---

## 1. General Principles

### 1.1 Be Explicit with Instructions

Claude 4.x models respond well to clear, explicit instructions. The "above and beyond" behavior from previous models requires explicit requests.

**Before (Less Effective)**:
```
Create an analytics dashboard
```

**After (More Effective)**:
```
Create an analytics dashboard. Include as many relevant features and interactions as possible. Go beyond the basics to create a fully-featured implementation.
```

### 1.2 Add Context to Improve Performance

Providing context or motivation behind instructions helps Claude understand your goals.

**Before (Less Effective)**:
```
NEVER use ellipses
```

**After (More Effective)**:
```
Your response will be read aloud by a text-to-speech engine, so never use ellipses since the text-to-speech engine will not know how to pronounce them.
```

**Key Insight**: Claude generalizes from explanations. Explain WHY, not just WHAT.

### 1.3 Be Vigilant with Examples & Details

Claude 4.x pays close attention to details and examples. Ensure examples align with desired behaviors and minimize undesired ones.

---

## 2. Long-Horizon Reasoning & State Tracking

Claude 4.5 models excel at long-horizon reasoning with exceptional state tracking. They maintain orientation across extended sessions by focusing on incremental progress.

### 2.1 Context Awareness

Claude 4.5 features context awareness, tracking its remaining token budget. For agent harnesses with context compaction:

```xml
<context_management>
Your context window will be automatically compacted as it approaches its limit, allowing you to continue working indefinitely from where you left off. Therefore, do not stop tasks early due to token budget concerns. As you approach your token budget limit, save your current progress and state to memory before the context window refreshes. Always be as persistent and autonomous as possible and complete tasks fully, even if the end of your budget is approaching. Never artificially stop any task early regardless of the context remaining.
</context_management>
```

### 2.2 Multi-Context Window Workflows

For tasks spanning multiple context windows:

1. **First Context Window Setup**: Use the first window to set up a framework (write tests, create setup scripts), then use future windows to iterate on a todo-list.

2. **Structured Test Format**:
   ```json
   // tests.json
   {
     "tests": [
       {"id": 1, "name": "authentication_flow", "status": "passing"},
       {"id": 2, "name": "user_management", "status": "failing"},
       {"id": 3, "name": "api_endpoints", "status": "not_started"}
     ],
     "total": 200,
     "passing": 150,
     "failing": 25,
     "not_started": 25
   }
   ```

3. **Quality of Life Tools**: Encourage Claude to create setup scripts (e.g., `init.sh`) for servers, test suites, and linters.

4. **Fresh vs Compacting**: Claude 4.5 is effective at discovering state from the local filesystem. Start with prescriptive instructions:
   - "Call pwd; you can only read and write files in this directory."
   - "Review progress.txt, tests.json, and the git logs."
   - "Manually run through a fundamental integration test before moving on."

5. **Encourage Complete Context Usage**:
   ```
   This is a very long task, so it may be beneficial to plan out your work clearly. It's encouraged to spend your entire output context working on the task - just make sure you don't run out of context with significant uncommitted work. Continue working systematically until you have completed this task.
   ```

### 2.3 State Management Best Practices

| Format | Use For |
|--------|---------|
| **Structured (JSON)** | Test results, task status, schema-dependent data |
| **Unstructured (Text)** | Progress notes, general context |
| **Git** | State tracking, checkpoints, session history |

**Progress Notes Example**:
```
// progress.txt
Session 3 progress:
- Fixed authentication token validation
- Updated user model to handle edge cases
- Next: investigate user_management test failures (test #2)
- Note: Do not remove tests as this could lead to missing functionality
```

---

## 3. Communication Style

Claude 4.5 models have evolved communication:

| Trait | Description |
|-------|-------------|
| **More Direct** | Fact-based progress reports, not self-celebratory |
| **More Conversational** | Fluent and colloquial, less machine-like |
| **Less Verbose** | May skip summaries unless prompted |

### 3.1 Balance Verbosity

If you want updates as Claude works:

```
After completing a task that involves tool use, provide a quick summary of the work you've done.
```

---

## 4. Tool Usage Patterns

### 4.1 Proactive vs Conservative Action

Claude 4.x benefits from explicit direction to use tools.

**For Proactive Action** (default to implementing):
```xml
<default_to_action>
By default, implement changes rather than only suggesting them. If the user's intent is unclear, infer the most useful likely action and proceed, using tools to discover any missing details instead of guessing. Try to infer the user's intent about whether a tool call (e.g., file edit or read) is intended or not, and act accordingly.
</default_to_action>
```

**For Conservative Action** (suggest first):
```xml
<do_not_act_before_instructions>
Do not jump into implementation or change files unless clearly instructed to make changes. When the user's intent is ambiguous, default to providing information, doing research, and providing recommendations rather than taking action. Only proceed with edits, modifications, or implementations when the user explicitly requests them.
</do_not_act_before_instructions>
```

### 4.2 Tool Triggering (Opus 4.5 Specific)

**Issue**: Opus 4.5 is more responsive to system prompts and may overtrigger on tools.

**Fix**: Dial back aggressive language.

| Before (Overtriggers) | After (Balanced) |
|-----------------------|------------------|
| `CRITICAL: You MUST use this tool when...` | `Use this tool when...` |
| `ALWAYS call this function` | `Call this function when appropriate` |

### 4.3 Parallel Tool Calling

Claude 4.x excels at parallel execution. Sonnet 4.5 is particularly aggressive.

**Maximum Parallel Efficiency**:
```xml
<use_parallel_tool_calls>
If you intend to call multiple tools and there are no dependencies between the tool calls, make all of the independent tool calls in parallel. Prioritize calling tools simultaneously whenever the actions can be done in parallel rather than sequentially. For example, when reading 3 files, run 3 tool calls in parallel to read all 3 files into context at the same time. Maximize use of parallel tool calls where possible to increase speed and efficiency. However, if some tool calls depend on previous calls to inform dependent values like the parameters, do NOT call these tools in parallel and instead call them sequentially. Never use placeholders or guess missing parameters in tool calls.
</use_parallel_tool_calls>
```

**Reduce Parallelization** (for stability):
```
Execute operations sequentially with brief pauses between each step to ensure stability.
```

---

## 5. Output Format Control

### 5.1 Effective Techniques

1. **Tell Claude what TO DO** (not what NOT to do):
   - Instead of: "Do not use markdown"
   - Use: "Your response should be composed of smoothly flowing prose paragraphs."

2. **Use XML format indicators**:
   ```
   Write the prose sections in <smoothly_flowing_prose_paragraphs> tags.
   ```

3. **Match prompt style to desired output**: Removing markdown from your prompt reduces markdown in output.

4. **Detailed formatting guidance**:
```xml
<avoid_excessive_markdown_and_bullet_points>
When writing reports, documents, technical explanations, analyses, or any long-form content, write in clear, flowing prose using complete paragraphs and sentences. Use standard paragraph breaks for organization and reserve markdown primarily for `inline code`, code blocks, and simple headings (###).

DO NOT use ordered lists (1. ...) or unordered lists (*) unless:
a) you're presenting truly discrete items where a list format is the best option, or
b) the user explicitly requests a list or ranking

Instead of listing items with bullets or numbers, incorporate them naturally into sentences. NEVER output a series of overly short bullet points.
</avoid_excessive_markdown_and_bullet_points>
```

---

## 6. Thinking & Reasoning

### 6.1 Thinking Sensitivity (Opus 4.5)

**Critical**: When extended thinking is disabled, Opus 4.5 is sensitive to the word "think".

| Avoid | Use Instead |
|-------|-------------|
| "think about" | "consider" |
| "think through" | "evaluate" |
| "think carefully" | "analyze" |
| "thinking" | "reasoning" |

### 6.2 Interleaved Thinking

Guide Claude's thinking after tool use:

```
After receiving tool results, carefully reflect on their quality and determine optimal next steps before proceeding. Use your thinking to plan and iterate based on this new information, and then take the best next action.
```

---

## 7. Agentic Coding Patterns

### 7.1 Reduce File Creation

Claude 4.x may create temporary files for iteration. To minimize:

```
If you create any temporary new files, scripts, or helper files for iteration, clean up these files by removing them at the end of the task.
```

### 7.2 Prevent Overengineering (Opus 4.5)

**Issue**: Opus 4.5 tends to overengineer with extra files, unnecessary abstractions, or unneeded flexibility.

**Fix**:
```xml
<avoid_overengineering>
Avoid over-engineering. Only make changes that are directly requested or clearly necessary. Keep solutions simple and focused.

Don't add features, refactor code, or make "improvements" beyond what was asked. A bug fix doesn't need surrounding code cleaned up. A simple feature doesn't need extra configurability.

Don't add error handling, fallbacks, or validation for scenarios that can't happen. Trust internal code and framework guarantees. Only validate at system boundaries (user input, external APIs). Don't use backwards-compatibility shims when you can just change the code.

Don't create helpers, utilities, or abstractions for one-time operations. Don't design for hypothetical future requirements. The right amount of complexity is the minimum needed for the current task. Reuse existing abstractions where possible and follow the DRY principle.
</avoid_overengineering>
```

### 7.3 Encourage Code Exploration

**Issue**: Opus 4.5 can be overly conservative when exploring code.

**Fix**:
```xml
<code_exploration>
ALWAYS read and understand relevant files before proposing code edits. Do not speculate about code you have not inspected. If the user references a specific file/path, you MUST open and inspect it before explaining or proposing fixes. Be rigorous and persistent in searching code for key facts. Thoroughly review the style, conventions, and abstractions of the codebase before implementing new features or abstractions.
</code_exploration>
```

### 7.4 Minimize Hallucinations

```xml
<investigate_before_answering>
Never speculate about code you have not opened. If the user references a specific file, you MUST read the file before answering. Make sure to investigate and read relevant files BEFORE answering questions about the codebase. Never make any claims about code before investigating unless you are certain of the correct answer - give grounded and hallucination-free answers.
</investigate_before_answering>
```

### 7.5 Avoid Hard-Coding & Test-Focused Solutions

```xml
<general_solutions>
Please write a high-quality, general-purpose solution using the standard tools available. Do not create helper scripts or workarounds to accomplish the task more efficiently. Implement a solution that works correctly for all valid inputs, not just the test cases. Do not hard-code values or create solutions that only work for specific test inputs. Instead, implement the actual logic that solves the problem generally.

Focus on understanding the problem requirements and implementing the correct algorithm. Tests are there to verify correctness, not to define the solution. Provide a principled implementation that follows best practices and software design principles.

If the task is unreasonable or infeasible, or if any of the tests are incorrect, please inform me rather than working around them. The solution should be robust, maintainable, and extendable.
</general_solutions>
```

---

## 8. Research & Information Gathering

Claude 4.5 has exceptional agentic search capabilities.

**Structured Research Approach**:
```xml
<structured_research>
Search for this information in a structured way. As you gather data, develop several competing hypotheses. Track your confidence levels in your progress notes to improve calibration. Regularly self-critique your approach and plan. Update a hypothesis tree or research notes file to persist information and provide transparency. Break down this complex research task systematically.
</structured_research>
```

---

## 9. Subagent Orchestration

Claude 4.5 has native subagent orchestration. It recognizes when tasks benefit from delegation and does so proactively.

**Conservative Subagent Usage**:
```
Only delegate to subagents when the task clearly benefits from a separate agent with a new context window.
```

---

## 10. Frontend Design

**Issue**: Without guidance, Claude defaults to generic "AI slop" aesthetics.

**Fix**:
```xml
<frontend_aesthetics>
You tend to converge toward generic, "on distribution" outputs. In frontend design, this creates what users call the "AI slop" aesthetic. Avoid this: make creative, distinctive frontends that surprise and delight.

Focus on:
- Typography: Choose fonts that are beautiful, unique, and interesting. Avoid generic fonts like Arial and Inter; opt instead for distinctive choices that elevate the frontend's aesthetics.
- Color & Theme: Commit to a cohesive aesthetic. Use CSS variables for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes. Draw from IDE themes and cultural aesthetics for inspiration.
- Motion: Use animations for effects and micro-interactions. Prioritize CSS-only solutions for HTML. Use Motion library for React when available. Focus on high-impact moments: one well-orchestrated page load with staggered reveals (animation-delay) creates more delight than scattered micro-interactions.
- Backgrounds: Create atmosphere and depth rather than defaulting to solid colors. Layer CSS gradients, use geometric patterns, or add contextual effects that match the overall aesthetic.

Avoid generic AI-generated aesthetics:
- Overused font families (Inter, Roboto, Arial, system fonts)
- Clichéd color schemes (particularly purple gradients on white backgrounds)
- Predictable layouts and component patterns
- Cookie-cutter design that lacks context-specific character

Interpret creatively and make unexpected choices that feel genuinely designed for the context. Vary between light and dark themes, different fonts, different aesthetics. Avoid converging on common choices across generations - think outside the box!
</frontend_aesthetics>
```

---

## 11. Vision Capabilities

Claude Opus 4.5 has improved vision capabilities:

- Better image processing and data extraction
- Improved multi-image context handling
- Better screenshot and UI interpretation
- Video analysis via frame extraction

**Performance Boost**: Give Claude a crop tool or skill to "zoom" in on relevant regions.

---

## 12. Model Self-Knowledge

```
The assistant is Claude, created by Anthropic. The current model is Claude Sonnet 4.5.
```

For API strings:
```
When an LLM is needed, please default to Claude Sonnet 4.5 unless the user requests otherwise. The exact model string for Claude Sonnet 4.5 is claude-sonnet-4-5-20250929.
```

---

## 13. Model-Specific Summary

### Haiku 4.5
- First Haiku with extended thinking
- Best for: High-volume, sub-agents, real-time applications
- Keep instructions concise but explicit
- Prioritize bulletized constraints

### Sonnet 4.5
- Most aggressive parallel tool calling
- Extended autonomous operation capability
- Best coding with extended thinking enabled
- 1M context window (beta)
- Best for: Coding, complex agents, large documents

### Opus 4.5
- Sensitive to "think" word when thinking disabled
- May overtrigger on tools - use calm language
- Tendency to overengineer - constrain scope explicitly
- Supports effort parameter: "low" | "medium" | "high"
- Best for: Maximum intelligence, complex reasoning

---

## 14. Migration Checklist

When migrating to Claude 4.5:

- [ ] Be specific about desired behavior
- [ ] Frame instructions with modifiers ("Go beyond basics", "Include all relevant features")
- [ ] Request animations/interactive elements explicitly
- [ ] Replace "think" with "consider", "evaluate", "analyze" if thinking disabled
- [ ] Dial back aggressive tool language for Opus
- [ ] Add explicit overengineering constraints for Opus
- [ ] Update example formatting to match desired output
- [ ] Test with representative inputs

---

## References

- [Anthropic Claude 4 Best Practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-4-best-practices)
- [What's New in Claude 4.5](https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-5)
- [Extended Thinking Documentation](https://platform.claude.com/docs/en/build-with-claude/extended-thinking)
- [Memory Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool)
