# Implementation Patterns & Anti-patterns (2025 Edition)

This technical reference documents optimal implementation patterns and common anti-patterns for prompt engineering in AI systems development, updated for reasoning models (GPT-5.x, Claude 4.x, Gemini 3.x).

---

## 1. Iterative Development Pattern (Still Valid 2025)

**Technical Implementation**:
```python
def iterative_prompt_development(base_prompt, input_data, evaluation_function):
    current_prompt = base_prompt
    current_score = 0

    while True:
        response = generate_response(current_prompt, input_data)
        new_score = evaluation_function(response)

        if new_score <= current_score:
            return current_prompt  # Return last best prompt

        current_score = new_score
        current_prompt = refine_prompt(current_prompt, response)
```

**2025 Update - Key Metrics**:
- Response quality delta between iterations
- Convergence rate (faster with reasoning models)
- Token efficiency (balance with reasoning overhead)
- **Simplicity score** (simpler often better in 2025)

**Technical Considerations (2025)**:
- Start with **minimal viable prompt** (even simpler than before)
- Test zero-shot before adding complexity
- Isolate and test one variable per iteration
- Maintain version control of prompt iterations
- **Measure against zero-shot baseline first**

---

## 2. Context Engineering Pattern (2025 Core Focus)

**2025 PARADIGM SHIFT**: Context engineering > Prompt engineering

**Technical Implementation Pattern**:
```
{
  "context": {
    "background": "[relevant domain knowledge]",
    "structure": "[hierarchical organization]",
    "data": "[well-formatted input]"
  },
  "instruction": "[clear, direct task]",
  "output_format": "[specific format requirements]"
}
```

**Context Prioritization Matrix (2025)**:
| Context Type | Priority | Token Allocation | Structure Importance |
|--------------|----------|------------------|---------------------|
| Task definition | Highest | 5-10% | Crystal clear |
| Relevant background | High | 20-30% | Well-organized |
| Input data | High | 40-50% | Properly formatted |
| Output format | High | 5-10% | Explicit schema |
| Reasoning guidance | **LOW** | **0-5%** | **Let model decide** |

**2025 Best Practices**:
```python
def optimize_context(content, model_type):
    """
    Optimize context for reasoning models
    """
    context = {
        # High priority: Structure and clarity
        "structured_data": format_with_clear_delimiters(content),

        # High priority: Relevant background
        "domain_context": extract_relevant_background(content),

        # High priority: Clear task
        "task": define_task_clearly(content),

        # Medium priority: Output format
        "format": specify_output_format(content)
    }

    # LOW priority: Don't add reasoning instructions for 2025 models
    if not is_reasoning_model(model_type):
        context["reasoning_guide"] = add_reasoning_guidance(content)

    return context
```

**XML Structure for Claude (Recommended)**:
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

---

## 3. Specificity Optimization (Enhanced 2025)

**Technical Implementation Pattern**:
```
{
  "instruction": {
    "action": "[specific_verb]",
    "object": "[specific_target]",
    "constraints": {
      "format": "[output_format]",
      "scope": "[what to include/exclude]"
    }
  },
  "context": "[rich, relevant information]",
  "input": "[content_to_process]"
}
```

**2025 Update - Specificity Parameters**:
- Action specificity: Use precise verbs
- Format specification: **Critical** for structured output
- Context richness: **More important** than reasoning instructions
- Scope definition: What to include/exclude
- **Avoid**: Over-specifying HOW to think

**Good Example (2025)**:
```
Extract security vulnerabilities from this code.

<context>
Authentication module for production API
</context>

<code>
[code block]
</code>

Return JSON: {
  "vulnerabilities": [
    {"type": "string", "severity": "critical|high|medium|low", "description": "string"}
  ]
}
```

**Bad Example (Anti-pattern)**:
```
# DON'T (over-engineered for 2025 reasoning models)
First, carefully read through the code.
Then, think about each function and what it does.
Next, consider potential security issues.
For each issue, think about the severity...
[etc.]
```

---

## 4. Delimiter Implementation Pattern (Still Important 2025)

**Technical Definition**: Structural markers that segment prompt components for improved parsing.

**2025 Recommendation: XML for Claude, Markdown for others**

**Implementation Options**:
```python
DELIMITER_PATTERNS = {
    "xml": {  # RECOMMENDED for Claude
        "context": "<context>{content}</context>",
        "instruction": "<instruction>{content}</instruction>",
        "data": "<data>{content}</data>",
        "output": "<output_format>{content}</output_format>"
    },
    "markdown": {  # Good for GPT-5, Gemini
        "section": "## {section_name}",
        "subsection": "### {subsection_name}",
        "code": "```{language}\n{code}\n```"
    }
}

def apply_delimiters(content, model_family):
    if model_family == "claude":
        return DELIMITER_PATTERNS["xml"]
    else:
        return DELIMITER_PATTERNS["markdown"]
```

**Best Practices (2025)**:
- Use consistent delimiters throughout
- XML tags work exceptionally well with Claude
- Clear section headers for all models
- Avoid over-nesting

---

## 5. Output Format Control Pattern (Enhanced 2025)

**Technical Definition**: Explicit specification of response structure, format, and characteristics.

**2025 Status**: ✅ **Even more important** - models excel at structured output

**Implementation Structure**:
```python
def specify_output_format(format_type, schema):
    format_templates = {
        "json": "Return as JSON with this exact structure:\n{schema}",
        "table": "Return as markdown table with columns:\n{columns}",
        "xml": "Return as XML with this structure:\n{schema}"
    }

    # 2025: Use native JSON mode if available
    if format_type == "json" and model_supports_json_mode():
        return {"response_format": {"type": "json_object"}, "schema": schema}

    return format_templates[format_type].format(schema=schema)
```

**2025 Best Practices**:
- Use native JSON mode (GPT-5, Claude) when available
- Provide explicit schema
- Validate output programmatically
- Request well-formed, parseable output

**Example (2025)**:
```
Analyze the document and return JSON matching this schema:

{
  "summary": "string",
  "key_points": ["array of strings"],
  "sentiment": "positive|neutral|negative",
  "confidence": 0.0-1.0,
  "entities": [
    {"name": "string", "type": "person|org|location"}
  ]
}
```

---

## 6. Model-Specific Optimization Patterns (2025)

### 6.1 Claude (Anthropic) Pattern

```xml
<context>
Provide rich background and domain context here.
Include relevant facts and information.
</context>

<task>
Clear, direct instruction without reasoning steps.
</task>

<data>
Input data, well-structured.
</data>

<thinking>
[Claude uses this space for internal reasoning if needed]
</thinking>

Expected output: [format specification]
```

**Best Practices**:
- Heavy use of XML tags
- Let Claude decide when to use `<thinking>`
- Provide rich context
- Clear, direct instructions

### 6.2 GPT-5 (OpenAI) Pattern

```markdown
## Context
Background information and relevant facts

## Task
Direct instruction without micromanaging reasoning

## Input
[Input data]

## Output Format
Specify desired format

# Optionally set reasoning profile:
# {"reasoning_profile": "deep"}
```

**Best Practices**:
- Use reasoning profiles (light/balanced/deep)
- Clear markdown structure
- Explicit output format
- Combine "deep" profile with verification requests

### 6.3 Gemini 3.x (Google) Pattern

```markdown
## Context
Background information

## Task
Direct, concise instruction - NO conversational fluff

## Input
[Input data]

## Output
Expected format

# CRITICAL: Set temperature to 1.0
# {"thinking": "auto", "temperature": 1.0}
```

**⚠️ CRITICAL for Gemini 3.x**:
- Temperature MUST be 1.0
- Absolutely NO conversational padding ("please", "kindly", etc.)
- Clear, direct instructions
- Use `thinking: auto` for complex tasks

---

## 7. Common Anti-patterns (2025 Updated)

### 7.1 Over-Engineering Anti-pattern (2025 #1 Issue)

**Technical Definition**: Adding unnecessary complexity that hinders reasoning model performance.

**Detection Metrics**:
- Prompt length > 500 tokens for simple tasks
- Multiple pages of instructions
- Elaborate CoT frameworks
- Excessive few-shot examples (>2)

**2025 Example (BAD)**:
```
# Anti-pattern: Over-engineered
You are an expert analyst. Please carefully consider the following task.

I need you to analyze this data, and here's how you should do it:

Step 1: First, read through the entire dataset carefully
Step 2: Then, identify the key patterns
Step 3: Next, think about what those patterns mean
Step 4: Consider alternative interpretations
Step 5: Weigh the evidence for each interpretation
...
[continues for multiple paragraphs]

Here are 5 examples of how to do this correctly:
Example 1: [long example with reasoning]
Example 2: [long example with reasoning]
...
```

**Remediation Pattern (2025)**:
```python
def simplify_prompt(over_engineered_prompt):
    """
    Strip down to essentials for reasoning models
    """
    simple_prompt = {
        "context": extract_relevant_context(over_engineered_prompt),
        "task": extract_core_task(over_engineered_prompt),
        "format": extract_output_format(over_engineered_prompt)
    }

    # Remove: reasoning instructions, excessive examples, fluff
    return format_simple_prompt(simple_prompt)
```

**GOOD (2025)**:
```
Analyze this dataset for patterns.

<context>
Sales data from Q1-Q4 2025, includes regions and product categories
</context>

<data>
[dataset]
</data>

Return JSON: {
  "patterns": ["array of identified patterns"],
  "insights": ["key insights"],
  "confidence": 0.0-1.0
}
```

### 7.2 Excessive Few-Shot Anti-pattern (2025)

**Technical Definition**: Providing too many examples that overwhelm native reasoning.

**Detection Metrics**:
- More than 2 examples for reasoning models
- Examples showing reasoning steps (unnecessary)
- Examples consuming >30% of prompt tokens

**Remediation Pattern**:
```python
def optimize_few_shot(examples, model_type):
    if is_reasoning_model(model_type):
        # Max 1-2 examples, format only
        return examples[:1]  # Just show format
    else:
        # Legacy models might need more
        return examples[:3]
```

### 7.3 CoT Instruction Anti-pattern (2025)

**Technical Definition**: Explicitly instructing models to "think step by step" when they already do this internally.

**Detection Metrics**:
- Contains "Let's think step by step"
- Contains "Step 1:", "Step 2:", etc.
- Prescriptive reasoning instructions
- Multi-step reasoning framework

**2025 Example (BAD)**:
```
Let's approach this step by step:

Step 1: First, analyze component A
Step 2: Then, examine component B
Step 3: Next, consider the relationship between A and B
Step 4: Finally, synthesize your findings

Now, solve the problem.
```

**Remediation Pattern**:
```python
def remove_cot_instructions(prompt):
    """
    Remove explicit CoT instructions for reasoning models
    """
    # Remove step-by-step frameworks
    prompt = remove_pattern(prompt, r"Step \d+:.*")
    prompt = remove_pattern(prompt, r"Let's think step by step")
    prompt = remove_pattern(prompt, r"First.*Then.*Next.*Finally")

    return prompt
```

**GOOD (2025)**:
```
Analyze the relationship between components A and B.

<context>
[background]
</context>

<data>
Component A: [data]
Component B: [data]
</data>

Explain the relationship and implications.
```

### 7.4 Conversational Fluff Anti-pattern (2025)

**Technical Definition**: Unnecessary conversational padding that wastes tokens and can hinder performance (especially Gemini 3.x).

**Detection Metrics**:
- Contains "please", "kindly", "if you could"
- Excessive politeness
- Unnecessary preambles
- Apologetic language

**Conversational Overhead Quantification**:

| Phrase Type | Token Cost | Signal Value | Verdict |
|-------------|------------|--------------|---------|
| "Hello! I hope you're doing well" | 8-12 tokens | Zero | ❌ Remove |
| "Could you please help me" | 5-7 tokens | Zero | ❌ Remove |
| "Thank you so much!" | 4-5 tokens | Zero | ❌ Remove |
| "I would really appreciate if" | 6-8 tokens | Zero | ❌ Remove |
| "When you have a moment" | 5 tokens | Zero (models are instant) | ❌ Remove |

**Impact Analysis**:
```
Fluffy prompt:    "Hello! Could you please help me analyze this data? Thanks!"
Tokens used:      ~15 tokens of pure overhead
Direct prompt:    "Analyze this data:"
Tokens saved:     ~12 tokens (80% reduction in instruction overhead)
```

**Model-Specific Impact**:
- **Gemini 3.x**: Conversational language actively degrades instruction-following
- **Claude 4.x**: Tolerates but gains nothing from it
- **GPT-5.x**: Neutral impact, but wastes tokens

**2025 Example (BAD for Gemini 3.x)**:
```
Hello! I hope you're doing well today. If you could please help me with this task, I would greatly appreciate it. Could you kindly analyze the following data when you have a moment? Thank you so much!

[task details]
```

**Remediation Pattern**:
```python
def remove_fluff(prompt):
    """
    Remove conversational padding
    """
    fluff_patterns = [
        r"please\s+",
        r"kindly\s+",
        r"if you could\s+",
        r"I hope.*",
        r"Thank you.*",
        r"I appreciate.*"
    ]

    for pattern in fluff_patterns:
        prompt = re.sub(pattern, "", prompt, flags=re.IGNORECASE)

    return prompt.strip()
```

**GOOD (2025)**:
```
Analyze this data.

[data]

Return results as JSON.
```

### 7.5 Temperature Misconfiguration Anti-pattern (Gemini 3.x)

**Technical Definition**: Using incorrect temperature settings for Gemini 3.x models.

**⚠️ CRITICAL**: Gemini 3.x **REQUIRES** temperature = 1.0

**Detection**:
```python
def validate_gemini_params(model, params):
    if "gemini-3" in model.lower():
        if params.get("temperature") != 1.0:
            raise ValueError("Gemini 3.x REQUIRES temperature=1.0")
    return params
```

**Remediation**:
```python
def fix_gemini_params(model, params):
    if "gemini-3" in model.lower():
        params["temperature"] = 1.0
    return params
```

---

## 8. Advanced Implementation Patterns (2025)

### 8.1 Knowledge Grounding Pattern (Enhanced)

**Technical Definition**: Ensuring model responses are strictly derived from verified knowledge sources.

**2025 Implementation**:
```python
def create_knowledge_grounded_prompt(query, knowledge_sources):
    # Reasoning models are better at grounding
    prompt = f"""
    Answer based ONLY on the provided sources. If information is not in sources, state "Not found in provided sources."

    <sources>
    {format_knowledge_sources(knowledge_sources)}
    </sources>

    <query>
    {query}
    </query>

    Cite sources in your answer: [Source 1], [Source 2], etc.
    """
    return prompt
```

**2025 Improvements**:
- Reasoning models better at staying grounded
- Can request verification of grounding
- Native thinking modes show reasoning process
- Improved citation accuracy

### 8.2 Structured Thinking Pattern (2025)

**Technical Definition**: Using model-native thinking modes instead of external CoT.

**Implementation by Model**:

**Claude**:
```xml
<task>
Complex analytical task requiring deep reasoning
</task>

<context>
[Rich contextual information]
</context>

<thinking>
[Claude uses this space automatically if needed]
</thinking>

Provide your analysis with supporting evidence.
```

**GPT-5**:
```json
{
  "model": "gpt-5",
  "reasoning_profile": "deep",
  "messages": [
    {
      "role": "user",
      "content": "Complex task requiring deep reasoning\n\n[context]"
    }
  ]
}
```

**Gemini**:
```json
{
  "model": "gemini-3-pro",
  "contents": [{"parts": [{"text": "Complex task\n\n[context]"}]}],
  "generationConfig": {
    "thinking": "auto",
    "temperature": 1.0
  }
}
```

---

## 9. System Prompt Optimization (2025)

**Technical Definition**: Techniques to create effective system-level instructions.

**2025 Best Practices**:
```python
def construct_system_prompt_2025(domain, capabilities, constraints):
    """
    Simple, clear system prompts for reasoning models
    """
    prompt = f"""You are an AI assistant specializing in {domain}.

Capabilities:
{format_capabilities(capabilities)}

Constraints:
{format_constraints(constraints)}

Provide accurate, helpful responses based on the context provided in each query.
"""
    # DON'T add: reasoning instructions, step-by-step frameworks, etc.
    return prompt
```

**Anti-pattern (Over-specified)**:
```
# DON'T
You are an AI assistant. When answering questions, you should:
1. First, carefully read the question
2. Then, think about what information is relevant
3. Next, organize your thoughts
4. Consider multiple perspectives
5. Weigh the evidence
[etc...]
```

---

## 10. Tool Calling Pattern (2025)

**Technical Definition**: Optimizing tool/function descriptions for reasoning models.

**2025 Best Practice: Crisp Descriptions (1-2 sentences)**

**GOOD (2025)**:
```json
{
  "name": "search_database",
  "description": "Search the customer database by name or ID.",
  "parameters": {
    "query": {"type": "string", "description": "Search term"},
    "field": {"type": "string", "enum": ["name", "id"]}
  }
}
```

**BAD (Over-described)**:
```json
{
  "name": "search_database",
  "description": "This function allows you to search through the customer database. You should use this function whenever the user asks about a customer or wants to find customer information. The function can search by either name or ID. When searching by name, partial matches will be returned. When searching by ID, only exact matches are returned. Make sure to validate the input before calling this function. If the user's request is ambiguous, ask for clarification before searching...",
  // ... TOO VERBOSE
}
```

---

## Best Practices Summary (2025)

**✅ IMPLEMENT**:
1. **Context Engineering**: Rich, structured context
2. **Simplicity**: Start with minimal prompt
3. **Zero-Shot First**: Test before adding examples
4. **Clear Output Format**: Explicit schemas
5. **XML Tags**: Especially for Claude
6. **Native Thinking Modes**: Use model capabilities
7. **Crisp Tool Descriptions**: 1-2 sentences max
8. **Correct Parameters**: Temperature 1.0 for Gemini 3.x

**❌ AVOID**:
1. **Over-engineering**: Complex multi-step frameworks
2. **Explicit CoT**: "Let's think step by step"
3. **Excessive Few-Shot**: >2 examples
4. **Conversational Fluff**: "Please", "kindly", etc.
5. **Prescriptive Reasoning**: Telling model HOW to think
6. **Verbose Tool Descriptions**: Multiple paragraphs
7. **Wrong Temperature**: Not 1.0 for Gemini 3.x

---

## Technical References

**2025 Best Practices**:
- OpenAI GPT-5 Documentation (2025)
- Anthropic Claude 4.x Best Practices (2025)
- Google Gemini 3.x Technical Guide (2025)

**Foundational Research**:
- Liu, P., et al. (2023). "Pre-train, Prompt, and Predict: A Systematic Survey of Prompting Methods in Natural Language Processing." [ACM Computing Surveys](https://dl.acm.org/doi/abs/10.1145/3560815)
- White, J., et al. (2023). "A Prompt Pattern Catalog to Enhance Prompt Engineering with ChatGPT." [arXiv:2302.11382](https://arxiv.org/abs/2302.11382)
