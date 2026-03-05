# Analysis & Research Tasks (March 2026)

## Analytical Reasoning

- Provide complete data context
- Specify analysis framework if relevant
- Request structured conclusions with confidence levels
- Ask for evidence citations from the provided context

### Pattern
```xml
<context>
[domain background, relevant definitions]
</context>

<data>
[dataset or document to analyze]
</data>

<task>
Analyze [specific aspect]. Identify [patterns/causes/implications].
</task>

<output_format>
{
  "findings": [{"finding": "", "evidence": "", "confidence": 0.0-1.0}],
  "summary": "",
  "recommendations": []
}
</output_format>
```

## Research Synthesis

- Provide source materials in context
- Specify synthesis framework (compare, contrast, timeline, thematic)
- Request citation of specific sources
- Set scope boundaries to prevent hallucination

### Pattern
```
Synthesize the following [N] sources on [topic].

<sources>
[source materials with labels]
</sources>

Focus on: [specific aspects]
Flag any contradictions between sources.
Cite sources by label for each claim.
```

## Comparative Analysis

- Provide clear evaluation criteria
- Specify weighting if some factors matter more
- Request tabular output for easy comparison

## Decision Support

- Frame as "evaluate options" not "decide for me"
- Provide decision criteria and constraints
- Request pros/cons with evidence
- Ask for risk assessment

## Model Selection for Analysis

| Task | Best Model |
|------|-----------|
| Deep reasoning | Opus 4.6 / GPT-5.2 Thinking |
| Large document analysis | Gemini 3.1 Pro (2M context) |
| Research with real-time data | Grok 4.20 |
| Quick classification | Haiku 4.5 / GPT-5.3 Instant |
| Budget analysis | DeepSeek V3.2 |
