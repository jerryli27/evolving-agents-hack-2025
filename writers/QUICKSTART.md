# Quick Start Guide

## Setup

1. **Activate the virtual environment:**
```bash
# Assume you have cloned the repo.
cd writers/
source .venv/bin/activate
```

2. **Set your API keys:**
```bash
cp .env.example .env
# Edit .env and add your API keys
```

Or export them directly:
```bash
export ANTHROPIC_API_KEY="your-key"
export OPENAI_API_KEY="your-key"
```

## Quick Commands

All commands assume you've activated the virtual environment first: `source .venv/bin/activate`

### Test a Single Configuration

```bash
# Test minimalist with Claude prompt
python quick_test.py minimalist prompts/claude_drama_prompt.md

# Test with different provider
python quick_test.py dreamweaver prompts/chatgpt5.1_drama_prompt.md --provider openai

# Test with different temperature
python quick_test.py chronicler prompts/claude_drama_prompt.md --temperature 0.9
```

### Compare Multiple Configurations

```bash
# Compare personalities
python compare_writers.py --preset personalities

# Compare temperature settings
python compare_writers.py --preset temperature

# Compare prompt files
python compare_writers.py --preset prompts

# Compare providers
python compare_writers.py --preset providers

# Quick 3-way comparison
python compare_writers.py --preset quick
```

Results are saved to `comparison_results/`

### Generate Config Files

```bash
# List all options
python generate_writer_configs.py --mode list

# Generate specific combinations
python generate_writer_configs.py --mode subset \
  --personalities minimalist chronicler \
  --prompts prompts/claude_drama_prompt.md \
  --llms anthropic_sonnet openai_gpt4o \
  --output config/experiments

# Generate ALL 90 combinations (warning: creates many files!)
python generate_writer_configs.py --mode all --output config/all_combinations
```

### Run Example

```bash
# Run the basic example
python example.py
```

This loads all writers from `config/writer_configs/` and runs Round 1.

## Common Workflows

### Explore Different Personalities

```bash
python quick_test.py chronicler prompts/claude_drama_prompt.md
python quick_test.py minimalist prompts/claude_drama_prompt.md
python quick_test.py realist prompts/claude_drama_prompt.md
```

### Find Best Prompt for a Personality

```bash
python compare_writers.py --preset prompts
# Edit the preset in compare_writers.py to use your preferred personality
```

### Test Temperature Impact

```bash
python quick_test.py minimalist prompts/claude_drama_prompt.md --temperature 0.5
python quick_test.py minimalist prompts/claude_drama_prompt.md --temperature 0.7
python quick_test.py minimalist prompts/claude_drama_prompt.md --temperature 0.9
```

### Batch Test Multiple Configs

```bash
# Generate configs
python generate_writer_configs.py --mode subset \
  --personalities minimalist experimenter \
  --prompts prompts/claude_drama_prompt.md \
  --llms anthropic_sonnet anthropic_sonnet_creative \
  --output config/test_batch

# Run them with orchestrator
python -c "
from orchestrator import WriterOrchestrator
orch = WriterOrchestrator(config_dir='config/test_batch')
orch.load_all_writers()
orch.run_round_for_all(round_num=1)
"
```

## Troubleshooting

### Debugging Failed Runs

All LLM interactions are automatically logged to `ignore/transcripts/` for debugging:

```bash
# List all transcripts
python view_transcript.py list

# View latest failed run
python view_transcript.py latest --status failed

# View specific transcript
python view_transcript.py view ignore/transcripts/writer_001/round_1_failed_20251114_123456.json

# View with full content (no truncation)
python view_transcript.py view path/to/transcript.json --full

# Compare multiple runs
python view_transcript.py compare transcript1.json transcript2.json
```

Transcripts include:
- Every iteration's input and output
- All tool calls and their results
- Configuration details
- Why the run failed or succeeded

## File Locations

- **Configurations**: `config/writer_configs/*.yaml`
- **Prompts**: `prompts/*.md`
- **Writer Data**: `data/writings/*.json`
- **Comparison Results**: `ignore/comparison_results/*.md`
- **Generated Configs**: `config/experiments/` (or wherever you specify)
- **Debug Transcripts**: `ignore/transcripts/{writer_id}/*.json`

## Next Steps

- Read [USAGE.md](USAGE.md) for API reference
- Read [ARCHITECTURE.md](ARCHITECTURE.md) for system design details
