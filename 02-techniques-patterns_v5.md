# Techniques, Patterns & Anti-Patterns (2026 Edition)

This module is the **canonical home for all prompting techniques and ALL anti-patterns**. No other module duplicates these. Auto-loaded by the main entry point.

> **Thinking modes**: Foundations covered in 01; model-specific details in 06/07/08.
> **Model specs**: See 03-model-catalog_v5.md.

---

## 1. Zero-Shot Prompting (Preferred Approach)

**Definition**: Direct instruction without examples, relying on the model's pre-trained knowledge and native reasoning.

**Status**: The **default approach** for all reasoning models (Claude 5 family, GPT-5.x, Gemini 3.x).

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
- Demonstrating a specific, non-standard output format (1 example)
- Non-standard patterns not in training data
- Legacy models without native reasoning

**When NOT to use**:
- Teaching reasoning (models do this internally)
- Standard tasks
- More than 2 examples

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

**Gemini exception**: Google recommends 2-3 few-shot examples with consistent formatting for Gemini models. See 07-gemini-practices_v5.md for details.

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

**Gemini-critical**: Place essential constraints and output-format requirements **in the system instruction, at the TOP**. Only the specific question goes last, and only to keep it from being buried under a long context. (Corrected July 2026 -- earlier editions of this guide said "constraints LAST", which contradicts Google's prompting-strategies documentation.)

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
- Large windows (1M-2M) allow extensive conversation history

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
- Use native JSON mode when available (GPT-5, Gemini)
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
responses = [model.generate(prompt, temperature=0.7) for _ in range(3)]
return majority_vote(responses)
```

**2026 Alternative**: Use the model's native reasoning with verification:
```
Solve this problem and verify your answer before responding.
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

**The #1 issue with reasoning models.**

Detection:
- Prompt >500 tokens for simple tasks
- Multiple pages of instructions
- Elaborate CoT frameworks
- Excessive few-shot (>5 examples; 3-5 is vendor-recommended)

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

**Scope: models with extended thinking ENABLED.** When thinking is off (Opus 4.8
default, Haiku 4.5, legacy/open-weight models), manual CoT is a supported technique
that vendors still document -- not an anti-pattern. See "When Explicit CoT Still
Works" in 01-foundations.

Detection (thinking-enabled targets only):
- Contains "Let's think step by step"
- Contains "Step 1:", "Step 2:", etc.
- Prescriptive reasoning instructions

**Bad**: `"Let's approach this step by step: First, analyze component A. Then, examine component B..."`

**Good**: `"Analyze the relationship between components A and B. Explain the implications."`

### AP-3: Excessive Few-Shot

> **Corrected July 2026.** Earlier editions of this KB set the warning line at
> >2 examples. Anthropic's own best-practices guidance recommends **3-5 diverse,
> relevant examples** in `<example>` tags. The anti-pattern is *redundant* examples
> and *reasoning-trace* examples -- not example count in the 3-5 range.

Detection:
- More than 5 examples (past that, added examples are usually redundant)
- Examples showing reasoning steps (the model reasons natively -- demo the FORMAT, not the thinking)
- Near-identical examples that cover the same case
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

**Good**: 3-5 diverse examples showing the output FORMAT only -- no reasoning steps.
Fewer is fine when the format is obvious; the ceiling matters more than the floor.

### AP-4: Conversational Fluff

**Especially harmful for Gemini 3.x where it degrades instruction-following.**

| Phrase | Token Cost | Signal Value | Verdict |
|--------|------------|--------------|---------|
| "Hello! I hope you're doing well" | 8-12 | Zero | Remove |
| "Could you please help me" | 5-7 | Zero | Remove |
| "Thank you so much!" | 4-5 | Zero | Remove |
| "I would really appreciate if" | 6-8 | Zero | Remove |
| "When you have a moment" | 5 | Zero (models are instant) | Remove |

**Impact by model**:
- **Gemini 3.x**: Actively degrades instruction-following
- **Claude 5 family**: Tolerates but gains nothing
- **GPT-5.x**: Neutral impact, wastes tokens

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

### AP-5: Temperature Misconfiguration (Gemini)

**Gemini 3.x: OMIT `temperature`/`top_p`/`top_k` entirely.** Official guidance is to remove them and use defaults; setting sub-1.0 temperature causes looping and degraded performance. Steer via prompt instead.

This is not a preference -- it's a hard requirement. The model's reasoning is calibrated for this setting.

### AP-6: "Think" Word Sensitivity (Claude)

When extended thinking is **disabled**, Claude can be sensitive to the word "think". Anthropic documents this for Opus 4.5 specifically -- treat it as a known behavior to test for, not a guaranteed property of every Claude model.

| Avoid | Use Instead |
|-------|-------------|
| "think about" | "consider" |
| "think through" | "evaluate" |
| "think carefully" | "analyze" |
| "thinking" | "reasoning" |

### AP-7: Tool Description Verbosity

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
  "description": "Search customers by name or ID. Returns customer details."
}
```

### AP-8: Prescribing Tool Sequence

**Bad**: "First use tool A, then tool B, then tool C"

**Good**: State goal + constraints, let model plan tool usage.

### AP-9: Over-Prompting GPT-5

GPT-5 models perform better with minimal prompts. Adding unnecessary instructions, verbose descriptions, or elaborate frameworks reduces quality.

### AP-10: Ignoring Model-Specific Parameters

Each model family has parameters that significantly affect output. Ignoring them wastes potential:
- Claude 5 family: `output_config.effort` (primary cost lever), adaptive thinking defaults
- GPT-5.x: `reasoning_effort` (none→xhigh)
- Gemini 3.x: `thinking_level` (OMIT temp/top_p/top_k)

### AP-11: Persona on Accuracy/Explanatory Tasks

"You are a world-class expert" on math/coding/factual/explanatory tasks trades clarity for depth with no broad capability gain (MMLU 71.6%→66.3%). Persona helps only advisory/depth tasks.

### AP-12: "Never Hallucinate" Instruction

"Never hallucinate", "do not make up information" has no mechanism and wastes tokens. Use grounding techniques instead (cite sources, quote context, request calibrated uncertainty).

### AP-13: Agentic Over-Eagerness Unmanaged

No stop conditions, no "what DONE looks like", no scope limits in agentic prompts leads to runaway execution, unrequested actions, and scope creep.

### AP-14: "Think Harder/Keep Going" on Reasoning Models

"Think more", "think longer", "keep reasoning" causes harmful overthinking that corrupts already-correct answers (stop-early = +21% accuracy, arXiv:2606.02835). Lower the effort parameter instead -- but note effort is soft behavioral guidance, not a hard cap. `max_tokens` is the only strict ceiling.

### AP-15: Offset-from-End References (Position Curse)

"The second-to-last item", "the last two lines" -- models mis-locate list tails even in tiny lists (arXiv:2605.07127, May 2026). Use forward indices or unique anchors instead.

### AP-16: Verification Instructions on Opus 5/Fable 5

Both Opus 5 and Fable 5 self-verify by default. Explicit instructions like "double-check" or "verify your answer" cause over-verification -- added cost, no accuracy gain.

### AP-17: Fable 5 Reasoning Echo

Detection:
- Contains "show your reasoning"
- Contains "explain your thought process"

Requesting Fable 5 to expose its internal reasoning triggers a `reasoning_extraction` refusal.

### AP-18: Over-Prescriptive Fable 5 Prompts

Anthropic's wording: a brief instruction "can be as effective as" enumerating each desired behavior for Fable 5. Prefer brevity because it costs less and is easier to maintain -- not because enumeration is documented to degrade output.

### AP-19: Overthinking DoS

Adversarial, logically-inconsistent prompts force runaway chain-of-thought in reasoning models. Cap thinking budgets in production (ICML 2026).

---

## Technique Decision Tree

```
START -> Is this a reasoning model (Claude 5 family / GPT-5.x / Gemini 3.x)?
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
            +-- Complex pattern? -> Few-shot (2-3 examples)
```

---

## Best Practices Summary

**DO**:
1. Use zero-shot as default
2. Provide rich, structured context
3. Specify clear output format (JSON schema)
4. Use XML tags for Claude, Markdown for others
5. Leverage native thinking modes
6. Keep tool descriptions to 1-2 sentences
7. Omit `temperature`/`top_p`/`top_k` for Gemini (AP-5)
8. Give models space to reason
9. Explain WHY, not just WHAT (especially Claude)
10. Place constraints in the system instruction (TOP) for Gemini; question last

**DON'T**:
1. Use complex CoT with reasoning models **when thinking is enabled** (AP-2)
2. Provide >5 few-shot examples, or examples that show reasoning steps (AP-3)
3. Use conversational padding (AP-4)
4. Set any sampling param on Gemini (AP-5)
5. Say "think" with Claude thinking disabled (AP-6)
6. Write verbose tool descriptions (AP-7)
7. Prescribe exact tool sequences (AP-8)
8. Over-prompt GPT-5 models (AP-9)
9. Ignore model parameters (AP-10)
10. Over-engineer prompts (AP-1)

---

## References

- Wei, J., et al. (2022). "Chain-of-Thought Prompting." [arXiv:2201.11903](https://arxiv.org/abs/2201.11903) -- Historical context
- Yao, S., et al. (2023). "Tree of Thoughts." [arXiv:2305.10601](https://arxiv.org/abs/2305.10601) -- Legacy technique
- Yao, S., et al. (2022). "ReAct." [arXiv:2210.03629](https://arxiv.org/abs/2210.03629) -- Still applicable for agents
- Liu, P., et al. (2023). "Pre-train, Prompt, and Predict." [ACM Computing Surveys](https://dl.acm.org/doi/abs/10.1145/3560815)
- White, J., et al. (2023). "Prompt Pattern Catalog." [arXiv:2302.11382](https://arxiv.org/abs/2302.11382)
