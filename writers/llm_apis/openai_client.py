"""OpenAI API client implementation."""

from typing import Any
import openai
from llm_apis.base import BaseLLMClient, Message, ToolDefinition, LLMResponse


class OpenAIClient(BaseLLMClient):
    """Client for OpenAI's API."""

    def __init__(self, model: str, temperature: float = 0.7, max_tokens: int = 4096, api_key: str | None = None, **kwargs):
        super().__init__(model, temperature, max_tokens, **kwargs)
        self.client = openai.OpenAI(api_key=api_key)

    def _convert_tools_to_openai_format(self, tools: list[ToolDefinition]) -> list[dict[str, Any]]:
        """Convert our tool format to OpenAI's format."""
        return [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.input_schema
                }
            }
            for tool in tools
        ]

    def _convert_messages_to_openai_format(self, messages: list[Message], system: str | None = None) -> list[dict[str, Any]]:
        """Convert our message format to OpenAI's format."""
        openai_messages = []

        # OpenAI includes system message as first message
        if system:
            openai_messages.append({
                "role": "system",
                "content": system
            })

        for msg in messages:
            openai_messages.append({
                "role": msg.role,
                "content": msg.content
            })

        return openai_messages

    def generate(
        self,
        messages: list[Message],
        tools: list[ToolDefinition] | None = None,
        system: str | None = None,
    ) -> LLMResponse:
        """Generate a response using OpenAI's API."""
        kwargs: dict[str, Any] = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "messages": self._convert_messages_to_openai_format(messages, system),
        }

        if tools:
            kwargs["tools"] = self._convert_tools_to_openai_format(tools)

        # Add any extra params
        kwargs.update(self.extra_params)

        response = self.client.chat.completions.create(**kwargs)

        # Extract content and tool calls
        message = response.choices[0].message
        content = message.content or ""
        tool_calls = []

        if message.tool_calls:
            for tc in message.tool_calls:
                tool_calls.append({
                    "id": tc.id,
                    "name": tc.function.name,
                    "input": tc.function.arguments  # Note: OpenAI returns JSON string
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
        """Generate a streaming response using OpenAI's API."""
        kwargs: dict[str, Any] = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "messages": self._convert_messages_to_openai_format(messages, system),
            "stream": True,
        }

        if tools:
            kwargs["tools"] = self._convert_tools_to_openai_format(tools)

        kwargs.update(self.extra_params)

        stream = self.client.chat.completions.create(**kwargs)
        for chunk in stream:
            yield chunk
