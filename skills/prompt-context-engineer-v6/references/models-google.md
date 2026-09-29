# Gemini (Google) Prompting Rules

*Source: 07-gemini-practices_v5.md, all sections; anti-pattern IDs from 02-techniques-patterns_v5.md.*

Gemini treats a prompt as an executable instruction list, not a conversation. Directness beats persuasion. Conversational padding ("please", "kindly", "could you") is AP-4 and actively degrades Gemini instruction-following — on other families it is merely wasted tokens. Do not carry over Gemini 2.x-era chain-of-thought scaffolding; native reasoning makes it counterproductive (AP-2).

## Settings

| Knob | Rule |
|------|------|
| `temperature`, `top_p`, `top_k` | **OMIT the keys entirely.** Formally deprecated; ignored on 3.6+ and a 400 on future generations. Sub-default values can still loop on 3.5 Flash, 3.1 Pro, and 3 Flash (AP-5). Steer style and variety through prompt text; for determinism use a system instruction with explicit rules plus a response schema. |
| `thinking_level` | Ceiling on reasoning depth. `minimal` is not available on 3.7/3.8 Flash or 3.1 Pro. Defaults differ per model: references/specs-current.md. Google's guide: `low` for latency-critical work, `medium` for most tasks including complex code and agents, `high` for deep reasoning and math. |
| `thinking_budget` | No longer recommended; kept for backward compatibility. Still a 400 when sent with `thinking_level` in the same request. Use `thinking_level`. |
| `response_mime_type` + `response_schema` | Structured output on `generateContent` only. On the Interactions API (GA, recommended) use `response_format` with `mime_type` and `schema`. |
| Prefill / `prefix` | None exists. A request ending in a non-empty `model` turn is a 400 on 3.6+. Anchor output with `system_instruction` or a response schema. |
| `collaborative_planning` (Deep Research) | Off by default, so research executes without showing a plan. Turn it on when you intend to edit the plan before execution — reviewing and editing the plan is the highest-leverage Deep Research technique. |

Prompt text still moves reasoning depth *within* the `thinking_level` ceiling: "Think very hard before answering" raises effort inside the level; pair a low level with "Think silently" for latency. Model settings are configuration, not prompt text.

Gemini 3.x is terse by default — ask for a conversational or detailed style explicitly. 3.8 Flash spends more tokens by design (smaller steps, iterative tools, self-verification): use `low` for everyday tasks or stay on 3.7 Flash. If the model over-uses tools, lower `thinking_level` first, then add "You have a limited action budget of <n> tool calls."

## Constraint ordering

Position is load-bearing.

| Position | Content | Why |
|---|---|---|
| 1 — TOP | Persona, behavioral constraints, and output-format requirements | They frame how everything after them is interpreted |
| 2 | Context and source material: documents, data, code | Context FIRST |
| 3 | Main task or question | Questions LAST, after an anchor phrase |
| 4 — optional | Recap of negative and quantitative limits | Google's Vertex prompt-design page suggests an end-of-prompt recap |

Bridge context to task with an anchoring transition — "Based on the information above...", "Using the data provided...", "Given the context..." — so the model knows where source material ends and the instruction begins.

Label every non-text input explicitly ("Image 1: product mockup", "Video 1: user testing session"). Gemini treats text, image, audio, and video as equal-class inputs and confuses unlabeled ones.

Personas are obeyed very seriously and can override later instructions (source archived). State persona boundaries explicitly and avoid ambiguous scenarios when a persona is set.

## Template (XML)

Choose XML or markdown headers and stay consistent within a single prompt. XML canonical form:

```xml
<role>
You are a specialized assistant for [domain]. You are precise, analytical, and direct.
</role>

<constraints>
- Tone: [formal | technical | plain]
- Cite sources: [yes | no]
- Output format: [shape of the answer]
</constraints>

<context>
[every document, dataset, code file, and background fact — before any question]
</context>

<task>
[one direct instruction, no fluff]
</task>

<final_instruction>
[optional recap of hard limits]
</final_instruction>
```

## Few-shot: an explicit exemption from AP-3

AP-3 caps examples for reasoning models. Gemini is the documented exception — Google recommends always including a few examples with identical formatting; too many overfit. Rules:

- Keep formatting identical across every example; inconsistent structure is worse than no examples.
- Show the correct pattern, never the pattern to avoid.
- Format demos only — no reasoning steps inside examples. AP-2 still applies.
- Experiment with the count. Excessive examples overfit and burn context.

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

## Function calling

Stateless multi-turn — when you manage history yourself rather than using Interactions API stateful mode (`store: true` + `previous_interaction_id`, the default):

- Gemini returns **thought signatures** alongside function calls. Send them back unmodified in the next turn's history, even when switching models; resend built-in tool (Search) signatures too. Dropping or altering them breaks reasoning continuity.
- Exactly one function response per function call, matched on **both** `id` and `name`. A mismatch on `generateContent` silently returns empty output with `finish_reason: STOP` (Interactions errors).
- Put multimodal content inside the function response. Append extra instructions to the function-response text after `\n\n`, not as separate parts.
- Do not demand structured status text (XML/JSON) right before a tool call — it can cause `Malformed_Function_Call`. Use an `update()` tool or Markdown headers.
- Keep 10-20 active tools at most.

## Audit notes

When reviewing a Gemini prompt, scan for the literal strings "please" / "kindly" / "could you" (AP-4), "step by step" (AP-2 — still a hit; note that Google's own template ends with "Remember to think step-by-step before answering.", so deletion is low-risk), and `temperature` / `top_p` / `top_k` (AP-5). A match inside a quoted example, inside a negation, or inside a code fence is a candidate, not a violation — confirm it is a live instruction before flagging it. Also check that persona, behavioral, and output-format constraints sit above the context block and the question sits last.

```
DO: Omit temperature, top_p, and top_k keys entirely from the request.
DO: Put persona, behavioral, and output-format constraints at the TOP.
DO: Put all context and source material FIRST, the question LAST.
DO: Optionally recap negative and quantitative limits at the very END.
DO: Anchor the handoff with "Based on the information above...".
DO: Use thinking_level to set reasoning depth; raise it for research, lower it for extraction.
DO: Include a few identically formatted examples when examples help.
DO: Label every image, audio, and video input by name and role.
DO: Return thought signatures unmodified in stateless multi-turn function calling.
DO: State the current year for anything time-sensitive.
DO: Pick XML or markdown headers and hold that dialect for the whole prompt.
DON'T: Set temperature to 1.0 — that is the old, wrong advice; remove the key instead.
DON'T: Set any sampling parameter below its default; sub-default temperature can loop.
DON'T: Send thinking_budget and thinking_level in the same request (400).
DON'T: End a request with a prefilled model turn (3.6+ → 400).
DON'T: Put persona, tone, or safety rules at the end.
DON'T: Send `thinking_level: minimal` to 3.7/3.8 Flash.
DON'T: Use "please", "kindly", or any conversational padding.
DON'T: Use Gemini 2.x-era explicit step-by-step CoT scaffolding.
DON'T: Write a broad "do not infer or assume anything"; scope it to external knowledge.
```
