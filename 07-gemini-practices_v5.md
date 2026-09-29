# Gemini Practices (Google, September 2026)

This module merges Gemini Deep Research and Gemini 3.x prompting guidance into a single reference for all Google Gemini models.

> **Model specs**: See 03-model-catalog_v5.md for Gemini family data.
> **Anti-patterns**: See 02-techniques-patterns_v5.md (canonical).
> **Current models covered**: Gemini 3.8 Flash (`gemini-3.8-flash`, GA Sep 2 2026, top text model; `thinking_level` default = `medium`), 3.7 Flash, 3.6 Flash, 3.5 Flash, 3.5 Flash-Lite, 3.1 Flash-Lite, 3.1 Pro Preview (`gemini-3.1-pro-preview`, still Preview) and 3 Flash Preview. Knowledge cutoff is January 2025 for 3.5 Flash and 3 Flash (not published for 3.6-3.8) -- explicitly state the current year/date for time-sensitive queries. Guidance below applies to all unless noted.
> **Status**: Gemini 3.5 Pro is unreleased ("coming soon"); Gemini 4 is in training with no release date. Neither is a usable model.
> **Google's default for new projects**: 3.5 Flash-Lite or 3.8 Flash. The Interactions API (GA June 2026) is Google's recommended surface; `generateContent` is legacy but fully supported.

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

**Audit note**: a "step by step" match in a Gemini prompt is still an AP-2 hit (flag it as usual) -- Google's own best-practice template ends with `Remember to think step-by-step before answering.`, so deleting it is low-risk.

### 1.3 Use the `thinking_level` Parameter

Controls the *maximum* reasoning depth via API/interface settings. Prompt text still has influence -- Google notes that phrasing like "Think very hard before answering" can increase reasoning within the level's ceiling.

| Level | Latency | Cost | Use For |
|-------|---------|------|---------|
| `"minimal"` (3.5/3.6 Flash, Flash-Lite models, 3 Flash -- **error** on 3.7 Flash, 3.8 Flash and 3.1 Pro) | Fastest | Lowest | Trivial lookups, near-zero reasoning |
| `"low"` | Fast | Lower | Latency-critical work (incident response, real-time chat, drafts), extraction, formatting, lookups |
| `"medium"` | Moderate | Moderate | Most tasks, including complex code and agents (higher first-pass accuracy) |
| `"high"` | Slower | Higher | Deep reasoning, math, hard multi-step work, research, planning |

**Defaults differ per model**: `medium` on 3.5/3.6/3.7/3.8 Flash; `high` on 3.1 Pro and 3 Flash; `minimal` on 3.5 Flash-Lite and 3.1 Flash-Lite. Coming from 3.1 Pro, the default drops from `high` to `medium`; coming from 3.5/3.6 Flash to 3.7/3.8, map any `minimal` usage to `low`.

**Never send `thinking_budget` together with `thinking_level`** in the same request -- the API returns a 400 error. `thinking_budget` is "no longer recommended" (AI Studio) / "deprecated" (Vertex) and kept only for backward compatibility; whether 3.7/3.8 Flash still accept it alone is unverified (Verify). Use `thinking_level`.

**3.8 Flash cost note**: it spends more tokens by design (smaller reasoning steps, iterative tool calls, self-verification), especially at higher levels. Use `low` for everyday tasks, or stay on 3.7 Flash for efficiency-first workloads. Intro price $0.75/$3.75 per 1M runs to Dec 31 2026, then $1.50/$7.50 from Jan 1 2027 (same intro/then pricing on 3.6 and 3.7 Flash).

### 1.4 Omit Sampling Parameters

**CRITICAL**: **OMIT** `temperature`, `top_p`, and `top_k` entirely. They were formally **deprecated on Jul 21 2026**.

- **3.6 Flash and later, and 3.5 Flash-Lite**: the API silently **ignores** them (a no-op, not an error -- easy to miss in audits). Google says "future model generations" will return **400**.
- **3.5 Flash, 3.1 Pro, 3 Flash**: still honored, and sub-1.0 temperature **may** cause looping and degraded performance on reasoning tasks (Google's wording -- not a guaranteed failure)
- On 3.8 Flash, `frequency_penalty`, `presence_penalty` and `candidate_count` return an **error**. Remove them too (`candidate_count` is unsupported on all 3.x)
- Do not carry over sampling-param tuning from earlier Gemini generations
- For determinism, define a system instruction with explicit rules and add a response schema (or fix `thinking_level`); steer style, tone, and variety through the prompt
- **Prefill is gone**: a request whose last non-empty turn is a `model` turn returns **400** on 3.6 Flash and later. Anchor output with `system_instruction` or a response schema
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

> **Rewritten September 2026.** Earlier editions told you to put formatting and
> negative constraints **last**. That rule came from the Vertex Gemini 3
> prompting guide, which now returns 404 (last archived May 2026). Google's live
> prompting-strategies documentation says: put "essential behavioral
> constraints, role definitions (persona), **and output format requirements**" in
> the system instruction or at the very beginning. Only the *specific question*
> goes last, and only when it follows a long context. Google's Vertex
> prompt-design page still suggests an optional end-of-prompt recap.

Put every constraint that governs behavior or output shape **at the TOP**, in
the system instruction where possible. The "last" slot is reserved for the
specific ask, and exists to solve a different problem: in long-context prompts,
a question buried above 100K tokens of source material gets lost.

**Recommended hierarchy**:
1. System instruction: persona, tone, safety rules, **and output-format requirements** -- TOP
2. Context and source material
3. Main task instructions
4. The specific question -- LAST (this is the long-context rule, not a constraint rule)
5. Optional: a short recap of hard negative/quantitative limits at the very end

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

Gemini 3.x defaults to **terse** responses; ask explicitly for a conversational or detailed style.

| Desired Style | Prompt Addition |
|---------------|-----------------|
| More conversational | "Explain as a friendly, talkative assistant." |
| Detailed explanation | "Provide a comprehensive, detailed response." |
| Technical depth | "Include technical details and edge cases." |
| Faster (with low thinking) | `thinking_level: "low"` + "Think silently." |

### Structured Output for Format Anchoring

The Gemini API has **no `prefix` parameter**, and a request ending in a `model` turn is a 400 on 3.6+. To enforce output shape, use structured output. On `generate_content` (legacy, fully supported):

```python
from google import genai
from pydantic import BaseModel

class User(BaseModel):
    name: str
    email: str

client = genai.Client()
response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="Return user data as JSON: ...",
    config={
        "response_mime_type": "application/json",
        "response_schema": User,
    },
)
```

On the Interactions API (GA, recommended) `response_mime_type` is removed; use `response_format: {type: "text", mime_type: "application/json", schema: {...}}`.

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

Google recommends **always** including few-shot examples for Gemini ("prompts without few-shot examples are likely to be less effective"), more than other providers. Use "a few" and experiment:

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
- Use a few examples and experiment with the count; too many overfit
- Format demos only -- no reasoning steps inside examples
- Use output prefixes inside the examples to anchor format

---

## 8. Persona Usage

- Put the persona at the top (system instruction)
- Gemini 3.x treats assigned personas **very seriously**; the model may ignore instructions that conflict with the persona (this rule comes from the archived Vertex guide -- keep it, but treat it as historical)
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

*(Figures in this Deep Research section — "40-250+ sites", "$20/mo", "30k characters" — are carried over; not re-verified this cycle.)*

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
- OMIT temperature/top_p/top_k entirely (deprecated Jul 21 2026; ignored on 3.6+, 400 on future generations, can loop on 3.5 Flash/3.1 Pro/3 Flash)
- Use thinking_level per model: 3.8/3.7 Flash = low|medium(default)|high; 3.6/3.5 Flash = minimal|low|medium(default)|high; 3.1 Pro = low|medium|high(default)
- Never send thinking_budget + thinking_level together (400 error)
- Return thought signatures unmodified in stateless multi-turn function calling (even across model switches)
- State the current year for time-sensitive queries (3.5 Flash cutoff Jan 2025)
- Be direct; ask explicitly for a longer/conversational style (default is terse)
- Put persona, behavioral constraints AND output-format requirements at the TOP (system instruction)
- Put context FIRST, the specific question LAST
- Include a few examples with identical formatting
- Anchor transitions: "Based on the above..."
- Label multimodal inputs explicitly

DON'T:
- Send temperature/top_p/top_k at all; on 3.8 also frequency_penalty/presence_penalty/candidate_count (error)
- End a request with a prefilled model turn (400 on 3.6+)
- Send thinking_level "minimal" to 3.7/3.8 Flash or 3.1 Pro (error)
- Bury the specific question above a long context
- Use conversational language ("please", "kindly")
- Use complex CoT from Gemini 2.x era
- Use broad "do not infer" (be specific instead)
- Demand XML/JSON status text right before a tool call (Malformed_Function_Call)

PROMPT ORDER:
1. System instruction: persona/tone/safety AND output-format rules -- TOP
2. Context/source material
3. Main task
4. The specific question LAST (keeps the ask from being buried)
5. Optional recap of hard limits at the very end

VERBOSITY: Default = terse
- More verbose: "Explain as friendly, talkative assistant"
- Faster: thinking_level=low + "Think silently"

TEMPLATE:
<role>[persona]</role>
<constraints>[behavioral + output-format rules -- TOP]</constraints>
<context>[all background first]</context>
<task>[direct instruction -- no fluff]</task>
<final_instruction>[optional recap of hard limits]</final_instruction>
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
[optional recap of hard limits]
</final_instruction>
```

---

## 12. Function Calling

### State: Interactions API vs Stateless

The Interactions API (GA, recommended) defaults to stateful mode (`store: true` + `previous_interaction_id`): the server handles thought signatures and reasoning carry-over, so you do nothing. Retention is 55 days on the paid tier, 1 day on the free tier; `store=false` gives stateless mode. On `generateContent` (legacy) or any stateless setup you manage history yourself, and the rules below apply.

### Thought Signatures

In stateless multi-turn, Gemini 3.x returns **thought signatures**. Resend all thought blocks **exactly as received** in the next turn's history; dropping or altering them breaks reasoning continuity and degrades multi-turn tool-use quality.

- Resend the previous model's thought blocks even when you **switch models** mid-session
- Built-in tools (e.g. Google Search) carry their own signatures on their call and result blocks; resend those too
- Interactions API: signatures appear only on thought steps and built-in tool steps. `generateContent`: a signature can sit on any part, including inside `functionCall` parts
- From 3.5 Flash on, `generateContent` reuses reasoning from earlier turns when signatures are present -- pass the full, unmodified history

### Strict Function-Response Matching

Each function call must be matched by exactly **one** function response, matched by both `id` (Interactions: `call_id`) and `name`. Do not:
- Omit a response for a call the model made
- Send multiple responses for a single call
- Mismatch the `id`/`name` pairing between call and response

The Interactions API returns an error on a mismatch. `generateContent` does not error, but in most cases returns an **empty response with `finish_reason: STOP`** -- easy to misread as a model failure.

### Function-Response Content

- Put multimodal content **inside** the function response parts, not beside them (content outside can cause "thought leakage")
- Append extra instructions to the **end of the function-response text, separated by `\n\n`**, not as separate parts

### Pre-Tool Text

If a prompt makes the model emit structured text (`<UPDATE>...</UPDATE>`, XML, YAML, JSON) right before a tool call, the call can fail with `Malformed_Function_Call`. Preferred fix: declare an `update(previous_step, plan, next_step, external)` function and tell the model to call it before other tools. Alternatives: Markdown headers (`# UPDATE`) instead of structured text, or do not require pre-tool text.

### Tool Set and Over-Calling

- Keep the active set to **10-20 tools** maximum
- `tool_choice` modes: `auto` (default), `any`, `none`, `validated`
- To reduce tool over-calling, first lower `thinking_level`; if that is not enough, add "You have a limited action budget of <n> tool calls. Use them efficiently."

---

## References

- [Vertex AI Overview of Prompting Strategies](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/prompts/prompt-design-strategies)
- [Vertex AI Gemini 3.x Prompting Guide](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/start/gemini-3-prompting-guide) (now 404; last archived May 15 2026 -- source of the historical persona rule)
- [Google AI Prompting Strategies](https://ai.google.dev/gemini-api/docs/prompting-strategies)
- [Gemini API: What's new in Gemini 3.8 Flash](https://ai.google.dev/gemini-api/docs/latest-model)
- [Gemini API: Function calling](https://ai.google.dev/gemini-api/docs/function-calling)
