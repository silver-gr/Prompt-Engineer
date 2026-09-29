# Task Recipes: Analysis, Research & Synthesis

*Source: 05-domain-applications_v5.md §2 (Analytical Reasoning), §6 (RAG Applications), §7 (Specialized Domains), §9 (Evaluation), §11 (Domain Anti-Patterns)*

Analysis quality is set by the data supplied and the output contract demanded. Framework prose adds nothing on reasoning models.

| Job | Grounding source | Failure to guard against | Contract that guards it |
|---|---|---|---|
| Analytical reasoning | Data you paste in | Unsupported assertion | `confidence` per claim, evidence required |
| Research over documents | Retrieved corpus | Answering from parametric memory | Per-claim citation + explicit not-found |
| Synthesis across sources | Multiple pre-read summaries | Silent averaging of contradictions | Named `conflicts` section |
| Domain analysis (legal, scientific, financial) | Primary document | Fluent-but-wrong specifics | Citation to section / figure / line item |

## Analytical reasoning

```
Analyze: [question]

<domain_context>
[what domain, what decision this feeds, what the reader already knows]
</domain_context>

<data>
[data, statistics, documents]
</data>

Return JSON:
{"executive_summary": "string",
 "key_findings": ["string"],
 "detailed_analysis": "string",
 "recommendations": ["string"],
 "confidence": "number (0.0-1.0)",
 "limits": ["what the data cannot support"]}
```

`limits` and `confidence` are the quality surface. Keep them as **sections of the output contract**, never as a behavioral instruction ("double-check your findings") — that phrasing is AP-16 and buys cost, not accuracy, on models that self-verify.

## Research over retrieved documents

Grounding needs three clauses together — source restriction, per-claim attribution, and an abstention path. Drop one and the model fills the gap from memory.

```
Answer the query using ONLY the provided documents.

<query>
[query]
</query>

<documents>
[Doc 1] [text]
[Doc 2] [text]
</documents>

Cite the document ID after every claim. If the documents do not contain the
answer, say "Not found in provided sources" -- do not answer from prior
knowledge.

Return JSON:
{"answer": "string", "sources": ["doc IDs"], "confidence": "number (0.0-1.0)"}
```

Structure the corpus with stable IDs and semantic chunks. Refer to documents by ID, never by position — "the second-to-last document" is AP-15 and degrades with context length.

## Synthesis across sources

Contradiction is signal. Force it into its own section or it gets smoothed away.

```
Synthesize the sources below into one account of [topic].

<sources>
[S1] [summary or excerpt]
[S2] [summary or excerpt]
</sources>

Return four sections:
Agreement -- claims supported by two or more sources, with source IDs.
Conflicts -- claims where sources disagree, stating each position and its source.
Gaps -- questions none of the sources answer.
Assessment -- your reading of the balance of evidence, with confidence.
```

## Domain variants

Change the evaluation axes and the citation target; the shape is unchanged.

| Domain | Evaluation axes | Cite to |
|---|---|---|
| Legal | Key clauses and obligations, risks, applicable precedent | Section / clause number |
| Scientific | Methodology rigor, statistical validity, findings vs limitations, implications | Figure, table, section |
| Financial | Key metrics, trends, risk assessment, recommendation | Line item and period |

Role prompts help set domain register but do not add accuracy — drop the persona on pure factual extraction (AP-11).

## Cross-references

Scored rubrics and judges → `patterns-eval.md`. Multi-step research with live tools or subagents → `patterns-agentic.md`. Untrusted or adversarial documents in the corpus → `patterns-safety.md`. Emitting the result as strict JSON for a downstream system → `tasks-data.md`. Effort and thinking settings for high-stakes analysis → the matching `models-*.md`; model settings are configuration, not prompt text.

```
DO: Supply the data; state the decision the analysis feeds.
DO: Require confidence, limits, and per-claim citation as output sections.
DO: Give every retrieved document a stable ID and cite by ID.
DO: Make abstention an explicit, allowed answer.
DO: Force disagreement between sources into its own named section.
DON'T: Prescribe the analytical steps — reasoning models decompose natively (AP-2).
DON'T: Add "verify your findings" or "double-check" instructions (AP-16).
DON'T: Reference sources by position in the context ("the last document", AP-15).
DON'T: Stack an expert persona onto a factual extraction task (AP-11).
DON'T: Say "think harder" or "keep going" when an answer looks thin (AP-14).
```
