# Interchangeable Writers - Full Integration Guide

## Overview

Baseline writers are now **fully interchangeable** with LLM writers across all scripts. You can use either type seamlessly in:
- `quick_test.py` - Quick testing
- `compare_writers.py` - Side-by-side comparisons
- `example.py` - Basic examples
- `orchestrator.py` - Batch operations

## Usage

### quick_test.py

Test baseline writers just like LLM writers:

```bash
# Baseline writer
python quick_test.py baseline

# Baseline writer, round 5
python quick_test.py baseline --round 5

# LLM writer (for comparison)
python quick_test.py minimalist prompts/claude_drama_prompt.md
```

**Key differences:**
- Baseline: No `prompt_file` argument needed
- Baseline: Returns instantly (no API call)
- Baseline: Same output every time for same round

### compare_writers.py

Compare baseline against LLM writers:

```bash
# Built-in preset comparing baseline vs LLM
python compare_writers.py --preset baseline_vs_llm

# Or create custom comparison
python compare_writers.py --configs my_comparison.json
```

**Example custom config** (`my_comparison.json`):
```json
[
  {
    "name": "Baseline Reference",
    "personality": "baseline"
  },
  {
    "name": "Chronicler",
    "personality": "chronicler",
    "prompt_file": "prompts/claude_drama_prompt.md",
    "provider": "anthropic",
    "temperature": 0.7
  }
]
```

### example.py

The basic example now loads both types automatically:

```bash
python example.py
```

This will:
1. Load all LLM writers from `config/writer_configs/`
2. Load all baseline writers from `config/baseline_writers/`
3. Run Round 1 for all writers
4. Display results with `[Baseline]` or `[LLM]` tags

### orchestrator.py (Programmatic)

Use the orchestrator to mix baseline and LLM writers:

```python
from orchestrator import WriterOrchestrator

orch = WriterOrchestrator(
    config_dir="config/writer_configs",
    baseline_config_dir="config/baseline_writers",
    data_dir="data/writings"
)

# Load both types
orch.load_all_writers(api_key=my_key, load_baselines=True)

# Load only baseline writers
orch.load_all_writers(api_key=None, load_baselines=True)

# Run round for all (baseline + LLM)
submissions = orch.run_round_for_all(round_num=1)

# Results work the same regardless of writer type
for writer_id, submission in submissions.items():
    print(f"{writer_id}: {submission.title}")
```

## Complete API Parity

Both writer types support the same operations:

| Operation | Baseline | LLM | Notes |
|-----------|----------|-----|-------|
| `write_round(n)` | ✅ | ✅ | Returns StorySubmission |
| `get_history()` | ✅ | ✅ | Returns WriterHistory |
| Data storage | ✅ | ✅ | Same JSON format |
| Feedback | ✅ | ✅ | Same mock feedback |
| Orchestrator | ✅ | ✅ | Fully compatible |
| Comparison tools | ✅ | ✅ | Same interface |

## Configuration

### Baseline Writer Config

Minimal YAML config:

```yaml
writer_id: "baseline_001"
writer_name: "Baseline Writer"
type: "baseline"
```

Place in: `config/baseline_writers/`

### LLM Writer Config

Standard YAML config:

```yaml
writer_id: "writer_001"
writer_name: "My Writer"
llm_provider: "anthropic"
llm_config:
  model: "claude-sonnet-4-20250514"
  temperature: 0.7
  max_tokens: 4096
prompt_file: "prompts/claude_drama_prompt.md"
system_prompt: "You are a creative writer..."
```

Place in: `config/writer_configs/`

## Quick Test Commands

```bash
# Test baseline
python quick_test.py baseline
python quick_test.py baseline --round 3

# Test LLM
python quick_test.py minimalist prompts/claude_drama_prompt.md
python quick_test.py minimalist prompts/claude_drama_prompt.md --round 3

# Compare baseline vs LLM
python compare_writers.py --preset baseline_vs_llm

# Run all writers
python example.py
```

## Identification

All scripts now display writer type:

```
Writer: Baseline Writer (ID: baseline_001) [Baseline]
Title: The Pattern
...

Writer: The Chronicler (ID: writer_001) [LLM]
Title: Whispers in the Ruins
...
```

## Performance Characteristics

| Aspect | Baseline | LLM |
|--------|----------|-----|
| Speed | < 1ms | 2-10s |
| Cost | $0.00 | $0.001-0.01 |
| Consistency | 100% | Variable |
| Learning | No | Yes (via feedback) |
| Creativity | Fixed | Variable |
| Stories | 10 | Unlimited |

## Use Cases

### When to Use Baseline Writers

✅ **Benchmarking** - Consistent reference points
✅ **Testing** - Fast integration tests
✅ **Development** - No API costs during dev
✅ **Comparison** - Ground truth for evaluation
✅ **Demos** - Instant results

### When to Use LLM Writers

✅ **Production** - Generate novel content
✅ **Research** - Study learning behavior
✅ **Experimentation** - Test different approaches
✅ **Scaling** - Need more than 10 rounds
✅ **Variation** - Want different stories each time

## Mixed Workflows

### Example: Development → Production

```bash
# Development: Test with baseline (fast, free)
python quick_test.py baseline --round 1

# Verify: Compare baseline vs your LLM config
python compare_writers.py --preset baseline_vs_llm

# Production: Run with LLM writers
python example.py
```

### Example: Benchmarking LLM Performance

```python
from orchestrator import WriterOrchestrator

orch = WriterOrchestrator()
orch.load_all_writers(api_key=key, load_baselines=True)

# Run 10 rounds
for round_num in range(1, 11):
    submissions = orch.run_round_for_all(round_num)

    # Compare LLM writers against baseline for this round
    baseline_sub = submissions["baseline_001"]
    llm_sub = submissions["writer_001"]

    print(f"Round {round_num}:")
    print(f"  Baseline: {baseline_sub.title}")
    print(f"  LLM: {llm_sub.title}")
```

## Advanced: Programmatic Selection

```python
from writer_agent import WriterAgent
from baseline_writer import BaselineWriter
from baseline_writer import BaselineWriter

def create_writer(writer_type: str, **kwargs):
    """Factory function to create either type."""
    if writer_type == "baseline":
        return BaselineWriter(
            writer_id=kwargs["writer_id"],
            writer_name=kwargs["writer_name"],
            data_dir=kwargs.get("data_dir", "data/writings")
        )
    else:  # LLM
        config = WriterConfig(**kwargs)
        return WriterAgent(
            config=config,
            api_key=kwargs["api_key"],
            data_dir=kwargs.get("data_dir", "data/writings")
        )

# Use the same interface
writer = create_writer("baseline", writer_id="test", writer_name="Test")
submission = writer.write_round(1)
```

## Type Checking

To check writer type at runtime:

```python
from baseline_writer import BaselineWriter

writer = orch.get_writer("some_id")

if isinstance(writer, BaselineWriter):
    print("This is a baseline writer")
    print(f"Has {len(writer.BASELINE_STORIES)} hardcoded stories")
else:
    print("This is an LLM writer")
    print(f"Uses {writer.config.llm_provider.value}")
```

## Benefits of Interchangeable Design

1. **Development Speed** - Test with baseline during development
2. **Cost Savings** - No API costs for testing
3. **Consistent Benchmarks** - Baseline provides stable reference
4. **Easy Comparison** - Direct side-by-side evaluation
5. **Flexible Workflows** - Mix and match as needed
6. **Simple Migration** - Easy to switch between types
7. **Testing** - Baseline for integration tests, LLM for e2e

## Limitations

### Baseline Writers
- ❌ Limited to 10 rounds (then empty templates)
- ❌ No learning from feedback
- ❌ Same story every time
- ❌ Cannot generate novel content

### LLM Writers
- ❌ Require API keys and costs
- ❌ Slower execution
- ❌ Variable output
- ❌ May fail to follow instructions

## Migration Guide

### From LLM-only to Mixed Setup

1. **Add baseline config:**
   ```bash
   mkdir -p config/baseline_writers
   echo 'writer_id: "baseline_001"
   writer_name: "Baseline"
   type: "baseline"' > config/baseline_writers/baseline_001.yaml
   ```

2. **Update orchestrator calls:**
   ```python
   # Old
   orch.load_all_writers(api_key=key)

   # New
   orch.load_all_writers(api_key=key, load_baselines=True)
   ```

3. **Handle both types:**
   ```python
   from baseline_writer import BaselineWriter

   writer = orch.get_writer(writer_id)
   if isinstance(writer, BaselineWriter):
       writer_name = writer.writer_name
   else:
       writer_name = writer.config.writer_name
   ```

## Troubleshooting

### Baseline writer not loading

```bash
# Check config exists
ls config/baseline_writers/baseline_001.yaml

# Verify orchestrator setting
orch.load_all_writers(load_baselines=True)  # Must be True!
```

### Type errors

```python
# Import both types for isinstance checks
from baseline_writer import BaselineWriter
from writer_agent import WriterAgent

# Check type explicitly
if isinstance(writer, BaselineWriter):
    # Handle baseline-specific logic
    pass
```

### Wrong story returned

Baseline writers cache submissions in data directory. To get fresh baseline:
```bash
# Clear cached data
rm -rf data/test_writings/baseline_*.json

# Or use different writer_id
python quick_test.py baseline --round 1  # Uses writer_id="test_writer"
```

## Summary

Baseline writers are now **first-class citizens** in the writers system:

✅ Same interface as LLM writers
✅ Work in all scripts
✅ Supported by orchestrator
✅ Can be compared directly
✅ Use same data formats
✅ Full API parity

You can now seamlessly switch between baseline and LLM writers depending on your needs - testing, benchmarking, development, or production.
