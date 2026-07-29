# Gemini (Google) Prompting Rules

*Source: 07-gemini-practices_v5.md, all sections; anti-pattern IDs from 02-techniques-patterns_v5.md.*

Gemini treats a prompt as an executable instruction list, not a conversation. Directness beats persuasion. Conversational padding ("please", "kindly", "could you") is AP-4 and actively degrades Gemini instruction-following — on other families it is merely wasted tokens. Do not carry over Gemini 2.x-era chain-of-thought scaffolding; native reasoning makes it counterproductive (AP-2).

## Settings

| Knob | Rule |
|------|------|
| `temperature`, `top_p`, `top_k` | **OMIT the keys entirely.** Do not set them to 1.0 — remove them from the request and let the model default. Sub-default temperature may cause looping and degraded reasoning (AP-5). Steer style, tone, and variety through prompt text instead. |
| `thinking_level` | Ceiling on reasoning depth. Raise it for research, planning, creative work, and hard problems; lower it for extraction, formatting, and lookups. Supported values and per-model defaults: references/specs-current.md. |
| `thinking_budget` | Never send it together with `thinking_level` in the same request — the API rejects the call. Pick one mechanism; prefer `thinking_level` on current models. |
| `response_mime_type` + `response_schema` | Structured-output config on `generate_content`. The Gemini API has **no `prefix` parameter** — anchor output shape here, or in prompt text where a schema is overkill. |
| `collaborative_planning` (Deep Research) | Off by default, so research executes without showing a plan. Turn it on when you intend to edit the plan before execution — reviewing and editing the plan is the highest-leverage Deep Research technique. |

Prompt text still moves reasoning depth *within* the `thinking_level` ceiling: "Think very hard before answering" raises effort inside the level; pair a low level with "Think silently" for latency. Model settings are configuration, not prompt text.

## Constraint ordering — the single highest-value Gemini rule

Gemini drops non-behavioral constraints placed too early. Position is load-bearing.

| Position | Content | Why |
|---|---|---|
| 1 — TOP | Behavioral constraints: persona, role, tone, safety rules | They frame how everything after them is interpreted |
| 2 | Context and source material: documents, data, code | Context FIRST |
| 3 | Main task instruction | Questions LAST |
| 4 — LAST | Negative, formatting, and quantitative constraints | Dropped if placed early |

Bridge context to task with an anchoring transition — "Based on the information above...", "Using the data provided...", "Given the context..." — so the model knows where source material ends and the instruction begins.

Label every non-text input explicitly ("Image 1: product mockup", "Video 1: user testing session"). Gemini treats text, image, audio, and video as equal-class inputs and confuses unlabeled ones.

Personas are obeyed very seriously and can override later instructions. State persona boundaries explicitly and avoid ambiguous scenarios when a persona is set.

## Template (XML)

Choose XML or markdown headers and stay consistent within a single prompt. XML canonical form:

```xml
<role>
You are a specialized assistant for [domain]. You are precise, analytical, and direct.
</role>

<constraints>
- Tone: [formal | technical | plain]
- Cite sources: [yes | no]
</constraints>

<context>
[every document, dataset, code file, and background fact — before any question]
</context>

<task>
[one direct instruction, no fluff]
</task>

<output_format>
[shape of the answer]
</output_format>

<final_instruction>
[negative, formatting, and quantitative limits — LAST]
</final_instruction>
```

## Few-shot: an explicit exemption from AP-3

AP-3 caps examples for reasoning models. Gemini is the documented exception — Google recommends 2-3 examples, more than any other family. Rules:

- Keep formatting identical across every example; inconsistent structure is worse than no examples.
- Show the correct pattern, never the pattern to avoid.
- Format demos only — no reasoning steps inside examples. AP-2 still applies.
- Stop at the band. Excessive examples overfit and burn context.

## Context grounding

Force the model onto supplied material when it might otherwise fill gaps from training data:

```
Treat the provided context as the absolute limit of truth; any facts not
directly mentioned must be considered completely unsupported.
```

```
Perform calculations based strictly on provided text.
Do not introduce external information or common knowledge.
```

```
Verify with high confidence if you're able to access [source].
If you cannot verify, state 'No Info' and STOP.
If verified, proceed with the following query:
```

Prefer the narrow instruction above to a broad "do not infer or assume anything" — the broad form suppresses legitimate deduction along with hallucination.

## Time-sensitive queries

State the current year or date in the prompt. The training cutoff precedes today, and Gemini will otherwise reason from a stale present. Cutoffs: references/specs-current.md.

## Function calling — stateless multi-turn

When you manage conversation history yourself rather than using a server-side session:

- Gemini returns **thought signatures** alongside function calls. Send them back unmodified in the next turn's history. Dropping or altering them breaks reasoning continuity and degrades multi-turn tool use.
- Exactly one function response per function call, matched on **both** `id` and `name`. Never omit a response, never send two responses for one call, never mismatch the pairing.

## Audit notes

When reviewing a Gemini prompt, scan for the literal strings "please" / "kindly" / "could you" (AP-4), "step by step" (AP-2), and `temperature` / `top_p` / `top_k` (AP-5). A match inside a quoted example, inside a negation, or inside a code fence is a candidate, not a violation — confirm it is a live instruction before flagging it. Also check that behavioral constraints sit above the context block and that formatting or quantitative limits sit below the task.

```
DO: Omit temperature, top_p, and top_k keys entirely from the request.
DO: Put behavioral constraints (persona, tone, safety) at the TOP.
DO: Put all context and source material FIRST, the question LAST.
DO: Put negative, formatting, and quantitative constraints at the very END.
DO: Anchor the handoff with "Based on the information above...".
DO: Use thinking_level to set reasoning depth; raise it for research, lower it for extraction.
DO: Use 2-3 few-shot examples with byte-identical formatting when examples help.
DO: Label every image, audio, and video input by name and role.
DO: Return thought signatures unmodified in stateless multi-turn function calling.
DO: State the current year for anything time-sensitive.
DO: Pick XML or markdown headers and hold that dialect for the whole prompt.
DON'T: Set temperature to 1.0 — that is the old, wrong advice; remove the key instead.
DON'T: Set any sampling parameter below its default; sub-default temperature can loop.
DON'T: Send thinking_budget and thinking_level in the same request.
DON'T: Put formatting or negative constraints before the context — they get dropped.
DON'T: Put persona, tone, or safety rules at the end.
DON'T: Use "please", "kindly", or any conversational padding.
DON'T: Use Gemini 2.x-era explicit step-by-step CoT scaffolding.
DON'T: Write a broad "do not infer or assume anything"; scope it to external knowledge.
DON'T: Expect a prefill or prefix parameter — use response_schema or prompt-text anchoring.
```
