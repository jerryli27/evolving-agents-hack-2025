# End-to-End Simulation Guide

## Overview

`end_to_end_v0.1.py` runs a complete writing competition with multiple writers over multiple rounds.

## Quick Start

### Prep work

First install the env.

```bash
# Assume that you have pyenv and uv installed.
pyenv local 3.12
uv venv .venv --python 3.12 --seed
source .venv/bin/activate
uv sync --frozen
```

Then do `cp .env.example .env` and modify that file to include your API keys.

### Run it in mock mode

To make sure that installation works correctly. You can also do one-sided mocks with `--mock-writers` or `--mock-readers` for debugging.

```bash
# Both writers and readers mocked (< 1 minute)
# --mock defaults to 5 baseline writers + mock feedback
source writers/.venv/bin/activate
python end_to_end_v0.1.py --mock
```

### Compare three prompt settings.
```bash
# Make sure all test configs exist
ls writers/config/writer_configs/writer_*test.yaml

# Launch all three tests in parallel
writers/.venv/bin/python end_to_end_v0.1.py --rounds 3 --data-dir data/claude_framework_run1 --writers writer_claude_test.yaml > logs/claude_final.log 2>&1 &

writers/.venv/bin/python end_to_end_v0.1.py --rounds 3 --data-dir data/gemini_framework_run1 --writers writer_gemini_test.yaml > logs/gemini_final.log 2>&1 &

writers/.venv/bin/python end_to_end_v0.1.py --rounds 3 --data-dir data/chatgpt_framework_run1 --writers writer_chatgpt_test.yaml > logs/chatgpt_final.log 2>&1 &

# Check they're running
ps aux | grep "end_to_end.*yaml" | grep -v grep

# Monitor progress (wait a bit for output to flush)
sleep 20
tail -20 logs/claude_final.log
tail -20 logs/gemini_final.log
tail -20 logs/chatgpt_final.log

# Check when they complete
ps aux | grep "end_to_end.*yaml" | grep -v grep  # Empty means done

# View results
ls -lh data/claude_framework_run1/
ls -lh data/gemini_framework_run1/
ls -lh data/chatgpt_framework_run1/

```

### Full Real LLM Mode

```bash
# 4 LLM writers, 5 rounds, real ReaderMarket feedback (~2-3 hours)
python end_to_end_v0.1.py --llm 4 --rounds 5
```

## How It Works

### Round Structure

Each round follows this pattern:

1. **Writing Phase (Parallel)**
   - All writers execute simultaneously
   - Each writer generates/submits a story
   - Writers are independent - no waiting

2. **Synchronization Point**
   - Wait for all writers to complete
   - All stories are submitted
   - Feedback is collected

3. **Feedback Phase**
   - ReaderMarket evaluates all submissions
   - OR mock feedback is generated instantly
   - Feedback is saved to writer histories

4. **Next Round**
   - Writers can access previous round feedback
   - Process repeats

### Saved Data

All data is saved to the data directory:

```
data/end_to_end_v0.1/
├── writer_001.json     # Complete history with feedback
├── writer_002.json
├── writer_003.json
└── baseline_001.json
```

## Advanced Usage

### Custom Writer Selection

```bash
# Use specific writer configs
python end_to_end_v0.1.py --mock \
  --writers writer_001.yaml writer_002.yaml writer_003.yaml
```

### Custom Data Directory

```bash
# Save to different location
python end_to_end_v0.1.py --mock --llm 4 \
  --data-dir data/experiment_001
```

### Help

```bash
python end_to_end_v0.1.py --help
```
