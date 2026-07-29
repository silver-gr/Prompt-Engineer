---
name: prompt-context-engineer
description: Create or optimize prompts and context packs for frontier LLMs (GPT-5, Claude 4.x, Gemini 3.x, Grok, DeepSeek/GLM/Qwen/Kimi). Use when asked to rewrite prompts, craft model-specific instructions, choose best practices per model, or assemble minimal context for LLM input.
---

# Prompt Context Engineer

## Overview
Design minimal, model-specific prompts and context packs by selecting only the references needed for the user's model and task.

## Workflow Decision Tree

1. Identify the user intent.
   - Prompt rewrite or optimization
   - New prompt creation
   - Context pack assembly for LLM input

2. Determine the target model.
   - If specified, use that model's reference file.
   - If not specified, assume a frontier default (state the assumption explicitly).

3. Determine the task type.
   - Code, analysis, content, data extraction/transform

4. Load the minimum references.
   - Always: `references/core-principles.md`
   - Model-specific: exactly one of `references/models-*.md`
   - Task-specific: exactly one of `references/tasks-*.md`
   - Optional: `references/patterns-agentic.md` (tools/agents)
   - Optional: `references/patterns-safety.md` (safety/guardrails)
   - Optional: `references/patterns-eval.md` (evaluation/testing)
   - Optional: `references/tools-*.md` (UI research features)

5. Produce the deliverable.
   - Provide the recommended prompt only (no alternatives).
   - Include model settings (temperature, reasoning profile, thinking_level) as config, not inside the prompt.
   - Provide a compact Context Pack listing only the references used.

## Output Format

Use this shape unless the user asks for a different format:

- Recommended Prompt: exact prompt text
- Model Settings: config parameters (not in the prompt)
- Context Pack: list of reference files used
- Notes: only if critical constraints or risks apply

## Reference Map (what to load)

- `references/core-principles.md`: Always.
- `references/models-openai.md`: GPT-5 family.
- `references/models-anthropic.md`: Claude 4.x family.
- `references/models-gemini.md`: Gemini 3.x family.
- `references/models-xai.md`: Grok family.
- `references/models-china.md`: DeepSeek/GLM/Qwen/Kimi.
- `references/tasks-code.md`: Coding tasks.
- `references/tasks-analysis.md`: Analysis/research tasks.
- `references/tasks-content.md`: Content generation.
- `references/tasks-data.md`: Extraction/transform.
- `references/patterns-agentic.md`: Tool-using agents.
- `references/patterns-safety.md`: Guardrails and injection defense.
- `references/patterns-eval.md`: Evaluation and testing.
- `references/tools-claude-research.md`: Claude Research UI.
- `references/tools-gemini-research.md`: Gemini Deep Research UI.
- `references/templates.md`: Minimal prompt templates.

## Scripts

- `scripts/build_context.py`: Assemble a minimal Context Pack from selected references.
- `scripts/lint_refs.py`: Validate reference file length and TOC rules.
