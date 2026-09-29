# Techniques, Patterns & Anti-Patterns (September 2026 Edition)

This module is the **canonical home for all prompting techniques and ALL anti-patterns**. No other module duplicates these. Auto-loaded by the main entry point.

> **Thinking modes**: Foundations covered in 01; model-specific details in 06/07/08.
> **Model specs**: See 03-model-catalog_v5.md.

---

## 1. Zero-Shot Prompting (Preferred Approach)

**Definition**: Direct instruction without examples, relying on the model's pre-trained knowledge and native reasoning.

**Status**: The **default approach** for all reasoning models (Claude 5/5.1/5.5 family, GPT-5.x/GPT-6, Gemini 3.x).

**When to use**: Almost always. Start here.

**Pattern**:
```
[Task instruction]

<context>
[Relevant background]
</context>

<data>
[Input content]
</data>

Return as [format specification].
```

**Example**:
```
Analyze this code for security vulnerabilities.

<context>
Production authentication module for a financial API.
</context>

<code>
[code block]
</code>

Return findings as JSON: {"vulnerabilities": [{"type": "", "severity": "", "remediation": ""}]}
```

---

## 2. Few-Shot Prompting (Use Sparingly)

**Definition**: Instruction with exemplars demonstrating desired patterns.

**Status**: Use **only when necessary** -- can reduce performance with reasoning models.

**When to use**:
- Demonstrating a specific, non-standard output format (1-2 examples)
- Non-standard patterns not in training data
- Legacy models without native reasoning

**When NOT to use**:
- Teaching reasoning on GPT and other reasoning models (they do this internally)
- Standard tasks
- More than 2 examples on GPT and other reasoning models (Claude and Gemini are exempt -- see below)

**Pattern (minimal)**:
```
[Task instruction]

Example:
Input: [example input]
Output: [example output]

Now process:
Input: [actual input]
Output:
```

**Claude exception**: Anthropic recommends 3-5 diverse, relevant examples in `<example>` tags, and allows `<thinking>` inside them to show the reasoning pattern. See 06-claude-practices_v5.md.

**Gemini exception**: Google recommends always including a few examples with identical formatting (too many overfit). See 07-gemini-practices_v5.md for details.

---

## 3. Role Prompting (Still Effective)

**Definition**: Assigning expertise identity to constrain responses within a domain.

**Pattern**:
```
You are a [expert_type] specializing in [domain].

[Task instruction]

[Context/data]
```

**Best practices**:
- Keep role descriptions concise (1-2 sentences)
- Focus on domain expertise, not reasoning instructions
- Avoid over-specifying (models infer well from role context)

**Accuracy tasks**: skip the persona on factual, math, or code work (AP-11).

**Gemini caution**: Gemini 3.x takes personas very seriously and may ignore instructions that conflict with the assigned role. Be explicit about persona boundaries.

---

## 4. Instruction-Based Prompting (Core Approach)

**Definition**: Explicit, structured directives specifying task requirements, constraints, and output format.

**Instruction Hierarchy (recommended order)**:
```
[System Context] -> [Task Instruction] -> [Examples] -> [Input Data] -> [Output Format] -> [Constraints]
```

| Component | Purpose | Token Budget |
|-----------|---------|--------------|
| System Context | Role, domain | 5-10% |
| Task Instruction | Actionable directive | 5-10% |
| Examples | Format demo (0-1) | 0-10% |
| Input Data | Content to process | 40-60% |
| Output Format | Schema/structure | 5-10% |
| Constraints | Boundaries, limits | 5-10% |

**Gemini-critical**: Place essential constraints and output-format requirements **in the system instruction, at the TOP**. Only the specific question goes last, and only to keep it from being buried under a long context. (Corrected July 2026, still current -- earlier editions of this guide said "constraints LAST", which contradicts Google's prompting-strategies documentation.)

---

## 5. Multi-Turn Prompting

**Definition**: Sequential interaction where context accumulates across exchanges.

**Pattern**:
```json
[
  {"role": "system", "content": "[system instructions]"},
  {"role": "user", "content": "[initial query]"},
  {"role": "assistant", "content": "[response 1]"},
  {"role": "user", "content": "[follow-up]"},
  {"role": "assistant", "content": "[response 2]"}
]
```

**2026 Considerations**:
- Context compaction handles long conversations automatically
- Save critical state to files/memory before compaction
- Monitor reasoning token overhead in multi-turn
- Large windows (1M-class; 10M on Llama 4 Scout) allow extensive conversation history

---

## 6. Structured Output Prompting

**Definition**: Requesting specific output formats for programmatic processing.

**Pattern**:
```
[Task instruction]

[Context/data]

Return results as JSON matching this schema:
{
  "field1": "type (description)",
  "field2": ["array of type"],
  "nested": {
    "subfield": "type"
  }
}
```

**Best practices**:
- Specify exact schema with types
- Use native JSON mode when available (GPT-5.x/GPT-6, Gemini)
- For Claude: XML output tags guide structure effectively
- Validate output programmatically
- For Gemini: Use response prefixes to anchor format

---

## 7. Multimodal Prompting

**Definition**: Combining multiple data modalities (text, images, audio, video).

**Pattern**:
```
I've provided:
- Image 1: [description]
- Image 2: [description]
- Document: [description]

Task: [instruction referencing specific modalities]

Return [format].
```

**Best practices**:
- Label each modality explicitly (critical for Gemini 3.x)
- Don't over-instruct cross-modal reasoning -- models handle integration natively
- Provide clear context per modality
- Specify which modalities to use for which aspects

---

## 8. Prompt Chaining

**Definition**: Decomposing complex tasks into sequential sub-tasks with output flowing between steps.

**When to use**: Complex workflows where each step needs different context or processing.

**Pattern**:
```python
chain = [
    {"step": "extract", "prompt": "Extract key entities from: {input}"},
    {"step": "analyze", "prompt": "Analyze relationships between: {entities}"},
    {"step": "synthesize", "prompt": "Create report from: {analysis}"}
]
```

**Best practices**:
- Each step has simple, clear prompt
- Let model reason at each step independently
- Use thinking modes when available
- Don't prescribe inter-step reasoning

---

## 9. ReAct Pattern (Reasoning + Acting)

**Definition**: Interleaving reasoning with tool execution.

**Status**: Still relevant for agentic systems, but simplified.

**2026 approach**: Don't prescribe "Thought/Action/Observation" format. Models manage reasoning-action cycles internally with native tool calling.

**Pattern**:
```
Complete this task: [goal]

Available tools: [tool list with 1-2 sentence descriptions]

Use tools as needed. Report results when done.
```

> **Deep guidance**: See 10-agentic-patterns_v5.md for full agentic patterns.

---

## 10. Self-Consistency (Reduced Necessity)

**Definition**: Sampling multiple reasoning paths and selecting by consensus.

**Status**: Mostly unnecessary with reasoning models (native consistency is high).

**When still useful**:
- High-stakes decisions requiring verification
- Tasks where model confidence varies significantly

**Pattern** (if needed):
```python
# N independent runs at default sampling. Do NOT set temperature: non-default returns 400 on Claude 5.x
# and is deprecated/ignored on Gemini 3.6+.
responses = [model.generate(prompt) for _ in range(3)]
return majority_vote(responses)
```

**2026 Alternative**: Use the model's native reasoning and ask for a checkable output contract instead of a "verify" instruction (AP-16):
```
Solve this problem. End with a Verdict section: final answer, confidence, and the evidence relied on.
```

---

## 11. Context Engineering Pattern

**Definition**: Strategic context structure for optimal model performance.

**Pattern**:
```xml
<context>
  <background>
    Domain-specific information and relevant facts
  </background>
  <data>
    Input data, properly structured
  </data>
</context>

<task>
Clear, direct instruction
</task>

<output_format>
Desired format specification
</output_format>
```

**Optimization priorities**:
1. Context quality (highest ROI)
2. Output format clarity
3. Instruction simplicity
4. Model-specific parameters
5. Thinking mode configuration

---

## ANTI-PATTERNS (Canonical Reference)

All anti-patterns are documented here and only here. Other modules cross-reference this section.

### AP-1: Over-Engineering

**Applies to: all models. Severity: Warning.**

**The #1 issue with reasoning models.**

Detection:
- Prompt >500 tokens for simple tasks
- Multiple pages of instructions
- Elaborate CoT frameworks
- Excessive few-shot (>5 examples; 3-5 is vendor-recommended on Claude and Gemini)
- Five or six or more simultaneous hard constraints (joint compliance collapses past about 5-6; conflicting pairs such as JSON-only plus a word count do the most damage)

**Fix**: state the task in one sentence, keep only the constraints the task needs, and consolidate conflicting ones or split them into separate calls.

**Bad**:
```
You are an expert analyst. Please carefully consider the following task.
I need you to analyze this data, and here's how you should do it:
Step 1: First, read through the entire dataset carefully
Step 2: Then, identify the key patterns
Step 3: Next, think about what those patterns mean
Step 4: Consider alternative interpretations
Step 5: Weigh the evidence for each interpretation...
[continues for paragraphs]
Here are 5 examples of how to do this correctly:
[long examples with reasoning]
```

**Good**:
```
Analyze this dataset for patterns.

<context>Sales data from Q1-Q4 2025, regions and product categories</context>
<data>[dataset]</data>

Return JSON: {"patterns": [], "insights": [], "confidence": 0.0-1.0}
```

### AP-2: Explicit CoT with Reasoning Models

**Scope: models with extended thinking ENABLED. Severity: Critical.** When thinking is off (Opus 4.8
default, Haiku 4.5, legacy/open-weight models), manual CoT is a supported technique
that vendors still document -- not an anti-pattern. See "When Explicit CoT Still
Works" in 01-foundations. Confirm the target is actually a reasoning model before flagging.

**Exceptions**:
- **Gemini (still a hit)**: a live "step by step" instruction on Gemini is flagged because thinking is on, but Google's own template ships such a line, so deleting it is low-risk. Say so in the finding.
- **Sonnet 5.5 (not a hit)**: Anthropic's closing "think the problem through" line for JSON reasoning with adaptive thinking is official guidance.

Detection (thinking-enabled targets only):
- Contains "Let's think step by step"
- Contains "Step 1:", "Step 2:", etc.
- Prescriptive reasoning instructions

**Bad**: `"Let's approach this step by step: First, analyze component A. Then, examine component B..."`

**Good**: `"Analyze the relationship between components A and B. Explain the implications."`

### AP-3: Excessive Few-Shot

**Applies to: reasoning models except Claude and Gemini. Severity: Warning.**

> **Claude and Gemini are exempt.** Anthropic recommends **3-5 diverse, relevant
> examples** in `<example>` tags and allows `<thinking>` inside them to show the
> reasoning pattern. Google recommends always including a few identically formatted
> examples. Do not flag either. Legacy and open-weight models without native
> reasoning are also exempt.

Detection (GPT and other reasoning models):
- More than 2 examples
- Examples showing reasoning steps (the model reasons natively -- demo the FORMAT, not the thinking)
- Examples consuming >30% of prompt tokens

**Bad**:
```json
{
  "examples": [
    {"input": "...", "reasoning": "step 1... step 2...", "output": "..."},
    {"input": "...", "reasoning": "step 1... step 2...", "output": "..."},
    {"input": "...", "reasoning": "step 1... step 2...", "output": "..."}
  ]
}
```

**Good**: at most 2 examples showing the output FORMAT only -- no reasoning steps.
(On Claude and Gemini, 3-5 diverse examples are fine; redundant near-identical examples are still waste.)

### AP-4: Conversational Fluff

**Applies to: all models; worst on Gemini. Severity: Info.** Especially harmful for Gemini 3.x where it degrades instruction-following.

| Phrase | Token Cost | Signal Value | Verdict |
|--------|------------|--------------|---------|
| "Hello! I hope you're doing well" | 8-12 | Zero | Remove |
| "Could you please help me" | 5-7 | Zero | Remove |
| "Thank you so much!" | 4-5 | Zero | Remove |
| "I would really appreciate if" | 6-8 | Zero | Remove |
| "When you have a moment" | 5 | Zero (models are instant) | Remove |

**Impact by model**:
- **Gemini 3.x**: Actively degrades instruction-following
- **Claude 5/5.1/5.5 family**: Tolerates but gains nothing
- **GPT-5.x / GPT-6**: Neutral impact, wastes tokens

**Bad** (for Gemini):
```
Hello! I hope you're doing well today. If you could please help me with this
task, I would greatly appreciate it. Could you kindly analyze the following
data when you have a moment? Thank you so much!
```

**Good**:
```
Analyze this data. Return results as JSON.
```

### AP-5: Sampling Misconfiguration (Gemini, Claude, Kimi)

**Applies to: Gemini, Claude, Kimi. Severity: Critical.** Any `temperature`/`top_p`/`top_k` on Gemini or Kimi; non-default sampling on current Claude.

**Omit sampling parameters entirely** and steer determinism from the prompt (`Output JSON only. Copy values verbatim.`). Omit -- do not "set to 1.0".

- **Claude 5 family**: non-default sampling returns 400.
- **Kimi K3/K2.7/K2.6**: sampling is fixed server-side; any value errors.
- **Gemini 3.x**: sub-1.0 temperature still loops on older 3.x; on 3.6+ the parameters are ignored (a silent no-op -- an audit blind spot); expect 400 on future generations. Gemini 3.8 variants also take no `candidate_count`, `frequency_penalty` or `presence_penalty`.
- **DeepSeek thinking mode** silently ignores temperature and penalties.
- **Muse Spark** accepts temperature, but clearer instructions beat lowering it.

### AP-6: "Think" Word Sensitivity (Claude)

**Applies to: Claude, extended thinking disabled only. Severity: Info.** Do not flag the word when thinking is enabled.

When extended thinking is **disabled**, Claude can be sensitive to the word "think". Anthropic documents this for Opus 4.5 specifically -- treat it as a known behavior to test for, not a guaranteed property of every Claude model.

| Avoid | Use Instead |
|-------|-------------|
| "think about" | "consider" |
| "think through" | "evaluate" |
| "think carefully" | "assess" |
| "thinking" | "reasoning" |

### AP-7: Tool Description Verbosity

**Applies to: GPT only. Severity: Warning.** OpenAI asks for what the tool does, **when to use it**, return fields and error behavior -- concisely -- and for only task-relevant tools. The finding is redundancy, policy prose and irrelevant tools exposed, never the "when to use" clause. Anthropic recommends stating what the tool does and when to use it; Google documents no maximum -- a long Claude or Gemini tool description is not a finding.

**Bad**:
```json
{
  "description": "This function allows you to search through the customer
  database. You should use this when the user asks about a customer. It can
  search by name or ID. When searching by name, partial matches are returned.
  Make sure to validate input first. If ambiguous, ask for clarification..."
}
```

**Good**:
```json
{
  "description": "Search customers by name or ID when the user asks about a customer. Returns id, name, status; errors on no match."
}
```

### AP-8: Prescribing Tool Sequence

**Applies to: agentic. Severity: Warning.**

**Bad**: "First use tool A, then tool B, then tool C"

**Good**: State goal + constraints, let model plan tool usage.

### AP-9: Over-Prompting GPT

**Applies to: GPT-5.x, GPT-6. Severity: Warning.**

GPT models perform better with an outcome statement plus constraints. Quality drops as instruction volume rises past what the task needs (OpenAI internal, directional: +10-15% score, -41-66% tokens). Recipe-style guidance over-constrains GPT-6 Astra; the harm is conflicting or excess rules, not length alone. XML tags are still fine as structure.

### AP-10: Ignoring Model-Specific Parameters

**Applies to: all models. Severity: Critical.** Effort, verbosity and thinking depth are configuration, not prose -- asked for in text they are a suggestion; set in the call they are binding. Each model family has parameters that significantly affect output (enums per model: see 03-model-catalog_v5.md):
- Claude 5/5.1/5.5 family: `output_config.effort` (primary cost lever), adaptive thinking defaults
- GPT-5.x / GPT-6: `reasoning_effort` (enum is per model)
- Gemini 3.x: `thinking_level` (OMIT temp/top_p/top_k)

### AP-11: Persona on Accuracy/Explanatory Tasks

**Applies to: all models. Severity: Warning.**

"You are a world-class expert" on math/coding/factual/explanatory tasks trades clarity for depth with no broad capability gain (MMLU 71.6%→66.3%). Persona helps only advisory/depth tasks.

### AP-12: "Never Hallucinate" Instruction

**Applies to: all models. Severity: Info.**

"Never hallucinate", "do not make up information" has no mechanism and wastes tokens. Use grounding techniques instead (cite sources, quote context, request calibrated uncertainty).

### AP-13: Agentic Over-Eagerness Unmanaged

**Applies to: agentic. Severity: Warning.**

No stop conditions, no "what DONE looks like", no scope limits, no subagent cap in agentic prompts leads to runaway execution, unrequested actions, and scope creep.

**Inverse**: GPT-6 Astra under-acts (premature stops, approval-seeking). Fix with a completion definition plus an initiative line, not more caution.

### AP-14: "Think Harder/Keep Going" on Reasoning Models

**Applies to: reasoning models. Severity: Critical.**

"Think more", "think longer", "keep reasoning" causes harmful overthinking that corrupts already-correct answers (stop-early = +21% accuracy, arXiv:2606.02835). Lower the effort parameter instead -- but note effort is soft behavioral guidance, not a hard cap. `max_tokens` is the only strict ceiling.

### AP-15: Offset-from-End References (Position Curse)

**Applies to: long context. Severity: Warning.**

"The second-to-last item", "the last two lines" -- models mis-locate list tails even in tiny lists (arXiv:2605.07127, May 2026). Use forward indices or unique anchors instead.

### AP-16: Verification Instructions on Opus 5 / GPT-6 Astra

**Applies to: Opus 5, GPT-6 Astra. Severity: Warning.**

Opus 5 self-verifies by default; Astra self-tests and over-tests. Explicit instructions like "double-check" or "verify your answer" buy cost and no accuracy gain.

**Not a hit**: Fable 5/5.1 guidance asks for explicit periodic self-checks on long runs. Opus 5.5 inherits the Opus 5 behavior as a starting point only (Verify). Sonnet 5.5 at `xhigh`/`max` needs an additive "stop and report when checks pass" line instead.

**Fix**: remove the behavioral instruction ("verify your findings") and keep the requirement as an **output-format contract** -- a `Sources`, `Limits` or `Verdict` section. Boundaries: the contract names sections and their contents, never an action verb; and it targets *self*-verification only -- "cross-reference three sources" inside a fact-check is the task definition, and deleting it breaks the task.

### AP-17: Reasoning Echo (Fable 5/5.1, Mythos, Opus 5.5, Sonnet 5.5)

**Applies to: Fable 5/5.1, Mythos, Opus 5.5, Sonnet 5.5. Severity: Critical.**

Detection:
- Contains "show your reasoning"
- Contains "explain your thought process"
- Contains "output your thinking" or "write out your reasoning in the response"

Requesting a model with a `reasoning_extraction` classifier to expose its internal reasoning triggers a refusal -- now billed, and never fallback-retried. **Fix**: read the summarized thinking blocks instead, or ask for a `Basis` section listing the evidence used and the confidence. Justification of the *output* is a different request and is answered normally.

### AP-18: Over-Prescriptive Fable Prompts

**Applies to: Fable 5, Fable 5.1. Severity: Info.**

Anthropic's wording: a brief instruction "can be as effective as" enumerating each desired behavior for Fable 5 and Fable 5.1. Replace ten enumerated behaviors with the one instruction that covers them. Prefer brevity because it costs less and is easier to maintain -- not because enumeration is documented to degrade output.

### AP-19: Overthinking DoS

**Applies to: reasoning models. Severity: Warning.**

Adversarial, logically-inconsistent prompts force runaway chain-of-thought in reasoning models. Cap thinking budgets in production (ICML 2026): a `max_tokens` ceiling, an input-length limit, and a pre-dispatch check that rejects self-contradictory instructions.

---

## Technique Decision Tree

```
START -> Is this a reasoning model (Claude 5/5.1/5.5 family / GPT-5.x / GPT-6 / Gemini 3.x)?
  |
  +-- YES -> Use zero-shot first
  |           |
  |           +-- Works? -> Done
  |           |
  |           +-- Need format demo? -> Add 1 example (format only)
  |           |
  |           +-- Need deeper reasoning? -> Enable thinking mode
  |
  +-- NO -> Legacy model
            |
            +-- Standard task? -> Zero-shot + CoT
            |
            +-- Complex pattern? -> Few-shot (2-3 examples; 3-5 on Claude/Gemini)
```

---

## Best Practices Summary

**DO**:
1. Use zero-shot as default
2. Provide rich, structured context
3. Specify clear output format (JSON schema)
4. Use XML tags for Claude, Markdown for others
5. Leverage native thinking modes
6. Keep GPT tool descriptions concise: what, when to use, returns, errors (AP-7)
7. Omit `temperature`/`top_p`/`top_k` for Gemini (AP-5)
8. Give models space to reason
9. Explain WHY, not just WHAT (especially Claude)
10. Place constraints in the system instruction (TOP) for Gemini; question last

**DON'T**:
1. Use complex CoT with reasoning models **when thinking is enabled** (AP-2)
2. Provide >2 few-shot examples on GPT/other reasoning models, or examples that show reasoning steps (AP-3; Claude 3-5 and Gemini a few are fine)
3. Use conversational padding (AP-4)
4. Set any sampling param on Gemini (AP-5)
5. Say "think" with Claude thinking disabled (AP-6)
6. Write verbose or redundant GPT tool descriptions (AP-7)
7. Prescribe exact tool sequences (AP-8)
8. Over-prompt GPT models (AP-9)
9. Ignore model parameters (AP-10)
10. Over-engineer prompts (AP-1)

---

## References

- Wei, J., et al. (2022). "Chain-of-Thought Prompting." [arXiv:2201.11903](https://arxiv.org/abs/2201.11903) -- Historical context
- Yao, S., et al. (2023). "Tree of Thoughts." [arXiv:2305.10601](https://arxiv.org/abs/2305.10601) -- Legacy technique
- Yao, S., et al. (2022). "ReAct." [arXiv:2210.03629](https://arxiv.org/abs/2210.03629) -- Still applicable for agents
- Liu, P., et al. (2023). "Pre-train, Prompt, and Predict." [ACM Computing Surveys](https://dl.acm.org/doi/abs/10.1145/3560815)
- White, J., et al. (2023). "Prompt Pattern Catalog." [arXiv:2302.11382](https://arxiv.org/abs/2302.11382)
