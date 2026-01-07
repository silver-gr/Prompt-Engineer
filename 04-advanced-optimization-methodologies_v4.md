# Advanced Optimization Methodologies (2025 Edition)

This technical reference documents systematic approaches to prompt optimization, evaluation frameworks, and advanced techniques for reasoning models (GPT-5.x, Claude 4.x, Gemini 3.x).

---

## 1. Prompt Engineering Development Lifecycle (2025 Simplified)

**2025 PARADIGM**: Start simple, add complexity only if needed

**Implementation Framework**:
```python
class PromptDevelopmentLifecycle2025:
    def __init__(self, task_description, evaluation_metrics, test_cases):
        self.current_prompt = None
        self.evaluation_metrics = evaluation_metrics
        self.test_cases = test_cases
        self.evaluation_results = []

    def design_phase(self):
        # 2025: Start with minimal zero-shot prompt
        self.current_prompt = create_minimal_prompt(self.task_description)

    def testing_phase(self):
        results = []
        for test_case in self.test_cases:
            response = generate_response(self.current_prompt, test_case)
            results.append(response)
        return results

    def evaluation_phase(self, test_results):
        scores = evaluate_against_metrics(test_results, self.evaluation_metrics)
        self.evaluation_results.append(scores)
        return scores

    def optimization_phase(self, evaluation_results):
        # 2025: Optimize context and clarity, not complexity
        improvements = identify_improvements(evaluation_results)

        # Priority: context > format > simplicity
        if needs_better_context(improvements):
            self.current_prompt = enhance_context(self.current_prompt)
        elif needs_clearer_format(improvements):
            self.current_prompt = clarify_output_format(self.current_prompt)

        # DON'T add: CoT instructions, excessive examples, reasoning steps

        return self.current_prompt

    def iterate(self, max_iterations=5):  # Reduced from 10
        self.design_phase()

        for i in range(max_iterations):
            test_results = self.testing_phase()
            scores = self.evaluation_phase(test_results)

            if meets_requirements(scores):
                return self.current_prompt

            self.optimization_phase(scores)

        return self.current_prompt
```

**2025 Key Changes**:
- Start with zero-shot minimal prompt
- Fewer iterations needed (reasoning models converge faster)
- Focus on context quality, not prompt complexity
- Avoid adding CoT or excessive examples

---

## 2. Quantitative Evaluation Framework (2025)

**Technical Definition**: Measuring prompt performance with emphasis on simplicity and effectiveness.

**Core Evaluation Metrics (2025)**:

| Metric | Definition | Weight | 2025 Addition |
|--------|------------|--------|---------------|
| Accuracy | Correctness of information | 0.25 | - |
| Relevance | Alignment with query | 0.20 | - |
| Completeness | Coverage of requirements | 0.20 | - |
| Consistency | Stability across runs | 0.15 | Higher with reasoning models |
| Efficiency | Token optimization | 0.10 | Includes reasoning overhead |
| Adherence | Following constraints | 0.10 | - |
| **Simplicity** | **Prompt complexity** | **NEW** | **Lower complexity preferred** |

**2025 Metric Implementation**:
```python
def evaluate_prompt_performance_2025(prompt, test_cases, model_type):
    results = {}

    # Standard metrics
    for metric_name, metric_func in STANDARD_METRICS.items():
        scores = []
        for test_case in test_cases:
            response = generate_response(prompt, test_case['input'])
            score = metric_func(response, test_case['expected'])
            scores.append(score)

        results[metric_name] = calculate_stats(scores)

    # 2025: Add simplicity metric
    results['simplicity'] = {
        'token_count': count_tokens(prompt),
        'complexity_score': measure_complexity(prompt),
        'has_unnecessary_cot': detect_cot_instructions(prompt),
        'has_excessive_examples': count_examples(prompt) > 2
    }

    # 2025: Penalize over-engineering
    if results['simplicity']['has_unnecessary_cot']:
        results['aggregate'] *= 0.9  # 10% penalty

    if results['simplicity']['has_excessive_examples']:
        results['aggregate'] *= 0.95  # 5% penalty

    return results
```

---

## 3. A/B Testing Methodology (2025 Focus: Simple vs Complex)

**Technical Definition**: Comparing prompt variants with emphasis on testing simplicity.

**2025 Common Test**: Zero-shot vs Few-shot, Simple vs Complex

**Implementation Framework**:
```python
def ab_test_prompts_2025(prompt_a, prompt_b, test_cases, metrics):
    """
    A/B test with focus on simplicity vs complexity
    """
    results_a = evaluate_prompt_performance(prompt_a, test_cases, metrics)
    results_b = evaluate_prompt_performance(prompt_b, test_cases, metrics)

    comparison = {
        'prompt_a_performance': results_a['aggregate'],
        'prompt_b_performance': results_b['aggregate'],
        'prompt_a_complexity': measure_complexity(prompt_a),
        'prompt_b_complexity': measure_complexity(prompt_b),

        # 2025: Track simplicity advantage
        'simpler_prompt': 'a' if measure_complexity(prompt_a) < measure_complexity(prompt_b) else 'b',
        'performance_per_complexity': {
            'a': results_a['aggregate'] / measure_complexity(prompt_a),
            'b': results_b['aggregate'] / measure_complexity(prompt_b)
        }
    }

    # 2025 insight: Simpler prompts often win
    if comparison['simpler_prompt'] == 'a' and results_a['aggregate'] >= results_b['aggregate'] * 0.95:
        comparison['recommendation'] = 'Use simpler prompt A'
    elif comparison['simpler_prompt'] == 'b' and results_b['aggregate'] >= results_a['aggregate'] * 0.95:
        comparison['recommendation'] = 'Use simpler prompt B'
    else:
        comparison['recommendation'] = 'Use higher performing prompt'

    return comparison
```

**Common 2025 A/B Tests**:
1. **Zero-shot vs Few-shot**: Zero-shot often wins
2. **Simple vs CoT**: Simple often wins
3. **Minimal vs Verbose**: Minimal often wins
4. **Context-rich vs Instruction-heavy**: Context-rich wins

---

## 4. Incremental Optimization (2025: Simplification Focus)

**Technical Definition**: Systematic improvement through testing individual components.

**2025 Optimization Priorities**:
1. **Context quality** (highest impact)
2. **Output format clarity** (high impact)
3. **Instruction clarity** (medium impact)
4. **Examples** (low impact, often reduce performance)
5. **CoT instructions** (negative impact - remove)

**Implementation Framework**:
```python
def incremental_optimization_2025(base_prompt, test_cases, metrics):
    """
    Optimize by improving context, not adding complexity
    """
    current_prompt = base_prompt
    baseline_score = evaluate_aggregate(current_prompt, test_cases, metrics)

    optimization_sequence = [
        ('context_enrichment', enrich_context),
        ('format_clarification', clarify_format),
        ('instruction_simplification', simplify_instructions),
        ('example_removal', remove_examples),  # 2025: Try removing examples
        ('cot_removal', remove_cot_instructions)  # 2025: Remove CoT
    ]

    for component_name, optimization_func in optimization_sequence:
        test_prompt = optimization_func(current_prompt)
        test_score = evaluate_aggregate(test_prompt, test_cases, metrics)

        if test_score > baseline_score:
            current_prompt = test_prompt
            baseline_score = test_score
            print(f"Improved with: {component_name}")

    return current_prompt
```

---

## 5. Advanced Optimization Techniques (2025 Status)

### 5.1 Prompt Chaining (Still Useful)

**2025 Status**: ✅ **Still valuable** for complex workflows

**Technical Definition**: Decomposition of complex tasks into sequential sub-tasks.

**Implementation**:
```python
class PromptChain2025:
    def __init__(self, chain_config):
        self.chain_config = chain_config
        self.results = {}

    def execute(self, initial_input, model):
        current_input = initial_input

        for step in self.chain_config:
            # 2025: Simple prompts for each step
            prompt = step['simple_prompt_template'].format(input=current_input)

            # Let reasoning models handle the thinking
            response = model.generate(
                prompt,
                thinking_mode='auto'  # 2025: Use native thinking
            )

            current_input = step.get('output_parser', lambda x: x)(response)

            self.results[step['name']] = {
                'prompt': prompt,
                'response': response,
                'parsed_output': current_input
            }

        return self.results
```

**2025 Best Practices**:
- Each step has simple, clear prompt
- Let model reason at each step
- Don't prescribe inter-step reasoning
- Use thinking modes when available

### 5.2 Prompt Ensembling (Reduced Necessity)

**2025 Status**: ⚠️ **Less necessary** with consistent reasoning models

**When to Use (2025)**:
- High-stakes decisions requiring verification
- Diverse perspectives needed
- Model confidence varies significantly

**Implementation** (if needed):
```python
def ensemble_prompts_2025(task, model, n=3):  # Reduced from 5
    """
    Generate multiple responses, use consensus
    """
    # 2025: All can be zero-shot
    responses = [
        model.generate(task, thinking_mode='auto')
        for _ in range(n)
    ]

    return consensus_selection(responses)
```

### 5.3 Self-Consistency (Mostly Unnecessary)

**2025 Status**: ⚠️ **Mostly unnecessary** - reasoning models are more consistent

**Legacy Implementation** (for reference):
```python
def self_consistency_2025(query, model, num_samples=3):  # Reduced from 5
    """
    Sample multiple reasoning paths - rarely needed in 2025
    """
    responses = []

    for i in range(num_samples):
        response = model.generate(
            query,
            temperature=0.7,  # Or 1.0 for Gemini
            thinking_mode='auto'
        )
        responses.append(extract_answer(response))

    return majority_vote(responses)
```

**2025 Alternative**: Use model's native reasoning with verification:
```
Solve this problem and verify your answer.

[problem]
```

---

## 6. Context Optimization Tools (2025 Focus)

### 6.1 Context Quality Analyzer

```python
class ContextQualityAnalyzer:
    def analyze(self, prompt):
        """
        Analyze context quality vs prompt complexity
        """
        analysis = {
            'context_richness': measure_context_richness(prompt),
            'structure_clarity': measure_structure(prompt),
            'relevance_score': measure_relevance(prompt),

            # 2025: Check for anti-patterns
            'has_cot_instructions': detect_cot(prompt),
            'excessive_examples': count_examples(prompt) > 2,
            'conversational_fluff': detect_fluff(prompt),
            'complexity_score': measure_complexity(prompt)
        }

        # Generate recommendations
        recommendations = []

        if analysis['context_richness'] < 0.5:
            recommendations.append("Enrich context with relevant background")

        if analysis['has_cot_instructions']:
            recommendations.append("Remove CoT instructions - use thinking modes")

        if analysis['excessive_examples']:
            recommendations.append("Reduce to 1-2 examples maximum")

        if analysis['conversational_fluff']:
            recommendations.append("Remove conversational padding")

        analysis['recommendations'] = recommendations
        return analysis
```

### 6.2 Simplification Tool

```python
def simplify_prompt(complex_prompt, model_type):
    """
    Simplify over-engineered prompts for reasoning models
    """
    # Extract core components
    context = extract_context(complex_prompt)
    task = extract_core_task(complex_prompt)
    output_format = extract_output_format(complex_prompt)

    # Remove anti-patterns
    context = remove_cot_instructions(context)
    context = remove_excessive_examples(context)
    context = remove_fluff(context)

    # Reconstruct as simple prompt
    if model_type == "claude":
        simplified = f"""
<context>
{context}
</context>

<task>
{task}
</task>

{output_format}
"""
    else:
        simplified = f"""
## Context
{context}

## Task
{task}

{output_format}
"""

    return simplified
```

---

## 7. Model-Specific Optimization (2025)

### 7.1 Claude Optimization

```python
def optimize_for_claude(prompt):
    """
    Optimize prompt for Claude 4.x
    """
    # Use XML structure
    structured = structure_with_xml(prompt)

    # Add thinking space
    structured = add_thinking_tag(structured)

    # Ensure rich context
    if context_richness(structured) < 0.7:
        structured = enrich_context(structured)

    return structured
```

### 7.2 GPT-5 Optimization

```python
def optimize_for_gpt5(prompt, task_complexity):
    """
    Optimize prompt for GPT-5
    """
    # Use markdown structure
    structured = structure_with_markdown(prompt)

    # Set appropriate reasoning profile
    config = {
        'prompt': structured,
        'reasoning_profile': 'balanced'
    }

    if task_complexity == 'high':
        config['reasoning_profile'] = 'deep'
        # Add verification request
        config['prompt'] += "\n\nVerify your answer before responding."

    return config
```

### 7.3 Gemini 3.x Optimization

```python
def optimize_for_gemini3(prompt):
    """
    Optimize prompt for Gemini 3.x
    """
    # Remove ALL conversational fluff
    cleaned = remove_all_fluff(prompt)

    # Ensure clear structure
    structured = structure_clearly(cleaned)

    # Set correct parameters
    config = {
        'prompt': structured,
        'temperature': 1.0,  # REQUIRED
        'thinking': 'auto'
    }

    return config
```

---

## 8. Evaluation Metrics (2025 Updated)

### 8.1 Prompt Quality Score

```python
def calculate_prompt_quality_2025(prompt, performance_results):
    """
    2025 scoring: Simpler is better if performance is maintained
    """
    # Performance component (60%)
    performance_score = performance_results['aggregate'] * 0.6

    # Simplicity component (40%) - NEW in 2025
    complexity = measure_complexity(prompt)
    simplicity_score = (1.0 - normalize(complexity)) * 0.4

    # Penalties for anti-patterns
    penalties = 0
    if detect_cot_instructions(prompt):
        penalties += 0.1
    if count_examples(prompt) > 2:
        penalties += 0.05
    if detect_fluff(prompt):
        penalties += 0.05

    total_score = performance_score + simplicity_score - penalties

    return {
        'total_score': total_score,
        'performance_component': performance_score,
        'simplicity_component': simplicity_score,
        'penalties': penalties,
        'grade': assign_grade(total_score)
    }
```

### 8.2 Zero-Shot Baseline Test

**2025 CRITICAL**: Always test zero-shot baseline first

```python
def test_zero_shot_baseline(task, test_cases, model):
    """
    Test zero-shot performance before adding complexity
    """
    # Minimal prompt
    zero_shot_prompt = f"""
{task}

[Input will be inserted here]

Return as: [format specification]
"""

    baseline_results = evaluate_prompt(zero_shot_prompt, test_cases, model)

    print(f"Zero-shot baseline: {baseline_results['aggregate']:.2f}")
    print("Only add complexity if it significantly improves on this baseline")

    return baseline_results
```

---

## 9. Prompt Distillation (2025 Enhanced)

**Technical Definition**: Creating efficient prompts while maintaining performance.

**2025 Approach**: Remove, don't just compress

**Implementation**:
```python
def distill_prompt_2025(complex_prompt, model, test_cases):
    """
    Distill by removing unnecessary elements
    """
    # Start with components
    components = {
        'context': extract_context(complex_prompt),
        'task': extract_task(complex_prompt),
        'format': extract_format(complex_prompt),
        'examples': extract_examples(complex_prompt),
        'cot_instructions': extract_cot(complex_prompt)
    }

    # 2025: Remove likely harmful elements first
    distillation_sequence = [
        # Remove CoT instructions
        lambda p: remove_component(p, 'cot_instructions'),

        # Remove examples (test if needed)
        lambda p: remove_component(p, 'examples'),

        # Simplify task description
        lambda p: simplify_component(p, 'task'),

        # Keep context (usually helpful)
        # Keep format (always helpful)
    ]

    current_prompt = complex_prompt
    baseline_score = evaluate(complex_prompt, test_cases)

    for distill_func in distillation_sequence:
        candidate = distill_func(current_prompt)
        score = evaluate(candidate, test_cases)

        # Accept if performance maintained (within 2%)
        if score >= baseline_score * 0.98:
            current_prompt = candidate
            print(f"Distillation successful, tokens reduced: {count_tokens(complex_prompt) - count_tokens(current_prompt)}")

    return current_prompt
```

---

## 10. Prompt Regression Testing (2025 NEW)

**Definition**: Automated testing to ensure prompt changes don't degrade performance.

### 10.1 Regression Test Suite

```python
class PromptRegressionSuite:
    def __init__(self, prompt_id, golden_examples):
        self.prompt_id = prompt_id
        self.golden_examples = golden_examples  # Known good input/output pairs
        self.thresholds = {
            'accuracy': 0.95,      # Must maintain 95% accuracy
            'consistency': 0.90,   # 90% same output for same input
            'format_compliance': 1.0  # 100% valid output format
        }

    def run_regression(self, old_prompt, new_prompt, model):
        """
        Test new prompt against golden examples
        """
        old_results = self.evaluate(old_prompt, model)
        new_results = self.evaluate(new_prompt, model)

        regressions = []

        for metric, threshold in self.thresholds.items():
            if new_results[metric] < old_results[metric] * threshold:
                regressions.append({
                    'metric': metric,
                    'old_value': old_results[metric],
                    'new_value': new_results[metric],
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
            # Run 3 times for consistency check
            responses = [model.generate(prompt.format(**example['input'])) for _ in range(3)]

            # Accuracy: Does output match expected?
            accuracy = semantic_similarity(responses[0], example['expected_output'])
            results['accuracy'].append(accuracy)

            # Consistency: Are all 3 runs similar?
            consistency = min(semantic_similarity(responses[i], responses[j])
                            for i in range(3) for j in range(i+1, 3))
            results['consistency'].append(consistency)

            # Format compliance: Valid JSON/structure?
            format_ok = all(validate_format(r, example.get('format_spec')) for r in responses)
            results['format_compliance'].append(1.0 if format_ok else 0.0)

        return {k: sum(v)/len(v) for k, v in results.items()}
```

### 10.2 Golden Example Management

```python
# Golden examples structure
GOLDEN_EXAMPLES = [
    {
        "id": "customer_lookup_basic",
        "input": {"query": "Find customer John Smith"},
        "expected_output": {"action": "search", "field": "name", "value": "John Smith"},
        "format_spec": "json",
        "critical": True  # Must pass for deployment
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

## 11. Automated Evaluation Pipelines (2025 NEW)

**Definition**: CI/CD-style automation for prompt testing and deployment.

### 11.1 Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    PROMPT CI/CD PIPELINE                    │
├─────────────────────────────────────────────────────────────┤
│  1. Lint         → Check prompt structure and anti-patterns │
│  2. Unit Test    → Test against golden examples             │
│  3. Regression   → Compare against previous version         │
│  4. A/B Test     → Test zero-shot vs new prompt             │
│  5. LLM Judge    → Quality assessment by evaluator model    │
│  6. Deploy       → Promote to production if all pass        │
└─────────────────────────────────────────────────────────────┘
```

### 11.2 Pipeline Implementation

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
                stage_result = stage_func(prompt, previous_prompt)
                results['stages'][stage_name] = stage_result

                if not stage_result['passed']:
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
        """Check for anti-patterns"""
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

### 11.3 CI Integration Example

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

## 12. LLM-as-Judge Patterns (2025 NEW)

**Definition**: Using a language model to evaluate outputs from another model or prompt.

### 12.1 Judge Prompt Template

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
  "scores": {
    "criterion_1": <1-5>,
    "criterion_2": <1-5>,
    ...
  },
  "overall": <1-5>,
  "reasoning": "Brief explanation",
  "issues": ["List any specific issues"]
}
"""
```

### 12.2 Evaluation Criteria Sets

```python
EVALUATION_CRITERIA = {
    'accuracy': {
        'factual_correctness': 'Are all facts accurate?',
        'completeness': 'Does it answer all parts of the question?',
        'no_hallucination': 'Are there any made-up facts or citations?'
    },
    'quality': {
        'clarity': 'Is the response clear and well-structured?',
        'relevance': 'Does it stay on topic?',
        'helpfulness': 'Would this help the user achieve their goal?'
    },
    'safety': {
        'no_harmful_content': 'Is the content safe and appropriate?',
        'follows_guidelines': 'Does it follow the specified constraints?',
        'honest': 'Does it acknowledge uncertainty appropriately?'
    }
}
```

### 12.3 Multi-Judge Consensus

```python
def multi_judge_evaluation(response, task, criteria, judge_models):
    """
    Use multiple LLM judges for more robust evaluation
    """
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

    # Consensus: Average scores, flag high variance
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

### 12.4 Judge Calibration

**Problem**: LLM judges can be biased (e.g., prefer verbose responses).

**Solution**: Calibrate with known examples.

```python
def calibrate_judge(judge_model, calibration_set):
    """
    Calibration set: responses with known ground-truth scores
    """
    predictions = []
    actuals = []

    for item in calibration_set:
        judgment = run_judge(judge_model, item['response'], item['task'])
        predictions.append(judgment['overall'])
        actuals.append(item['ground_truth_score'])

    # Calculate correlation
    correlation = pearson_correlation(predictions, actuals)

    # Calculate bias (does judge consistently over/under rate?)
    bias = sum(predictions) / len(predictions) - sum(actuals) / len(actuals)

    return {
        'correlation': correlation,
        'bias': bias,
        'reliable': correlation > 0.7 and abs(bias) < 0.5
    }
```

---

## 13. Best Practices Summary (2025)

**Development Workflow**:
1. ✅ Start with zero-shot minimal prompt
2. ✅ Test baseline performance
3. ✅ Optimize context if needed
4. ✅ Clarify output format if needed
5. ✅ Use model-native thinking modes
6. ❌ Don't add CoT instructions
7. ❌ Don't add excessive examples
8. ❌ Don't over-engineer

**Optimization Priorities**:
1. **Context quality** (highest ROI)
2. **Output format clarity**
3. **Instruction simplicity**
4. **Model-specific parameters** (temp 1.0 for Gemini)
5. **Thinking mode configuration**

**Evaluation Focus**:
- Performance (accuracy, relevance, completeness)
- Simplicity (token count, complexity score)
- Consistency (stable across runs)
- Efficiency (performance per token)

---

## Technical References

**2025 Research & Documentation**:
- OpenAI GPT-5 Optimization Guide (2025)
- Anthropic Claude 4.x Best Practices (2025)
- Google Gemini 3.x Technical Documentation (2025)
- "Simpler Prompts for Reasoning Models" - Industry findings (2025)

**Foundational Research**:
- Wei, J., et al. (2022). "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models." [arXiv:2201.11903](https://arxiv.org/abs/2201.11903) - Historical context
- Liu, P., et al. (2023). "Pre-train, Prompt, and Predict: A Systematic Survey." [ACM Computing Surveys](https://dl.acm.org/doi/abs/10.1145/3560815)
- White, J., et al. (2023). "A Prompt Pattern Catalog." [arXiv:2302.11382](https://arxiv.org/abs/2302.11382)
