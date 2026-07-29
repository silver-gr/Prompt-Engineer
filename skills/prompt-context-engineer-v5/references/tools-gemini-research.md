# Gemini Deep Research (March 2026)

## Activation
- Available in Gemini UI with Deep Research enabled
- Not available via API -- UI-only feature
- Creates a research plan, executes multi-step web research

## When to Use
- Broad topic surveys requiring comprehensive coverage
- Competitive landscape analysis
- State-of-the-art reviews
- Any research benefiting from an editable plan

## Workflow
1. Submit research query
2. Gemini proposes a research plan (sections, sources, approach)
3. **Review and edit the plan** before execution (critical step)
4. Gemini executes research across multiple sources
5. Delivers structured report with citations

## Prompting Tips

### Be Specific About Scope
```
Research [topic] comparing [items] across these dimensions:
- [dimension 1]
- [dimension 2]
- [dimension 3]

Focus on [time period]. Include quantitative data where available.
Output as a structured report with comparison tables.
```

### Edit the Research Plan
This is the most important step. Before clicking "execute":
- Remove irrelevant sections
- Add missing dimensions
- Specify depth per section
- Redirect source types (academic vs industry vs news)

### Request Structure
```
Output format:
1. Executive summary
2. Methodology
3. Findings by dimension (with tables)
4. Key takeaways
5. Sources
```

## Strengths
- Broad coverage across many sources
- Structured, report-style output
- Editable research plan (unique feature)
- Good for initial landscape mapping

## Limitations
- **English-only** sources (significant limitation for non-English topics)
- Broad coverage, weaker depth on niche topics
- Time-sensitive data can be stale
- No API access
- Verify critical claims -- hallucination possible

## Comparison with Claude Research

| Feature | Gemini Deep Research | Claude Research |
|---------|---------------------|---------------|
| Plan editing | Yes (key differentiator) | No |
| Source languages | English only | Multilingual |
| Output style | Structured report | Analytical synthesis |
| Depth vs breadth | Breadth-focused | Depth-focused |
| Best for | Surveys, landscapes | Analysis, synthesis |
