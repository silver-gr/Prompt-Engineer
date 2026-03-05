# Evaluation & Optimization Methodologies (2026 Edition)

This module documents systematic approaches to prompt evaluation, regression testing, CI/CD pipelines, and LLM-as-judge patterns.

> **Anti-patterns**: See 02-techniques-patterns_v5.md (canonical).
> **Model specs**: See 03-model-catalog_v5.md.

---

## 1. Development Lifecycle

### 2026 Paradigm: Start Simple, Add Complexity Only If Measured

```python
class PromptDevelopmentLifecycle:
    def __init__(self, task, eval_metrics, test_cases):
        self.task = task
        self.eval_metrics = eval_metrics
        self.test_cases = test_cases

    def design_phase(self):
        # Start with minimal zero-shot prompt
        self.current_prompt = create_minimal_prompt(self.task)

    def test_phase(self):
        results = []
        for case in self.test_cases:
            response = generate_response(self.current_prompt, case)
            results.append(response)
        return results

    def evaluate_phase(self, results):
        return evaluate_against_metrics(results, self.eval_metrics)

    def optimize_phase(self, scores):
        # Optimize context and clarity, not complexity
        if needs_better_context(scores):
            self.current_prompt = enhance_context(self.current_prompt)
        elif needs_clearer_format(scores):
            self.current_prompt = clarify_output_format(self.current_prompt)
        # DON'T add: CoT instructions, excessive examples, reasoning steps
        return self.current_prompt

    def iterate(self, max_iterations=5):
        self.design_phase()
        for i in range(max_iterations):
            results = self.test_phase()
            scores = self.evaluate_phase(results)
            if meets_requirements(scores):
                return self.current_prompt
            self.optimize_phase(scores)
        return self.current_prompt
```

### Optimization Priorities (ranked by impact)

1. **Context quality** -- highest ROI
2. **Output format clarity** -- high impact
3. **Instruction clarity** -- medium impact
4. **Examples** -- low impact, often reduce performance
5. **CoT instructions** -- negative impact, remove

---

## 2. Quantitative Evaluation Framework

### Core Metrics

| Metric | Definition | Weight | Notes |
|--------|------------|--------|-------|
| Accuracy | Correctness of information | 0.25 | Primary metric |
| Relevance | Alignment with query | 0.20 | |
| Completeness | Coverage of requirements | 0.20 | |
| Consistency | Stability across runs | 0.15 | Higher with reasoning models |
| Efficiency | Token optimization | 0.10 | Includes reasoning overhead |
| Adherence | Following constraints | 0.10 | |
| Simplicity | Prompt complexity (inverse) | Bonus | Lower complexity preferred |

### Implementation

```python
def evaluate_prompt_performance(prompt, test_cases, model):
    results = {}

    for metric_name, metric_func in STANDARD_METRICS.items():
        scores = []
        for case in test_cases:
            response = generate_response(prompt, case['input'])
            score = metric_func(response, case['expected'])
            scores.append(score)
        results[metric_name] = calculate_stats(scores)

    # Simplicity bonus: penalize over-engineering
    results['simplicity'] = {
        'token_count': count_tokens(prompt),
        'has_unnecessary_cot': detect_cot_instructions(prompt),
        'has_excessive_examples': count_examples(prompt) > 2
    }

    # Apply penalties for anti-patterns
    aggregate = results['aggregate']
    if results['simplicity']['has_unnecessary_cot']:
        aggregate *= 0.9   # 10% penalty
    if results['simplicity']['has_excessive_examples']:
        aggregate *= 0.95  # 5% penalty

    results['final_score'] = aggregate
    return results
```

---

## 3. A/B Testing

### 2026 Focus: Simple vs Complex

The most common and valuable test is comparing a simpler prompt against a more complex one.

```python
def ab_test_prompts(prompt_a, prompt_b, test_cases, metrics):
    results_a = evaluate_prompt(prompt_a, test_cases, metrics)
    results_b = evaluate_prompt(prompt_b, test_cases, metrics)

    comparison = {
        'a_score': results_a['aggregate'],
        'b_score': results_b['aggregate'],
        'a_complexity': measure_complexity(prompt_a),
        'b_complexity': measure_complexity(prompt_b),
        'simpler': 'a' if measure_complexity(prompt_a) < measure_complexity(prompt_b) else 'b',
        'efficiency': {
            'a': results_a['aggregate'] / measure_complexity(prompt_a),
            'b': results_b['aggregate'] / measure_complexity(prompt_b)
        }
    }

    # Prefer simpler prompt if within 5% of complex prompt's performance
    simpler = comparison['simpler']
    simpler_score = comparison[f'{simpler}_score']
    other_score = comparison[f'{"b" if simpler == "a" else "a"}_score']

    if simpler_score >= other_score * 0.95:
        comparison['recommendation'] = f'Use simpler prompt ({simpler})'
    else:
        comparison['recommendation'] = 'Use higher performing prompt'

    return comparison
```

### Standard Test Battery

| Test | What It Validates |
|------|-------------------|
| Zero-shot vs few-shot | Whether examples help (often they don't) |
| Simple vs CoT | Whether explicit reasoning helps (rarely) |
| Minimal vs verbose | Whether brevity maintains quality (usually) |
| Context-rich vs instruction-heavy | Whether context > instructions (yes) |

---

## 4. Zero-Shot Baseline Test

**Critical**: Always establish zero-shot baseline before adding any complexity.

```python
def test_zero_shot_baseline(task, test_cases, model):
    zero_shot_prompt = f"""
{task}

[Input will be inserted here]

Return as: [format specification]
"""
    baseline = evaluate_prompt(zero_shot_prompt, test_cases, model)

    print(f"Zero-shot baseline: {baseline['aggregate']:.2f}")
    print("Only add complexity if it significantly improves on this.")

    return baseline
```

---

## 5. Incremental Optimization

### Simplification-First Approach

```python
def incremental_optimization(base_prompt, test_cases, metrics):
    current = base_prompt
    baseline = evaluate_aggregate(current, test_cases, metrics)

    # Try each optimization; keep if it improves score
    optimizations = [
        ('context_enrichment', enrich_context),
        ('format_clarification', clarify_format),
        ('instruction_simplification', simplify_instructions),
        ('example_removal', remove_examples),      # Try removing examples
        ('cot_removal', remove_cot_instructions),   # Remove explicit CoT
        ('fluff_removal', remove_conversational_fluff)
    ]

    for name, func in optimizations:
        candidate = func(current)
        score = evaluate_aggregate(candidate, test_cases, metrics)
        if score > baseline:
            current = candidate
            baseline = score
            print(f"Improved with: {name} -> {score:.2f}")

    return current
```

---

## 6. Prompt Distillation

**Definition**: Removing unnecessary elements while maintaining performance.

```python
def distill_prompt(complex_prompt, model, test_cases):
    baseline_score = evaluate(complex_prompt, test_cases)

    # Remove elements in order of likely harm
    removals = [
        ('cot_instructions', remove_cot),
        ('excess_examples', remove_examples_beyond_one),
        ('fluff', remove_conversational_padding),
        ('verbose_instructions', simplify_task_description),
    ]

    current = complex_prompt
    for name, remove_func in removals:
        candidate = remove_func(current)
        score = evaluate(candidate, test_cases)

        # Accept if within 2% of baseline
        if score >= baseline_score * 0.98:
            current = candidate
            tokens_saved = count_tokens(complex_prompt) - count_tokens(current)
            print(f"Removed {name}: saved {tokens_saved} tokens")

    return current
```

---

## 7. Context Quality Analysis

```python
class ContextQualityAnalyzer:
    def analyze(self, prompt):
        analysis = {
            'context_richness': measure_context_richness(prompt),
            'structure_clarity': measure_structure(prompt),
            'relevance_score': measure_relevance(prompt),
            # Anti-pattern detection
            'has_cot_instructions': detect_cot(prompt),
            'excessive_examples': count_examples(prompt) > 2,
            'conversational_fluff': detect_fluff(prompt),
            'complexity_score': measure_complexity(prompt)
        }

        recommendations = []
        if analysis['context_richness'] < 0.5:
            recommendations.append("Enrich context with relevant background")
        if analysis['has_cot_instructions']:
            recommendations.append("Remove CoT instructions -- use thinking modes")
        if analysis['excessive_examples']:
            recommendations.append("Reduce to 0-1 examples")
        if analysis['conversational_fluff']:
            recommendations.append("Remove conversational padding")

        analysis['recommendations'] = recommendations
        return analysis
```

---

## 8. Prompt Regression Testing

### Regression Test Suite

```python
class PromptRegressionSuite:
    def __init__(self, prompt_id, golden_examples):
        self.prompt_id = prompt_id
        self.golden_examples = golden_examples
        self.thresholds = {
            'accuracy': 0.95,
            'consistency': 0.90,
            'format_compliance': 1.0
        }

    def run_regression(self, old_prompt, new_prompt, model):
        old_results = self.evaluate(old_prompt, model)
        new_results = self.evaluate(new_prompt, model)

        regressions = []
        for metric, threshold in self.thresholds.items():
            if new_results[metric] < old_results[metric] * threshold:
                regressions.append({
                    'metric': metric,
                    'old': old_results[metric],
                    'new': new_results[metric],
                    'threshold': threshold,
                    'severity': 'critical' if metric == 'accuracy' else 'warning'
                })

        return {
            'passed': len(regressions) == 0,
            'regressions': regressions,
            'old_results': old_results,
            'new_results': new_results
        }

    def evaluate(self, prompt, model):
        results = {'accuracy': [], 'consistency': [], 'format_compliance': []}

        for example in self.golden_examples:
            responses = [model.generate(prompt.format(**example['input'])) for _ in range(3)]

            accuracy = semantic_similarity(responses[0], example['expected_output'])
            results['accuracy'].append(accuracy)

            consistency = min(
                semantic_similarity(responses[i], responses[j])
                for i in range(3) for j in range(i+1, 3)
            )
            results['consistency'].append(consistency)

            format_ok = all(validate_format(r, example.get('format_spec')) for r in responses)
            results['format_compliance'].append(1.0 if format_ok else 0.0)

        return {k: sum(v)/len(v) for k, v in results.items()}
```

### Golden Example Management

```python
GOLDEN_EXAMPLES = [
    {
        "id": "customer_lookup_basic",
        "input": {"query": "Find customer John Smith"},
        "expected_output": {"action": "search", "field": "name", "value": "John Smith"},
        "format_spec": "json",
        "critical": True   # Must pass for deployment
    },
    {
        "id": "edge_case_empty",
        "input": {"query": ""},
        "expected_output": {"error": "empty_query"},
        "format_spec": "json",
        "critical": True
    }
]
```

---

## 9. Automated Evaluation Pipeline (CI/CD)

### Pipeline Architecture

```
+-------------------------------------------------------------+
|                    PROMPT CI/CD PIPELINE                      |
+-------------------------------------------------------------+
|  1. Lint         -> Check prompt structure and anti-patterns  |
|  2. Unit Test    -> Test against golden examples              |
|  3. Regression   -> Compare against previous version          |
|  4. A/B Test     -> Test zero-shot vs new prompt              |
|  5. LLM Judge    -> Quality assessment by evaluator model     |
|  6. Deploy       -> Promote to production if all pass         |
+-------------------------------------------------------------+
```

### Pipeline Implementation

```python
class PromptPipeline:
    def __init__(self, config):
        self.config = config
        self.stages = [
            ('lint', self.lint_stage),
            ('unit_test', self.unit_test_stage),
            ('regression', self.regression_stage),
            ('ab_test', self.ab_test_stage),
            ('llm_judge', self.llm_judge_stage),
        ]

    def run(self, prompt, previous_prompt=None):
        results = {'prompt': prompt, 'stages': {}}

        for stage_name, stage_func in self.stages:
            try:
                result = stage_func(prompt, previous_prompt)
                results['stages'][stage_name] = result

                if not result['passed']:
                    results['status'] = 'failed'
                    results['failed_stage'] = stage_name
                    return results
            except Exception as e:
                results['status'] = 'error'
                results['error'] = str(e)
                return results

        results['status'] = 'passed'
        return results

    def lint_stage(self, prompt, _):
        issues = []
        if detect_cot_instructions(prompt):
            issues.append('Contains unnecessary CoT instructions')
        if count_examples(prompt) > 2:
            issues.append('Excessive examples (>2)')
        if detect_fluff(prompt):
            issues.append('Contains conversational fluff')
        if count_tokens(prompt) > self.config['max_tokens']:
            issues.append(f'Exceeds token limit ({self.config["max_tokens"]})')
        return {'passed': len(issues) == 0, 'issues': issues}
```

### CI Integration

```yaml
# .github/workflows/prompt-ci.yml
name: Prompt CI
on:
  push:
    paths:
      - 'prompts/**'

jobs:
  test-prompts:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Lint Prompts
        run: python scripts/lint_prompts.py prompts/

      - name: Run Golden Tests
        run: python scripts/test_prompts.py --golden-set tests/golden.json
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}

      - name: Regression Check
        run: python scripts/regression_check.py --baseline main

      - name: LLM Judge Evaluation
        run: python scripts/llm_judge.py --threshold 0.8
```

---

## 10. LLM-as-Judge Patterns

### Judge Prompt Template

```python
LLM_JUDGE_PROMPT = """
You are an expert evaluator assessing AI assistant responses.

<task_description>
{task_description}
</task_description>

<input>
{input}
</input>

<response_to_evaluate>
{response}
</response_to_evaluate>

<evaluation_criteria>
{criteria}
</evaluation_criteria>

Rate the response on each criterion from 1-5:
- 1: Completely fails
- 2: Major issues
- 3: Acceptable
- 4: Good
- 5: Excellent

Return JSON:
{
  "scores": {"criterion_1": <1-5>, "criterion_2": <1-5>},
  "overall": <1-5>,
  "reasoning": "Brief explanation",
  "issues": ["List any specific issues"]
}
"""
```

### Evaluation Criteria Sets

```python
EVALUATION_CRITERIA = {
    'accuracy': {
        'factual_correctness': 'Are all facts accurate?',
        'completeness': 'Does it answer all parts?',
        'no_hallucination': 'Are there any fabricated facts?'
    },
    'quality': {
        'clarity': 'Is the response clear and well-structured?',
        'relevance': 'Does it stay on topic?',
        'helpfulness': 'Would this help the user?'
    },
    'safety': {
        'no_harmful_content': 'Is the content safe?',
        'follows_guidelines': 'Does it follow constraints?',
        'honest': 'Does it acknowledge uncertainty?'
    }
}
```

### Multi-Judge Consensus

```python
def multi_judge_evaluation(response, task, criteria, judge_models):
    judge_scores = []

    for judge_model in judge_models:
        prompt = LLM_JUDGE_PROMPT.format(
            task_description=task,
            input=response['input'],
            response=response['output'],
            criteria=format_criteria(criteria)
        )
        judgment = judge_model.generate(prompt, temperature=0.3)
        judge_scores.append(parse_judgment(judgment))

    # Consensus: average scores, flag high variance
    consensus = {}
    for criterion in criteria:
        scores = [j['scores'][criterion] for j in judge_scores]
        consensus[criterion] = {
            'mean': sum(scores) / len(scores),
            'variance': variance(scores),
            'agreement': max(scores) - min(scores) <= 1
        }

    return {
        'consensus': consensus,
        'individual_judgments': judge_scores,
        'high_agreement': all(c['agreement'] for c in consensus.values())
    }
```

### Judge Calibration

**Problem**: LLM judges can be biased (e.g., prefer verbose responses).

```python
def calibrate_judge(judge_model, calibration_set):
    predictions = []
    actuals = []

    for item in calibration_set:
        judgment = run_judge(judge_model, item['response'], item['task'])
        predictions.append(judgment['overall'])
        actuals.append(item['ground_truth_score'])

    correlation = pearson_correlation(predictions, actuals)
    bias = sum(predictions) / len(predictions) - sum(actuals) / len(actuals)

    return {
        'correlation': correlation,
        'bias': bias,
        'reliable': correlation > 0.7 and abs(bias) < 0.5
    }
```

---

## 11. Model-Specific Optimization Functions

### Claude Optimization

```python
def optimize_for_claude(prompt):
    structured = structure_with_xml(prompt)
    if context_richness(structured) < 0.7:
        structured = enrich_context(structured)
    return structured
```

### GPT-5 Optimization

```python
def optimize_for_gpt5(prompt, complexity):
    structured = structure_with_markdown(prompt)
    config = {'prompt': structured, 'reasoning_profile': 'balanced'}
    if complexity == 'high':
        config['reasoning_profile'] = 'deep'
        config['prompt'] += "\n\nVerify your answer before responding."
    return config
```

### Gemini 3.x Optimization

```python
def optimize_for_gemini(prompt):
    cleaned = remove_conversational_fluff(prompt)
    structured = structure_clearly(cleaned)
    return {
        'prompt': structured,
        'temperature': 1.0,     # REQUIRED
        'thinking': 'auto'
    }
```

---

## 12. Prompt Quality Score

```python
def calculate_prompt_quality(prompt, performance_results):
    # Performance component (60%)
    performance = performance_results['aggregate'] * 0.6

    # Simplicity component (40%)
    complexity = measure_complexity(prompt)
    simplicity = (1.0 - normalize(complexity)) * 0.4

    # Anti-pattern penalties
    penalties = 0
    if detect_cot_instructions(prompt): penalties += 0.1
    if count_examples(prompt) > 2: penalties += 0.05
    if detect_fluff(prompt): penalties += 0.05

    total = performance + simplicity - penalties

    return {
        'total_score': total,
        'performance': performance,
        'simplicity': simplicity,
        'penalties': penalties,
        'grade': assign_grade(total)
    }
```

---

## Best Practices Summary

**Development Workflow**:
1. Start with zero-shot minimal prompt
2. Test baseline performance
3. Optimize context if needed
4. Clarify output format if needed
5. Use model-native thinking modes
6. DON'T add CoT or excessive examples
7. Run regression tests before deploying
8. Use LLM-as-judge for quality assessment

**Evaluation Focus**:
- Performance (accuracy, relevance, completeness)
- Simplicity (token count, complexity score)
- Consistency (stability across runs)
- Efficiency (performance per token)

---

## References

- OpenAI GPT-5 Optimization Guide (2025-2026)
- Anthropic Claude 4.x Best Practices (2025-2026)
- Google Gemini 3.x Technical Documentation (2025-2026)
- Wei, J., et al. (2022). "Chain-of-Thought Prompting." [arXiv:2201.11903](https://arxiv.org/abs/2201.11903)
- Liu, P., et al. (2023). "Pre-train, Prompt, and Predict." [ACM Computing Surveys](https://dl.acm.org/doi/abs/10.1145/3560815)
