# Task Pattern: Data Extraction / Transform

## Guidance
- Provide the input data verbatim.
- Specify exact output schema and allowed values.
- Define how to handle missing or ambiguous fields.

## Minimal Template
```
Extract fields from the data below.

<data>
[raw input]
</data>

Return JSON matching:
{
  "records": [
    {"field_a": "string", "field_b": "number", "field_c": "enum"}
  ]
}
```
