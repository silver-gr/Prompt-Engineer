# Task Recipes: Writing & Content Generation

*Source: 05-domain-applications_v5.md §1 (Content Generation), §10 (Creative Applications), §11 (Domain Anti-Patterns)*

Content quality tracks the **specification**, not the instructions about how to write. Describe the artifact and its reader; never describe the writing process.

## The five slots

Fill all five. A missing slot is filled by the model's default, which is generic.

| Slot | What it fixes | Weak | Strong |
|---|---|---|---|
| Audience | Register, assumed knowledge, jargon budget | "for developers" | "senior engineers who have run a monolith in production" |
| Purpose | What the reader should do or believe after | "about microservices" | "decide whether to start a migration this quarter" |
| Scope | What to cover and what to exclude | "cover the topic" | "benefits, migration risks, rollback; exclude vendor comparison" |
| Length | Prevents padding and truncation | "detailed" | "1500-2000 words" |
| Form | Structure and register | "well-organized" | "H2 sections, code example per section, technical but plain" |

## Recipe

```
Write [content type] on [topic].

<context>
Audience: [who they are, what they already know]
Purpose: [what the reader should be able to do after reading]
Voice: [tone, person, register]
</context>

<specifications>
Length: [range]
Cover: [required points]
Exclude: [out of scope]
Structure: [heading levels, sections, required elements]
</specifications>

Return [format].
```

## Controlling form

State the target form positively. Prohibitions ("do not use markdown") are followed less reliably than the equivalent instruction to do something.

| Instead of | Write |
|---|---|
| "Do not use markdown" | "Write in smoothly flowing prose paragraphs." |
| "Don't be verbose" | "Keep each section under 150 words." |
| "Avoid bullet lists" | "Incorporate the items into sentences." |
| "Don't be too formal" | "Write in second person, contractions allowed." |

Paste-ready prose control for long-form pieces:

```
Write in complete paragraphs and full sentences. Reserve lists for genuinely
discrete items, and reserve markdown for inline code, code blocks, and headings.
Match the length to what the subject needs -- do not pad with filler sections,
redundant summaries, or boilerplate.
```

The formatting style of your own prompt leaks into the output: a heavily bulleted prompt produces bulleted prose. Write the prompt in the register you want back.

## Iteration and variation

| Goal | Move |
|---|---|
| Different angle | Change audience or purpose, then regenerate — do not ask for "a better version" |
| Multiple candidates | Generate N independently and select; do not ask for N variants in one response |
| Targeted revision | Quote the span to change and state the target property; leave the rest untouched |
| Consistent voice across pieces | Supply one exemplar of the target voice, not a list of voice adjectives |

One exemplar beats a description. Two or three beat one for format demonstration; past that you are in AP-3 territory and outputs start collapsing onto the examples.

## Anti-patterns specific to content work

| ID | Shows up as | Cost |
|---|---|---|
| AP-1 | Prescribing the writing process: "first brainstorm, then outline, then draft" | Wasted tokens, worse structure |
| AP-4 | "please", "kindly", "if you could" in the prompt | Degrades instruction following, worst on Gemini |
| AP-11 | "You are a world-class copywriter" on an explanatory or factual piece | No gain; can add flourish that hurts accuracy |
| AP-3 | Six sample paragraphs pasted as style guides | Output mimics the samples instead of the brief |

When scanning a draft prompt for these literal strings, a match inside a quoted example, a negation, or a code fence is a **candidate, not a violation** — confirm it is a live instruction first.

## Cross-references

Whether one draft prompt beats another, or a style rubric → `patterns-eval.md`. Emitting content as strict JSON fields for a CMS → `tasks-data.md`. Research or fact-gathering that feeds the piece → `tasks-analysis.md`. Per-model formatting tags, verbosity, and creative sampling behavior → the matching `models-*.md`; model settings are configuration, not prompt text.

```
DO: Fill all five slots — audience, purpose, scope, length, form.
DO: State the target form positively.
DO: Supply one exemplar when voice matters more than you can describe.
DO: Change the brief and regenerate rather than asking for "something better".
DO: Write the prompt in the register you want the output to have.
DON'T: Prescribe the writing process (AP-1).
DON'T: Pad the prompt with politeness (AP-4).
DON'T: Add a creative persona to an explanatory or factual piece (AP-11).
DON'T: Paste more than a few style samples (AP-3).
DON'T: Ask for many variants in one response when you intend to pick one.
```
