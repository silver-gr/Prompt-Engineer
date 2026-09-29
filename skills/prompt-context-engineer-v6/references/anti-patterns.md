# Anti-Pattern Rewrites (AP-1 … AP-19)

*Source: 02-techniques-patterns_v5.md § Anti-Patterns (Canonical Reference); severities and detection signals from the parent SKILL.md scan table.*

> **A detection signal is a candidate, not a verdict.** A literal match inside a quoted example, inside a negation ("do not say *let's think step by step*"), or inside a fenced code block is **not** a violation. Confirm the string is a live instruction to the model before you report it. Applied without this rule, the scanner gets worse the harder you apply it.

The parent SKILL.md carries the scan table (ID, name, signal, applies-to, severity). This file carries the fix. `C` = Critical, `W` = Warning, `I` = Info. Critical hits (AP-2, AP-5, AP-10, AP-14, AP-17) get full rewrite pairs; the rest get the pair where the rewrite is non-obvious and a one-line fix where it is not.

---

### AP-2 · Explicit CoT · C
**Bad** `Let's think step by step. Step 1: analyze component A. Step 2: examine component B. Step 3: weigh the evidence.`
**Good** `Analyze the relationship between A and B. Explain the implications.`
**Why** Reasoning models plan natively. A prescribed ladder replaces that plan with a shorter, fixed, worse one — and you pay tokens for the downgrade.
**Not a hit** Anthropic's closing "Think the problem through before you answer." for Sonnet 5.5 JSON reasoning with adaptive thinking is official guidance. **Gemini caveat (still a hit):** Google's own template ends with a step-by-step line. Flag a live instruction as usual and note that deleting it is low-risk.

### AP-5 · Sampling misconfiguration · C
**Bad** `{"temperature": 0.2, "top_p": 0.9, "top_k": 40}` sent to Gemini 3.x or Kimi K3/K2.7/K2.6, or non-default `temperature` sent to a current Claude model. Gemini 3.8 variants: `candidate_count`, `frequency_penalty`, `presence_penalty`.
**Good** Delete the keys. Send no sampling parameters at all. Steer determinism from the prompt: `Output JSON only. Copy values verbatim.`
**Why** Claude 5 family: non-default sampling returns 400. Kimi: sampling is fixed server-side and any value errors. Gemini: still loops on older 3.x; ignored on 3.6+ (a silent no-op — an audit blind spot); expect 400 on future generations. DeepSeek thinking mode silently ignores temperature and penalties. Omit — do not "set to 1.0". Muse Spark accepts temperature, but clearer instructions beat lowering it.

### AP-10 · Ignoring model parameters · C
**Bad** `Think really hard about this one and be thorough. Give a long, detailed answer.`
**Good** Prompt states the task only. Reasoning depth moves to config: `output_config.effort` (Claude 5 family), `reasoning_effort` (GPT-5.x), `thinking_level` (Gemini 3.x). Enums live in `references/specs-current.md`.
**Why** Effort and verbosity are configuration, not prose. Asked for in text they are a suggestion the model may ignore; set in the call they are binding — and they are the primary cost lever.

### AP-14 · "Think harder" · C
**Bad** `Think harder. Keep going until you are certain. Try again, more carefully this time.`
**Good** Remove the line entirely. If the task genuinely needs more depth, raise the effort/thinking parameter in config.
**Why** Escalation phrases inflate reasoning after the model has already reached the right answer, and overthinking corrupts correct answers. There is no "try harder" lever in prompt text.

### AP-17 · Reasoning echo · C
**Bad** `Show your reasoning before the answer. Explain your thought process step by step.`
**Bad (variant)** `Write out your reasoning in the response.`
**Good** `Return the answer, then a Basis section listing the evidence you used and the confidence you place in it.`
**Why** Asking a model with a `reasoning_extraction` classifier (Fable 5/5.1, Opus 5.5, Sonnet 5.5) to expose reasoning triggers a refusal — now billed, and never fallback-retried. Read summarized thinking blocks instead. Justification of the *output* is a different request and is answered normally.

---

### AP-1 · Over-engineering · W
**Bad** `You are an expert analyst. Please approach this carefully. Step 1: read the entire dataset. Step 2: identify patterns. Step 3: consider alternatives. [five worked examples follow]`
**Good** `Analyze this dataset for patterns.` + `<data>…</data>` + `Return JSON: {"patterns": [], "insights": [], "confidence": 0.0-1.0}`
**Why** The #1 issue on reasoning models. Scaffolding for a one-sentence task costs tokens and narrows the model's approach. Joint compliance collapses past about 5–6 simultaneous hard constraints, and conflicting pairs (JSON-only plus a word count) do the most damage — consolidate, or split into separate calls.

### AP-3 · Excessive few-shot · W
**Fix** Cut to ≤2 examples on **GPT and other reasoning models**, and keep only those that demonstrate **output format** — delete any example that walks through reasoning. Flag also when examples exceed ~30% of the prompt. **Claude is exempt:** Anthropic recommends 3–5 relevant, diverse examples in `<example>` tags and allows `<thinking>` inside them to show the reasoning pattern. **Gemini is exempt:** Google recommends always including a few identically formatted examples (too many overfit). Legacy and open-weight models without native reasoning are also exempt.

### AP-4 · Conversational fluff · I
**Bad** `Hello! I hope you're doing well. Could you please analyze the following data when you have a moment? Thank you so much!`
**Good** `Analyze this data. Return results as JSON.`
**Why** Zero signal value at real token cost on every model, and on Gemini 3.x it actively degrades instruction-following.

### AP-6 · "Think" word sensitivity · I
**Fix** Only when extended thinking is **disabled**: swap `think about` → `consider`, `think through` → `evaluate`, `think carefully about` → `assess`. Documented for Opus 4.5 — treat as behavior to test for, not a property of every Claude model.

### AP-7 · Tool description verbosity · W
**Bad** `Use this tool to search through the customer database. Make sure to validate input first. Always be careful with partial matches. If ambiguous, ask for clarification, and never call it twice…` (policy prose, plus unrelated tools exposed alongside it)
**Good** `Search customers by name or ID when the user asks about a customer. Returns id, name, status; errors on no match.`
**Why** Tool descriptions are resident on every turn. OpenAI asks for what the tool does, **when to use it**, return fields and error behavior — concisely — and for only task-relevant tools. The finding is redundancy, policy prose and irrelevant tools, never the "when to use" clause.
**Scope — GPT only.** Anthropic recommends stating what the tool does **and when to use it**; Gemini documents no maximum. Do not flag a long Claude or Gemini tool description. See `patterns-agentic.md` for the per-provider guidance.

### AP-8 · Prescribed tool sequence · W
**Bad** `First call search_docs, then call summarize, then call format_output.`
**Good** `Produce a formatted summary of the docs matching {{QUERY}}.` — state goal and constraints; let the model plan the calls.
**Why** A fixed sequence cannot adapt when a call returns nothing, and it blocks parallel calls the model would otherwise make.

### AP-9 · Over-prompting GPT · W
**Fix** Collapse multi-section scaffolding to an outcome statement plus constraints. GPT-5.x and GPT-6 quality drops as instruction volume rises past what the task needs (OpenAI internal, directional: +10–15% score, −41–66% tokens). Recipe-style guidance over-constrains Astra; the harm is conflicting or excess rules, not length alone. XML tags are still fine as structure.

### AP-11 · Persona on accuracy tasks · W
**Bad** `You are a world-class mathematician with 30 years of experience.` (on a computation or factual task)
**Good** Drop the persona. State the task and the output format.
**Why** Persona trades precision for depth and register. It helps on advisory and explanatory-tone work; on math, code, and factual recall it measurably costs accuracy.

### AP-12 · "Never hallucinate" · I
**Bad** `Never hallucinate. Do not make anything up. Only state facts.`
**Good** `Answer only from <context>. Quote the sentence you relied on. If the context does not answer the question, reply "not in context".`
**Why** The bad version names a failure with no mechanism to prevent it. The good version supplies grounding, a citation requirement, and a legal escape hatch.

### AP-13 · Unmanaged agentic eagerness · W
**Bad** `Fix all the failing tests in the repo.`
**Good** `Fix the failing tests under tests/auth/. Do not modify src/. Stop when pytest tests/auth/ exits 0. Do not spawn more than 3 subagents.`
**Why** Without a stop condition, a scope bound, and a subagent cap, an autonomous run expands until something external stops it.
**Inverse** GPT-6 Astra under-acts (premature stops, approval-seeking). Fix with a completion definition plus an initiative line, not more caution.

### AP-15 · Offset-from-end reference · W
**Bad** `Summarize the second-to-last document.` / `Follow the format of the final example above.`
**Good** `Summarize document id="d7".` / `Follow the format of <example id="fmt-a">.`
**Why** Position Curse: offset-from-end references mis-resolve even in short lists. Use forward indices or unique anchors.

### AP-16 · Verification instructions · W
**Bad** `Double-check your answer. Verify your findings before responding.` (on Opus 5 or GPT-6 Astra)
**Good** Delete the behavioral instruction; keep the requirement as an output contract — `Sources`, `Limits`, `Verdict` sections.
**Why** Opus 5 self-verifies; Astra self-tests and over-tests — the instruction buys cost and no accuracy. Fable 5/5.1 guidance asks for explicit interval self-checks on long runs — not a hit. Opus 5.5 inherits this from Opus 5 as a starting point only (Verify). Sonnet 5.5 at `xhigh`/`max` needs an additive "stop and report when checks pass" line instead. Boundaries: the contract names sections and their contents, never an action verb (an enumerated, task-specific checklist written as output items beats a generic self-check); and it targets *self*-verification only — `cross-reference three sources` inside a fact-check is the task definition, and deleting it breaks the task.

### AP-18 · Over-prescriptive enumeration · I
**Fix** On Fable 5 and Fable 5.1, replace ten enumerated behaviors with the one instruction that covers them. Anthropic's claim is that a brief instruction *can be as effective as* enumeration — prefer brevity because it costs less and is easier to maintain, not because enumeration is documented to degrade output.

### AP-19 · Overthinking DoS · W
**Fix** Bound every production run: a `max_tokens` ceiling, an input-length limit, and a pre-dispatch check that rejects self-contradictory instructions. Adversarial or logically inconsistent input drives runaway chain-of-thought in reasoning models.

---

```
DO: Cite the AP by number so the user can look it up and dispute it.
DO: Confirm a literal match is a live instruction before reporting it as a hit.
DO: Fix every Critical hit before delivering the prompt.
DO: In OPTIMIZE, make exactly one change — highest severity, ties broken by lowest AP number.
DO: Relocate a real requirement into the output contract instead of deleting it (AP-16).
DON'T: Flag Claude (3–5) or Gemini few-shot examples under AP-3.
DON'T: Flag a "when to use it" clause in a tool description — AP-7 targets redundancy.
DON'T: Flag the word "think" when extended thinking is enabled — AP-6 applies only when it is off.
DON'T: Strip task procedure while removing self-verification — "cross-reference three sources" is the task.
DON'T: Rewrite the whole prompt because the scan returned nineteen rows.
DON'T: Steer effort, thinking, or verbosity in prompt text — that is AP-10, and it belongs in config.
```
