# LLM Writers System

A flexible system for creating autonomous AI writers that compose stories, learn from feedback, and improve over multiple rounds.

## Features

- **Autonomous Writers**: Each writer is a fully autonomous LLM agent with its own personality and style
- **Multi-Provider Support**: Use Anthropic, OpenAI, or easily add new providers (Gemini, Grok, DeepSeek, etc.)
- **Learning & Improvement**: Writers access their past work and feedback to improve
- **Flexible Configuration**: YAML-based configuration with Pydantic validation
- **Tool-Based Architecture**: Writers use tools to access history and submit stories
- **Mock Feedback System**: Built-in placeholder feedback for testing (easy to replace with real feedback)

## Installation

We install this env using uv. You can use other tools as well.

```bash
# Assume that you have pyenv and uv installed.
pyenv local 3.12
uv venv .venv --python 3.12 --seed
source .venv/bin/activate
uv sync --frozen
```

## Quick Start

1. Set your API keys (choose one method):

   **Option A: Using .env file (recommended)**
   ```bash
   cp .env.example .env
   # Edit .env and add your actual API keys
   ```

   **Option B: Export environment variables**
   ```bash
   export ANTHROPIC_API_KEY="your-key"
   export OPENAI_API_KEY="your-key"
   ```

2. Run the example:
```bash
python example.py
```

This will load all writers from `config/writer_configs/` and run them through Round 1.

## Usage

### Basic Usage

```python
from writers import WriterOrchestrator

# Initialize
orchestrator = WriterOrchestrator()

# Load a specific writer
writer = orchestrator.load_writer("writer_001.yaml")

# Run a round
submission = orchestrator.run_round("writer_001", round_num=1)
```

### Running Multiple Writers

```python
# Load all writers
orchestrator.load_all_writers()

# Run a round for everyone
submissions = orchestrator.run_round_for_all(round_num=1)
```

## Project Structure

```
writers/
├── models.py              # Core data models (Pydantic)
├── writer_agent.py        # Writer agent implementation
├── orchestrator.py        # Orchestrator for managing writers
├── llm_apis/              # Multi-provider LLM clients
│   ├── base.py
│   ├── anthropic_client.py
│   ├── openai_client.py
│   └── factory.py
├── tools/                 # Writer tools
│   ├── past_writings.py
│   └── submit_story.py
├── config/
│   └── writer_configs/    # YAML configs for each writer
└── data/
    └── writings/          # JSON storage for histories
```

## Configuration

Writers are configured via YAML files with support for external prompt files:

```yaml
writer_id: "writer_001"
writer_name: "The Chronicler"
llm_provider: "anthropic"
llm_config:
  model: "claude-sonnet-4-20250514"
  temperature: 0.7
  max_tokens: 4096
prompt_file: "prompts/claude_drama_prompt.md"  # Optional: Path to detailed writing guide
system_prompt: |
  You are a creative writer specializing in drama with historical elements.
  Follow the drama writing guide provided to structure your stories.
  Learn from your past performance feedback to refine your craft.
can_see_other_writers: false
```

### Prompt File Support

The `prompt_file` field lets you reference external markdown files with detailed writing guides. This approach:
- **Keeps configs clean** - Complex prompts live in separate files
- **Easy swapping** - Change writing styles by updating the path
- **Reusable prompts** - Multiple writers can share the same guide
- **Version control friendly** - Prompts can be versioned separately

The system combines `prompt_file` content with `system_prompt` to create the complete prompt sent to the LLM.

See `config/writer_configs/` for examples and `prompts/` for available writing guides.

## Experimentation Tools

The system includes powerful tools for mixing and matching different configurations:

**Quick Testing:**
```bash
# Test combinations instantly without creating config files
python quick_test.py minimalist prompts/claude_drama_prompt.md
python quick_test.py dreamweaver prompts/chatgpt5.1_drama_prompt.md --provider openai --temperature 0.9
```

**Batch Generation:**
```bash
# Generate multiple config files for systematic testing
python generate_writer_configs.py --mode subset \
  --personalities minimalist chronicler \
  --prompts prompts/claude_drama_prompt.md \
  --llms anthropic_sonnet openai_gpt4o
```

See [EXPERIMENTS.md](EXPERIMENTS.md) for a complete guide to finding optimal writer configurations.

## Documentation

- [USAGE.md](USAGE.md) - Detailed usage guide and API reference
- [EXPERIMENTS.md](EXPERIMENTS.md) - Guide to mixing and matching configurations
- [example.py](example.py) - Working example script
- [quick_test.py](quick_test.py) - Quick testing tool
- [generate_writer_configs.py](generate_writer_configs.py) - Batch config generation

## Adding New LLM Providers

The system is designed to easily support new providers:

1. Add provider to `LLMProvider` enum in [models.py](models.py)
2. Create client class in `llm_apis/` extending `BaseLLMClient`
3. Register in `LLMClientFactory`

See [USAGE.md](USAGE.md) for detailed instructions.

## Current Features

- ✅ Multi-provider LLM support (Anthropic, OpenAI)
- ✅ Pydantic-backed YAML configurations
- ✅ Writer tools (access history, submit stories)
- ✅ Mock feedback system
- ✅ Writer history persistence
- ✅ Simple orchestrator

## TODO / Future Enhancements

- [ ] Real reader feedback integration (replace mock feedback)
- [ ] Cross-writer visibility (writers can see each other's work)
- [ ] Advanced orchestrator with parallel execution
- [ ] Web interface for monitoring writers
- [ ] Performance analytics and visualization
- [ ] More sophisticated scoring algorithms
- [ ] Support for streaming responses
- [ ] Writer evolution/mutation capabilities

## License

See project root for license information.

