# Evaluation, Regression, and Token Budget

*Source: 04-evaluation-optimization_v5.md (lifecycle, A/B testing, baselines, distillation, regression suites, CI pipeline, LLM-as-judge) plus 01-foundations_v5.md section 8 (prompt caching and token efficiency)*

## Zero-shot baseline first — always

Establish a minimal zero-shot baseline before adding a single element. Without it, every later comparison is against nothing and complexity accumulates unchallenged.

```
[Task statement, one or two sentences]
[Input will be inserted here]
Return as: [format specification]
```

Score that. Only keep an addition that measurably beats it. This is the gate that stops AP-1 (over-engineering), AP-2 (explicit CoT), and AP-3 (excessive few-shot) from entering a prompt at all.

## Optimization priority

| Rank | Lever | Impact |
|---|---|---|
| 1 | Context quality | Highest ROI |
| 2 | Output-format clarity | High |
| 3 | Instruction clarity | Medium |
| 4 | Examples | Low; often reduce performance |
| 5 | CoT instructions | Negative — remove |

## A/B: simple vs complex

The most valuable test is not two clever variants — it is simple against complex.

| Test | What it validates |
|---|---|
| Zero-shot vs few-shot | Whether examples help (often they do not) |
| Simple vs explicit CoT | Whether spelled-out reasoning helps (rarely, on reasoning models) |
| Minimal vs verbose | Whether brevity holds quality (usually) |
| Context-rich vs instruction-heavy | Whether context beats instructions (yes) |

**Decision rule:** ship the simpler prompt when it scores within 5% of the complex one. Report score-per-unit-complexity, not raw score alone, or the complex variant wins every marginal call and the prompt ratchets upward forever.

## Distillation

Strip in descending order of expected harm, re-scoring after each removal; accept a removal that stays within 2% of baseline.

| Order | Remove |
|---|---|
| 1 | CoT instructions (AP-2, AP-14) |
| 2 | Examples beyond one format demo (AP-3) |
| 3 | Conversational padding (AP-4) |
| 4 | Verbose task restatement (AP-1) |

## Regression suite

Golden examples are the contract. Each carries an id, input, expected output, format spec, and a `critical` flag that blocks deployment on failure.

```json
{
  "id": "customer_lookup_basic",
  "input": {"query": "Find customer John Smith"},
  "expected_output": {"action": "search", "field": "name", "value": "John Smith"},
  "format_spec": "json",
  "critical": true
}
```

| Metric | Threshold | How measured |
|---|---|---|
| Accuracy | 0.95 of prior version | Semantic similarity to expected output |
| Consistency | 0.90 of prior version | Min pairwise similarity across 3 runs of the same input |
| Format compliance | 1.0 | Schema validation on every run |

A regression on accuracy is critical; the others are warnings. Run the suite against old and new prompt in the same session, on the same model — a prompt change and a model change evaluated together produce an uninterpretable result. On a model change, compare at the same effort and one level lower, measure cost per *successful* task, and count fewer tokens as a win only if evals still pass.

## CI pipeline

| Stage | Gate |
|---|---|
| 1 Lint | Structural anti-patterns, token ceiling |
| 2 Unit | Golden examples pass |
| 3 Regression | No metric below its threshold vs previous version |
| 4 A/B | New prompt beats the zero-shot baseline |
| 5 Judge | LLM-as-judge score above threshold |
| 6 Deploy | All prior stages green |

Lint checks are literal-string scans: CoT phrasing, example count above threshold, conversational padding, token count. A match inside a quoted example, inside a negation ("do not say *let's think step by step*"), or inside a code fence is a **candidate, not a violation** — a linter without this rule gets worse the harder you tune it.

## LLM-as-judge

```
Score the assistant response below against the rubric.

<task_description>{task_description}</task_description>
<input>{input}</input>
<reference_answer>{reference}</reference_answer>
<response_to_evaluate>{response}</response_to_evaluate>
<evaluation_criteria>{criteria}</evaluation_criteria>

Rate the response on each criterion from 1 to 5, where 1 completely fails,
3 is acceptable, and 5 is excellent.

Return JSON:
{"scores": {"criterion_name": 1-5}, "overall": 1-5, "reasoning": "brief explanation", "issues": ["specific issues"]}
```

Criteria sets worth separating rather than merging: accuracy (factual correctness, completeness, no fabrication), quality (clarity, relevance, helpfulness), safety (no harmful content, constraint adherence, acknowledged uncertainty).

### Judge failure modes

| Failure mode | Symptom | Mitigation |
|---|---|---|
| Verbosity bias | Longer answers score higher regardless of content (mainly reference-free; not observed under rubric + reference grading) | Calibrate against ground-truth-scored items; penalize length explicitly in criteria |
| Miscalibration | Scores drift from human judgment | Correlate judge scores with a labelled set; treat correlation above 0.7 and absolute bias below 0.5 as the reliability bar |
| Single-judge variance | One judge, one opinion, no error estimate | Multi-judge consensus; report mean and variance, flag spread above 1 point |
| Anchoring | Prior scores, attempt counts or "revised" framing in judge context shift scores; CoT and warnings do not remove it | Strip them from judge context |
| Authorship labels | Judge favors output labelled its own | Blind self/other labels |
| Criteria collapse | Judge rates one global impression across every criterion | Force per-criterion JSON scores and require an issues list |
| Judge inherits prompt anti-patterns | Judge prompt itself carries CoT scaffolding and drifts | Apply AP-1..AP-19 to the judge prompt too |

A judge is an unvalidated instrument until it is calibrated. Report the calibration, not just the score.

## Prompt caching as a token-budget lever

Cache hits depend on an exact prefix match, so any edit invalidates everything downstream of it. Order the prompt stable-first and the cache does the budgeting for you.

```
[1. SYSTEM PROMPT]         <- stable, cached
[2. REFERENCE DOCUMENTS]   <- stable across requests, cached
[3. FEW-SHOT EXAMPLES]     <- cached if used at all
[4. USER QUERY]            <- changes per request, not cached
```

| Provider | Mechanism |
|---|---|
| Anthropic | Explicit `cache_control` breakpoints |
| OpenAI | Automatic prefix caching; explicit breakpoints optional on GPT-5.6+ |
| Google | Explicit cache creation via API |

xAI cache hits need append-only history plus a sticky routing key. Kimi and Claude 5.x: pick effort before the session; top-level effort changes break the cache.

See `references/specs-current.md` for pricing and any numeric cache terms. Complementary token levers: zero-shot first (fewer tokens *and* usually better output), at most one or two examples and only to demonstrate format, structured output over verbose prose, no conversational padding, and the smallest model tier that passes the eval.

```
DO: Establish and score a zero-shot baseline before adding anything.
DO: Ship the simpler prompt when it lands within 5% of the complex one.
DO: Re-score after every distillation step and accept within 2% of baseline.
DO: Keep golden examples with a critical flag that blocks deployment.
DO: Measure consistency across repeated runs of the same input, not one run.
DO: Calibrate the judge against labelled items and use multiple judges, reporting variance.
DON'T: Treat a lint string match inside a quote, negation, or code fence as a violation.
DON'T: Edit stable prefix content casually — it invalidates every cached token after it.
```
