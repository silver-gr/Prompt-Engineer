# Evaluation & Testing Patterns (March 2026)

## Evaluation Metrics

| Metric | Measures | Method |
|--------|----------|--------|
| Accuracy | Correctness of output | Golden examples comparison |
| Relevance | Task alignment | LLM-as-judge scoring |
| Completeness | Coverage of requirements | Checklist verification |
| Adherence | Following constraints/format | Programmatic validation |
| Consistency | Reproducibility across runs | Multiple runs, variance check |
| Efficiency | Token usage, latency | Instrumentation |

## Zero-Shot Baseline Test

Always test zero-shot first. Only add complexity if baseline fails:

```
1. Run zero-shot prompt on 10-20 representative inputs
2. Score against golden outputs
3. If score >= threshold: done (use zero-shot)
4. If score < threshold: add ONE improvement, retest
```

## A/B Testing

- Compare exactly two variants at a time
- Use same test set for both
- Prefer the simpler prompt if performance is within 5%
- Track: accuracy, token cost, latency

### Simple A/B Pattern
```python
results_a = [evaluate(prompt_a, input) for input in test_set]
results_b = [evaluate(prompt_b, input) for input in test_set]
winner = "A" if mean(results_a) > mean(results_b) else "B"
```

## Regression Testing

- Maintain golden input/output pairs (10-50 examples)
- Run after every prompt change
- Track deltas: which examples improved/degraded
- Block deployment if regression > threshold

### Golden Example Format
```json
{
  "id": "test-001",
  "input": "...",
  "expected_output": "...",
  "evaluation_criteria": ["accuracy", "format"],
  "tags": ["edge-case", "multilingual"]
}
```

## LLM-as-Judge

Use a separate model to evaluate outputs:

```
Rate the following response on a scale of 1-5 for [criteria].

<rubric>
5: [description of excellent]
3: [description of acceptable]
1: [description of poor]
</rubric>

<response>
[output to evaluate]
</response>

Return JSON: {"score": N, "justification": "..."}
```

### Calibration Tips
- Always require justification for scores
- Use multi-judge consensus (2-3 judges, take median)
- Calibrate for known bias (models tend to rate high)
- Use a stronger model as judge (Opus judging Sonnet output)

## CI/CD Pipeline for Prompts

```
Lint (format check) -> Unit Test (golden examples)
  -> Regression Test -> A/B Test -> LLM Judge -> Deploy
```

## Prompt Quality Scoring

Quick self-assessment checklist:
- [ ] Zero-shot attempted first?
- [ ] No anti-patterns present? (run scanner)
- [ ] Output format explicitly specified?
- [ ] Model-specific settings configured?
- [ ] Tested on representative inputs?
- [ ] Cost/latency acceptable?
