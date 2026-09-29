# Other Frontier Models — Grok, DeepSeek, GLM, Qwen, Kimi, MiniMax, Llama, Mistral, Mercury

*Source: 03-model-catalog_v5.md §4-§9 (xAI, Chinese frontier, open-weight/EU, specialized architectures, selection guide, cost economics).*

A router to a choice, not a deep dive. Claude, OpenAI, and Gemini each have their own file in this directory. Every version-volatile number — context sizes, pricing, output caps, model IDs, effort enums — lives in references/specs-current.md.

## Pick-one table

| Model | Pick it when | Distinctive control or strength | Template dialect |
|---|---|---|---|
| **Grok 4.5** | You want an always-reasoning model over a very large single prompt | `reasoning_effort` — reasoning **cannot be disabled**. `presence_penalty`, `frequency_penalty`, and `stop` are rejected as errors. No official prompting guide exists; treat behavior as empirical. Crossing the large-prompt tier reprices the **entire** request, not the overage — budget before you pad context. | Markdown headers. Hierarchical headings are the documented way to structure large contexts. |
| **DeepSeek V4** | Cost is the binding constraint and you still need frontier reasoning | Thinking is switched on through the request body's thinking config, **not** by emitting raw `<think>` tags. Thinking mode ignores sampling parameters entirely. | Markdown headers (dialect unspecified in source). |
| **GLM-5.2** | You need the strongest permissively-licensed open-weight model, or you self-host | `reasoning_effort`. Supply bilingual glossaries for multilingual output and define function-calling payloads explicitly. | Markdown headers (unspecified). |
| **Qwen 3.7** | Multilingual breadth is the deciding factor and the task is text-only | `enable_thinking` toggle — the cleanest reasoning on/off switch in this group. Always name the target output language explicitly. Note `qwen3.7-max` has **no vision at all**; `qwen3.7-plus` is the multimodal sibling. | Markdown headers (unspecified). |
| **Qwen 3.8-Max-Preview** | You want Qwen's multilingual strength *and* vision — image understanding, OCR, chart and document analysis, visual grounding | Same dialect and `enable_thinking` toggle as 3.7. Access is gated to a subscription tier, so confirm availability before designing around it. Its published specs are vendor-console figures with no independent corroboration. | Markdown headers (unspecified). |
| **Kimi K3** | Long-horizon coding or end-to-end knowledge work with native vision (no separate image pipeline) | Always-on thinking, returns `reasoning_content`, `reasoning_effort` available. Built for extended multi-step sessions. | Markdown headers (unspecified). |
| **Kimi K2.6** | Large-scale agent orchestration — swarm decomposition at a scale no other vendor matches | Agent Swarm v2. Models reach no external resources by default; wire tools explicitly. Still uses sampling parameters, and the right value differs between thinking and instant modes. | Markdown headers (unspecified). |
| **MiniMax M3** | Budget coding plus native multimodal in one model | No distinctive reasoning knob documented. Plan against the guaranteed context floor rather than a headline maximum. | Markdown headers (unspecified). |
| **Llama 4 (Scout / Maverick)** | Self-hosting, customization, or the largest available context; Meta's frontier line is frozen here | Open weights, no documented reasoning control. Scout is the efficiency variant. | Claude/GPT-style structured context — XML tags work, markdown headers work. Stay consistent. |
| **Mistral Large 3** | EU sovereignty or compliance is a hard requirement | Strong function calling and JSON generation. Lead with explicit function schemas. | Markdown headers with explicit JSON/function schemas (dialect unspecified). |
| **Mercury 2** | Latency is the binding constraint — voice agents, phone calls, real-time tool loops — and the context fits comfortably | A **diffusion** LLM, not autoregressive: tokens emerge in parallel, so it runs an order of magnitude faster but streaming does not arrive strictly left-to-right. Tune `reasoning_effort` (`instant`/`low`/`medium`/`high`) before reaching for anything else. Text-only, and its context window is small for this generation — wrong pick for large-document work no matter how fast it is. | Markdown headers; OpenAI-compatible API, no special dialect. |

Only Grok's heading preference and Llama's Claude/GPT-style structured context are stated outright in the source. The rest are marked unspecified: markdown headers are the safe default because no vendor-specific XML guidance exists for them.

## Replay fidelity — DeepSeek, GLM, Kimi

These models carry reasoning state inside the conversation and are strict about how it comes back:

| Model | Requirement |
|---|---|
| DeepSeek V4 | Echo `reasoning_content` back on tool-result turns or the API errors. |
| GLM-5.2 | Preserved thinking blocks must match exactly when replayed. |
| Kimi K3 | Preserved thinking history mode — replay full assistant messages verbatim, including `reasoning_content` and `tool_calls`. |

One rule covers all three: never summarize, reformat, reorder, or strip a reasoning block you are sending back.

## Where AP-2 and AP-3 do not apply

Explicit chain-of-thought (AP-2) and multi-example few-shot (AP-3) are anti-patterns because frontier reasoning models already reason natively and the scaffolding fights them. They remain legitimate technique on:

- **Llama 4 family** and **Mistral Large 3** — open-weight/legacy lines with no documented native reasoning control.
- **Any model in this file run with thinking off** — Qwen with `enable_thinking` false, Kimi K2.6 in instant mode, DeepSeek without the thinking config enabled.

On those, step-by-step decomposition and several worked examples improve output. Everywhere else in this file — Grok, DeepSeek in thinking mode, GLM, Qwen in thinking mode, Kimi K3 — AP-2 and AP-3 stay in force.

## Audit note

If you scan a DeepSeek prompt for literal `<think>` tags, or a Grok request for `stop` / `presence_penalty` / `frequency_penalty`, remember that a match inside a quoted example, inside a negation, or inside a code fence is a candidate, not a violation. Confirm it is a live instruction or a real request key before flagging it.

Model settings are configuration, not prompt text.

```
DO: Pick by constraint — cost picks DeepSeek, multilingual picks Qwen, EU compliance picks Mistral, swarm orchestration picks Kimi K2.6, self-hosting picks GLM or Llama.
DO: Structure large Grok contexts with hierarchical markdown headings.
DO: Enable DeepSeek thinking through the request body's thinking config.
DO: Echo reasoning_content and replay preserved thinking blocks verbatim on DeepSeek, GLM, and Kimi.
DO: Name the target output language explicitly for Qwen and GLM multilingual work.
DO: Wire tools explicitly for Kimi — it reaches nothing external by default.
DO: Lead with function schemas on Mistral when you want structured JSON.
DO: Keep explicit CoT and multi-example few-shot for Llama, Mistral, and any thinking-off run.
DO: Hold one template dialect per prompt, whichever you pick.
DON'T: Send raw <think> tags to DeepSeek.
DON'T: Send presence_penalty, frequency_penalty, or stop to Grok — they error.
DON'T: Assume Grok reasoning can be turned off; it cannot.
DON'T: Summarize, reformat, or drop a reasoning block you are replaying.
DON'T: Apply explicit step-by-step CoT to Grok, GLM, Kimi K3, or any thinking-on run.
DON'T: Pad context past a pricing tier boundary without checking specs-current.md first.
DON'T: Assume these vendors accept Claude- or Gemini-style parameter conventions — verify per vendor.
```
