# Agentic Prompting Patterns (2025 Edition)

This technical reference documents prompt engineering patterns for AI agents, tool orchestration, and autonomous workflows with reasoning models (GPT-5.x, Claude 4.x, Gemini 3.x).

---

## 1. Agentic Architecture Overview

**Definition**: Agentic systems are AI applications where models autonomously plan, execute, and iterate on multi-step tasks using tools and external resources.

**2025 Context**: Reasoning models excel at agentic workflows due to native planning and state tracking capabilities.

**Core Components**:
```
┌─────────────────────────────────────────────────────────┐
│                    AGENT LOOP                           │
├─────────────────────────────────────────────────────────┤
│  1. Observe    → Receive task + context                 │
│  2. Think      → Plan approach (native reasoning)       │
│  3. Act        → Execute tool(s)                        │
│  4. Observe    → Process results                        │
│  5. Iterate    → Repeat until goal achieved             │
└─────────────────────────────────────────────────────────┘
```

---

## 2. Tool Description Patterns

**2025 Principle**: Crisp, 1-2 sentence tool descriptions. Reasoning models infer usage well.

### 2.1 Optimal Tool Description Format

**Structure**:
```json
{
  "name": "tool_name",
  "description": "[What it does]. [When to use it].",
  "parameters": {
    "param1": {"type": "string", "description": "Brief description"}
  }
}
```

**Before/After Example**:

❌ **Before (Over-described)**:
```json
{
  "name": "search_database",
  "description": "This function allows you to search through the customer database. You should use this function whenever the user asks about a customer or wants to find customer information. The function can search by either name or ID. When searching by name, partial matches will be returned. When searching by ID, only exact matches are returned. Make sure to validate the input before calling this function. If the user's request is ambiguous, ask for clarification before searching. The function returns a JSON object with customer details including name, email, phone, and account status..."
}
```

✅ **After (2025 Crisp)**:
```json
{
  "name": "search_database",
  "description": "Search customers by name or ID. Returns customer details.",
  "parameters": {
    "query": {"type": "string", "description": "Name or customer ID"},
    "field": {"type": "string", "enum": ["name", "id"]}
  }
}
```

### 2.2 Tool Description Anti-patterns

| Anti-pattern | Problem | Fix |
|--------------|---------|-----|
| Multi-paragraph descriptions | Token waste, can confuse | 1-2 sentences max |
| Usage instructions in description | Models infer this | Remove |
| Edge case handling in description | Over-constrains | Handle in code |
| "You should use this when..." | Redundant with reasoning | Remove |

---

## 3. Multi-Step Planning Patterns

**2025 Insight**: Let reasoning models plan internally. Don't prescribe steps.

### 3.1 Goal-Oriented Prompting

**Pattern**: State the goal, provide tools, let model plan.

```xml
<goal>
Deploy the updated API to production and verify it's working
</goal>

<available_tools>
- build: Compile and test the code
- deploy: Deploy to specified environment
- health_check: Verify service health
- rollback: Revert to previous version
</available_tools>

<constraints>
- Run tests before deploying
- Verify health after deploy
- Rollback if health check fails
</constraints>
```

**Why It Works**: Model determines the sequence (build → deploy → health_check → conditional rollback) without explicit step prescription.

### 3.2 State Tracking Pattern

**For long-running tasks, maintain explicit state**:

```xml
<task_state>
{
  "goal": "Migrate database schema",
  "completed_steps": ["backup_created", "schema_validated"],
  "current_step": "applying_migration",
  "pending_steps": ["verify_data", "update_app_config"],
  "blockers": []
}
</task_state>

Continue from current state. If blocked, update blockers and pause.
```

---

## 4. Parallel Tool Calling

**2025 Reality**: Claude 4.x and GPT-5.x aggressively parallelize tool calls.

### 4.1 Enabling Parallel Execution

**Prompt Pattern**:
```
Research these topics in parallel:
1. Current market size for AI assistants
2. Top 5 competitors and their features
3. Regulatory landscape in US and EU

Synthesize findings into a comparison matrix.
```

**Model Behavior**: Will launch 3 parallel search/research calls, then synthesize.

### 4.2 Controlling Parallelization

**When to Enforce Sequential**:
```
Execute these steps IN ORDER (each depends on previous):
1. Get current user permissions
2. Based on permissions, determine accessible resources
3. Query only accessible resources
```

**When to Allow Parallel**:
```
Gather this information (order doesn't matter):
- User profile
- Recent activity
- Notification settings
```

### 4.3 Claude-Specific: Parallel Call Limits

**Issue**: Claude Sonnet 4.5 can bottleneck systems with aggressive parallelization.

**Mitigation**:
```xml
<execution_constraints>
Maximum 3 concurrent tool calls. Wait for results before next batch.
</execution_constraints>
```

---

## 5. Error Recovery Patterns

### 5.1 Graceful Degradation

```xml
<task>Complete the data analysis</task>

<error_handling>
- If primary data source fails: Use cached data with staleness warning
- If analysis tool errors: Retry once, then report partial results
- If output format fails: Return plain text with apology
- Always: Report what succeeded and what failed
</error_handling>
```

### 5.2 Retry with Backoff

```xml
<retry_policy>
- Max retries: 3
- On failure: Report error, attempt alternative approach
- After max retries: Summarize attempts and request human intervention
</retry_policy>
```

### 5.3 Checkpoint Pattern

**For long tasks, save progress**:
```xml
<checkpoint_policy>
After each major step:
1. Save current state to scratch
2. Report progress to user
3. If interrupted, resume from last checkpoint
</checkpoint_policy>
```

---

## 6. Sub-Agent Orchestration

**Definition**: Delegating subtasks to specialized agents with minimal context.

### 6.1 Orchestrator Pattern

```
You are the ORCHESTRATOR. You coordinate specialists but don't do detailed work yourself.

Available specialists:
- researcher: Deep web research, citation gathering
- coder: Implementation, debugging, testing
- reviewer: Code review, security audit
- writer: Documentation, user-facing content

For each subtask:
1. Identify the right specialist
2. Provide focused context (not everything)
3. Collect and synthesize results
4. Decide next steps
```

### 6.2 Context Minimization

**Principle**: Pass minimal context to sub-agents.

❌ **Bad**: Pass entire conversation history to each sub-agent
✅ **Good**: Pass only relevant slice

```python
def create_subagent_context(task, full_context):
    """Extract minimal relevant context for subtask"""
    return {
        "task": task,
        "relevant_files": extract_relevant_files(task, full_context),
        "key_decisions": extract_decisions(full_context),
        # NOT: full_conversation_history
    }
```

### 6.3 Handoff Protocol

```xml
<handoff_format>
When delegating to a specialist, provide:
1. TASK: Specific deliverable (1-2 sentences)
2. CONTEXT: Only what they need to know
3. CONSTRAINTS: Quality requirements, boundaries
4. OUTPUT: Expected format

When receiving results:
1. Validate completeness
2. Integrate into main workflow
3. Decide next action
</handoff_format>
```

---

## 7. IDE Agent Patterns (Claude Code, Cursor, etc.)

### 7.1 CLAUDE.md Best Practices

**Structure**:
```markdown
# CLAUDE.md

## Project Context
[1-2 sentences: what this project does]

## Commands
[Essential build/test/run commands]

## Architecture
[Key patterns, not file listings]

## Conventions
[Only non-obvious rules]
```

**Anti-patterns**:
- ❌ Listing every file and directory
- ❌ Generic advice ("write good tests")
- ❌ Obvious instructions ("don't commit secrets")
- ❌ Duplicating README content

### 7.2 Skill/Command Design

**Effective Skill Structure**:
```markdown
---
name: skill-name
description: [What]. USE WHEN [triggers].
---

## Context
[Minimal background]

## Process
[Clear steps or decision tree]

## Output Format
[Expected deliverable]
```

### 7.3 Agentic Coding Patterns

**For implementation tasks**:
```
<task>Implement user authentication</task>

<approach>
1. Explore existing patterns in codebase first
2. Follow established conventions
3. Implement incrementally with tests
4. Verify each step before proceeding
</approach>

<constraints>
- Don't over-engineer
- Match existing code style
- Ask before major architectural decisions
</constraints>
```

---

## 8. Model-Specific Agentic Guidance

### Claude 4.x
- **Strength**: Long-horizon reasoning, parallel tool calling, extended autonomous operation
- **Watch**: May overtrigger tools, tendency to over-engineer
- **Prompt**: Use calm language for tools, constrain scope explicitly

### GPT-5.x
- **Strength**: Clean instruction following, minimal verbosity
- **Watch**: Agentic persistence at low reasoning levels
- **Prompt**: Add persistence reminders for long tasks at light/balanced profiles

### Gemini 3.x
- **Strength**: Massive context, direct instruction execution
- **Watch**: Requires temperature=1.0, no conversational language
- **Prompt**: Context first, questions last; be direct

---

## 9. Agentic Anti-patterns

| Anti-pattern | Problem | Fix |
|--------------|---------|-----|
| Prescribing exact tool sequence | Limits model's planning | State goal + constraints |
| Passing full context to sub-agents | Token waste, confusion | Minimal relevant context |
| No error handling | Failures cascade | Explicit recovery patterns |
| No state tracking | Can't resume, loses progress | Checkpoint pattern |
| Over-parallelization | System bottlenecks | Explicit concurrency limits |
| Micromanaging reasoning | Degrades native capabilities | Goal-oriented prompting |

---

## 10. Agentic Evaluation Metrics

| Metric | Definition | Target |
|--------|------------|--------|
| Task completion rate | % of goals achieved | >90% |
| Step efficiency | Actions taken vs optimal | <1.5x optimal |
| Error recovery rate | % of errors gracefully handled | >80% |
| Tool accuracy | Correct tool selection | >95% |
| Parallelization efficiency | Time saved via parallel calls | >30% reduction |
| Context efficiency | Tokens used vs minimum needed | <2x minimum |

---

## References

- Anthropic Claude Code Documentation (2025)
- OpenAI GPT-5 Agentic Workflows Guide (2025)
- "Building Effective Agents" - Anthropic Research (2025)
- Yao, S., et al. (2022). "ReAct: Synergizing Reasoning and Acting in Language Models." [arXiv:2210.03629](https://arxiv.org/abs/2210.03629)
