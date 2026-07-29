# Gemini Practices (Google, July 2026)

This module merges Gemini Deep Research and Gemini 3.x prompting guidance into a single reference for all Google Gemini models.

> **Model specs**: See 03-model-catalog_v5.md for Gemini family data.
> **Anti-patterns**: See 02-techniques-patterns_v5.md (canonical).
> **Current models covered**: Gemini 3.5 Flash (`thinking_level` default = `medium`; knowledge cutoff January 2025 -- explicitly state the current year/date for time-sensitive queries) and Gemini 3.1 Pro Preview (`gemini-3.1-pro-preview`). Guidance below applies to both unless noted.

---

## 1. Core Prompting Principles (Gemini 3.x)

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

Controls the *maximum* reasoning depth via API/interface settings. Prompt text still has influence -- Google notes that phrasing like "Think very hard before answering" can increase reasoning within the level's ceiling.

| Level | Latency | Cost | Use For |
|-------|---------|------|---------|
| `"minimal"` (Gemini 3.5 Flash only -- **not** supported on 3.1 Pro) | Fastest | Lowest | Trivial lookups, near-zero reasoning |
| `"low"` | Fast | Lower | Simple queries, extraction, formatting, lookups |
| `"medium"` (default on Gemini 3.5 Flash) | Moderate | Moderate | Balanced everyday tasks |
| `"high"` | Slower | Higher | Research, planning, creative writing, complex problems |

**Never send `thinking_budget` together with `thinking_level`** in the same request -- the API returns a 400 error. Pick one mechanism (prefer `thinking_level` on current models).

### 1.4 Omit Sampling Parameters

**CRITICAL**: Current official Google guidance is to **OMIT** `temperature`, `top_p`, and `top_k` entirely and let the model use its defaults.

- Setting sub-1.0 temperature **may** cause looping and degraded performance on reasoning tasks (Google's wording -- not a guaranteed failure)
- Do not carry over sampling-param tuning from earlier Gemini generations
- Steer style, tone, and variety through the prompt instead of sampling knobs
- This mirrors an industry-wide shift: Claude current-gen returns 400 on **non-default** values of these params (defaults still accepted; `top_k` rejected outright), DeepSeek thinking mode ignores them

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

> **Corrected July 2026.** Earlier editions of this guide told you to put
> formatting and negative constraints **last**. Google's prompting-strategies
> documentation says the opposite: **essential constraints and output-format
> requirements belong in the system instruction, at the beginning.** Only the
> *specific question* goes last, and only when it follows a long context.

Put every constraint that governs behavior or output shape **at the TOP**, in
the system instruction where possible. The "last" slot is reserved for the
specific ask, and exists to solve a different problem: in long-context prompts,
a question buried above 100K tokens of source material gets lost.

**Recommended hierarchy**:
1. System instruction: persona, tone, safety rules, **and output-format requirements** -- TOP
2. Context and source material
3. Main task instructions
4. The specific question -- LAST (this is the long-context rule, not a constraint rule)

**Bad** (constraints stranded after a long context, competing with the data for attention):
```
Find laptop recommendations from the catalog below:
[50K tokens of catalog data]

Requirements:
- Do not include prices over $100
- Maximum 5 items
- Format as bullet points
```

**Good** (constraints in the system instruction, question last):
```
system_instruction:
  You recommend laptops from a supplied catalog.
  Never include items priced over $100.
  Return at most 5 items, formatted as bullet points.

user:
  [50K tokens of catalog data]

  Which laptops should I consider?
```

---

## 3. Context and Transitions

### Context First, Questions Last

For long contexts, provide all documents/data/code first, then the specific question at the end. This is about keeping the *ask* from being buried -- standing constraints still belong in the system instruction at the top.

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
| Faster (with low thinking) | `thinking_level: "low"` + "Think silently." |

### Structured Output for Format Anchoring

The Gemini API has **no `prefix` parameter**. To enforce output shape, use the
structured-output config on `generate_content`:

```python
from google import genai
from pydantic import BaseModel

class User(BaseModel):
    name: str
    email: str

client = genai.Client()
response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents="Return user data as JSON: ...",
    config={
        "response_mime_type": "application/json",
        "response_schema": User,
    },
)
```

Where a schema is overkill, anchor the format in the prompt text instead
("Respond with a single JSON object and no prose.").

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
- Research plan review is **opt-in**: set `collaborative_planning=true`. Default is `false`, so execution normally starts without showing a plan
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

**Edit the plan**: The most impactful technique is reviewing and editing the proposed research plan before execution -- but you must opt in with `collaborative_planning=true` first. Once shown, add, remove, or refocus steps using natural language.

### Key Capabilities
- Iterative research: 40-250+ sites per query
- 1M token context for processing hundreds of pages
- File uploads: up to 10 files (PDFs, Docs, images)
- Google Workspace integration (Drive, Docs)
- Canvas transformation (infographics, audio summaries, interactive pages)
- API access via the **Gemini Interactions API** (the Deep Research Agent is exclusive to it -- not the Vertex AI Discovery Engine API)

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
- OMIT temperature/top_p/top_k entirely (defaults; sub-1.0 causes looping)
- Use thinking_level: "minimal" | "low" | "medium" (default on 3.5 Flash) | "high"
- Never send thinking_budget + thinking_level together (400 error)
- Return thought signatures in stateless multi-turn function calling
- State the current year for time-sensitive queries (3.5 Flash cutoff Jan 2025)
- Be direct and concise
- Put context FIRST, questions LAST
- Put CONSTRAINTS at END (critical -- dropped if early!)
- Use 2-3 few-shot examples with consistent formatting
- Anchor transitions: "Based on the above..."
- Label multimodal inputs explicitly

DON'T:
- Set temperature/top_p/top_k below defaults (causes loops/degradation) -- prefer omitting entirely
- Put constraints (behavioral OR formatting) at the END instead of the system instruction
- Bury the specific question above a long context
- Use conversational language ("please", "kindly")
- Use complex CoT from Gemini 2.x era
- Use broad "do not infer" (be specific instead)

CONSTRAINT ORDER (CRITICAL):
1. System instruction: persona/tone/safety AND output-format rules -- TOP
2. Context/source material
3. Main task
4. The specific question LAST (long-context rule -- keeps the ask from being buried)

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

## 12. Function Calling (Stateless Multi-Turn)

### Thought Signatures

When using function calling in a stateless multi-turn setup (you manage conversation history yourself, rather than a server-side Live session), Gemini 3.x returns **thought signatures** alongside function calls. These signatures must be sent back unmodified in the next turn's request history. Dropping or altering them breaks reasoning continuity and degrades multi-turn tool-use quality.

### Strict Function-Response Matching

Each function call must be matched by exactly **one** function response, matched by both `id` and `name`. Do not:
- Omit a response for a call the model made
- Send multiple responses for a single call
- Mismatch the `id`/`name` pairing between call and response

Violating this contract causes errors or malformed conversation state in subsequent turns.

---

## References

- [Vertex AI Gemini 3.x Prompting Guide](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/start/gemini-3-prompting-guide)
- [Google AI Prompting Strategies](https://ai.google.dev/gemini-api/docs/prompting-strategies)
- [Official Google Gemini 3 Prompting Guidelines](https://ai.google.dev/gemini-api/docs)
