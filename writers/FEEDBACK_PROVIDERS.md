## Feedback Provider System

The writers system supports two types of feedback providers for story evaluation:

### 1. MockFeedbackProvider (Default)

Fast, offline feedback provider that generates random but realistic scores. Perfect for development and testing.

**Features:**
- No external dependencies
- Fast execution (instant feedback)
- Reproducible with seed parameter
- Useful for unit tests and offline development

**Usage:**
```python
from feedback_providers import MockFeedbackProvider
from writer_agent import WriterAgent

# Create provider
feedback_provider = MockFeedbackProvider(seed=42)  # seed optional

# Use with writer
writer = WriterAgent.from_yaml(
    config_path="config/writer_configs/writer_001.yaml",
    api_key=api_key,
    feedback_provider=feedback_provider
)
```

### 2. ReaderMarketFeedbackProvider

LLM-based feedback using generative reader agents with memory. Provides realistic, context-aware feedback.

**Features:**
- Uses `ReaderMarket` class with generative agents
- Readers have memory - they remember past stories
- Realistic feedback based on reader personalities and preferences
- Individual reader feedback available
- Memory persists across rounds (timestep tracking)

**Requirements:**
- `genagents` package installed (see `genagents/requirements.txt`)
- Reader agents available at `genagents/agent_bank/populations/gss_agents/`
- `ReaderMarket.py` and `readers_parameters.py` configured

**Usage:**
```python
from feedback_providers import ReaderMarketFeedbackProvider
from writer_agent import WriterAgent

# Create provider (initializes reader agents)
feedback_provider = ReaderMarketFeedbackProvider()

# Use with writer
writer = WriterAgent.from_yaml(
    config_path="config/writer_configs/writer_001.yaml",
    api_key=api_key,
    feedback_provider=feedback_provider
)

# Run multiple rounds - readers will remember previous stories
submission1 = writer.write_round(round_num=1)
submission2 = writer.write_round(round_num=2)  # Readers remember round 1
```

**Important: Memory and Timesteps**

ReaderMarket maintains memory across rounds through timesteps:
- Each story submission increments the timestep
- Reader agents remember stories at specific timesteps
- Future feedback can reference past stories
- Keep the same `ReaderMarketFeedbackProvider` instance across rounds

### Default Behavior

If no feedback provider is specified, the system uses `MockFeedbackProvider` by default:

```python
# These are equivalent:
writer = WriterAgent.from_yaml(config_path="config/writer_configs/writer_001.yaml")
writer = WriterAgent.from_yaml(config_path="config/writer_configs/writer_001.yaml",
                               feedback_provider=MockFeedbackProvider())
```

### Feedback Response Format

Both providers return the same `FeedbackResponse` format:

```python
{
    "sold_percentage": 0.65,           # 0.0-1.0: % of readers who purchased
    "aggregated_total_score": 0.75,    # 0.0-1.0: Overall quality
    "aggregated_novelty_score": 0.80,  # 0.0-1.0: How novel/unexpected
    "aggregated_relevance_score": 0.70, # 0.0-1.0: Personal relevance
    "aggregated_quality_score": 0.75,  # 0.0-1.0: Technical quality
    "aggregated_qualitative_feedback": "Reader feedback summary...",
    "raw_feedback": [...]              # Individual reader responses
}
```

### Examples

**Example 1: Quick test with mock feedback**
```bash
python quick_test.py minimalist prompts/claude_drama_prompt.md
```

**Example 2: Using ReaderMarket feedback**
```bash
python example_with_reader_market.py
```

**Example 3: Testing both providers**
```bash
python test_feedback_providers.py
```

### Custom Feedback Providers

You can create custom feedback providers by extending `FeedbackProvider`:

```python
from feedback_providers.base import FeedbackProvider
from models import FeedbackResponse

class CustomFeedbackProvider(FeedbackProvider):
    def get_feedback(self, title, full_story, short_summary, price,
                    timestep, writer_id, round_num) -> FeedbackResponse:
        # Your custom logic here
        return FeedbackResponse(...)
```

### Performance Comparison

| Provider | Speed | Cost | Realism | Memory |
|----------|-------|------|---------|--------|
| MockFeedbackProvider | Instant | Free | Low | No |
| ReaderMarketFeedbackProvider | ~2-5 min | LLM costs | High | Yes |

### Troubleshooting

**Error: "Failed to initialize ReaderMarket"**
- Ensure `genagents` is installed: `pip install -r genagents/requirements.txt`
- Check reader agents exist at the configured path
- Verify `readers_parameters.py` is properly configured

**Feedback seems random/inconsistent**
- With MockFeedbackProvider: This is expected, use `seed` parameter for reproducibility
- With ReaderMarket: Check that reader agents are properly initialized and have diverse personalities

**Reader memory not working**
- Ensure you're using the same `ReaderMarketFeedbackProvider` instance across rounds
- Verify timesteps are incrementing correctly
- Check that reader agents are persisting between rounds
