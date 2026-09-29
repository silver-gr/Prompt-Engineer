# Task Recipes: Extraction, Transformation & Structured Output

*Source: 05-domain-applications_v5.md §4 (Data Extraction & Transformation), §10 (Batch Processing); 01-foundations_v5.md §7 (Structured Outputs & Constrained Decoding); 02-techniques-patterns_v5.md §6 (Structured Output Prompting)*

## Schema first

The schema is the prompt. Write it before the instruction text and the instruction text shrinks to one line.

| Rule | Why |
|---|---|
| Give the exact schema, with a type per field | "Return JSON" without a schema returns a plausible shape, not yours |
| Annotate constrained fields inline: `"type": "person|org|location"` | Enumerations in the schema beat enumerations in prose |
| Include a field for absence — `null`, `"not_found"`, or `"unknown"` | Without it the model invents a value to fill the slot |
| Add `confidence` when downstream code will route on it | Makes low-quality extractions filterable instead of silent |
| Validate every response programmatically | The schema is a request, not a guarantee |

```
Return JSON matching this schema exactly:
{
  "summary": "string",
  "entities": [
    {"name": "string", "type": "person|org|location", "confidence": "number (0.0-1.0)"}
  ],
  "metrics": {"score": "number (0.0-1.0)"},
  "unresolved": ["fields the source did not contain"]
}
```

## Native structured outputs vs prompt-level instructions

Prefer the native mechanism whenever the provider exposes one — it constrains decoding rather than requesting cooperation, and removes the parse-failure class entirely.

| Provider | Native mechanism documented in the KB |
|---|---|
| OpenAI | `response_format={"type": "json_object"}` |
| Google | `generation_config={"response_mime_type": "application/json"}` |
| Anthropic | No JSON-mode flag documented — the KB directs you to XML output tags or an explicit JSON instruction; check `references/specs-current.md` before asserting otherwise |

| Use native structured output when | Use prompt-level format instructions when |
|---|---|
| Output is consumed by code | Output is read by a human |
| The job is batch or high volume | The shape is exploratory and still changing |
| Parse failure is expensive | The provider has no native mode for this call |
| The schema is stable | The response mixes prose and structure |

Native mode and a schema in the prompt are complements: the flag guarantees valid JSON, the schema decides *which* JSON. Ship both. For Gemini, opening the expected structure inside the prompt text (showing the response starting with `{"`) anchors the format — this is prompt-level anchoring, not an API `prefix` parameter, which Gemini does not have. For Claude, XML output tags delimit structure reliably.

## Extraction

```
Extract information from the text below according to the schema.

<text>
[source text]
</text>

<schema>
[schema with a type per field]
</schema>

Return valid JSON matching the schema exactly. If a field is not present in the
text, return null for it -- do not infer, and do not omit the key.
```

Do not narrate the procedure — "scan for names, then dates, then amounts" is AP-1 and costs recall.

## Transformation

```
Transform the [input format] data below into [output format].

<input>
[data]
</input>

<output_requirements>
[target schema, field mapping, units, precision, date format, null handling]
</output_requirements>

Preserve every input record. Return only the transformed data.
```

Name the silently ambiguous rules: rounding, timezone, encoding, ordering, and the fate of records that fail the mapping.

## Classification

Enumerate the label set in the schema, not in prose. Always give an `unknown` / `other` escape hatch or borderline items get forced into a real class. State multi-label explicitly — single-label is the default assumption. Include a rationale field only when a human reviews the output; it costs tokens per item.

```
Classify each item using exactly one label from the set.

<items>
[1] [item]
[2] [item]
</items>

Return JSON:
{"results": [{"id": "number",
              "label": "label_a|label_b|label_c|unknown",
              "confidence": "number (0.0-1.0)"}]}
Use "unknown" when the item does not clearly fit a label. Do not add labels
outside the set.
```

Borderline definitions belong in the schema annotation or in two or three examples — not in a paragraph of rules per class (AP-3 above five examples).

## Batch and pipeline notes

Validate on receipt and re-run failures rather than repairing text; process independent records in parallel; keep the schema block byte-identical across calls so the shared prefix stays cacheable.

## Cross-references

Grounding extraction in retrieved documents with citations → `tasks-analysis.md`. Extracting from untrusted or injected text → `patterns-safety.md`. Measuring extraction accuracy or building a regression set → `patterns-eval.md`. Per-model format anchoring and parameter rules → the matching `models-*.md`; model settings are configuration, not prompt text.

```
DO: Write the schema first and give a type for every field.
DO: Use the provider's native structured-output mechanism when code consumes the result.
DO: Give absence its own representation — null, "unknown", or an unresolved list.
DO: Enumerate closed label sets inside the schema.
DO: Validate every response programmatically and re-run failures.
DON'T: Ask for "JSON" without supplying the exact schema.
DON'T: Narrate the extraction or transformation procedure (AP-1).
DON'T: Rely on prompt text alone for format when a native mode exists.
DON'T: Leave rounding, timezone, units, or ordering to inference.
DON'T: Force borderline items into a real class by omitting an escape label.
```
