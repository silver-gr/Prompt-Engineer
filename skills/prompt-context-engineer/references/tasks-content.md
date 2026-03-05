# Content Generation Tasks (March 2026)

## Core Guidance

- Specify audience, tone, length, and format upfront
- Provide key points or source material -- don't force an outline
- Let the model structure content (reasoning models organize well)
- Request formatting (headings, bullets) only if needed

## Pattern

```xml
<context>
Audience: [who will read this]
Tone: [formal | conversational | technical | persuasive]
Purpose: [inform | persuade | entertain | instruct]
</context>

<task>
Write a [content type] about [topic].
Key points to cover: [list]
</task>

<constraints>
- Length: [word count or range]
- Format: [blog post | email | report | social media]
- Include: [required elements]
- Avoid: [topics or styles to exclude]
</constraints>
```

## Content Types

### Long-Form (Articles, Reports)
- Provide thesis or central argument
- Specify section structure only if you have a strong preference
- Request citations/sources if factual accuracy matters

### Short-Form (Social, Email, Ads)
- Provide brand voice examples (1 example max)
- Specify platform constraints (character limits, hashtag style)
- Request multiple variants for A/B testing

### Technical Writing
- Specify audience expertise level
- Provide terminology glossary if domain-specific
- Request code examples where relevant

### Creative Writing
- Provide style references or examples
- Specify narrative constraints (POV, tense, setting)
- Use higher temperature for more creative output (Gemini: stay at 1.0)

## "AI Slop" Prevention

To avoid generic, over-polished AI output:
- Provide specific voice examples
- Add constraints: "Write as if explaining to a colleague, not presenting to a board"
- Request imperfect, natural language: "Use conversational tone with personality"
- For Claude: explain WHY the tone matters

## Model Selection for Content

| Task | Best Model |
|------|-----------|
| Long-form, nuanced writing | Opus 4.6 |
| Marketing copy, emails | Sonnet 4.6 / GPT-5.2 |
| Social media, short-form | GPT-5.3 Instant / Haiku 4.5 |
| Multilingual content | Qwen 3.5 |
| SEO content at scale | DeepSeek V3.2 |
