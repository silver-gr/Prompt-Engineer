# Other Frontier Models — Grok, DeepSeek, GLM, Qwen, Kimi, MiniMax, MiMo, Muse/Llama, Mistral, Mercury

*Source: 03-model-catalog_v5.md §4-§9 (xAI, Chinese frontier, open-weight/EU, specialized architectures, selection guide, cost economics).*

A router to a choice, not a deep dive. Claude, OpenAI, and Gemini each have their own file in this directory. Every version-volatile number — context sizes, pricing, output caps, model IDs, effort enums — lives in references/specs-other.md.


## Pick-one table

| Model | Pick it when | Distinctive control or strength | Template dialect |
|---|---|---|---|
| **Grok 4.7** (4.6/4.5 siblings) | You want an always-reasoning model over a very large single prompt; **Grok 4.3** accepts `none` — pick it for cheap reasoning-off work | `reasoning_effort` — reasoning **cannot be disabled** on 4.5–4.7. Responses API primary, Chat Completions legacy; replay `reasoning.encrypted_content` unchanged; set `prompt_cache_key` / `x-grok-conv-id` or cache hits are unreliable. Still no official xAI text prompting guide; docs now brand as "SpaceXAI" (API still x.ai). Crossing the large-prompt tier reprices the **entire** request — budget before you pad context. | Markdown headers. Hierarchical headings are the documented way to structure large contexts. |
| **DeepSeek V4.1-Flash** | Cost is the binding constraint and you still need frontier reasoning | Native vision; Responses API supported; effort enum changed — see specs-other.md. Thinking is switched on through the request body's thinking config, **not** by raw `<think>` tags, and ignores temperature and penalties (`top_p` is clamped, not ignored — specs-other.md). | Markdown headers (dialect unspecified in source). |
| **GLM-5.2 / GLM-5.3 / 5.3-Flash** | You need the strongest permissively-licensed open-weight model, or you self-host | `reasoning_effort`. **5.3 family forces thinking** (`disabled` → error). Supply bilingual glossaries for multilingual output and define function-calling payloads explicitly. | Markdown headers (unspecified). |
| **Qwen 3.8-Max** (3.7 = text-only sibling) | Multilingual breadth, plus vision (image, OCR, chart, document, grounding) on 3.8 | GA, multimodal, open weights under a custom license. `enable_thinking` toggle; effort enum has no `high`; never send effort and `thinking_budget` together. Always name the target output language. `qwen3.7-max` has **no vision**; `qwen3.7-plus` is the multimodal 3.7 sibling. | Markdown headers (unspecified). |
| **Kimi K3** | Long-horizon coding or end-to-end knowledge work with native vision | Always-on thinking, returns `reasoning_content`, `reasoning_effort` available. Built for extended multi-step sessions. | Markdown headers (unspecified). |
| **Kimi K2.6** | Large-scale agent orchestration — swarm decomposition at a scale no other vendor matches (Verify swarm numbers) | Agent Swarm v2. Models reach no external resources by default; wire tools explicitly. Sampling parameters are fixed server-side on K3/K2.7/K2.6 — send none. | Markdown headers (unspecified). |
| **MiniMax M3** | Budget coding plus native multimodal in one model | `thinking.type:"disabled"` exists; the Anthropic-compatible endpoint is the recommended path. Plan against the real context ceiling in specs-other.md; the pricing-tier boundary there is not a limit. | Markdown headers (unspecified). |
| **MiMo-V2.6-Pro / Flash** (Xiaomi) | You want the top open-weights model under MIT | No distinctive control documented. | Unspecified. |
| **Muse Spark** (Meta, closed API) | Meta's current line; you accept its fixed request contract | `developer` role outranks `user`; `system` = `developer`. Meta injects a hidden steering prompt — keep temperature 1.0 and prefer clearer instructions to lowering it. `stop`, `n>1`, `logprobs`, `top_p:0`, `reasoning_effort:"none"` → 400. Its Anthropic-compatible Messages endpoint rejects `stop_sequences`, `top_k`, `thinking:disabled`. | Markdown/XML both work; stay consistent. |
| **Muse Glimmer** (Meta, Apache-2.0 open weights) | Self-hosting Meta's current line | Native reasoning — "you don't prompt this into existence". Needs `apply_chat_template`; no parallel tool calls; avoid meta-instructions about internals. | As Muse Spark. |
| **Llama 4 (Scout / Maverick)** | Self-hosting only; Llama is frozen at Llama 4 | Open weights, no documented reasoning control. Scout is the efficiency variant. | Claude/GPT-style structured context — XML tags and markdown headers both work. Stay consistent. |
| **Mistral Medium 3.5** (Large 3 = open-weight alternative) | EU sovereignty or compliance is a hard requirement | `reasoning_effort` (`high` for agentic/code). Magistral is retired. Response content becomes a chunk list when thinking is on. Avoid asking the model to count words/characters, or numeric instead of worded rating scales. Lead with explicit function schemas; use structured outputs for format enforcement. | "Markdown and/or XML-style tags" (stated). |
| **Mercury 2.5** | Latency is the binding constraint — voice agents, phone calls, real-time tool loops — and the context fits comfortably | A **diffusion** LLM: tokens emerge in parallel, so it runs an order of magnitude faster but streaming is not strictly left-to-right. Tune `reasoning_effort` first. Text-only, small context — wrong pick for large-document work. Rebuild a `<current_state>` block each turn. | XML tags for multi-section prompts; critical rules placed **last** (recency-weighted). OpenAI-compatible API. |

Vendors that now state a dialect outright: Grok (headings), Mistral, Mercury, Muse Spark, plus Llama. The rest are unspecified; markdown headers are the safe default. Post-trains of Kimi K3 (e.g. Ember-1, SWE-2) may not inherit the base model's replay/effort rules — check their docs.

## Replay fidelity

These models carry reasoning state inside the conversation and are strict about how it comes back:

| Model | Requirement |
|---|---|
| DeepSeek | Any request carrying `tools` needs `reasoning_content` of all prior turns, even non-tool turns. |
| GLM | Preserved thinking is off on the standard API, on with Coding Plan; enable with `clear_thinking:false`. Blocks must match exactly. |
| Qwen | `preserve_thinking` — historical reasoning is billed as input. |
| MiniMax | Replay the full assistant message incl. `<think>` / `reasoning_details`. |
| Kimi K3 | Replay full assistant messages verbatim, including `reasoning_content` and `tool_calls`. |
| Grok 4.7 | Encrypted reasoning items unchanged. |
| Muse Spark | Chat Completions redacts `reasoning_content` — use Responses with `previous_response_id` or `include:["reasoning.encrypted_content"]`. |
| Muse Glimmer | `reasoning_content` on the assistant message. |

One rule covers all: never summarize, reformat, reorder, or strip a reasoning block you are sending back.

## API-breaking keys (never send)

- Kimi K3/K2.7/K2.6: any sampling key → error; `tool_choice:"required"` on K2.x → error.
- GLM-5.3 family: `thinking.type:"disabled"` → error. MiniMax M3.1-Flash-Preview: `disabled`/`none` → 400.
- DeepSeek: a `tools` request missing prior `reasoning_content` → 400.
- Qwen 3.8-Max: effort + `thinking_budget` together → error.
- Grok: `presence_penalty` / `frequency_penalty` / `stop` → error.
- Muse Spark: the keys listed in its row → 400.

## Where AP-2 and AP-3 do not apply

Explicit chain-of-thought (AP-2) and multi-example few-shot (AP-3) are anti-patterns because frontier reasoning models already reason natively and the scaffolding fights them. They remain legitimate technique on:

- **Llama 4** and **Mistral Large 3** — no documented native reasoning control. (Mistral Medium 3.5 and Small 4 are reasoning models via `reasoning_effort`, so AP-2 applies to them.)
- **Small open-weight models** (a recent study found CoT and few-shot still pay off on small open-weight models).
- **Any model in this file run with thinking off** — Qwen with `enable_thinking` false, Kimi K2.6 in instant mode, DeepSeek without the thinking config, any `reasoning_effort:"none"` run.

On those, step-by-step decomposition and several worked examples improve output. AP-2 and AP-3 stay in force on Grok, DeepSeek in thinking mode, GLM-5.3, MiniMax M3.1-Flash-Preview, Muse Spark, Muse Glimmer, Qwen in thinking mode, and Kimi K3 — the ones that cannot run thinking-off or reason natively.

## Audit note

If you scan a DeepSeek prompt for literal `<think>` tags, a Grok request for `stop` / `presence_penalty` / `frequency_penalty`, a Muse Spark request for its rejected keys, or a Kimi request for sampling keys, remember that a match inside a quoted example, inside a negation, or inside a code fence is a candidate, not a violation. Confirm it is a live instruction or a real request key before flagging it.

Model settings are configuration, not prompt text.

```
DO: Pick by constraint — cost picks DeepSeek, multilingual picks Qwen, EU compliance picks Mistral, swarm orchestration picks Kimi K2.6, self-hosting picks MiMo, GLM-5.3-Flash, DeepSeek V4.1-Flash, or Muse Glimmer.
DO: Structure large Grok contexts with hierarchical markdown headings.
DO: Enable DeepSeek thinking through the request body's thinking config.
DO: Echo reasoning_content and replay preserved thinking blocks verbatim on DeepSeek, GLM, and Kimi.
DO: Name the target output language explicitly for Qwen and GLM multilingual work.
DO: Wire tools explicitly for Kimi — it reaches nothing external by default.
DO: Lead with function schemas on Mistral; use structured outputs for format enforcement.
DO: Pin Mistral major-minor IDs — -latest aliases switch silently; retired IDs 404.
DO: Keep explicit CoT and multi-example few-shot for Llama, Mistral Large 3, and any thinking-off run.
DO: Hold one template dialect per prompt, whichever you pick.
DON'T: Send raw <think> tags to DeepSeek.
DON'T: Send presence_penalty, frequency_penalty, or stop to Grok — they error.
DON'T: Send any sampling key to Kimi K3/K2.7/K2.6.
DON'T: Send thinking.type:"disabled" to GLM-5.3 or M3.1-Flash-Preview.
DON'T: Send reasoning_effort:"none" to Muse Spark.
DON'T: Carry effort `high` to Qwen 3.8, or `medium` to DeepSeek/Kimi/GLM.
DON'T: Assume Grok 4.5–4.7 reasoning can be turned off; it cannot.
DON'T: Summarize, reformat, or drop a reasoning block you are replaying.
DON'T: Apply explicit step-by-step CoT to Grok, GLM, Kimi K3, or any thinking-on run.
DON'T: Pad context past a pricing tier boundary without checking specs-other.md first.
DON'T: Assume these vendors accept Claude- or Gemini-style parameter conventions — verify per vendor.
```
