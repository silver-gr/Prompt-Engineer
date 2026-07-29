# Claude Research Tool (March 2026)

## Activation
- Available in Claude UI (claude.ai) with Research toggle enabled
- Not available via API -- UI-only feature
- Uses extended thinking + web search + document analysis

## When to Use
- Multi-source research requiring synthesis
- Fact-checking against current sources
- Literature reviews and competitive analysis
- Any task requiring web-sourced evidence

## Prompting Tips

### Be Explicit About Scope
```xml
<research_request>
Research [topic] with these parameters:
- Time range: [dates]
- Sources: [academic, news, industry reports]
- Depth: [overview | detailed | comprehensive]
- Geographic focus: [if relevant]
</research_request>

<deliverable>
[specific output format -- report, table, comparison]
</deliverable>
```

### Provide Motivation
Explain WHY you need the research -- Claude prioritizes better with context:
- "I'm evaluating vendors for [project]" > "Compare these vendors"
- "I need to brief my team on [topic]" > "Summarize [topic]"

### Structure Output Expectations
```xml
<output_format>
- Executive summary (3-5 sentences)
- Key findings (numbered, with source citations)
- Comparison table (if comparing items)
- Recommendations
- Sources list
</output_format>
```

## Reliability

- Treat citations as **starting points** -- verify critical claims
- Use a quote-first pass for long documents: "Quote the exact text that supports..."
- Cross-reference multiple sources for important facts
- Hallucination rate is lower with Research but not zero

## Comparison with Gemini Deep Research

| Feature | Claude Research | Gemini Deep Research |
|---------|---------------|---------------------|
| Interface | Claude.ai | Gemini UI |
| Depth | Focused, analytical | Broad, comprehensive |
| Citations | Inline with quotes | Report-style |
| Languages | Multilingual | English-only sources |
| Plan review | No pre-review | Editable research plan |
| Best for | Analytical synthesis | Broad surveys |

## Limitations
- Rate limits and beta behavior
- Can hallucinate -- always cross-check critical facts
- No API access (can't automate)
- Quality varies with query specificity
