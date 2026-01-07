# Core Concepts & Technical Terminology in Prompt Engineering (2025 Edition)

This section provides technical definitions and implementation details of key prompt engineering concepts for AI systems development, updated with 2025 best practices for reasoning models.

---

## 1. Prompt Structure

**Definition**: A prompt is the input text provided to an LLM to elicit a specific response.

**Technical Components**:
- **Role**: System-level identity assignment (e.g., "You are a specialized code analyzer")
- **Instruction**: Primary directive specifying the required task
- **Context**: Supplementary information for task execution
- **Format Specification**: Output structure requirements

**Functional Categories**:
- **Interrogative**: Information retrieval prompts
- **Imperative**: Task execution prompts
- **Completion-based**: Text continuation prompts

**Implementation Example**:
```
{role: "You are a specialized data analyst with expertise in financial metrics",
instruction: "Extract all quarterly revenue figures from the following report",
context: "This is a Q3 2023 financial report for a SaaS company",
format: "Return data as JSON with quarters as keys and values in USD millions"}
```

---

## 2. LLM Technical Specifications

**Definition**: Large Language Models are transformer-based neural networks trained on vast text corpora that generate text by predicting token sequences.

**Architectural Elements**:
- **Transformer Architecture**: Self-attention mechanism for contextual understanding
- **Token Processing**: Text segmentation into processable units
- **Parameter Space**: Model weight configurations (ranging from billions to trillions)
- **Reasoning Capabilities**: Advanced models include built-in chain-of-thought reasoning (GPT-5.x, Claude 4.x, Gemini 3.x)

**Context Window Specifications (2025)**:
- OpenAI: 128K tokens (GPT-5) to 256K tokens (GPT-5-Codex)
- Anthropic: 200K tokens (Claude Sonnet 4.5, Claude Haiku 4.5)
- Google Gemini: 1M tokens (Gemini 2.5 Pro, Gemini 2.5 Flash)
- Zhipu AI: 512K tokens (GLM 4.5)
- xAI: 2M tokens (Grok 4 Fast - largest available)

**Technical Capabilities Matrix (2025 Models)**:
| Model | Context Window | Key Strength | Reasoning | Special Feature | Release Date |
|-------|----------------|--------------|-----------|-----------------|--------------|
| GPT-5 | 128K | Unified flagship, all benchmarks | Advanced (native) | Enterprise-grade | Aug 2025 |
| GPT-5-Codex | 256K | Software engineering + agent orchestration | Advanced (native) | Regression-aware guardrails | Oct 2025 |
| Claude Sonnet 4.5 | 200K | Frontier coding & agentic workflows | Advanced (native) | Claude Code backbone | Sep 2025 |
| Claude Haiku 4.5 | 200K | Low-latency deployment | Strong (native) | Fast inference, 4.5 accuracy | Sep 2025 |
| Gemini 2.5 Pro | 1M | Multimodal precision | Advanced (native) | Adaptive `thinking` budgets | 2025 |
| Gemini 2.5 Flash | 1M | Real-time iteration | Strong (native) | Streaming-optimized | 2025 |
| GLM 4.5 | 512K | Bilingual reasoning, finance analytics | Advanced (native) | Enterprise compliance | Sep 2025 |
| Grok 4 Fast | 2M | Massive context + live tool use | Advanced (native) | Tool-use RL, unified reasoning | Sep 2025 |

**Legacy Models (Deprecated 2025)**:
- GPT-4o: Removed from ChatGPT (Aug 2025), Pro users only
- GPT-4: Removed 2025
- DeepSeek V3/R1 line: Replaced operationally by GLM 4.5

---

## 3. Large Context Management (1M-2M Tokens)

**Definition**: For massive context windows (1M+ tokens), the primary challenge shifts from fitting information to ensuring its accurate retrieval.

**Core Principles**:
- **Structure Over Append**: Do not simply append large texts. Structure documents with clear markdown headers, sections, and tables to aid model navigation.
- **Strategic Information Placement**: In "Needle in a Haystack" (NIAH) tests, retrieval is often better at the beginning or end of the context. Place the most critical information or instructions in these high-recall zones.
- **Explicit Retrieval Instructions**: Add instructions like "Scan the entire provided document before answering" or "The answer is located within the attached financial report."

**Implementation Patterns**:
1. **Retrieval-Augmented Generation (RAG)**: The standard for knowledge bases larger than the context window. Instead of including the full text, retrieve relevant chunks from a vector database and insert them into the prompt.
2. **Document Structuring**: Use clear, hierarchical markdown (e.g., `# Title`, `## Section`, `### Subsection`) to create a navigable structure within the prompt itself.
3. **Instructional Anchors**: Place key instructions or questions at both the beginning and the end of the context to maximize the chance of them being followed.

---

## 4. Instruction Engineering (2025 Approach)

**Definition**: The systematic design of directives that specify the exact task requirements for an LLM.

**2025 Key Principle**: **Clarity over complexity**. With reasoning models (GPT-5.x, Claude 4.x, Gemini 3.x), simpler and more direct instructions often outperform elaborate prompt engineering techniques.

**Instruction Categories**:
1. **Generative Instructions**: `create`, `write`, `develop`, `design`
2. **Analytical Instructions**: `analyze`, `evaluate`, `compare`, `assess`
3. **Transformative Instructions**: `convert`, `translate`, `summarize`, `simplify`
4. **Classification Instructions**: `categorize`, `identify`, `label`, `sort`

**Technical Implementation Principles (2025)**:
- **Direct Instructions**: Single, clear directives work best with reasoning models
- **Context-Rich Instructions**: Focus on providing good context rather than step-by-step reasoning prompts
- **Minimal Fluff**: Avoid conversational padding (especially important for Gemini 3.x)
- **Room to Think**: Give models space to engage their internal reasoning without over-constraining

**Instruction Optimization Metrics**:
- Task completion rate
- Execution accuracy
- Instruction-following precision
- Token efficiency (balance with reasoning needs)

---

## 5. Input Data Processing

**Definition**: The preparation and structuring of data provided to an LLM for processing.

**Data Types and Handling**:
- **Unstructured Text**: Requires minimal preprocessing
- **Semi-structured Data**: Requires format preservation (tables, lists)
- **Structured Data**: Requires specific format specifications (JSON, XML)
- **Code**: Requires syntax preservation and execution context

**Technical Implementation**:
```
def prepare_input_data(data, data_type):
    if data_type == "structured":
        return format_as_json(data)
    elif data_type == "code":
        return format_with_syntax_highlighting(data)
    else:
        return clean_and_normalize(data)
```

**Delimiter Implementation** (Claude models especially benefit from XML tags):
```
INSTRUCTION_DELIMITER = "### Instruction:"
CONTEXT_DELIMITER = "### Context:"
DATA_DELIMITER = "### Data:"

# For Claude models, prefer XML:
<instruction>Your task here</instruction>
<context>Background information</context>
<data>Input data</data>
```

---

## 6. Output Control Mechanisms

**Definition**: Technical specifications that determine the format, structure, and characteristics of model responses.

**Control Parameters**:
- **Format Specifiers**: JSON, XML, Markdown, CSV
- **Structure Templates**: Lists, tables, hierarchical formats
- **Style Directives**: Technical, formal, simplified

**Implementation Example**:
```
"Return the analysis as a JSON object with the following structure:
{
  'key_findings': [list of strings],
  'metrics': {
    'accuracy': float,
    'confidence': float
  },
  'recommendations': [list of objects]
}"
```

**Programmatic Output Parsing**:
```python
def parse_llm_output(output, expected_format="json"):
    if expected_format == "json":
        try:
            return json.loads(output)
        except:
            return extract_json_from_text(output)
    elif expected_format == "table":
        return convert_markdown_table_to_dict(output)
```

---

## 7. Prompting Techniques (2025 Update)

### Zero-shot vs. Few-shot Prompting

**2025 Critical Update**: For reasoning models (GPT-5.x, Claude 4.x, Gemini 3.x), **zero-shot prompting often works better** than complex few-shot examples. Excessive examples can overwhelm the model's internal reasoning.

**Technical Comparison**:

| Aspect | Zero-shot (2025) | Few-shot (2025) |
|--------|------------------|-----------------|
| Token Efficiency | High | Low |
| Implementation Complexity | Low | Medium |
| Recommended For Reasoning Models | **Strongly recommended** | Use sparingly (1-2 examples max) |
| Consistency | High (with reasoning models) | Can reduce performance if overused |
| Pattern Recognition | Native (built-in) | Only when pattern is non-standard |

**Implementation Decision Tree (2025)**:
```
if model_has_native_reasoning (GPT-5.x, Claude 4.x, Gemini 3.x):
    use_zero_shot()  # Preferred approach
    if task_requires_specific_format_example:
        use_minimal_few_shot(examples=1)  # Show format only
elif task_is_standard:
    use_zero_shot()
else:
    use_few_shot(examples=2-3)  # Reduced from previous 3-5
```

### Chain-of-Thought (CoT) - 2025 Deprecation Notice

**⚠️ IMPORTANT 2025 UPDATE**: Complex CoT techniques can **HINDER** performance with reasoning models.

**Technical Definition**: A prompting technique that instructs the model to decompose reasoning into sequential logical steps.

**2025 Status**:
- **Deprecated** for reasoning models (GPT-5.x, Claude 4.x, Gemini 3.x)
- **Still useful** for legacy models or simple tasks requiring transparency
- Models perform internal chain-of-thought automatically

**When to Use (2025)**:
- ❌ **DO NOT** use explicit CoT with reasoning models
- ✅ **DO** use for legacy models without native reasoning
- ✅ **DO** request step-by-step output for transparency/debugging
- ✅ **DO** use thinking modes (see Section 8)

**Legacy Implementation Variants** (for non-reasoning models):
1. **Zero-shot CoT**: `"Let's think step by step"` (mostly obsolete)
2. **Few-shot CoT**: Providing reasoning examples (can reduce reasoning model performance)
3. **Self-consistency CoT**: Multiple reasoning paths with majority voting (unnecessary with reasoning models)

---

## 8. Thinking Modes & Reasoning Traces (2025 Native Capabilities)

**Definition**: Model-native capabilities that expose or enhance internal reasoning processes.

**2025 Approach**: **Use model-native thinking modes** instead of prompt-based CoT.

**Implementation by Model Family (2025)**:

### Anthropic (Claude Series)
- **Method**: XML tags and slash commands
- **Implementation**:
  ```xml
  <thinking>
  [Model uses this space for internal reasoning]
  </thinking>
  ```
- **Slash Commands**: `/think`, `/megathink`, `/ultrathink` (in supported interfaces)
- **Best Practice**: Let Claude decide when to think; don't over-structure

### Google (Gemini 2.5 Series)
- **Method**: API parameter `thinking`
- **⚠️ CRITICAL**: Temperature MUST be 1.0 for Gemini 3.x
- **Implementation**:
  ```json
  {
    "thinking": "auto",  // or {budget}
    "temperature": 1.0   // REQUIRED for Gemini 3.x
  }
  ```
- **Options**:
  - `thinking: auto`: Dynamic allocation based on complexity
  - `thinking: {budget}`: Explicit computational budget

### OpenAI (GPT-5 Family)
- **Method**: Reasoning profiles
- **Profiles**:
  - `light`: Fast responses for straightforward tasks
  - `balanced`: Default depth for general reasoning
  - `deep`: Additional compute for complex work
- **Implementation**: Set via API parameter or system message
- **Best Practice**: Use `deep` profile with verification scaffolds for high-assurance tasks

---

## 9. Parameter Optimization (2025)

### Temperature and Top-p

**Technical Definitions**:
- **Temperature**: Sampling parameter controlling prediction probability distribution
- **Top-p (nucleus sampling)**: Cumulative probability threshold for token selection

**⚠️ 2025 CRITICAL UPDATE - Gemini 3.x Requirement**:
```python
def optimize_parameters(task_type, model_family):
    if model_family == "gemini_3":
        # MUST use temperature 1.0 for Gemini 3.x
        params = {"temperature": 1.0, "top_p": 0.95}
    elif task_type == "factual" or task_type == "code":
        params = {"temperature": 0.2, "top_p": 0.3}
    elif task_type == "creative":
        params = {"temperature": 0.8, "top_p": 0.9}
    return params
```

**Parameter Matrix for Different Tasks (2025)**:
| Task Type | Temperature | Top-p | Rationale | Gemini 3.x Override |
|-----------|-------------|-------|-----------|---------------------|
| Factual responses | 0.1-0.2 | 0.3 | Maximize accuracy | **1.0** (required) |
| Analytical reasoning | 0.2-0.4 | 0.4 | Balance precision | **1.0** (required) |
| Creative writing | 0.7-0.9 | 0.9 | Enable variation | 1.0 |
| Code generation | 0.1-0.3 | 0.3 | Prioritize correctness | **1.0** (required) |

---

## 10. Hallucination Management

**Technical Definition**: Hallucinations are model-generated content that is factually incorrect, unverifiable, or contradictory to provided information.

**Hallucination Types**:
1. **Intrinsic**: Contradictions to provided context
2. **Extrinsic**: Unverifiable information outside context

**Technical Mitigation Strategies (2025)**:
```python
def implement_hallucination_controls(prompt, model_type):
    controls = [
        "Only use information explicitly provided in the context.",
        "For any information not in the context, respond with 'I don't have enough information.'",
        "Cite the specific part of the context that supports each statement."
    ]

    # Reasoning models can self-verify
    if model_has_native_reasoning(model_type):
        controls.append("Verify your reasoning before providing the final answer.")

    return prompt + "\n" + "\n".join(controls)
```

**Advanced Hallucination Reduction (2025)**:
- Leverage native reasoning for self-verification
- Apply knowledge boundary enforcement
- Request citations to provided context
- Use thinking modes to expose reasoning (easier to verify)

---

## 11. Tool Calling & Function Use (2025)

**Definition**: Models' ability to invoke external functions or APIs during response generation.

**2025 Best Practices**:
- **Keep descriptions crisp**: 1-2 sentences per tool
- **Clear parameter schemas**: Use JSON schema or equivalent
- **Avoid over-description**: Reasoning models infer usage well

**Implementation Example (2025)**:
```json
{
  "name": "get_weather",
  "description": "Get current weather for a location.",
  "parameters": {
    "location": {"type": "string", "description": "City name"},
    "units": {"type": "string", "enum": ["celsius", "fahrenheit"]}
  }
}
```

**❌ Avoid (Over-description)**:
```json
{
  "name": "get_weather",
  "description": "This function retrieves the current weather conditions for a specified location. You should use this when the user asks about weather, temperature, conditions, or forecasts. Make sure to extract the location from the user's query. If the user doesn't specify units, default to celsius...",
  // ... overly verbose
}
```

---

## 12. Context Engineering > Prompt Engineering (2025 Paradigm)

**Definition**: The shift from clever prompt wording to strategic context structure.

**2025 Core Principle**: **Give models good context and room to think, rather than prescriptive instructions.**

**Implementation Framework**:
```
GOOD (2025):
- Clear problem statement
- Relevant background context
- Well-structured input data
- Desired output format
- Let model reason

BAD (2025):
- Step 1: Do this
- Step 2: Then do that
- Step 3: Now think about...
- [Over-constraining reasoning]
```

**Context Engineering Checklist**:
- ✅ Provide relevant background
- ✅ Structure information hierarchically
- ✅ Use clear delimiters (especially XML for Claude)
- ✅ Specify output format
- ✅ Give space for reasoning
- ❌ Don't micromanage reasoning steps
- ❌ Don't use conversational fluff
- ❌ Don't over-engineer complex prompts

---

## 13. What Still Works (2025)

**Foundational Best Practices**:
- ✅ **Clarity**: Clear, unambiguous instructions
- ✅ **Context**: Rich, relevant background information
- ✅ **Specificity**: Precise task definitions
- ✅ **Structured Output**: Format specifications (JSON, tables, etc.)
- ✅ **XML Tags**: Especially effective for Claude models
- ✅ **System Instructions**: Proper placement and structure
- ✅ **Examples**: 1-2 examples for format demonstration (not reasoning)

---

## 14. What's Deprecated (2025)

**Techniques Less Useful with Reasoning Models**:
- ❌ **Elaborate CoT**: Models do this internally now
- ❌ **Complex Few-Shot**: Can overwhelm native reasoning
- ❌ **Excessive Examples**: 1-2 max, not 3-5+
- ❌ **Step-by-Step Reasoning Prompts**: Use thinking modes instead
- ❌ **"Please" and Conversational Fluff**: Especially harmful for Gemini 3.x
- ❌ **Over-Engineered Prompts**: Simpler is better

---

This technical reference is optimized for implementation with 2025 reasoning models and reflects validated best practices for GPT-5.x, Claude 4.x, and Gemini 3.x systems.
