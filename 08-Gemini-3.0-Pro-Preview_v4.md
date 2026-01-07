# Gemini 3.0 Pro: Quick Reference (v4 - Updated December 2025)

## Model Overview
Gemini 3.0 Pro (officially released November 2025) is Google's most advanced reasoning model, designed for direct, efficient instruction-following and advanced reasoning tasks. It features a 1M token context window, 64k token output limit, and a knowledge cutoff of January 2025.

## Core Prompting Principles

### 1. Be Precise and Direct
- **State your goal clearly:** Gemini 3 prefers direct, executable instructions over conversational or persuasive language.
- **Avoid:** "Could you please help me understand..."
- **Use:** "Explain the differences between..."
- **Key insight:** Directness over persuasion. Gemini 3 is optimized for task execution, not chat.

### 2. Simplify Your Prompts
- **Stop using complex Chain-of-Thought from Gemini 2.x:** Gemini 3 has native advanced reasoning. You don't need to force it to "think step-by-step" for most tasks.
- **Old way (Gemini 2.x):** "Let's approach this step-by-step: First, identify the problem. Second, brainstorm solutions. Third, evaluate each solution..."
- **New way (Gemini 3):** "Solve this problem: [problem]. Show your reasoning."
- **Exception:** For very complex reasoning tasks, you can still use explicit planning or self-critique prompts (see "Enhancing Reasoning" section below).

### 3. Use the `thinking_level` Parameter
- **New in Gemini 3:** The `thinking_level` parameter controls the depth of reasoning.
  - **`"low"`:** Fast, efficient responses for straightforward tasks. Lower latency, lower cost.
  - **`"high"`:** Default. Deep reasoning for complex tasks requiring multi-step analysis.
- **When to use `"low"`:** Simple queries, data extraction, formatting tasks, quick lookups.
- **When to use `"high"`:** Research, planning, creative writing, complex problem-solving, code generation with edge cases.
- **Important:** This is a parameter you set in the API or interface settings, not something you prompt for.

### 4. Keep Temperature at 1.0
- **Critical:** Gemini 3 is calibrated for `temperature = 1.0` (default). Do NOT change this unless you have a specific reason.
- **Why:** The model's reasoning and instruction-following are optimized for this setting. Lowering temperature can make outputs overly deterministic and reduce creative problem-solving. Raising it can introduce unwanted randomness.
- **Exception:** For highly creative tasks (poetry, fiction), you might experiment with slightly higher values (1.1-1.2), but 1.0 is the recommended starting point.

### 5. Use Consistent Structure
- **XML tags or Markdown headings:** Choose one format and stick with it throughout a single prompt.
- **XML example:**
  ```
  <role>
  You are a senior data analyst.
  </role>

  <constraints>
  - Focus on 2024-2025 data only
  - Cite all sources
  </constraints>

  <context>
  [Insert data, documents, or background information here]
  </context>

  <task>
  Analyze the trend in Q3 revenue and identify root causes for the decline.
  </task>
  ```
- **Markdown example:**
  ```
  # Role
  You are a technical writer.

  # Constraints
  - Use simple language (8th grade reading level)
  - Include code examples
  - Maximum 500 words

  # Task
  Explain how async/await works in JavaScript.
  ```

### 6. Context First, Questions LAST
- **For long contexts:** Provide all documents, data, or code first. Place your specific instructions or questions at the very end.
- **Why:** This structure helps Gemini 3 process all relevant information before executing the task.
- **Example:**
  ```
  <context>
  [Full text of three research papers, 50k tokens]
  </context>

  <task>
  Based on the three papers above, identify common themes and contradictions. Present in a comparison table.
  </task>
  ```

### 7. Anchor Context with Transitions
- **After large blocks of data:** Use a clear transition phrase to bridge context and your query.
- **Examples:**
  - "Based on the information above..."
  - "Using the data provided..."
  - "Given the context..."
- **Why:** This helps the model understand where the context ends and the task begins.

### 8. Explicit Multimodal Labels
- **When using images, audio, or video:** Explicitly reference each modality in your instructions.
- **Example:**
  ```
  I've uploaded three files:
  - Image 1: Product mockup
  - Image 2: Competitor product
  - Video 1: User testing session

  Task: Compare the UX design in Image 1 and Image 2. Use insights from Video 1 to identify usability improvements.
  ```
- **Why:** Gemini 3 treats text, images, audio, and video as equal-class inputs. Explicit labels prevent confusion.

### 9. Prioritize Critical Instructions
- **System Instruction or top of prompt:** Place essential behavioral constraints, role definitions (persona), and output format requirements at the beginning.
- **Example:**
  ```
  <role>
  You are a strict code reviewer. You reject code with any security vulnerabilities.
  </role>

  <constraints>
  - Flag all SQL injection risks
  - Flag all XSS vulnerabilities
  - Reject code with hardcoded credentials
  </constraints>

  <task>
  Review this Python Flask API code: [code]
  </task>
  ```

### 10. Define Ambiguous Parameters
- **Explain terms:** If your prompt uses domain-specific jargon or ambiguous parameters, define them explicitly.
- **Example:**
  ```
  Task: Calculate the "engagement score" for each user.

  Definition: Engagement score = (comments + likes * 2 + shares * 3) / days_active
  ```

## Enhancing Reasoning and Planning

Gemini 3 has native advanced reasoning, but you can still improve its output for complex tasks by prompting it to plan or self-critique before providing the final response.

### Explicit Planning
Use this for multi-step tasks where you want to see the model's thought process.

```
Before providing the final answer, please:
1. Parse the stated goal into distinct sub-tasks.
2. Check if the input information is complete.
3. Create a structured outline to achieve the goal.
4. Execute each sub-task.
5. Synthesize the results into the final answer.
```

### Self-Critique
Use this to improve quality and alignment with your intent.

```
Before returning your final response, review your generated output against the user's original constraints:
1. Did I answer the user's *intent*, not just their literal words?
2. Is the tone authentic to the requested persona?
3. Did I follow all the specified constraints?
4. Are there any logical inconsistencies or errors?

If you find issues, revise your response before submitting.
```

### When NOT to Use These Techniques
- **Simple tasks:** For straightforward queries (data extraction, formatting, quick lookups), skip the explicit planning. Just state the task.
- **`thinking_level: "low"`:** When using the low setting, avoid explicit reasoning prompts—it defeats the purpose of the fast mode.

## Structured Prompting Examples

### Example 1: Research Task
```
<role>
You are a market research analyst specializing in SaaS.
</role>

<context>
We're launching a new project management tool targeting remote teams of 10-50 people.
</context>

<task>
Identify the top 5 competitors in this space. For each, provide:
1. Key features
2. Pricing (as of 2024-2025)
3. Target audience
4. Unique selling proposition
</task>

<output_format>
Present as a comparison table with columns: [Competitor, Key Features, Pricing, Target Audience, USP]
</output_format>
```

### Example 2: Code Generation
```
<role>
You are a senior Python developer.
</role>

<constraints>
- Use Python 3.11+ syntax
- Include type hints
- Write docstrings for all functions
- Handle edge cases (empty inputs, None values)
- No external libraries
</constraints>

<task>
Write a function to merge two sorted lists into one sorted list.
</task>

<output_format>
Return a single code block with the function and 3 test cases.
</output_format>
```

### Example 3: Document Analysis
```
<context>
[Full text of 10-page legal contract, ~15k tokens]
</context>

<task>
Based on the contract above, identify:
1. All payment terms and deadlines
2. Termination clauses
3. Liability limitations
4. Any unusual or risky provisions
</task>

<output_format>
1. Summary table of payment terms
2. Termination section (verbatim quotes + analysis)
3. Liability section (verbatim quotes + analysis)
4. Risk assessment (bullet points)
</output_format>
```

## Complete Template

This template combines all best practices for Gemini 3. Adapt for your specific use case.

**System Instruction (optional, but recommended for complex workflows):**
```
<role>
You are Gemini 3, a specialized assistant for [Insert Domain, e.g., Data Science, Legal Analysis, Software Engineering].
You are precise, analytical, and direct.
</role>

<instructions>
1. **Analyze**: Parse the user's task and context.
2. **Plan**: For complex tasks, create a step-by-step plan.
3. **Execute**: Carry out the plan or task.
4. **Validate**: Review your output against the user's requirements.
5. **Format**: Present the final answer in the requested structure.
</instructions>

<constraints>
- Verbosity: [Low/Medium/High - specify based on your needs]
- Tone: [Formal/Casual/Technical]
- Cite sources: [Yes/No]
</constraints>

<output_format>
Structure your response as follows:
1. **Executive Summary**: [Short overview]
2. **Detailed Response**: [The main content]
3. **References**: [If applicable]
</output_format>
```

**User Prompt:**
```
<context>
[Insert relevant documents, code snippets, data, or background info here]
</context>

<task>
[Insert specific user request here]
</task>

<final_instruction>
[Optional: Add any last-minute clarifications or constraints]
</final_instruction>
```

## Key Capabilities
- **1M Context Window:** Process entire codebases, multiple research papers, or long documents in a single prompt.
- **64k Output Limit:** Generate comprehensive reports, full application code, or detailed analyses.
- **Multimodal:** Native support for text, images, audio, and video as equal-class inputs.
- **Advanced Reasoning:** Native deep thinking without requiring complex Chain-of-Thought prompts from Gemini 2.x era.
- **`thinking_level` Control:** Adjust reasoning depth for latency/cost optimization.
- **Knowledge Cutoff:** January 2025.

## Critical Limitations
- **Temperature Sensitivity:** Calibrated for `temperature = 1.0`. Deviating can degrade performance.
- **Directness Required:** Performs worse with overly conversational or persuasive language. Be concise and explicit.
- **Hallucination Risk:** Like all LLMs, Gemini 3 can hallucinate. Always verify critical facts.
- **Multimodal Label Dependency:** Without explicit labels (e.g., "Image 1," "Video 2"), the model may confuse inputs.

## Best Practices Summary
1. **Be direct:** Skip persuasive language. State the task clearly.
2. **Simplify prompts:** Don't over-engineer. Gemini 3 has native reasoning.
3. **Use `thinking_level`:** `"low"` for speed, `"high"` (default) for depth.
4. **Keep temperature at 1.0:** Don't change it unless you have a specific reason.
5. **Structure with XML or Markdown:** Choose one format and be consistent.
6. **Context first, questions last:** For long contexts, provide data before instructions.
7. **Anchor with transitions:** Use "Based on the above..." to bridge context and task.
8. **Label multimodal inputs:** Explicitly reference "Image 1," "Video 2," etc.
9. **Prioritize critical instructions:** Put role, constraints, and output format at the top.
10. **Define ambiguous terms:** Explain any domain-specific jargon or parameters.

## What's New in Gemini 3 (November 2025)
- **Official Release:** Gemini 3.0 Pro officially launched November 2025.
- **`thinking_level` Parameter:** New parameter for controlling reasoning depth (`"low"` vs. `"high"`).
- **Simplified Prompting:** No longer requires complex Chain-of-Thought prompts from Gemini 2.x. Native reasoning is built-in.
- **Directness Optimization:** Performs best with direct, executable instructions rather than conversational language.
- **Temperature Calibration:** Optimized for `temperature = 1.0`. Do not change unless necessary.
- **Multimodal Enhancements:** Better handling of images, audio, and video when explicitly labeled.
- **Knowledge Cutoff:** January 2025 (same as Claude 4.x models).

## Quick Comparison
- **vs. Claude 4.x:** Gemini 3 prefers more direct communication and simpler prompts. Claude 4.x benefits from explicit context/motivation and XML structure. Both have similar reasoning capabilities, but Claude excels at very long documents (200k context) while Gemini 3 maxes out at 1M context (with 64k output).
- **vs. GPT-4:** Gemini 3 is more efficient with direct instructions and has a larger context window. GPT-4 Turbo is often more conversational and flexible with prompt styles.
- **vs. Gemini 2.x:** Gemini 3 requires LESS prompting complexity. Stop using elaborate Chain-of-Thought techniques unless needed for specific edge cases.
