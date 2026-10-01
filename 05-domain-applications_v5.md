# Domain-Specific Applications (September 2026)

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
    return call_model(prompt, effort="medium")  # pseudocode helper; real config: output_config.effort (Claude) · reasoning.effort (GPT) · thinking_level (Gemini)
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

### Model-Specific Writing Fixes

Output-style defaults, fixed in the prompt (settings stay in the model modules).

| Model | Symptom | Fix |
|---|---|---|
| Fable 5.1 | Dense, mannered prose | Define "mannered prose" (prefer the user message), or just `Please remove all mannered prose.` |
| Fable 5.1 | Too little formatting | Delete anti-formatting rules; add a when-to-use-lists rule instead |
| Fable 5.1 | Unmarked quotations | One complete `<example>` (request, response, rationale) showing quotes marked |
| GPT-6 Astra | Heavy Markdown, recurring phrases | Specify the style (plain paragraphs, lists only for parallel or sequential items) and add the blocklist below |
| GPT-5.6 | Too brief under a broad "be concise" | State what a short answer must keep; define tone by concrete writing choices, not labels like "friendly" |

Official GPT-6 anti-slop blocklist: "delve", "foster", "leverage", "it's worth noting", "importantly", "genuinely", "Bottom Line:", "In short:", and contrastive "X, not Y" framing. Use it as an output-style fix, not a prompt anti-pattern.

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
    return model.generate(prompt, reasoning_effort='high')
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
- Opus 5.5 chat analysis: optionally add `Once you have answered something, treat that answer as done. On later turns, focus your thinking on what the user is asking now, and don't go back over an earlier answer unless the user asks about it or points out a problem with it.` Skip it for long analyses and agentic work -- it can suppress self-correction.

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
    return model.generate(prompt)  # no temperature/top_p/top_k: 400 on current Claude, omitted on Gemini
```

### Best Practices
- Don't prescribe code review steps ("first check syntax, then review logic...")
- Specify language, conventions, and constraints
- Don't set sampling parameters: non-default `temperature`/`top_p`/`top_k` return 400 on current Claude; on Gemini omit the keys entirely (deprecated Jul 21 2026; sub-default values can still loop on older Gemini models)
- Let models do comprehensive analysis naturally
- Review prompts tuned for earlier models show lower recall on current ones: a filter such as "only report high-severity" is followed literally and drops real findings. Ask for full coverage with confidence and severity per finding, and filter in a separate pass

### Model-Specific Code Levers

Behavior fixes in the prompt (settings stay in the model modules).

| Model | Failure | Add |
|---|---|---|
| Sonnet 5.5 | Stops to check in; adds unrequested files | `Keep working until everything the user asked for is done, and only stop to ask when you can't go on without the user or before a risky step.` Then: `When the work the user asked for is done and checked, stop and report. Don't add features, tests, files, docs or refactors that weren't asked for. If you think one would help, mention it at the end instead of doing it.` The first line raises cost at low/medium effort. |
| Fable 5.1 | Extra fixes, extra tests, whole-file rewrites | Extras-only paragraph: report nearby problems as follow-ups rather than fixing them; commit tests only where the task asks, roughly one focused test per stated behavior; implement every requested behavior completely. Edit line: `when it will not affect the end result, try to surgically edit a file rather than rewrite the entire thing.` |
| Opus 5.5 (frontend) | Default look | Name the specific patterns to avoid (e.g. cream background, italic accent words, "01/02/03" labels, monospace labels, pill buttons) and iterate the list. "Avoid a generic AI look" only swaps one default for another. |
| GPT-6 Astra | Over-testing; heavy reliance on repo guidance | `Do not write tests for reversible, low-impact changes that mirror the implementation.` Broaden testing only when new changes, failures, or unresolved concerns justify it. Astra is more sensitive to AGENTS.md and skills: use contextual doc pointers, not "read X, Y, Z before every edit", and grant explicit permission for safe local test loops. |
| GPT-5.6 | Skipped verification | Keep explicit steps: targeted tests, type check, build, smoke test. |

Sonnet 5.5 at low effort: add a real-check paragraph -- run a real check that exercises the change before reporting done; install declared deps with the project's own package manager, never sudo; if no real check can run, say which one was not run and why.

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
- Give absence its own representation (`null`, `"unknown"`, or an `unresolved` list) so the model doesn't invent values
- JSON on multi-step reasoning (Sonnet 5.5): use structured outputs plus adaptive thinking, and end the system prompt with "Think the problem through before you answer." (or use `xhigh` alone; not `between_tools`). Treat `stop_reason:"max_tokens"` as failure even when the JSON is valid. Without structured outputs, parse the **last** JSON value, not first `{` to last `}`
- Batch: keep the schema block byte-identical across calls so the shared prefix stays cacheable

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
- Dense visual inputs (charts, drawings, scans): crop/zoom/code tools beat raising effort on Sonnet 5.5 and Fable 5.1; Opus 5.5 needs less scaffolding, so re-test old vision scaffolding before keeping it

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
- Leverage large context windows (1M-class; 10M on Llama 4 Scout) for more documents
- Require citation to specific sources
- Enforce "not found" responses for missing information
- Freshness (Sonnet 5.5): `Use the search tool to check specifics that may have changed since your training, such as what is allowed, required or charged, even when you feel confident. For researched work such as a report or a comparison, gather current sources rather than writing from your training knowledge.`
- Low-effort memory answers on Fable 5.1: recognizing a name is not knowing its current state -- tell it to search the name as written, or raise effort for that turn
- Deep-search prompts: state an explicit completion criterion (what counts as done) up front

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
    return call_model(prompt, effort="high")  # pseudocode helper; real config: output_config.effort (Claude) · reasoning.effort (GPT) · thinking_level (Gemini)
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
    return call_model(prompt, effort="high")  # pseudocode helper; real config: output_config.effort (Claude) · reasoning.effort (GPT) · thinking_level (Gemini)
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
    return call_model(prompt, effort="high")  # pseudocode helper; real config: output_config.effort (Claude) · reasoning.effort (GPT) · thinking_level (Gemini)
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
- Claude: `output_config.effort: "xhigh"` or `"max"` · GPT-5.x / GPT-6: `reasoning.effort: "high"` (`"xhigh"` on 5.2+ (not re-verified this cycle — Verify), `"max"` on 5.6+ -- GPT-5 base tops out at `"high"`) · Gemini: `thinking_level: "high"`
- Structured output with confidence scores
- Note: on Opus 5 and GPT-6 Astra, skip explicit verification requests (AP-16) — keep the requirement as an output section (Sources, Limits, confidence)

### Real-Time Applications (Chatbots, Interactive)
- Claude: `output_config.effort: "low"` · GPT-5.x / GPT-6: `reasoning.effort: "low"` (`"none"` on 5.2+ (not re-verified this cycle — Verify) except GPT-6 Astra, where `none` returns 400, and GPT-6.1 Sol, which has no `none`; GPT-5 base uses `"minimal"`) · Gemini: `thinking_level: "low"` on 3.8 Flash (`"minimal"` errors there; valid on 3.6 Flash, 3.5 Flash and Flash-Lite)
- Optimize for latency
- Cache system prompts

### Batch Processing (Data extraction, Transformation)
- Use native JSON mode
- Parallel processing
- Validate outputs programmatically
- Use batch API for 50% cost savings
- Gemini Flash-Lite extraction: keep the default `minimal` thinking for throughput; raise it only for subagents that use tools

### Creative Applications (Content, Ideation)
- Multiple generations for variety (no temperature on current Claude or Gemini -- steer variety through prompt text)
- Generate N independently and select; don't ask for N variants in one response
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

- OpenAI GPT-5 / GPT-6 Application Patterns (2025-2026)
- Anthropic Claude 5.x Use Cases (2026)
- Google Gemini 3.x Domain Applications (2025-2026)
- Yao, S., et al. (2022). "ReAct: Synergizing Reasoning and Acting." [arXiv:2210.03629](https://arxiv.org/abs/2210.03629)
- Liu, P., et al. (2023). "Pre-train, Prompt, and Predict." [ACM Computing Surveys](https://dl.acm.org/doi/abs/10.1145/3560815)
