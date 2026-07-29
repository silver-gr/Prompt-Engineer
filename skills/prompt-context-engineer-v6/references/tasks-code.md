# Task Recipes: Code

*Source: 05-domain-applications_v5.md §3 (Code Analysis & Generation), §11 (Domain Anti-Patterns); 06-claude-practices_v5.md §5 (Agentic Coding Patterns), §14 (Code Review Harnesses)*

Three jobs, three shapes. Pick by deliverable, not by language.

| Job | Deliverable | Must supply | Output contract |
|---|---|---|---|
| Generation | New code | Requirements, language, conventions, constraints | Fenced code block + one usage/test example |
| Review | Findings list | Code, review dimension (security / correctness / perf) | JSON: `issues[]` with type, severity, description, line |
| Debugging | Root cause + fix | Failing code, exact error/output, repro steps, expected behavior | Cause statement, then minimal diff |

## Generation

Specify the target, not the procedure — enumerating steps costs tokens and quality (AP-1, AP-2).

```
Generate [language] code for these requirements:

<requirements>
[requirements]
</requirements>

Conventions: [style guide / framework / existing patterns to match]
Constraints: [runtime, deps allowed, perf or memory bounds]

Include comments only for non-obvious logic, error handling at boundaries,
type annotations where the language supports them, and one usage example.
Return a single fenced code block.
```

Bound the scope explicitly or the model expands it:

```
<scope_control>
Don't add features, refactor, or introduce abstractions beyond what the task
requires. A bug fix doesn't need surrounding cleanup; a one-shot operation
doesn't need a helper. Don't design for hypothetical future requirements.
Don't add error handling, fallbacks, or validation for scenarios that can't
happen. Trust internal code and framework guarantees. Only validate at system
boundaries (user input, external APIs).
</scope_control>
```

## Review — the recall trap

Review prompts tuned for earlier models show **lower recall** on current models. This is a harness effect, not a capability regression: current models follow a filter instruction such as `only report high-severity` literally and silently drop real findings that fall under the bar.

When scanning an existing review prompt for that string, a match inside a quoted example, a negation, or a code fence is a **candidate, not a violation** — confirm it is a live instruction before rewriting.

Fix: ask for full coverage, filter in a **separate** pass. Paste-ready coverage prompt:

```
Report every issue you find, including ones you are uncertain about or consider
low-severity. Do not filter for importance or confidence at this stage -- a
separate verification step will do that. Your goal is coverage: it is better to
surface a finding that later gets filtered out than to silently drop a real bug.
For each finding, include your confidence level and an estimated severity.
```

Second pass consumes that list and applies the bar. Where a second pass is impossible, use the narrowest single-pass filter — scoped by consequence, not by severity label:

```
Report any bugs that could cause incorrect behavior, a test failure, or a
misleading result; only omit nits like pure style or naming preferences.
```

Structure the findings for the filter pass:

```
Return JSON:
{"issues": [{"type": "string", "severity": "critical|high|medium|low",
             "confidence": "number (0.0-1.0)", "description": "string",
             "line": "number"}],
 "summary": "string"}
```

## Debugging

Supply the exact error text and stack trace (paraphrase produces guessed causes), repro steps with expected vs actual (this is the success criterion), and the surrounding code rather than the failing line alone (otherwise you get a symptom fix). Then ground the answer against code actually opened:

```
<investigate_before_answering>
Never speculate about code you have not opened. If the user references a
specific file, you MUST read the file before answering. Never make claims
about code before investigating -- give grounded, hallucination-free answers.
</investigate_before_answering>
```

For agent-driven fixes, add the generality and cleanup contracts:

```
Write a high-quality, general-purpose solution using standard tools. Do not
create helper scripts or workarounds. Implement a solution that works correctly
for all valid inputs, not just the test cases. Do not hard-code values.
If you create any temporary files, scripts, or helper files for iteration,
clean up by removing them at the end of the task.
```

## Cross-references

Long autonomous runs (progress grounding, action boundaries, subagent caps) → `patterns-agentic.md`. Judging whether one review prompt beats another → `patterns-eval.md`. Code containing untrusted input or tool output → `patterns-safety.md`. Effort, thinking, and sampling settings → the matching `models-*.md`; model settings are configuration, not prompt text.

```
DO: State language, conventions, and constraints; leave the method to the model.
DO: Ask for full coverage in review, then filter findings in a separate pass.
DO: Attach the exact error text, repro steps, and expected behavior when debugging.
DO: Bound scope explicitly so a fix stays a fix.
DO: Require confidence and severity per finding so a later pass can rank them.
DON'T: Prescribe review steps ("first check syntax, then logic, then security").
DON'T: Put a severity filter in the same pass that generates findings.
DON'T: Ask for a verification or double-check step on models that self-verify (AP-16).
DON'T: Let the model answer about a file it has not opened.
DON'T: Accept a fix that also refactors, renames, or "cleans up" adjacent code.
```
