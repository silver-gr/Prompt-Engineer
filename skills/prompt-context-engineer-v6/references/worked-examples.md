# Worked Examples — One Filled Contract Per Mode

*Source: parent SKILL.md § Output contracts (CRAFT · OPTIMIZE · REVIEW · ADAPT · SELECT), instantiated against 02-techniques-patterns_v5.md § Anti-Patterns.*

These are finished answers, not templates. `{{VAR}}` is a runtime input the caller substitutes; there is no `[choose one]` anywhere, because a slot handed to the user is an unfinished draft. Match this density and this level of commitment.

## CRAFT — extraction prompt for Opus 5.5
*Request: "Write a prompt that pulls structured fields out of freight-invoice text for our ingest pipeline."*

Mode: CRAFT · Target: Opus 5.5 (assumed — no target named)
### Recommended Prompt
```
Extract these fields from the invoice text. Output JSON only.

<invoice>{{INVOICE_TEXT}}</invoice>

Fields: invoice_number, issue_date (ISO 8601), carrier_name, currency (ISO 4217),
line_items[] (description, quantity, unit_price, amount), subtotal, tax, total.

Copy values verbatim — do not normalize casing or number format. A field absent
from the text: null; never infer it. A field present but unparseable: return the
raw string and add its name to unreadable_fields.
```
### Model Settings
```
model: Opus 5.5
thinking: {type: "adaptive"}
output_config.effort: low
```
Send no `temperature`, `top_p`, or `top_k` — non-default sampling returns 400 on current Claude.
### Why
- Extraction is mechanical: the field list *is* the task, so no persona and no reasoning scaffold (AP-1, AP-11).
- `null` plus `unreadable_fields` gives failure an explicit destination, which suppresses invented values far better than a "never hallucinate" line (AP-12).
- The field list fully specifies the task, so each rule is stated once, where it applies.

## OPTIMIZE — bloated triage prompt for Opus 5
*Request: "Our support-ticket triage prompt got slower and less accurate after we expanded it. Tighten it."*

Mode: OPTIMIZE · Target: Opus 5
### Change
**AP-2 (Critical)** — removed the prescribed reasoning ladder: `"Let's think step by step. Step 1: read the ticket. Step 2: identify the product area. Step 3: consider severity. Step 4: decide whether the customer is blocked."` Opus 5 plans natively; the ladder replaced that plan with a shorter fixed one, which is the accuracy regression you measured.
### Optimized Prompt
```
Triage this support ticket.

<ticket>{{TICKET}}</ticket>
<product_areas>billing, auth, sync, mobile, api</product_areas>

sev1 = production down or data loss. sev2 = feature broken, workaround exists.
sev3 = everything else.

Return JSON: {"area": one of product_areas, "severity": "sev1"|"sev2"|"sev3",
"customer_blocked": true|false, "summary": one sentence, "confidence": 0.0-1.0}
```
### Model Settings
```
model: Opus 5
thinking: {type: "adaptive"}
output_config.effort: low
```
Send no sampling parameters. Never pair `thinking: disabled` with effort `xhigh`/`max` on Opus 5 — that combination returns 400 and is re-validated per request.
### Notes
AP-1 also fires: the 300-token "you are a senior support engineer" preamble is still in place. OPTIMIZE makes one change per pass so the edit stays reviewable — say the word and that goes next.

## REVIEW — Gemini summarizer carrying a Critical
*Request: "Review our Gemini research-summarizer prompt before we ship it to production."*

Mode: REVIEW · Target: Gemini 3.8 Flash
### Verdict
**Fix first.** One Critical present; do not ship until it is removed.
### Findings
| AP · Sev | Quoted location | Fix |
|---|---|---|
| AP-5 · **C** | `"temperature": 0.2, "top_p": 0.9` in the request body | Delete both keys — omit, do not set to 1.0. On Gemini 3.6+ they are silently ignored today and will return 400 on future generations; on older 3.x, sub-1.0 temperature loops. Get determinism from the prompt instead: "Output JSON only. Quote verbatim." |
| AP-4 · I | `"Could you please summarize the sources below… thank you so much!"` | Delete the padding. Fluff is worst on this family, where it actively degrades instruction-following rather than merely costing tokens. |
| AP-15 · W | `"cite the second-to-last source"` | Replace with a unique anchor — `<source id="s4">` … `cite source s4`. Offset-from-end references mis-resolve even in short lists. |
### Not Checked
Factual accuracy of the summaries — no eval set was run. Token cost against your budget. Behavior when input exceeds the context window. Whether your template engine escapes the angle brackets before the call. These are **not checked**, not absent.

## ADAPT — Claude XML prompt ported to Gemini
*Request: "We have a Claude prompt for competitive briefs. Port it to Gemini."*

Mode: ADAPT · Target: Gemini 3.8 Flash
### Adapted Prompt
```
Write a competitive brief on the vendor described below.

Dossier: {{COMPANY_DOSSIER}}
Comparison set: {{COMPETITOR_LIST}}

Sections, in this order: Positioning · Pricing posture · Three differentiators ·
Three vulnerabilities · Where they beat us · Where we beat them.

Constraints:
- 700 words maximum. No preamble and no closing summary.
- Every claim traces to a line in the dossier. Mark anything untraceable
  "unsourced", inline.
- Do not speculate about unannounced products.
- Plain prose, except the differentiator and vulnerability sections, which are
  bulleted.
```
### Model Settings
```
model: Gemini 3.8 Flash
thinking_level: high
```
Omit `temperature`, `top_p`, and `top_k` entirely. Never send `thinking_budget` alongside `thinking_level` — the pair returns 400.
### What Changed
| Source (Claude) | Target (Gemini) | Reason |
|---|---|---|
| `<context>` / `<task>` / `<constraints>` tags | Plain labeled headers | Gemini needs no XML delimiting; the tags cost tokens and buy nothing |
| Constraint block placed second | Constraint block kept after the task as a recap | Google's current guide puts format requirements up front; an end-of-prompt recap of hard limits is optional |
| `"Please carefully consider…"` lead-in | Deleted | AP-4, and fluff is worst on this family |
| `output_config.effort` | `thinking_level` | Effort does not transfer across families; set from the target's own scale (`references/specs-current.md`) |
| Few-shot ceiling of 2 | No ceiling of 2 | AP-3 exempts Gemini — Google recommends always including a few identically formatted examples |

## SELECT — cost-sensitive high-volume classification
*Request: "We classify roughly 4M support emails a month into 12 intent buckets. Which model, and what settings?"*

Mode: SELECT · Target: to be recommended
### Recommendation
**Claude Haiku 4.5.** Fixed-label classification is not a reasoning task, and at this volume unit cost dominates every other consideration.
### Settings
```
model: Haiku 4.5
thinking: off
temperature: 0
max_tokens: 16
```
Haiku 4.5 is exempt from the current-Claude sampling restrictions, so `temperature: 0` is legal at the API (the Python SDK v1.0 dropped the typed param) and worth setting for label reproducibility — the one remaining place a sampling parameter earns its keep. Cache the taxonomy and rubric as a static prefix. Confirm pricing, cache TTLs, and the exact model ID in `references/specs-current.md` before committing a budget.
### Why
- Twelve fixed buckets need pattern-matching, not deliberation; thinking spend buys no accuracy and multiplies across 4M calls.
- A 16-token output cap makes runaway generation structurally impossible, which matters more than prompt wording at this volume.
- The taxonomy block is byte-identical on every call, so prefix caching — not model choice — is the largest single lever on the bill.
### Runner-up
**Sonnet 5.5 at low effort**, routed selectively: if Haiku 4.5 misses your accuracy bar, escalate only the tickets under a confidence threshold rather than upgrading all traffic.

```
DO: Open every response with "Mode: <MODE> · Target: <model>".
DO: Emit that mode's sections, in contract order, and nothing else.
DO: Give one recommended prompt — never a menu of alternatives to choose between.
DO: Keep prompt text and model settings in two separate blocks.
DO: Name the model you assumed, in one line, when the user named none.
DON'T: Ship unfilled slots as an answer — {{VAR}} is a runtime input, [choose one] is a draft.
DON'T: Attach a numeric quality score; Verdict is two-valued and derived from severity.
DON'T: Write "absent" in Not Checked — write "not checked".
DON'T: Include Notes unless a critical constraint or a real risk applies.
DON'T: Copy an effort value across model families — it does not transfer.
```
