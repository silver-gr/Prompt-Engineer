# Data Extraction & Transformation Tasks (March 2026)

## Core Guidance

- Provide input data verbatim
- Specify exact output schema with types and allowed values
- Define handling for missing, ambiguous, or malformed fields
- Use native JSON mode when available (GPT-5, Gemini)

## Extraction Pattern

```xml
<task>
Extract [entity types] from the data below.
</task>

<data>
[raw input -- structured or unstructured]
</data>

<output_format>
Return JSON matching this schema exactly:
{
  "records": [
    {
      "field_a": "string",
      "field_b": "number",
      "field_c": "enum(value1|value2|value3)"
    }
  ]
}

For missing fields, use null.
For ambiguous values, use the most likely interpretation and set "confidence": 0.0-1.0.
</output_format>
```

## Transformation Pattern

```xml
<task>
Convert the following [source format] to [target format].
</task>

<data>
[input data]
</data>

<rules>
- [mapping rule 1]
- [mapping rule 2]
- [handling for edge cases]
</rules>

<output_format>
[target schema]
</output_format>
```

## Summarization Pattern

```
Summarize the following [document type] in [length constraint].

<data>
[document]
</data>

Focus on: [specific aspects]
Format: [bullets | paragraph | structured]
```

## Best Practices

- Always provide the exact JSON schema you expect
- Include examples of edge cases in the data if known
- For large datasets: process in batches, validate each batch
- Use response prefixes for Gemini: `Start with: {"records":`
- Validate output programmatically -- don't trust format compliance

## Model Selection for Data Tasks

| Task | Best Model |
|------|-----------|
| Complex entity extraction | Opus 4.6 / GPT-5.2 Thinking |
| High-volume extraction | Haiku 4.5 / GPT-5.3 Instant |
| Large document summarization | Gemini 3.1 Pro (2M context) |
| Budget batch processing | DeepSeek V3.2 |
| Structured data transform | Sonnet 4.6 |
