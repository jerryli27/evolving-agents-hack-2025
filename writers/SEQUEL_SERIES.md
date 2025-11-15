# Sequel Series Feature

## Overview

Writers can now be configured to write connected story series instead of standalone stories. The system automatically provides sequel-aware prompts that guide writers to maintain continuity and plan narrative arcs across multiple rounds.

## Configuration

### YAML Config

Add these fields to your writer config:

```yaml
writer_id: "writer_001"
writer_name: "My Writer"
# ... other config ...
target_num_rounds: 5          # Number of stories in the planned series
should_write_sequel: true      # Enable sequel mode (false for standalone)
```

**Parameters:**
- `target_num_rounds` (int, default: 5) - How many rounds/stories the writer should plan for
- `should_write_sequel` (bool, default: true) - Whether to write sequels or standalone stories

### Programmatic Usage

```python
from models import WriterConfig, LLMProvider, LLMConfig
from writer_agent import WriterAgent

config = WriterConfig(
    writer_id="test",
    writer_name="My Writer",
    llm_provider=LLMProvider.ANTHROPIC,
    llm_config=LLMConfig(model="claude-sonnet-4-20250514"),
    prompt_file="prompts/claude_drama_prompt.md",
    system_prompt="...",
    target_num_rounds=5,
    should_write_sequel=True
)

writer = WriterAgent(config, api_key=api_key)
```

### Quick Test

```bash
# Sequel mode (default: 5-part series)
python quick_test.py chronicler prompts/claude_drama_prompt.md --round 1

# Custom series length
python quick_test.py chronicler prompts/claude_drama_prompt.md --round 1 --target-rounds 3

# Standalone mode
python quick_test.py chronicler prompts/claude_drama_prompt.md --standalone
```

## How It Works

### Sequel Mode (`should_write_sequel: true`)

The system provides different prompts based on the round number:

#### **Round 1: Series Opening**
```
You are beginning a 5-part story series. This is Round 1 of 5.

IMPORTANT: You are writing the FIRST story in a connected series.
Set up characters, world, and conflicts that will develop across 5 stories.
End with hooks that make readers want to continue the series.
```

#### **Rounds 2-4: Middle Chapters**
```
You are continuing your 5-part story series. This is Round 3 of 5.

IMPORTANT: This is a SEQUEL building on your previous stories.
Continue character arcs, develop ongoing plot threads, and maintain consistency
with established canon. You still have 2 more stories after this one.
```

#### **Round 5: Series Finale**
```
You are writing the FINAL story in your 5-part series. This is Round 5 of 5.

IMPORTANT: This is the CONCLUSION of your story series.
Resolve major plot threads, deliver satisfying character conclusions, and provide
closure while staying true to everything you've established.
```

#### **Round 6+: Bonus Content**
```
You have completed your planned 5-part series. This is Round 6 (BONUS CONTENT).

IMPORTANT: Write additional content that expands the universe. This could be a
spin-off, prequel, sequel, or side story that enriches the world you've built.
```

### Standalone Mode (`should_write_sequel: false`)

```
It's now Round 1. Your task is to write a short story synopsis.

Each story you write is STANDALONE - no need for continuity with previous rounds.
```

## Benefits

### For Writers (LLMs)
- **Clear Context** - Knows position in the series arc
- **Planning Guidance** - Understands how much story is left
- **Consistency Prompts** - Reminded to maintain continuity
- **Closure Guidance** - Knows when to resolve threads

### For Readers
- **Cohesive Narrative** - Stories build on each other
- **Character Development** - Arcs across multiple stories
- **Investment** - Reason to return for next story
- **Satisfying Conclusion** - Proper series finale

### For Experiments
- **Controlled Study** - Compare sequel vs standalone performance
- **Series Dynamics** - Study multi-story narrative development
- **Reader Retention** - Test if sequels increase engagement

## Examples

### 5-Part Drama Series

**Config:**
```yaml
target_num_rounds: 5
should_write_sequel: true
```

**Expected Output:**
- Round 1: Introduce protagonist, setup world, establish conflict
- Round 2: Deepen character relationships, escalate stakes
- Round 3: Major plot twist, raise new questions
- Round 4: Darkest moment, test character resolve
- Round 5: Resolution, character growth, satisfying conclusion

### 3-Part Trilogy

**Config:**
```yaml
target_num_rounds: 3
should_write_sequel: true
```

**Quick Test:**
```bash
# Act 1
python quick_test.py chronicler prompts/claude_drama_prompt.md --round 1 --target-rounds 3

# Act 2
python quick_test.py chronicler prompts/claude_drama_prompt.md --round 2 --target-rounds 3

# Act 3
python quick_test.py chronicler prompts/claude_drama_prompt.md --round 3 --target-rounds 3
```

### Standalone Stories

**Config:**
```yaml
target_num_rounds: 5  # Ignored in standalone mode
should_write_sequel: false
```

**Quick Test:**
```bash
python quick_test.py minimalist prompts/claude_drama_prompt.md --standalone
```

## Use Cases

### Default: 5-Part Sequel Series
```yaml
target_num_rounds: 5
should_write_sequel: true
```

**Why 5 stories?**
- Enough for meaningful character/plot development
- Not too long that readers lose interest
- Allows for classic 3-act structure with setup/conclusion
- Gives flexibility for experimentation

**Narrative Structure:**
1. **Introduction** - Setup world, characters, conflict
2. **Rising Action** - Deepen stakes, develop relationships
3. **Midpoint** - Major revelation or setback
4. **Climax** - Darkest moment, critical choices
5. **Resolution** - Conclude arcs, deliver payoff

### Alternative: Standalone Mode
For comparing sequel performance vs standalone:

```bash
# Run both modes
python quick_test.py chronicler prompts/claude_drama_prompt.md --round 1
python quick_test.py chronicler prompts/claude_drama_prompt.md --round 1 --standalone
```

## Comparison: Sequel vs Standalone

| Aspect | Sequel Series | Standalone |
|--------|---------------|------------|
| Continuity | Required | Not expected |
| Character Development | Across multiple stories | Within single story |
| Plot Complexity | Can be more complex | Must be self-contained |
| Reader Investment | Building over time | Per-story basis |
| Writer Flexibility | Constrained by canon | Full freedom each round |
| Market Appeal | Serialization audience | Anthology audience |

## Integration with Past Writings Tool

Writers can review their previous stories to maintain continuity:

```python
# Writer sees their previous stories
past_writings = writer.past_writings_tool.get_past_writings(writer_id)

# In sequel mode, prompt encourages this:
# "1. (Optional) Review your past writings to learn from feedback"

# Writer can then reference:
# - Character names and traits
# - Plot threads from previous stories
# - World-building details
# - Feedback on what readers liked
```

## Testing Sequel Functionality

```bash
# Test all phases of a 5-part series
for i in {1..5}; do
  python quick_test.py chronicler prompts/claude_drama_prompt.md --round $i
done

# Test bonus content
python quick_test.py chronicler prompts/claude_drama_prompt.md --round 6

# Test standalone
python quick_test.py chronicler prompts/claude_drama_prompt.md --round 1 --standalone
```

## Migration Guide

### Updating Existing Configs

All existing configs have been updated with defaults:
```yaml
target_num_rounds: 5
should_write_sequel: true
```

**No changes needed** - existing writers will automatically use sequel mode.

**To opt-out** (use standalone mode):
```yaml
should_write_sequel: false
```

### Backward Compatibility

✅ **Fully backward compatible**
- Existing configs work with defaults
- Existing data/histories unchanged
- API unchanged (new fields optional)
- System prompt format preserved

## Advanced Usage

### Dynamic Series Length

```python
# Adjust series length based on performance
if avg_feedback_score > 0.8:
    config.target_num_rounds = 7  # Extend successful series
else:
    config.target_num_rounds = 3  # Shorten struggling series
```

### Mixed Mode

```python
# First 3 rounds: sequel series
config.should_write_sequel = True
for round in range(1, 4):
    writer.write_round(round)

# Switch to standalone for variety
config.should_write_sequel = False
writer.write_round(4)
```

### Custom Target per Round

```python
# Start ambitious
config.target_num_rounds = 10
writer.write_round(1)

# Adjust based on feedback
if poor_performance:
    config.target_num_rounds = 5  # Trim to conclusion
```

## Future Enhancements

Potential additions to sequel system:

1. **Recap Tool** - Automatic summary of previous stories
2. **Consistency Checker** - Flag contradictions with past canon
3. **Arc Templates** - Pre-defined narrative structures (3-act, hero's journey)
4. **Branching** - Multiple storylines within series
5. **Shared Universe** - Multiple writers in same world

## Troubleshooting

### Writer ignores continuity

**Solution:** Emphasize past writings tool:
```yaml
system_prompt: |
  CRITICAL: This is a sequel series. You MUST review your past writings
  to maintain consistency with characters, plot, and world-building.
```

### Series feels repetitive

**Solution:** Adjust arc distribution:
```yaml
target_num_rounds: 3  # Tighter, more focused arc
```

### Unclear series position

**Check config:**
```python
print(f"Round {round_num} of {config.target_num_rounds}")
print(f"Sequel mode: {config.should_write_sequel}")
```

## Summary

The sequel series feature enables:

✅ **Connected narratives** across multiple rounds
✅ **Configurable series length** (default: 5 stories)
✅ **Automatic sequel-aware prompts** for each phase
✅ **Standalone mode** for comparison
✅ **Full backward compatibility**

Writers now understand whether they're:
- Starting a series (setup)
- Continuing a series (development)
- Concluding a series (resolution)
- Adding bonus content (expansion)
- Writing standalone stories (independent)

This creates more cohesive, engaging narratives that encourage reader investment across multiple stories.
