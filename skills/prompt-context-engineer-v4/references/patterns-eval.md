# Evaluation Patterns

## Metrics
- Accuracy, relevance, completeness, adherence
- Consistency across runs
- Simplicity (fewer tokens, fewer examples)

## A/B Testing
- Compare zero-shot vs few-shot.
- Prefer the simpler prompt if performance is within 5%.

## Regression Testing
- Maintain golden inputs/outputs.
- Track deltas after prompt changes.

## LLM-as-Judge
- Use a fixed rubric and calibrate for bias.
- Require justification for scores.
