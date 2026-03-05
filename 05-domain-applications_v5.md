# Domain-Specific Applications (2026 Edition)

This module documents specialized implementation patterns for prompt engineering across different domains and use cases.

> **Anti-patterns**: See 02-techniques-patterns_v5.md (canonical).
> **Model specs**: See 03-model-catalog_v5.md.
> **Agentic patterns**: See 10-agentic-patterns_v5.md.

---

## 1. Content Generation

### Pattern

```python
def generate_content(content_type, domain, specs, model):
    prompt = f"""
Generate a {content_type} about {domain}.

<context>
{format_domain_context(domain)}
</context>

<specifications>
{format_specs(specs)}
</specifications>

<output_format>
{specify_output_structure(content_type)}
</output_format>
"""
    return model.generate(prompt, thinking_mode='auto')
```

### Example

```
Generate a technical blog post about microservices architecture.

<context>
Target audience: Senior software engineers
Focus: Migration from monolith to microservices
Tone: Technical but accessible
</context>

<specifications>
Length: 1500-2000 words
Include: Benefits, challenges, best practices
Format: H2 sections with code examples
</specifications>

Return markdown with proper structure.
```

### Best Practices
- Provide rich domain context (audience, tone, focus)
- Clear specifications (length, style, structure)
- Explicit output format
- DON'T prescribe writing process ("first brainstorm, then outline, then...")

---

## 2. Analytical Reasoning

### Pattern

```python
def analyze(task, domain, data, model):
    prompt = f"""
Analyze: {task}

<domain_context>
{domain}
</domain_context>

<data>
{format_data(data)}
</data>

Provide comprehensive analysis with supporting evidence.

Return as:
{{
  "executive_summary": "string",
  "key_findings": ["array"],
  "detailed_analysis": "string",
  "recommendations": ["array"],
  "confidence_level": 0.0-1.0
}}
"""
    return model.generate(prompt, reasoning_profile='deep')
```

### Example

```
Analyze market trends for electric vehicles in 2025-2026.

<context>
Focus: North American market
Data period: 2025-2026
Key factors: Sales, charging infrastructure, policy changes
</context>

<data>
[Market data, statistics, policy documents]
</data>

Identify trends, drivers, and future outlook.
Return JSON: {trends, analysis, forecast, confidence}
```

### Best Practices
- Let reasoning models handle decomposition (don't prescribe steps)
- Clear analytical framework in context
- Well-structured input data
- Explicit output format with confidence scores

---

## 3. Code Analysis & Generation

### Code Analysis

```python
def analyze_code(code, analysis_type, model):
    prompt = f"""
Analyze this code for {analysis_type}.

<code>
{code}
</code>

Return JSON:
{{
  "issues": [
    {{"type": "string", "severity": "critical|high|medium|low",
      "description": "string", "line": "number"}}
  ],
  "recommendations": ["array"],
  "summary": "string"
}}
"""
    return model.generate(prompt)
```

### Code Generation

```python
def generate_code(requirements, language, model):
    prompt = f"""
Generate {language} code meeting these requirements:

<requirements>
{format_requirements(requirements)}
</requirements>

Include:
- Clear comments for non-obvious logic
- Error handling at boundaries
- Type hints (if applicable)
- Unit test example

Return as markdown code block.
"""
    return model.generate(prompt, temperature=0.2)  # Except Gemini: 1.0
```

### Best Practices
- Don't prescribe code review steps ("first check syntax, then review logic...")
- Specify language, conventions, and constraints
- Lower temperature for code (except Gemini: always 1.0)
- Let models do comprehensive analysis naturally

---

## 4. Data Extraction & Transformation

### Extraction

```python
def extract_structured(text, schema, model):
    prompt = f"""
Extract information from this text matching the schema.

<text>
{text}
</text>

<schema>
{json.dumps(schema, indent=2)}
</schema>

Return valid JSON matching the schema exactly.
"""
    return model.generate(prompt, response_format={"type": "json_object"})
```

### Transformation

```python
def transform_data(input_data, input_fmt, output_fmt, model):
    prompt = f"""
Transform this {input_fmt} data to {output_fmt}.

<input>
{input_data}
</input>

<output_requirements>
{specify_requirements(output_fmt)}
</output_requirements>

Return transformed data.
"""
    return model.generate(prompt)
```

### Best Practices
- Use native JSON mode when available
- Provide explicit schemas with types
- Validate output programmatically
- Don't over-instruct extraction process

---

## 5. Multimodal Applications

### Document Understanding

```python
def understand_document(text, images, task, model):
    prompt = f"""
{task}

<text_content>
{text}
</text_content>

[Images provided separately]

Analyze both text and visual elements.
Return findings as structured JSON.
"""
    return model.generate_multimodal(text=prompt, images=images)
```

### Visual Analysis

```python
def analyze_images(images, analysis_type, model):
    prompt = f"""
Perform {analysis_type} on the provided images.

Identify and describe relevant visual elements.

Return JSON:
{{
  "observations": ["array"],
  "analysis": "string",
  "key_findings": ["array"]
}}
"""
    return model.generate_multimodal(text=prompt, images=images)
```

### Best Practices
- Label each modality explicitly (critical for Gemini)
- Don't over-instruct cross-modal reasoning
- Clear context per modality
- Let models integrate modalities naturally

---

## 6. RAG Applications

### Pattern

```python
def rag_query(query, retrieved_docs, model):
    prompt = f"""
Answer this query using ONLY the provided documents.

<query>
{query}
</query>

<documents>
{format_documents_with_ids(retrieved_docs)}
</documents>

Requirements:
- Base answer on provided documents only
- Cite sources: [Doc 1], [Doc 2], etc.
- If not in documents: "Not found in provided sources"

Return JSON:
{{
  "answer": "string",
  "sources": ["doc IDs"],
  "confidence": 0.0-1.0
}}
"""
    return model.generate(prompt)
```

### Best Practices
- Structure retrieved context clearly with document IDs
- Use semantic chunking for retrieval
- Leverage large context windows (1M-2M) for more documents
- Require citation to specific sources
- Enforce "not found" responses for missing information

---

## 7. Specialized Domains

### Legal Analysis

```python
def analyze_legal(document, analysis_type, model):
    prompt = f"""
You are a legal analyst. Perform {analysis_type} on this document.

<document>
{document}
</document>

Focus on:
- Key clauses and obligations
- Potential risks or issues
- Relevant legal precedents (if applicable)

Return structured analysis with citations to specific sections.
"""
    return model.generate(prompt, thinking_mode='deep')
```

### Scientific/Medical Analysis

```python
def analyze_scientific(paper, focus, model):
    prompt = f"""
You are a scientific researcher. Analyze this paper focusing on {focus}.

<paper>
{paper}
</paper>

Evaluate:
- Methodology rigor
- Statistical validity
- Key findings and limitations
- Implications

Provide evidence-based analysis with specific citations.
"""
    return model.generate(prompt, thinking_mode='deep')
```

### Financial Analysis

```python
def analyze_financial(data, analysis_type, model):
    prompt = f"""
Perform {analysis_type} on this financial data.

<data>
{format_financial_data(data)}
</data>

Provide:
- Key metrics analysis
- Trends and patterns
- Risk assessment
- Recommendations

Return structured JSON with numerical precision.
"""
    return model.generate(prompt, thinking_mode='deep')
```

---

## 8. Conversational Applications

### Chatbot Pattern

```python
def chatbot_response(history, message, domain, model):
    system = f"""You are a helpful assistant specializing in {domain}.

Provide accurate, helpful responses based on conversation context.

Capabilities: {list_capabilities()}
Constraints: {list_constraints()}
"""
    messages = [
        {"role": "system", "content": system},
        *history,
        {"role": "user", "content": message}
    ]
    return model.generate(messages)
```

### Best Practices
- System prompts: clear and concise, not pages of instructions
- Monitor context accumulation in multi-turn
- Use context compaction for long conversations
- State management for complex interactions

---

## 9. Evaluation & Testing

### Response Evaluation

```python
def evaluate_response(response, criteria, model):
    prompt = f"""
Evaluate this response against the criteria.

<response>
{response}
</response>

<criteria>
{format_criteria(criteria)}
</criteria>

Return JSON:
{{
  "scores": {{"criterion": 0.0-1.0}},
  "strengths": ["array"],
  "weaknesses": ["array"],
  "overall_score": 0.0-1.0
}}
"""
    return model.generate(prompt)
```

### Test Case Generation

```python
def generate_test_cases(spec, test_type, model):
    prompt = f"""
Generate {test_type} test cases for this specification.

<specification>
{spec}
</specification>

Create comprehensive test cases covering:
- Normal cases
- Edge cases
- Error cases

Return as JSON array of test cases.
"""
    return model.generate(prompt)
```

---

## 10. Performance Optimization by Application

### High-Stakes Analysis (Legal, Medical, Financial)
- Use `thinking_mode='deep'` or `reasoning_profile='deep'`
- Request verification
- Structured output with confidence scores

### Real-Time Applications (Chatbots, Interactive)
- Use `thinking_mode='light'` or `reasoning_profile='light'`
- Optimize for latency
- Cache system prompts

### Batch Processing (Data extraction, Transformation)
- Use native JSON mode
- Parallel processing
- Validate outputs programmatically
- Use batch API for 50% cost savings

### Creative Applications (Content, Ideation)
- Higher temperature (except Gemini: always 1.0)
- Multiple generations with selection
- Less strict output format

---

## 11. Domain Anti-Patterns

All anti-patterns reference 02-techniques-patterns_v5.md. Domain-specific examples:

### Content Generation
**Don't**: "First brainstorm, then outline, then write intro, then body, then conclusion..."
**Do**: "Generate article about {topic}. Context: {background}. Length: {words}. Style: {tone}."

### Code Analysis
**Don't**: "Step 1: Check syntax. Step 2: Review logic. Step 3: Assess security..."
**Do**: "Analyze this code for security vulnerabilities. Return issues with severity."

### Data Extraction
**Don't**: "Carefully read the text. Identify each entity. For each, extract name and type..."
**Do**: "Extract entities from text. Schema: {schema}. Return valid JSON."

---

## References

- OpenAI GPT-5 Application Patterns (2025-2026)
- Anthropic Claude 4.x Use Cases (2025-2026)
- Google Gemini 3.x Domain Applications (2025-2026)
- Yao, S., et al. (2022). "ReAct: Synergizing Reasoning and Acting." [arXiv:2210.03629](https://arxiv.org/abs/2210.03629)
- Liu, P., et al. (2023). "Pre-train, Prompt, and Predict." [ACM Computing Surveys](https://dl.acm.org/doi/abs/10.1145/3560815)
