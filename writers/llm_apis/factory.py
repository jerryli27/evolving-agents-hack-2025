"""Factory for creating LLM clients."""

from typing import Any
from models import LLMProvider, LLMConfig
from llm_apis.base import BaseLLMClient
from llm_apis.anthropic_client import AnthropicClient
from llm_apis.openai_client import OpenAIClient


class LLMClientFactory:
    """Factory for creating LLM clients based on provider."""

    @staticmethod
    def create_client(
        provider: LLMProvider,
        config: LLMConfig,
        api_key: str | None = None,
    ) -> BaseLLMClient:
        """
        Create an LLM client for the specified provider.

        Args:
            provider: The LLM provider to use
            config: Configuration for the LLM
            api_key: Optional API key (if not provided, will use env vars)

        Returns:
            An instance of BaseLLMClient for the provider

        Raises:
            ValueError: If provider is not supported
        """
        client_kwargs: dict[str, Any] = {
            "model": config.model,
            "temperature": config.temperature,
            "max_tokens": config.max_tokens,
            "api_key": api_key,
            **config.extra_params,
        }

        if provider == LLMProvider.ANTHROPIC:
            return AnthropicClient(**client_kwargs)
        elif provider == LLMProvider.OPENAI:
            return OpenAIClient(**client_kwargs)
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")

    @staticmethod
    def get_supported_providers() -> list[str]:
        """Get list of supported provider names."""
        return [provider.value for provider in LLMProvider]
