# Baseline Writers

Baseline writers are non-LLM based writers with hardcoded story submissions. They serve as benchmarks for evaluating LLM-generated stories by providing consistent, high-quality reference points based on real fictional works.

## Overview

- **Purpose**: Provide baseline performance metrics for comparison with LLM writers
- **Implementation**: Hardcoded submissions (no API calls, instant execution)
- **Story Count**: 10 pre-written plot synopses per writer
- **Source Material**: Plot synopses based on quality fictional works, not too well-known to avoid immediate recognition

## Story Sources

The baseline stories are adapted from classic and contemporary short fiction:

1. **Round 1 - "The Pattern"**: Inspired by "The Yellow Wallpaper" by Charlotte Perkins Gilman
   - A woman's psychological descent while confined for rest cure

2. **Round 2 - "The Cost of Paradise"**: Inspired by "The Ones Who Walk Away from Omelas" by Ursula K. Le Guin
   - Utopian society built on the suffering of one child

3. **Round 3 - "The Drawing"**: Inspired by "The Lottery" by Shirley Jackson
   - Small town tradition with dark consequences

4. **Round 4 - "The Change"**: Inspired by "The Metamorphosis" by Franz Kafka
   - Man transforms and family's true nature is revealed

5. **Round 5 - "The Sound"**: Inspired by "The Tell-Tale Heart" by Edgar Allan Poe
   - Perfect crime unravels through guilt

6. **Round 6 - "By the Sea"**: Inspired by "The Lady with the Dog" by Anton Chekhov
   - Brief affair evolves into transformative love

7. **Round 7 - "I Would Prefer Not To"**: Inspired by "Bartleby, the Scrivener" by Herman Melville
   - Passive resistance consumes everyone around

8. **Round 8 - "The Journey Home"**: Inspired by "The Swimmer" by John Cheever
   - Surreal journey reveals life has fallen apart

9. **Round 9 - "Everything Dies"**: Inspired by "The School" by Donald Barthelme
   - Series of deaths leads to existential questions

10. **Round 10 - "The Good Neighbor"**: Inspired by "The Housebreaker of Shady Hill" by John Cheever
    - Suburban father's descent into crime

## Usage

### Direct Instantiation

```python
from baseline_writer import BaselineWriter

writer = BaselineWriter(
    writer_id="baseline_001",
    writer_name="Baseline Writer 1",
    data_dir="data/writings"
)

# Run a round
submission = writer.write_round(1)
print(f"Title: {submission.title}")
print(f"Story: {submission.full_story}")
```

### From YAML Config

Create a config file in `config/baseline_writers/`:

```yaml
writer_id: "baseline_001"
writer_name: "Baseline Writer 1"
type: "baseline"
```

Load with orchestrator:

```python
from orchestrator import WriterOrchestrator

orch = WriterOrchestrator(
    baseline_config_dir="config/baseline_writers",
    data_dir="data/writings"
)

# Load all writers (including baselines)
orch.load_all_writers(load_baselines=True)

# Run rounds
submission = orch.run_round("baseline_001", 1)
```

### Test Script

Run the provided test script to verify baseline writer functionality:

```bash
python test_baseline.py
```

This tests:
- Direct baseline writer instantiation
- Multiple round execution (rounds 1, 5, 11)
- Orchestrator integration
- Empty template for rounds > 10

## Behavior

### Rounds 1-10
Returns the corresponding hardcoded story from `BASELINE_STORIES` with:
- Title
- Short summary
- Full story text (250-500 words)
- Price ($1.00)

### Rounds 11+
Returns an empty template:
```python
{
    "title": "Round {n} - No Story",
    "short_summary": "",
    "full_story": "",
    "price": 1.0
}
```

## Integration with Existing System

Baseline writers integrate seamlessly with the existing infrastructure:

- **Data Storage**: Uses same JSON format as LLM writers
- **Feedback System**: Receives same mock feedback as LLM writers
- **History Tracking**: Past writings stored in `data/writings/{writer_id}.json`
- **Orchestrator**: Can be mixed with LLM writers in same run
- **Tools**: Uses same `SubmitStoryTool` and `PastWritingsTool`

## Comparison Use Cases

### Performance Benchmarking
Compare LLM-generated stories against baseline:
```python
# Run same round for both types
llm_submission = orch.run_round("writer_001", 1)
baseline_submission = orch.run_round("baseline_001", 1)

# Compare feedback scores
# (when real feedback system is implemented)
```

### Consistency Testing
Baselines provide consistent reference points across runs:
- Same story every time for same round
- No temperature/randomness variation
- Predictable output for system testing

### Quality Calibration
Use baseline scores to calibrate feedback system:
- Known-quality stories provide ground truth
- Help establish scoring thresholds
- Validate feedback mechanisms

## Creating Additional Baseline Writers

To add more baseline writers:

1. **Add stories to `BaselineWriter.BASELINE_STORIES`**:
   - Maintain 10 stories per writer
   - Source from quality fiction
   - Adapt to drama synopsis format
   - 250-500 words per story

2. **Create config file**:
   ```yaml
   writer_id: "baseline_002"
   writer_name: "Baseline Writer 2"
   type: "baseline"
   ```

3. **OR create separate class** (for different story sets):
   ```python
   class BaselineWriter2(BaselineWriter):
       BASELINE_STORIES = [
           # Different set of 10 stories
       ]
   ```

## File Locations

- **Implementation**: `baseline_writer.py`
- **Configs**: `config/baseline_writers/*.yaml`
- **Test Script**: `test_baseline.py`
- **Data**: `data/writings/baseline_*.json`

## API Reference

### BaselineWriter Class

```python
class BaselineWriter:
    def __init__(
        self,
        writer_id: str,
        writer_name: str,
        data_dir: str = "data/writings"
    )

    @classmethod
    def from_yaml(
        cls,
        config_path: str,
        data_dir: str = "data/writings"
    ) -> "BaselineWriter"

    def write_round(self, round_num: int) -> StorySubmission

    def get_history(self) -> Optional[WriterHistory]
```

### Orchestrator Updates

```python
class WriterOrchestrator:
    def __init__(
        self,
        config_dir: str = "config/writer_configs",
        data_dir: str = "data/writings",
        baseline_config_dir: str = "config/baseline_writers"  # NEW
    )

    def load_writer(
        self,
        config_filename: str,
        api_key: Optional[str] = None,
        is_baseline: bool = False  # NEW
    ) -> Union[WriterAgent, BaselineWriter]

    def load_all_writers(
        self,
        api_key: Optional[str] = None,
        load_baselines: bool = True  # NEW
    )
```

## Advantages

✅ **No API Costs**: No LLM calls = no per-run costs
✅ **Instant Execution**: Hardcoded stories return immediately
✅ **Consistent Output**: Same story every time for reproducibility
✅ **Quality Reference**: Based on proven literary works
✅ **System Testing**: Reliable for integration tests
✅ **Benchmarking**: Ground truth for comparison

## Limitations

❌ **No Learning**: Cannot improve from feedback
❌ **Limited Rounds**: Only 10 hardcoded stories
❌ **No Variation**: Same output regardless of past performance
❌ **No Creativity**: Cannot generate novel combinations

## Future Enhancements

Potential improvements to baseline writers:

1. **Multiple Story Sets**: Create variations (e.g., baseline_scifi_001, baseline_mystery_001)
2. **Parameterized Stories**: Add variables that change based on round or feedback
3. **Hybrid Approach**: Mix hardcoded structure with LLM-generated details
4. **Quality Tiers**: Different baseline writers at different quality levels
5. **Genre-Specific**: Baseline writers for different genres (sci-fi, mystery, romance)

## Questions?

See also:
- [QUICKSTART.md](QUICKSTART.md) - Getting started guide
- [USAGE.md](USAGE.md) - Full API documentation
- [ARCHITECTURE.md](ARCHITECTURE.md) - System design details
