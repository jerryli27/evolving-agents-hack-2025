# Writing Prompts

This directory contains markdown files with detailed writing guides that can be referenced by writer configurations.

## Available Prompts

### `claude_drama_prompt.md`
**Best for:** Claude models (Anthropic)
**Style:** Comprehensive, step-by-step approach
**Features:**
- 7-step development process
- Extensive decision-making strategies (10 strategies)
- Focus on "What if?" questions and emotional journeys
- Detailed example with "The Last Dinner"
- Target length: 250-500 words

**Use when:** You want structured guidance with multiple decision-making frameworks.

---

### `chatgpt5.1_drama_prompt.md`
**Best for:** GPT models (OpenAI)
**Style:** Framework-based with emotional focus
**Features:**
- Foundation-first approach with constraints
- "North Star Emotion" concept
- Emphasis on confined settings and time frames
- Practical steps from emotion to synopsis
- Clear protagonist development

**Use when:** You want emotion-driven storytelling with practical constraints.

---

### `gpt2.5pro_drama_prompt.md`
**Best for:** Balanced approach across models
**Style:** Structured, pragmatic framework
**Features:**
- Systematic development process
- Focus on practical constraints (duration, resources)
- Clear protagonist and conflict definition
- Template-based structure
- Emphasis on specificity and stakes

**Use when:** You want a straightforward, template-driven approach.

---

## Usage in Writer Configs

Reference these prompts in your YAML configs:

```yaml
writer_id: "writer_001"
writer_name: "My Writer"
llm_provider: "anthropic"
llm_config:
  model: "claude-sonnet-4-20250514"
  temperature: 0.7
  max_tokens: 4096
prompt_file: "prompts/claude_drama_prompt.md"  # Path relative to writers/ directory
system_prompt: |
  You are a creative writer.
  Follow the drama writing guide provided to structure your stories.
```

## Creating Your Own Prompts

1. Create a new `.md` file in this directory
2. Structure your prompt with clear sections and examples
3. Include:
   - Overview of the writing approach
   - Step-by-step instructions
   - Decision-making guidance
   - Examples or templates
   - Key takeaways
4. Reference it in your writer config's `prompt_file` field

## Tips for Effective Prompts

- **Be specific:** Provide concrete examples and templates
- **Structure clearly:** Use headers, lists, and sections
- **Include examples:** Show, don't just tell
- **Provide decision frameworks:** Help the LLM make choices when multiple paths are valid
- **Set constraints:** Word counts, character limits, etc. help focus the output
- **Use markdown formatting:** Bold, italics, lists make prompts easier to parse

## Mixing and Matching

You can:
- Use the same prompt file for multiple writers with different `system_prompt` personalities
- Experiment by swapping prompt files for the same writer
- Combine prompts (manually merge content) for hybrid approaches
- Create writer-specific prompts for unique styles

## Contributing Prompts

When adding new prompts:
1. Use descriptive filenames (e.g., `genre_model_prompt.md`)
2. Document the prompt in this README
3. Include clear examples in the prompt itself
4. Test with at least one writer configuration
