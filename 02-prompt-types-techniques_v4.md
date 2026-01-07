# Prompt Types & Advanced Techniques (2025 Edition)

This technical reference documents the primary prompt types and advanced techniques used in AI systems development, updated with 2025 best practices for reasoning models.

---

## 1. Zero-shot Prompting (2025: Preferred Approach)

**Technical Definition**: Direct instruction without examples, relying on the model's pre-trained knowledge and native reasoning capabilities.

**⚠️ 2025 CRITICAL UPDATE**: Zero-shot is now the **PREFERRED** approach for reasoning models (GPT-5.x, Claude 4.x, Gemini 3.x).

**Implementation Characteristics**:
- Token efficiency: Minimal token consumption
- Implementation complexity: Low
- Response predictability: **High** (with reasoning models)
- **Native reasoning**: Models engage internal CoT automatically

**Technical Applications**:
- Almost all tasks with reasoning models
- Standard NLP tasks (classification, translation, summarization)
- Knowledge retrieval
- Complex reasoning (reasoning models handle this natively)

**Implementation Pattern (2025)**:
```
{
  "instruction": "Perform [task] on [input]",
  "context": "[relevant background]",
  "input": "[content]"
}
```

**Optimization Parameters (2025)**:
- Instruction clarity: **Critical**
- Context richness: **High priority**
- Context structure: **Use XML tags for Claude**
- Temperature: Task-dependent (1.0 for Gemini 3.x)
- Thinking mode: Let model decide (auto)

**Example (2025 Best Practice)**:
```
Analyze the following code for security vulnerabilities.

<context>
This is production code handling user authentication.
</context>

<code>
[code block]
</code>

Return findings as JSON with vulnerability type, severity, and remediation.
```

---

## 2. Few-shot Prompting (2025: Use Sparingly)

**Technical Definition**: Instruction with exemplars demonstrating the desired pattern, enabling in-context learning.

**⚠️ 2025 CRITICAL UPDATE**: Few-shot can **REDUCE** performance with reasoning models by overwhelming internal reasoning. Use only when absolutely necessary.

**Implementation Characteristics**:
- Token consumption: High (scales with example count)
- Pattern recognition: **Native in reasoning models**
- Consistency: Can be lower with reasoning models if overused
- **Risk**: May interfere with native reasoning

**When to Use (2025)**:
- ✅ Demonstrating **specific output format** (1 example)
- ✅ Non-standard patterns not in training data
- ✅ Legacy models without native reasoning
- ❌ **NOT** for teaching reasoning (models do this internally)
- ❌ **NOT** for standard tasks

**Implementation Pattern (2025 - Minimal)**:
```
{
  "instruction": "Perform [task] following this format:",
  "examples": [
    {"input": "[example_input_1]", "output": "[example_output_1]"}
  ],  # MAX 1-2 examples
  "input": "[actual_input]"
}
```

**Technical Considerations (2025)**:
- **Optimal example count**: 1-2 (reduced from 3-5)
- **Purpose**: Format demonstration ONLY
- **Avoid**: Showing reasoning steps (models have internal CoT)
- Context window awareness: Examples consume valuable tokens

**❌ Anti-pattern (2025)**:
```
# DON'T: Multiple examples showing reasoning steps
{
  "examples": [
    {"input": "...", "reasoning": "step 1... step 2...", "output": "..."},
    {"input": "...", "reasoning": "step 1... step 2...", "output": "..."},
    {"input": "...", "reasoning": "step 1... step 2...", "output": "..."}
  ]
}
# This overwhelms native reasoning in GPT-5.x, Claude 4.x, Gemini 3.x
```

---

## 3. Chain-of-Thought (CoT) Prompting - DEPRECATED

**⚠️ 2025 STATUS**: **DEPRECATED** for reasoning models

**Technical Definition**: A prompting technique that instructs the model to decompose reasoning into explicit intermediate steps before producing a final answer.

**Why Deprecated (2025)**:
- Reasoning models (GPT-5.x, Claude 4.x, Gemini 3.x) perform internal CoT automatically
- Explicit CoT prompts can **HINDER** performance
- Adds unnecessary tokens and constraints
- Models reason better when given space, not prescriptive steps

**Legacy Implementation Variants** (for historical reference):
1. **Zero-shot CoT**: `"Let's think step by step"` - **Obsolete**
2. **Few-shot CoT**: Providing examples with detailed reasoning steps - **Can reduce performance**
3. **Self-consistency CoT**: Multiple reasoning paths - **Unnecessary**

**2025 Replacement: Thinking Modes**

Instead of explicit CoT, use model-native thinking modes:

### Claude (Anthropic)
```xml
<thinking>
[Model uses this space autonomously]
</thinking>
```
Or use `/think`, `/megathink`, `/ultrathink` commands

### Gemini (Google)
```json
{
  "thinking": "auto",
  "temperature": 1.0  // REQUIRED
}
```

### GPT-5 (OpenAI)
```json
{
  "reasoning_profile": "deep"  // light, balanced, or deep
}
```

**When to Request Step-by-Step (2025)**:
- ✅ For **output transparency** (not reasoning guidance)
- ✅ For debugging/verification
- ✅ When user needs to see the logic

**Example (2025 - Output Transparency)**:
```
Solve this problem and show your work step by step.
[Not telling model HOW to think, but asking to SHOW thinking]
```

---

## 4. Role Prompting (Still Effective 2025)

**Technical Definition**: Assigning a specific identity or expertise profile to the model to constrain responses within a particular knowledge domain or communication style.

**2025 Status**: ✅ **Still effective** - works well with reasoning models

**Implementation Characteristics**:
- Domain specificity: High
- Response consistency: Improved
- Style adaptation: Strong

**Technical Applications**:
- Domain-specific responses
- Specialized knowledge tasks
- Style-constrained generation
- Perspective-based reasoning

**Implementation Pattern (2025)**:
```
{
  "system_role": "You are [expert_type] with expertise in [domain].",
  "instruction": "[task]",
  "context": "[content]"
}
```

**Best Practices (2025)**:
- Keep role descriptions concise
- Avoid over-specifying (reasoning models infer well)
- Focus on domain expertise, not reasoning instructions

**Example (2025)**:
```
You are a senior security engineer specializing in authentication systems.

Review this authentication flow for vulnerabilities.

[flow description]
```

---

## 5. Instruction-based Prompting (2025: Core Approach)

**Technical Definition**: Explicit, structured directives that precisely specify task requirements, constraints, and output format.

**2025 Status**: ✅ **Core best practice** - the foundation of modern prompting

**Implementation Characteristics**:
- Directive clarity: **Critical**
- Context richness: **High priority**
- Constraint definition: **Explicit but not over-constrained**
- **Simplicity**: Direct instructions > elaborate frameworks

**Technical Applications**:
- Data transformation
- Content generation with specific requirements
- Information extraction
- Format conversion
- All standard tasks

**Implementation Pattern (2025)**:
```
{
  "task": "[specific_action]",
  "context": "[relevant background]",
  "input": "[content]",
  "constraints": {
    "format": "[output_format]",
    "style": "[style_parameters]"
  }
}
```

**2025 Best Practices**:
- ✅ Clear, direct instructions
- ✅ Rich context
- ✅ Specific output format
- ❌ No conversational fluff (especially Gemini 3.x)
- ❌ Don't over-engineer
- ❌ Don't prescribe reasoning steps

**Example (2025)**:
```
Extract all mentioned dates and associated events from the text.

<context>
Historical document about World War II
</context>

<text>
[document text]
</text>

Return as JSON: {"dates": [{"date": "YYYY-MM-DD", "event": "description"}]}
```

---

## 6. Multi-turn Prompting

**Technical Definition**: Sequential interaction pattern where context from previous exchanges informs subsequent responses.

**2025 Status**: ✅ **Still effective and important**

**Implementation Characteristics**:
- Context retention: Critical
- State management: Required
- Token accumulation: Progressive (watch context limits)

**Technical Applications**:
- Conversational agents
- Interactive problem solving
- Progressive refinement
- Context-dependent tasks

**Implementation Pattern (2025)**:
```
[
  {"role": "system", "content": "[system_instructions]"},
  {"role": "user", "content": "[initial_query]"},
  {"role": "assistant", "content": "[response_1]"},
  {"role": "user", "content": "[follow_up_1]"},
  {"role": "assistant", "content": "[response_2]"}
]
```

**Technical Considerations (2025)**:
- Context window management: Even more critical with large windows (1M-2M tokens)
- Reasoning overhead: Account for thinking tokens
- Token efficiency: Monitor and optimize
- State tracking: Implement for complex interactions

---

## 7. Thinking Modes & Native Reasoning (2025 Core Feature)

**Technical Definition**: Model-native capabilities that expose or enhance internal reasoning processes without external prompt engineering.

**2025 Status**: ✅ **REPLACES** traditional CoT techniques

### 7.1 Claude (Anthropic) Thinking

**Method**: XML tags and slash commands

**Implementation**:
```xml
<thinking>
First, I need to identify the key components...
Then I'll analyze each component...
Finally, I'll synthesize the findings...
</thinking>

Based on this analysis, the answer is...
```

**Slash Commands**:
- `/think`: Standard thinking depth
- `/megathink`: Extended reasoning
- `/ultrathink`: Maximum reasoning depth

**Best Practice**: Let Claude decide when to think; provide good context

### 7.2 Gemini (Google) Thinking

**Method**: API parameter `thinking`

**⚠️ CRITICAL**: Temperature MUST be 1.0 for Gemini 3.x

**Implementation**:
```json
{
  "contents": [{"parts": [{"text": "Solve this complex problem..."}]}],
  "generationConfig": {
    "thinking": "auto",  // or explicit budget
    "temperature": 1.0   // REQUIRED
  }
}
```

**Options**:
- `thinking: auto`: Dynamic allocation based on query complexity
- `thinking: {budget}`: Explicit computational budget for control

### 7.3 GPT-5 (OpenAI) Reasoning Profiles

**Method**: Reasoning profiles via API or system message

**Profiles**:
- `light`: Fast responses for straightforward tasks
- `balanced`: Default depth for general reasoning
- `deep`: Additional compute for complex, multi-step work

**Best Practice**: Combine `deep` profile with verification scaffolds (e.g., "list assumptions", "verify answer") for high-assurance tasks

**Implementation**:
```json
{
  "model": "gpt-5",
  "reasoning_profile": "deep",
  "messages": [...]
}
```

---

## 8. Structured Output Prompting (Still Essential 2025)

**Technical Definition**: Requesting specific output formats (JSON, XML, tables) for programmatic processing.

**2025 Status**: ✅ **Essential** - works excellently with reasoning models

**Implementation Pattern**:
```
Analyze the data and return results as JSON with this structure:
{
  "summary": "string",
  "key_findings": ["array of strings"],
  "metrics": {
    "score": number,
    "confidence": number
  }
}
```

**Best Practices (2025)**:
- Specify exact schema
- Use native JSON mode if available (GPT-5, Claude)
- Validate output programmatically
- Request well-formed output

---

## 9. Multimodal Prompting (Enhanced 2025)

**Technical Definition**: Techniques that combine multiple data modalities (text, images, audio) in prompts.

**2025 Status**: ✅ **Significantly improved** with native multimodal reasoning

**Implementation Characteristics**:
- Cross-modal reasoning: Native in advanced models
- Modal-specific processing: Automatic
- Unified representation: Integrated internally

**Technical Applications**:
- Image understanding with textual context
- Visual reasoning tasks
- Cross-modal information extraction
- Document understanding (text + images)

**Implementation Pattern (2025)**:
```
{
  "instruction": "Analyze this document",
  "text_input": "[textual_content]",
  "image_input": "[image_data_or_url]",
  "output_requirements": "[response_specifications]"
}
```

**Best Practices (2025)**:
- Let models integrate modalities naturally
- Don't over-instruct cross-modal reasoning
- Provide clear context for each modality
- Specify desired output format

---

## 10. Advanced Techniques (2025 Status)

### 10.1 Self-Consistency - Reduced Necessity

**2025 Status**: ⚠️ **Less necessary** with reasoning models

**Why**: Native reasoning is more consistent than multiple external samples

**When to Use (2025)**:
- High-stakes decisions requiring verification
- Tasks where model confidence varies
- Comparing different reasoning approaches

**Implementation** (if needed):
```python
def self_consistency(prompt, model, n=3):  # Reduced from 5
    responses = [model.generate(prompt) for _ in range(n)]
    return majority_vote(responses)
```

### 10.2 Tree-of-Thought (ToT) - Mostly Obsolete

**2025 Status**: ⚠️ **Mostly obsolete** for reasoning models

**Why**: Models explore multiple reasoning paths internally

**When to Use (2025)**:
- Complex decision trees requiring explicit exploration
- When external branching logic is needed
- Legacy systems or non-reasoning models

### 10.3 ReAct (Reasoning + Acting) - Still Relevant

**2025 Status**: ✅ **Still relevant** for agentic systems

**Why**: Tool use still requires external action cycles

**Implementation Pattern (2025)**:
```
# Model reasons internally, then acts
Thought: [automatic internal reasoning]
Action: [tool_name](parameters)
Observation: [result]
# Repeat as needed
```

**Best Practice (2025)**:
- Don't prescribe "Thought:" format (models do this internally)
- Focus on clear tool descriptions (1-2 sentences)
- Let model manage reasoning-action cycles

### 10.4 Retrieval-Augmented Generation (RAG) - Essential

**2025 Status**: ✅ **Essential** for knowledge-intensive tasks

**Implementation**:
1. Retrieve relevant documents
2. Provide as context
3. Let model reason over retrieved information

**Best Practices (2025)**:
- Structure retrieved context clearly
- Use semantic chunking
- Leverage large context windows (1M-2M tokens)
- Let model synthesize information

---

## 11. Anti-patterns (2025)

**What NOT to Do**:

❌ **Complex CoT Engineering**
```
# DON'T
"Step 1: Think about X
 Step 2: Consider Y
 Step 3: Analyze Z..."
```

❌ **Excessive Few-Shot Examples**
```
# DON'T
[5+ examples with detailed reasoning]
```

❌ **Conversational Fluff**
```
# DON'T (especially Gemini 3.x)
"Please, if you could, kindly analyze..."
```

❌ **Over-Engineering**
```
# DON'T
[Complex multi-page prompt with elaborate frameworks]
```

❌ **Prescriptive Reasoning**
```
# DON'T
"First, you must think about... then you should consider..."
```

---

## 12. Best Practices Summary (2025)

**✅ DO**:
- Use zero-shot as default
- Provide rich, structured context
- Specify clear output format
- Use XML tags (especially for Claude)
- Leverage native thinking modes
- Keep tool descriptions concise (1-2 sentences)
- Set temperature to 1.0 for Gemini 3.x
- Give models space to reason

**❌ DON'T**:
- Use complex CoT with reasoning models
- Provide excessive few-shot examples (>2)
- Over-engineer prompts
- Prescribe reasoning steps
- Use conversational padding
- Micromanage the reasoning process

---

## Technical References

**2025 Updates**:
- OpenAI GPT-5 Technical Documentation (2025)
- Anthropic Claude 4.x Reasoning Capabilities (2025)
- Google Gemini 3.x Best Practices (2025)

**Foundational Research** (Still relevant):
- Wei, J., et al. (2022). "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models." [arXiv:2201.11903](https://arxiv.org/abs/2201.11903) - Historical context
- Yao, S., et al. (2023). "Tree of Thoughts: Deliberate Problem Solving with Large Language Models." [arXiv:2305.10601](https://arxiv.org/abs/2305.10601) - Legacy technique
- Yao, S., et al. (2022). "ReAct: Synergizing Reasoning and Acting in Language Models." [arXiv:2210.03629](https://arxiv.org/abs/2210.03629) - Still applicable for agents
- Liu, P., et al. (2023). "Pre-train, Prompt, and Predict: A Systematic Survey of Prompting Methods in Natural Language Processing." [ACM Computing Surveys](https://dl.acm.org/doi/abs/10.1145/3560815) - Comprehensive survey
