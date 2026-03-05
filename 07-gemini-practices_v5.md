# Gemini Practices (Google, March 2026)

This module merges Gemini Deep Research and Gemini 3.x prompting guidance into a single reference for all Google Gemini models.

> **Model specs**: See 03-model-catalog_v5.md for Gemini family data.
> **Anti-patterns**: See 02-techniques-patterns_v5.md (canonical).

---

## 1. Core Prompting Principles (Gemini 3.1)

### 1.1 Be Precise and Direct

Gemini 3.x treats prompts as executable instructions. Directness over persuasion.

**Avoid**: "Could you please help me understand..."
**Use**: "Explain the differences between..."

### 1.2 Simplify Your Prompts

Gemini 3.x has native advanced reasoning. Stop using complex CoT from the 2.x era.

**Old way (2.x)**: "Let's approach this step-by-step: First, identify the problem. Second, brainstorm solutions..."
**New way (3.x)**: "Solve this problem: [problem]. Show your reasoning."

**Exception**: For very complex reasoning, you can still use explicit planning or self-critique prompts (see Section 5).

### 1.3 Use the `thinking_level` Parameter

Controls reasoning depth via API/interface settings, not via prompt text.

| Level | Latency | Cost | Use For |
|-------|---------|------|---------|
| `"low"` | Fast | Lower | Simple queries, extraction, formatting, lookups |
| `"high"` (default) | Slower | Higher | Research, planning, creative writing, complex problems |

### 1.4 Keep Temperature at 1.0

**CRITICAL**: Gemini 3.x is calibrated for `temperature = 1.0`. Do NOT change.

- Lowering causes loops and degraded performance on reasoning tasks
- Exception: For highly creative tasks, experiment with 1.1-1.2
- Safety fallback: If safety filters trigger, try increasing temperature slightly

### 1.5 Use Consistent Structure

Choose XML or Markdown and stick with it throughout a single prompt.

**XML**:
```xml
<role>You are a senior data analyst.</role>

<constraints>
- Focus on 2025-2026 data only
- Cite all sources
</constraints>

<context>
[data and background]
</context>

<task>
Analyze the trend in Q3 revenue and identify root causes for the decline.
</task>
```

**Markdown**:
```markdown
# Role
You are a technical writer.

# Constraints
- Simple language (8th grade reading level)
- Include code examples
- Maximum 500 words

# Task
Explain how async/await works in JavaScript.
```

---

## 2. Constraint Organization (Critical)

### Order Matters

Place negative constraints, formatting constraints, and quantitative limits **at the END**.

Gemini 3.x may drop constraints placed too early in the prompt.

**Recommended hierarchy**:
1. Context and source material
2. Main task instructions
3. Negative/formatting/quantitative constraints (LAST)

**Bad** (constraints may be dropped):
```
Do not include prices over $100.
Maximum 5 items.
Format as bullet points.

Find laptop recommendations from the catalog below:
[catalog data]
```

**Good** (constraints preserved):
```
Find laptop recommendations from the catalog below:
[catalog data]

Requirements:
- Do not include prices over $100
- Maximum 5 items
- Format as bullet points
```

---

## 3. Context and Transitions

### Context First, Questions Last

For long contexts, provide all documents/data/code first. Place instructions at the end.

```xml
<context>
[Full text of research papers, 50k tokens]
</context>

<task>
Based on the entire document above, identify common themes and contradictions.
Present in a comparison table.
</task>
```

### Anchor with Transitions

Use bridging phrases to connect data to queries:
- "Based on the information above..."
- "Using the data provided..."
- "Given the context..."

This helps the model understand where context ends and the task begins.

---

## 4. Multimodal and Formatting

### Explicit Multimodal Labels

When using images, audio, or video, explicitly reference each modality:

```
I've uploaded three files:
- Image 1: Product mockup
- Image 2: Competitor product
- Video 1: User testing session

Task: Compare UX design in Image 1 and Image 2.
Use insights from Video 1 to identify usability improvements.
```

Gemini treats text, images, audio, and video as equal-class inputs. Without explicit labels, it may confuse inputs.

### Output Verbosity Control

Gemini 3.x defaults to **concise** responses.

| Desired Style | Prompt Addition |
|---------------|-----------------|
| More conversational | "Explain as a friendly, talkative assistant." |
| Detailed explanation | "Provide a comprehensive, detailed response." |
| Technical depth | "Include technical details and edge cases." |
| Faster (with low thinking) | `thinking_level: "LOW"` + "Think silently." |

### Response Prefixes for Format Anchoring

Begin the model's response to enforce structure:

```python
response = model.generate(
    prompt="Return user data as JSON...",
    prefix='```json\n{"user": '  # Forces JSON format
)
```

---

## 5. Enhanced Reasoning Patterns

### Explicit Planning (Complex Tasks)

```
Before providing the final answer:
1. Parse the stated goal into distinct sub-tasks.
2. Check if the input information is complete.
3. Create a structured outline to achieve the goal.
4. Execute each sub-task.
5. Synthesize results into the final answer.
```

### Self-Critique

```
Before returning your final response, review against the original constraints:
1. Did I answer the user's *intent*, not just their literal words?
2. Is the tone authentic to the requested persona?
3. Did I follow all specified constraints?
4. Are there logical inconsistencies or errors?

If issues found, revise before submitting.
```

### When NOT to Use These

- **Simple tasks**: Skip explicit planning. Just state the task.
- **`thinking_level: "low"`**: Avoid reasoning prompts -- defeats the purpose of fast mode.

---

## 6. Context Grounding

### Split-Step Verification

For topics where the model might hallucinate:

```
Verify with high confidence if you're able to access [source].
If you cannot verify, state 'No Info' and STOP.
If verified, proceed with the following query:
[actual request]
```

### Strict Context Adherence

For hypothetical scenarios or when context contradicts common knowledge:

```
Treat the provided context as the absolute limit of truth; any facts not
directly mentioned must be considered completely unsupported.

[context]

[question]
```

For calculations:
```
Perform calculations based strictly on provided text.
Do not introduce external information.
```

### Distinguishing Deduction from External Knowledge

Instead of broad "do not infer":
```
# Less effective
Do not infer or assume anything.

# More effective
Perform calculations based strictly on provided text.
Do not introduce external information or common knowledge.
```

---

## 7. Few-Shot Examples (Gemini-Specific)

Google recommends 2-3 few-shot examples for Gemini (more than other providers):

```
**Consistent formatting is critical** -- maintain identical structure across all examples.

Example 1:
Input: [example input]
Output: [example output]

Example 2:
Input: [example input]
Output: [example output]

Your turn:
Input: [actual input]
Output:
```

**Best practices**:
- Show positive patterns (correct behavior) rather than what to avoid
- 2-3 examples typically sufficient
- Excessive examples risk overfitting
- Use output prefixes to anchor format

---

## 8. Persona Usage

- Gemini 3.x treats assigned personas **very seriously**
- The model may ignore instructions that conflict with the persona
- Avoid ambiguous scenarios when using personas
- Be explicit about persona boundaries

```xml
<role>
You are a strict code reviewer. You reject code with any security vulnerabilities.
</role>

<constraints>
- Flag all SQL injection risks
- Flag all XSS vulnerabilities
- Reject code with hardcoded credentials
</constraints>
```

---

## 9. Gemini Deep Research

### Core Functionality

Gemini Deep Research is an autonomous AI assistant that analyzes 40-250+ websites to produce comprehensive, multi-page reports with full citations. It iteratively searches, learns, and synthesizes information.

### Activation
- Available in the Gemini web interface
- Research plan presented for review before execution
- Tiered access: free (limited), AI Pro ($20/mo), Ultra (highest limits)

### Effective Prompt Patterns

**Specificity is key**:
```
Research AI chatbots available in 2026, comparing 5 platforms on capabilities,
pricing, and enterprise use cases. Include user reviews and future trends.
```

**Structural elements**:
```
Act as a market research analyst. Research:
1) Market size (2020-2026)
2) Key competitors
3) Emerging trends

Deliverables: Executive summary, competitor comparison table, risk analysis.
```

**Edit the plan**: The most impactful technique is reviewing and editing the proposed research plan before execution. Add, remove, or refocus steps using natural language.

### Key Capabilities
- Iterative research: 40-250+ sites per query
- 1M token context for processing hundreds of pages
- File uploads: up to 10 files (PDFs, Docs, images)
- Google Workspace integration (Drive, Docs)
- Canvas transformation (infographics, audio summaries, interactive pages)
- API access via Discovery Engine API in Vertex AI

### Limitations
- No academic source filtering (unsuitable for scholarly work)
- English-only research (significant bias on global topics)
- Surface-level analysis (overviews, not expert depth)
- Unreliable for real-time data (stock prices, breaking news)
- Hallucination risk (verify all claims)
- Context collapse after ~30k characters (start new chats)

---

## 10. Gemini Cheat Sheet

```
DO:
- Set temperature = 1.0 (REQUIRED -- lower causes loops!)
- Use thinking_level: "low" | "high"
- Be direct and concise
- Put context FIRST, questions LAST
- Put CONSTRAINTS at END (critical -- dropped if early!)
- Use 2-3 few-shot examples with consistent formatting
- Anchor transitions: "Based on the above..."
- Label multimodal inputs explicitly

DON'T:
- Lower temperature (causes loops/degradation)
- Put negative/formatting constraints BEFORE context
- Use conversational language ("please", "kindly")
- Use complex CoT from Gemini 2.x era
- Use broad "do not infer" (be specific instead)

CONSTRAINT ORDER (CRITICAL):
1. Context/source material
2. Main task
3. Constraints LAST (or they're dropped!)

VERBOSITY: Default = concise
- More verbose: "Explain as friendly, talkative assistant"
- Faster: thinking_level=LOW + "Think silently"

TEMPLATE:
<context>[all background first]</context>
<task>[direct instruction -- no fluff]</task>
<constraints>[negative/formatting limits LAST]</constraints>
```

---

## 11. Complete Template

**System Instruction** (optional, for complex workflows):
```xml
<role>
You are a specialized assistant for [domain].
You are precise, analytical, and direct.
</role>

<instructions>
1. Analyze: Parse the user's task and context.
2. Plan: For complex tasks, create a step-by-step plan.
3. Execute: Carry out the plan.
4. Validate: Review output against requirements.
5. Format: Present in requested structure.
</instructions>

<constraints>
- Verbosity: [Low/Medium/High]
- Tone: [Formal/Casual/Technical]
- Cite sources: [Yes/No]
</constraints>

<output_format>
1. Executive Summary
2. Detailed Response
3. References (if applicable)
</output_format>
```

**User Prompt**:
```xml
<context>
[documents, code, data, background]
</context>

<task>
[specific request]
</task>

<final_instruction>
[last-minute clarifications or constraints]
</final_instruction>
```

---

## References

- [Vertex AI Gemini 3.1 Prompting Guide](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/start/gemini-3-prompting-guide)
- [Google AI Prompting Strategies](https://ai.google.dev/gemini-api/docs/prompting-strategies)
- [Official Google Gemini 3 Prompting Guidelines](https://ai.google.dev/gemini-api/docs)
