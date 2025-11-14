"""Anthropic API client implementation."""

from typing import Any
import anthropic
from llm_apis.base import BaseLLMClient, Message, ToolDefinition, LLMResponse


class AnthropicClient(BaseLLMClient):
    """Client for Anthropic's Claude API."""

    def __init__(self, model: str, temperature: float = 0.7, max_tokens: int = 4096, api_key: str | None = None, **kwargs):
        super().__init__(model, temperature, max_tokens, **kwargs)
        self.client = anthropic.Anthropic(api_key=api_key)

    def _convert_tools_to_anthropic_format(self, tools: list[ToolDefinition]) -> list[dict[str, Any]]:
        """Convert our tool format to Anthropic's format."""
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.input_schema
            }
            for tool in tools
        ]

    def _convert_messages_to_anthropic_format(self, messages: list[Message]) -> list[dict[str, Any]]:
        """Convert our message format to Anthropic's format."""
        return [
            {
                "role": msg.role,
                "content": msg.content
            }
            for msg in messages
        ]

    def generate(
        self,
        messages: list[Message],
        tools: list[ToolDefinition] | None = None,
        system: str | None = None,
    ) -> LLMResponse:
        """Generate a response using Anthropic's API."""
        kwargs: dict[str, Any] = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "messages": self._convert_messages_to_anthropic_format(messages),
        }

        if system:
            kwargs["system"] = system

        if tools:
            kwargs["tools"] = self._convert_tools_to_anthropic_format(tools)

        # Add any extra params
        kwargs.update(self.extra_params)

        response = self.client.messages.create(**kwargs)

        # Extract content and tool calls
        content = ""
        tool_calls = []

        for block in response.content:
            if block.type == "text":
                content += block.text
            elif block.type == "tool_use":
                tool_calls.append({
                    "id": block.id,
                    "name": block.name,
                    "input": block.input
                })

        return LLMResponse(
            content=content,
            tool_calls=tool_calls,
            raw_response=response
        )

    def generate_stream(
        self,
        messages: list[Message],
        tools: list[ToolDefinition] | None = None,
        system: str | None = None,
    ):
        """Generate a streaming response using Anthropic's API."""
        kwargs: dict[str, Any] = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "messages": self._convert_messages_to_anthropic_format(messages),
        }

        if system:
            kwargs["system"] = system

        if tools:
            kwargs["tools"] = self._convert_tools_to_anthropic_format(tools)

        kwargs.update(self.extra_params)

        with self.client.messages.stream(**kwargs) as stream:
            for chunk in stream:
                yield chunk
