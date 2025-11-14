"""Base interface for LLM API clients."""

from abc import ABC, abstractmethod
from typing import Any


class Message(dict):
    """Standard message format across all providers."""

    def __init__(self, role: str, content: str):
        super().__init__(role=role, content=content)
        self.role = role
        self.content = content


class ToolDefinition(dict):
    """Standard tool definition format."""

    def __init__(self, name: str, description: str, input_schema: dict[str, Any]):
        super().__init__(name=name, description=description, input_schema=input_schema)
        self.name = name
        self.description = description
        self.input_schema = input_schema


class LLMResponse:
    """Standard response format from LLM."""

    def __init__(
        self,
        content: str,
        tool_calls: list[dict[str, Any]] | None = None,
        raw_response: Any | None = None
    ):
        self.content = content
        self.tool_calls = tool_calls or []
        self.raw_response = raw_response

    def has_tool_calls(self) -> bool:
        """Check if response includes tool calls."""
        return len(self.tool_calls) > 0


class BaseLLMClient(ABC):
    """Abstract base class for LLM API clients."""

    def __init__(self, model: str, temperature: float = 0.7, max_tokens: int = 4096, **kwargs):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.extra_params = kwargs

    @abstractmethod
    def generate(
        self,
        messages: list[Message],
        tools: list[ToolDefinition] | None = None,
        system: str | None = None,
    ) -> LLMResponse:
        """
        Generate a response from the LLM.

        Args:
            messages: List of conversation messages
            tools: Optional list of tool definitions the LLM can use
            system: Optional system prompt

        Returns:
            LLMResponse with content and optional tool calls
        """
        pass

    @abstractmethod
    def generate_stream(
        self,
        messages: list[Message],
        tools: list[ToolDefinition] | None = None,
        system: str | None = None,
    ):
        """
        Generate a streaming response from the LLM.

        Args:
            messages: List of conversation messages
            tools: Optional list of tool definitions
            system: Optional system prompt

        Yields:
            Chunks of the response as they arrive
        """
        pass
