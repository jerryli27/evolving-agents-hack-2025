# LLM Writers System - Architecture

## Overview

The LLM Writers System is designed as a modular, extensible framework for autonomous AI writers. Each component is loosely coupled and can be extended or replaced independently.

## Core Components

### 1. Data Models (`models.py`)

**Purpose**: Define all data structures using Pydantic for validation and serialization.

**Key Models**:
- `LLMProvider` - Enum of supported providers
- `LLMConfig` - LLM configuration (model, temperature, etc.)
- `WriterConfig` - Complete writer configuration
- `StorySubmission` - Format for story submissions
- `FeedbackResponse` - Feedback structure
- `PastWriting` - Historical writing with feedback
- `WriterHistory` - Complete writer history

**Design Decisions**:
- Pydantic for validation and YAML serialization
- Datetime tracking for all submissions
- Extensible feedback structure for future enhancements

### 2. LLM API Layer (`llm_apis/`)

**Purpose**: Provide a unified interface for multiple LLM providers.

**Components**:
- `base.py` - Abstract base class defining the interface
- `anthropic_client.py` - Anthropic API implementation
- `openai_client.py` - OpenAI API implementation
- `factory.py` - Factory pattern for creating clients

**Key Design**:
```python
class BaseLLMClient:
    def generate(messages, tools, system) -> LLMResponse
    def generate_stream(messages, tools, system) -> Iterator
```

**Standardization**:
- Common `Message` format
- Common `ToolDefinition` format
- Common `LLMResponse` format
- Each provider client converts to/from their native format

**Adding Providers**:
1. Implement `BaseLLMClient`
2. Convert provider-specific formats to/from common format
3. Register in factory

### 3. Tools (`tools/`)

**Purpose**: Provide capabilities to writer agents.

**Tools**:
1. **PastWritingsTool** (`past_writings.py`)
   - Loads writer history from JSON
   - Returns formatted past performance
   - Supports filtering (e.g., last N rounds)
   - Future: cross-writer visibility

2. **SubmitStoryTool** (`submit_story.py`)
   - Accepts story submission
   - Generates feedback (currently mock)
   - Saves to writer history
   - Returns formatted feedback

**Tool Interface**:
```python
@staticmethod
def get_tool_definition() -> dict:
    """Returns OpenAI/Anthropic-compatible tool schema"""
```

**Data Storage**:
- JSON files in `data/writings/{writer_id}.json`
- Pydantic models ensure consistency
- Easy to query and modify

### 4. Writer Agent (`writer_agent.py`)

**Purpose**: The autonomous writer agent that orchestrates the writing process.

**Key Methods**:
- `from_yaml()` - Load from config file
- `write_round()` - Execute a writing round
- `get_history()` - Access writer history

**Agent Loop**:
```
1. Send initial prompt to LLM with tools
2. LLM responds (content + optional tool calls)
3. Execute tool calls
4. Send tool results back to LLM
5. Repeat until story is submitted
6. Max iterations to prevent infinite loops
```

**Conversation Management**:
- Maintains conversation history
- Handles tool call/result cycle
- Enforces submission completion

### 5. Orchestrator (`orchestrator.py`)

**Purpose**: Manage multiple writers and coordinate rounds.

**Capabilities**:
- Load writers from YAML configs
- Run individual rounds
- Run rounds for all writers
- Access writer histories

**Current Design**: Simple, synchronous
**Future**: Could support parallel execution, scheduling, etc.

## Data Flow

### Writing Round Flow

```
1. Orchestrator.run_round(writer_id, round_num)
   ↓
2. WriterAgent.write_round(round_num)
   ↓
3. LLM generates response with tools
   ↓
4. Agent executes tools:
   - get_past_writings → PastWritingsTool
   - submit_story → SubmitStoryTool
   ↓
5. SubmitStoryTool:
   - Creates StorySubmission
   - Generates FeedbackResponse (mock)
   - Saves to WriterHistory
   ↓
6. Returns submission to orchestrator
```

### Tool Execution Flow

```
Writer Agent
    ↓
LLM Client (with tools)
    ↓
LLM Response (tool calls)
    ↓
Agent executes tool
    ↓
Tool accesses/modifies data
    ↓
Tool returns result
    ↓
Result sent back to LLM
```

## Storage Architecture

### Configuration Storage
```
config/writer_configs/
├── writer_001.yaml
├── writer_002.yaml
└── writer_003.yaml
```

**Format**: YAML (Pydantic-backed)
**Contains**: WriterConfig data

### Data Storage
```
data/writings/
├── writer_001.json
├── writer_002.json
└── writer_003.json
```

**Format**: JSON (Pydantic-backed)
**Contains**: WriterHistory data

**Structure**:
```json
{
  "writer_id": "writer_001",
  "writer_name": "The Chronicler",
  "writings": [
    {
      "submission": { ... },
      "feedback": { ... }
    }
  ]
}
```

## Extension Points

### 1. Adding New LLM Providers

**Files to modify**:
1. `models.py` - Add to `LLMProvider` enum
2. Create `llm_apis/{provider}_client.py`
3. `llm_apis/factory.py` - Add to factory

**Example**: Adding Gemini
```python
# models.py
class LLMProvider(str, Enum):
    GEMINI = "gemini"

# llm_apis/gemini_client.py
class GeminiClient(BaseLLMClient):
    def generate(self, messages, tools, system):
        # Implement Gemini-specific logic
        pass

# llm_apis/factory.py
elif provider == LLMProvider.GEMINI:
    return GeminiClient(**kwargs)
```

### 2. Adding New Tools

**Steps**:
1. Create tool class in `tools/`
2. Implement `get_tool_definition()`
3. Add to `WriterAgent._get_tools()`
4. Add handler in `WriterAgent._handle_tool_call()`

**Example**: Price optimization tool
```python
class PriceOptimizationTool:
    @staticmethod
    def get_tool_definition():
        return {
            "name": "optimize_price",
            "description": "Suggest optimal price based on past performance",
            "input_schema": { ... }
        }

    def suggest_price(self, writer_id: str) -> float:
        # Analyze history and suggest price
        pass
```

### 3. Real Feedback Integration

**Replace**: `SubmitStoryTool._generate_mock_feedback()`

**With**: Call to actual feedback service
```python
def _get_real_feedback(self, submission: StorySubmission) -> FeedbackResponse:
    # Call feedback service API
    # Parse and return FeedbackResponse
    pass
```

### 4. Cross-Writer Visibility

**Modify**: `PastWritingsTool.get_past_writings()`

**Add**: Logic to load other writers' histories when `include_other_writers=True`
```python
if include_other_writers:
    other_histories = self._load_all_histories()
    # Format and include
```

## Design Principles

1. **Separation of Concerns**
   - LLM API abstraction separate from business logic
   - Tools are self-contained
   - Data models independent

2. **Extensibility**
   - Easy to add new providers
   - Easy to add new tools
   - Factory pattern for client creation

3. **Testability**
   - Mock feedback for testing without external services
   - Each component can be tested independently
   - Clear interfaces

4. **Type Safety**
   - Pydantic for runtime validation
   - Type hints throughout
   - Enum for constrained choices

5. **Data Persistence**
   - Human-readable formats (YAML, JSON)
   - Easy to inspect and modify
   - Git-friendly

## Future Architecture Considerations

### Parallel Execution
```python
async def run_round_parallel(self, round_num: int):
    tasks = [writer.write_round(round_num) for writer in self.writers.values()]
    return await asyncio.gather(*tasks)
```

### Event-Driven Architecture
```python
class WriterEventBus:
    def on_submission(self, submission: StorySubmission):
        # Trigger feedback generation
        # Notify analytics
        # Update leaderboards
```

### Caching Layer
```python
class CachedLLMClient(BaseLLMClient):
    def generate(self, messages, tools, system):
        cache_key = hash((messages, tools, system))
        if cached := self.cache.get(cache_key):
            return cached
        # ... generate and cache
```

### Database Backend
Replace JSON files with SQLite/PostgreSQL for:
- Better querying capabilities
- Concurrent access
- Relationships between writers
- Analytics queries

## Security Considerations

1. **API Keys**: Never commit API keys, use environment variables
2. **Input Validation**: Pydantic validates all inputs
3. **File Paths**: Use Path objects to prevent path traversal
4. **Rate Limiting**: Consider adding rate limits for LLM calls
5. **Cost Control**: Max iterations prevents runaway costs

## Performance Considerations

1. **LLM Calls**: Most expensive operation
   - Cache when possible
   - Use appropriate models (don't use GPT-4 for simple tasks)

2. **File I/O**: Minimal impact
   - JSON files are small
   - Could optimize with streaming for large histories

3. **Parallelization**:
   - Current: Sequential execution
   - Future: Parallel writer execution with asyncio

## Conclusion

The architecture is designed to be:
- **Simple** to understand and use
- **Flexible** for different use cases
- **Extensible** for new features
- **Maintainable** with clear separation of concerns

The modular design allows each component to evolve independently while maintaining backward compatibility.
