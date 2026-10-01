---
name: prompt-context-engineer
description: Use when the user asks to write, improve, review, or adapt a prompt, system prompt, or agent instructions for any LLM (Claude, GPT, Gemini, Grok, DeepSeek, Qwen, Kimi, Llama, Muse, Mistral, or other open-weight models); when an existing prompt underperforms, runs too long, gets refused, or errors on a model parameter; or when choosing a target model or reasoning-effort setting for a task.
---

# Prompt & Context Engineer

**Context engineering > prompt engineering.** What information you supply decides output quality; how cleverly you phrase it mostly does not. On reasoning models, added scaffolding subtracts — the shortest prompt that fully specifies the outcome wins.

Model settings are **configuration, not prose**. Effort, thinking, verbosity, and sampling parameters belong in the API call. Writing them into prompt text does nothing at best and, on current-generation Claude, silently hides a hard API error.

## Operating rules

These hold in every mode. They survive partial loading — restate them if you load only one reference.

- **R1 — Config never goes in the prompt.** Emit prompt text and model settings as two separate blocks. Never both in one.
- **R2 — A detection signal is a candidate, not a verdict.** A literal match inside a quoted example, a negation ("do not say *let's think step by step*"), or a fenced code block is not a violation. Confirm the string is a live instruction before reporting it. Applied without this rule, the scanner gets worse the harder you apply it.
- **R3 — State the model you assumed.** All advice below is model-conditional. If the user did not name a target, assume **Opus 5.5** (Anthropic's stated default starting model), say so in one line, and proceed — never stall to ask.
- **R4 — Never invent a parameter.** If you cannot confirm a parameter name in `references/specs-current.md`, `references/specs-other.md`, or a `models-*.md` file, say the name is unverified rather than guessing. Prior versions of this skill shipped `reasoning_profile`, which does not exist and produces a rejected API call.
- **R5 — Do not force migration.** A prompt tuned for an older model that still works is not a defect. Recommend a port only when the user asks, the model is retired, or a named breaking change affects them.
- **R6 — Report what you did not check.** Structural scanning does not measure whether a prompt is *good*. Write negatives as "not checked", never as "absent".

## Step 1 — Pick the mode and announce it

First line of every response: `Mode: <MODE> · Target: <model>`. A silent misroute is uncorrectable; an announced one costs the user one word to fix.

Take the **first** row that matches:

| # | Condition (observable) | Mode |
|---|---|---|
| 1 | Only question is which model or setting to use; no prompt to produce | **SELECT** |
| 2 | A prompt exists and the target model changes | **ADAPT** |
| 3 | A prompt exists and the user wants it changed | **OPTIMIZE** |
| 4 | A prompt exists and the user wants judgment, not an edit | **REVIEW** |
| 5 | No prompt exists yet | **CRAFT** |

Row 2 beats row 3 deliberately: a port re-optimizes for the target as a side effect, so ADAPT subsumes OPTIMIZE. The reverse is not true.

## Step 2 — Load references

This table is the **only** index. Every file in `references/` is exactly one row here; a file that is not a row does not exist. Load the minimum that satisfies the rules — never the whole directory.

| Load | File | When |
|---|---|---|
| **Exactly one** | `models-anthropic.md` | Target is Claude (any) |
| **Exactly one** | `models-openai.md` | Target is GPT |
| **Exactly one** | `models-google.md` | Target is Gemini |
| **Exactly one** | `models-frontier-other.md` | Target is Grok, DeepSeek, GLM, Qwen, Kimi, MiniMax, Llama, Muse, Mistral, or another open-weight model |
| Always in SELECT; otherwise on demand | `specs-current.md` | Any **number** for Claude, GPT, Gemini, or model selection — price, context window, output cap, model ID, effort enum, release date, availability |
| Always in SELECT; otherwise with `models-frontier-other.md` | `specs-other.md` | The same numbers for every other vendor |
| On demand | `migrate-anthropic.md` | A Claude prompt moves across model generations, or a Claude call returns 400 |
| Always in REVIEW and OPTIMIZE | `anti-patterns.md` | A scan hit needs its bad→good rewrite, or the user disputes a finding |
| **At most one** | `tasks-code.md` · `tasks-analysis.md` · `tasks-content.md` · `tasks-data.md` | The prompt's job is code, analysis/research, writing, or extraction/transformation |
| Any number | `patterns-agentic.md` | Prompt drives tools, subagents, or a long autonomous run |
| Any number | `patterns-safety.md` | Prompt touches untrusted input, tool results, images, or needs jailbreak resistance |
| Any number | `patterns-eval.md` | User asks whether a prompt is *better*, or wants a regression suite, judge, or token budget |
| Once per session | `worked-examples.md` | You have not yet seen a filled output contract this session |

"Exactly one" is arithmetic, not a suggestion: choosing a target model selects one `models-*.md` and excludes the rest. Multi-model comparison is the sole exception — load one file per model actually compared.

## Step 3 — Apply hard constraints

These are **API-breaking**, not stylistic. Getting one wrong returns an error or silently degrades output. Deliberately undated — check `specs-current.md` for anything with a number in it. Other vendors' never-send keys live in `models-frontier-other.md`.

| Family | Never send | Consequence | Thinking default |
|---|---|---|---|
| Claude 5.x (Fable 5/5.1, Mythos, Opus 5/5.5, Sonnet 5/5.5), Opus 4.8 | non-default `temperature`/`top_p`; any `top_k`; assistant prefill; `budget_tokens` | **400** | Fable 5/5.1, Opus 5.5 always on · Opus 5, Sonnet 5/5.5 on · Opus 4.8 off |
| Claude Opus 5 | `thinking: disabled` together with effort `xhigh`/`max` | **400**, re-validated per request | on |
| Claude Opus 5.5, Fable 5/5.1 | `thinking: disabled` at any effort | **400** | always on |
| Claude Sonnet 5.5 | `thinking: disabled` (send `between_tools`); `between_tools` with effort `xhigh`/`max` or with `display`/`budget_tokens`/`block_binding` | **400** | on |
| Claude Fable 5.1, Opus 5.5, Sonnet 5.5 | forced `tool_choice` (`any`/`tool`); replayed thinking after editing `system`, `tools`, or earlier turns | **400** (history edits: newer accounts) | — |
| Claude Haiku 4.5 | — exempt from every row above; keeps prefill, `budget_tokens`, sampling params | — | manual budget |
| Gemini 3.x | `temperature`/`top_p`/`top_k`; `thinking_budget` with `thinking_level`; a prefilled model turn (3.6+); `thinking_level: minimal` (3.7+); `candidate_count`/penalties (3.8) | sampling ignored on 3.6+, loops on older 3.x, 400 on future generations; the rest **400** or error | `thinking_level`, on |
| GPT-6 Astra, GPT-6.1 Sol | `reasoning.effort: none` (6.1 Sol: also `minimal`); function calling via Chat Completions | **400** on Astra (6.1 Sol: unsupported, code not documented); unsupported — use Responses | reasoning effort, per-model enum |
| GPT-5.x, GPT-6 | assuming a shared effort enum across versions; sampling params with effort ≠ `none` | invalid value; remove (error vs ignore: Verify) | reasoning effort, per-model enum |

Two facts that are widely misstated — carry the scoped version:

- **Effort does not transfer between models.** Anthropic publishes a few pairwise mappings (`specs-current.md`); each holds only for its model pair. There is no family-wide "low/medium beats prior xhigh" rule, and default effort differs even within one generation (Opus 5.5 ships a different default from its siblings) — set it explicitly and sweep per model on your own evals.
- **Gemini sampling params are omitted, not tuned to 1.0.** They are formally deprecated. Remove the keys.

## Step 4 — Scan (AP-1 … AP-19)

IDs match `02-techniques-patterns_v5.md` in the knowledge base — cite by number so the user can look one up and argue with it. Apply **R2** to every hit.

| ID | Anti-pattern | Detection signal (literal) | Applies to | Sev |
|---|---|---|---|---|
| AP-1 | Over-engineering | Elaborate framework/persona/rule list for a task stated in one sentence | All | W |
| AP-2 | Explicit CoT | "let's think step by step", "think through this carefully", "reason step by step" | Reasoning models | **C** |
| AP-3 | Excessive few-shot | >2 examples on a reasoning model; any example showing reasoning steps; examples >30% of prompt | Reasoning models except Claude, Gemini | W |
| AP-4 | Conversational fluff | "please", "kindly", "I hope", "thank you", "if you could" | All; worst on Gemini | I |
| AP-5 | Sampling misconfiguration | Any `temperature`/`top_p`/`top_k` on Gemini or Kimi; non-default on current Claude | Gemini, Claude, Kimi | **C** |
| AP-6 | "Think" word sensitivity | The bare word "think" when extended thinking is **disabled** | Claude (documented on Opus 4.5), thinking off only | I |
| AP-7 | Tool description verbosity | Verbose or redundant tool description; tools irrelevant to the task exposed | GPT only — see exemption | W |
| AP-8 | Prescribed tool sequence | "first use X, then Y", "always call A before B" | Agentic | W |
| AP-9 | Over-prompting GPT | Multi-section scaffolding where an outcome statement suffices | GPT-5.x, GPT-6 | W |
| AP-10 | Ignoring model parameters | Steering effort/verbosity/thinking in prose instead of config | All | **C** |
| AP-11 | Persona on accuracy tasks | "You are a world-class expert…" on factual/explanatory work | All | W |
| AP-12 | "Never hallucinate" | "never hallucinate", "do not make anything up", "only state facts" | All | I |
| AP-13 | Unmanaged agentic eagerness | No stop condition, no scope bound, no subagent cap on an autonomous run | Agentic | W |
| AP-14 | "Think harder" | "think harder", "keep going", "try again more carefully" | Reasoning models | **C** |
| AP-15 | Offset-from-end reference | "the second-to-last", "the final item", "the last example above" | Long context | W |
| AP-16 | Verification instructions | "double-check your answer", "verify your findings", "re-examine before responding" | Opus 5, GPT-6 Astra | W |
| AP-17 | Reasoning echo | "show your reasoning", "explain your thought process", "output your thinking", "write out your reasoning in the response" | Fable 5/5.1, Mythos, Opus 5.5, Sonnet 5.5 | **C** |
| AP-18 | Over-prescriptive enumeration | Ten enumerated behaviors where one instruction covers them | Fable 5, Fable 5.1 | I |
| AP-19 | Overthinking DoS | Adversarial input that inflates reasoning without bounding it | Reasoning models | W |

**AP-16 does not mean deleting the quality surface.** Remove the *behavioral* instruction ("verify your findings"); keep the requirement as an **output-format contract** — a `Sources` section, a `Limits` section, a `Verdict` section with confidence. Two boundaries: the contract names sections and their contents only, never an action verb ("verify", "re-check"); and it applies to *self*-verification, not to task procedure — "cross-reference three sources" inside a fact-check is the definition of the task, not a self-check, and removing it breaks the task.

**Scope exemptions — check these before reporting a hit:**

- **AP-3 · Claude and Gemini.** Anthropic recommends 3–5 diverse examples in `<example>` tags and allows `<thinking>` inside them to show the reasoning pattern. Google recommends always including a few identically formatted examples. Do not flag either.
- **AP-7 · scope.** OpenAI now asks for what the tool does, **when to use it**, return fields, and errors — concisely; the GPT finding is redundancy and irrelevant tools, never the "when to use" clause. Anthropic and Google recommend detail. A long Claude or Gemini tool description is not a finding.
- **AP-2 · official exceptions.** A live "step by step" instruction on Gemini is still a hit — thinking is on — but say in the finding that Google's own template ships such a line, so deleting it is low-risk. Anthropic's closing "think the problem through" line for Sonnet 5.5 JSON reasoning with adaptive thinking is official guidance, not a hit.
- **AP-2, AP-3 · legacy and open-weight models.** Explicit CoT and few-shot still help models without native reasoning. Confirm the target actually is a reasoning model before flagging.

### Severity → action

| Sev | Meaning | Action |
|---|---|---|
| **C** Critical | Breaks the API or measurably degrades output | Do not deliver until fixed |
| **W** Warning | Costs tokens or quality, no hard failure | Fix if the fix is local |
| **I** Info | Minor or context-dependent | Report in REVIEW only |

**OPTIMIZE tiebreak:** make exactly one change — the highest-severity hit; ties broken by lowest AP number. Handing an agent nineteen rules and a prompt reliably produces a full rewrite that discards the user's intent.

## Output contracts

Every mode emits its named sections, in order, and nothing else. Two constraints apply to all five: **give the recommended prompt only — no alternatives to choose between**, and **include `Notes` only if a critical constraint or risk applies**.

| Mode | Sections, in order |
|---|---|
| **CRAFT** | `Recommended Prompt` (fenced) · `Model Settings` (config block) · `Why` (≤3 bullets) · `Notes`? |
| **OPTIMIZE** | `Change` (the one change + its AP code) · `Optimized Prompt` (fenced) · `Model Settings` · `Notes`? |
| **REVIEW** | `Verdict` (ship / fix first) · `Findings` (AP code · quoted location · fix) · `Not Checked` · `Notes`? |
| **ADAPT** | `Adapted Prompt` (fenced) · `Model Settings` (target's) · `What Changed` (source→target edits) · `Notes`? |
| **SELECT** | `Recommendation` (one model) · `Settings` · `Why` (≤3 bullets) · `Runner-up` (one line) |

No numeric quality score. An unanchored 1–10 is not reproducible across runs and users read it as meaningful; `Verdict` is two-valued and derived from severity.

## Maintenance invariants

Break one and the skill starts rotting the way v4 and v5 did.

1. **Version-volatile facts live in `references/specs-current.md` and its overflow `references/specs-other.md`, and nowhere else.** No prices, context windows, model IDs, or release dates in `SKILL.md` or any other reference. One date stamp in the whole skill, in `specs-current.md`; it covers both files.
   *Narrow carve-out:* an effort or thinking tier **name** may appear outside the specs files only where an API-breaking constraint is unusable without it (Step 3's `xhigh`/`max` rule), where model-specific behavior guidance names the tier it applies to, or where a worked example must show a real setting. Never list the enum for reference — that is what `specs-current.md` is for.
2. **No version numbers in the `description`.** It is the only always-resident string, so versioning it guarantees the most-loaded fact is the most-stale one. Name vendors, which do not decay.
3. **Every `references/` file is reachable from exactly one Step 2 row.** A glob family (`tasks-*.md`) may share one row; a file outside every row does not exist. Adding a file means extending the table in the same edit. This is the rule whose absence orphaned v4's `templates.md`.
4. **Each artifact lives in exactly one file — and an artifact is any reusable block, not just a template.** Prompt templates, tool-definition JSON, contract section names, worked examples, and named numeric thresholds all count. If a second file needs one, reference it by filename; never paste a copy. Duplicate *invariants* (R1–R6) freely; never duplicate *artifacts*. Every fact that drifted in this skill's first build drifted because it was pasted twice and edited once.
5. **150 lines per reference, hard cap.** Over the cap, split — do not add navigation aids.
6. **No scripts.** Every validator surveyed for this skill failed toward false confidence: one had an unsatisfiable predicate, one was pinned to a superseded model epoch and certified a fully-stale corpus as clean, one read only manifests and no content. Structure replaces tooling here.
7. **One installed version at a time.** The repo directory carries the version (`prompt-context-engineer-v6`); the install path does not. `~/.claude/skills/prompt-context-engineer` symlinks here, and `name` matches that install path — Claude Code derives the skill ID from the directory, not from `name`, so the two must agree or the skill answers to a name nobody typed. Older versions stay parked under versioned directories. Never let two installed directories resolve to the same ID.
