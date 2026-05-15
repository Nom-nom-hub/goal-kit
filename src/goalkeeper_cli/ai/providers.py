"""AI Integration Layer for Goal Kit v3.

This module provides the foundation for AI-native workflows in Goal Kit.
It supports multiple AI providers with a unified interface for goal drafting,
strategy exploration, and milestone suggestions.
"""

import os
import json
import ssl
from pathlib import Path
from typing import Optional, Literal, Any
from dataclasses import dataclass, field
from abc import ABC, abstractmethod

import httpx
import truststore

ssl_context = truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)


@dataclass
class AIProvider:
    """Base configuration for an AI provider."""

    name: str
    requires_api_key: bool = True
    supports_streaming: bool = True
    base_url: Optional[str] = None


@dataclass
class AIResponse:
    """Standardized response from AI providers."""

    content: str
    provider: str
    model: Optional[str] = None
    usage: Optional[dict] = None
    raw: Optional[dict] = None
    success: bool = True
    error: Optional[str] = None


@dataclass
class GoalDraft:
    """A drafted goal from natural language."""

    raw_text: str
    suggested_name: str
    primary_outcome: str
    beneficiary: str
    success_metrics: list[str] = field(default_factory=list)
    out_of_scope: list[str] = field(default_factory=list)
    refinement_questions: list[str] = field(default_factory=list)
    confidence: float = 0.0


@dataclass
class StrategyOption:
    """A suggested strategy option."""

    name: str
    description: str
    pros: list[str] = field(default_factory=list)
    cons: list[str] = field(default_factory=list)
    estimated_effort: str = "medium"
    confidence: float = 0.0


@dataclass
class MilestoneSuggestion:
    """A suggested milestone."""

    name: str
    description: str
    verification_plan: str
    success_criteria: str
    estimated_duration: str = "1 week"
    priority: str = "medium"


class AIProviderBase(ABC):
    """Abstract base class for AI providers."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or self._get_api_key()
        self.client = httpx.Client(verify=ssl_context)

    @abstractmethod
    def complete(self, messages: list[dict], **kwargs) -> AIResponse:
        """Send a completion request to the AI provider."""
        pass

    @abstractmethod
    def stream_complete(self, messages: list[dict], **kwargs) -> AIResponse:
        """Send a streaming completion request."""
        pass

    def _get_api_key(self) -> Optional[str]:
        """Get API key from environment variables."""
        return None

    def close(self):
        """Close the HTTP client."""
        self.client.close()


class AnthropicProvider(AIProviderBase):
    """Anthropic Claude API provider."""

    PROVIDER_INFO = AIProvider(
        name="anthropic",
        requires_api_key=True,
        supports_streaming=True,
        base_url="https://api.anthropic.com/v1",
    )

    def _get_api_key(self) -> Optional[str]:
        return os.getenv("ANTHROPIC_API_KEY") or os.getenv("CLAUDE_API_KEY")

    def complete(self, messages: list[dict], model: str = "claude-sonnet-4-20250514", **kwargs) -> AIResponse:
        """Send a completion request to Anthropic."""
        if not self.api_key:
            return AIResponse(
                content="",
                provider="anthropic",
                success=False,
                error="ANTHROPIC_API_KEY not found",
            )

        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }

        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": kwargs.get("max_tokens", 4096),
        }

        if system := kwargs.get("system"):
            payload["system"] = system

        try:
            response = self.client.post(
                f"{self.PROVIDER_INFO.base_url}/messages",
                headers=headers,
                json=payload,
                timeout=60,
            )
            response.raise_for_status()
            data = response.json()
            return AIResponse(
                content=data.get("content", [{}])[0].get("text", ""),
                provider="anthropic",
                model=model,
                usage=data.get("usage", {}),
                raw=data,
            )
        except Exception as e:
            return AIResponse(
                content="",
                provider="anthropic",
                success=False,
                error=str(e),
            )

    def stream_complete(self, messages: list[dict], model: str = "claude-sonnet-4-20250514", **kwargs) -> AIResponse:
        """Streaming not fully implemented - use complete() for now."""
        return self.complete(messages, model=model, **kwargs)


class OpenAIProvider(AIProviderBase):
    """OpenAI API provider."""

    PROVIDER_INFO = AIProvider(
        name="openai",
        requires_api_key=True,
        supports_streaming=True,
        base_url="https://api.openai.com/v1",
    )

    def _get_api_key(self) -> Optional[str]:
        return os.getenv("OPENAI_API_KEY")

    def complete(self, messages: list[dict], model: str = "gpt-4o", **kwargs) -> AIResponse:
        """Send a completion request to OpenAI."""
        if not self.api_key:
            return AIResponse(
                content="",
                provider="openai",
                success=False,
                error="OPENAI_API_KEY not found",
            )

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "content-type": "application/json",
        }

        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": kwargs.get("max_tokens", 4096),
        }

        if system := kwargs.get("system"):
            payload["system"] = system

        try:
            response = self.client.post(
                f"{self.PROVIDER_INFO.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=60,
            )
            response.raise_for_status()
            data = response.json()
            return AIResponse(
                content=data.get("choices", [{}])[0].get("message", {}).get("content", ""),
                provider="openai",
                model=model,
                usage=data.get("usage", {}),
                raw=data,
            )
        except Exception as e:
            return AIResponse(
                content="",
                provider="openai",
                success=False,
                error=str(e),
            )


class OllamaProvider(AIProviderBase):
    """Ollama local LLM provider."""

    PROVIDER_INFO = AIProvider(
        name="ollama",
        requires_api_key=False,
        supports_streaming=True,
        base_url="http://localhost:11434",
    )

    def _get_api_key(self) -> Optional[str]:
        return None

    def complete(self, messages: list[dict], model: str = "llama3", **kwargs) -> AIResponse:
        """Send a completion request to Ollama."""
        headers = {"content-type": "application/json"}

        payload = {
            "model": model,
            "messages": messages,
            "stream": False,
        }

        try:
            response = self.client.post(
                f"{self.PROVIDER_INFO.base_url}/api/chat",
                headers=headers,
                json=payload,
                timeout=120,
            )
            response.raise_for_status()
            data = response.json()
            return AIResponse(
                content=data.get("message", {}).get("content", ""),
                provider="ollama",
                model=model,
                raw=data,
            )
        except Exception as e:
            return AIResponse(
                content="",
                provider="ollama",
                success=False,
                error=str(e),
            )


class LMStudioProvider(AIProviderBase):
    """LM Studio local LLM provider (OpenAI-compatible)."""

    PROVIDER_INFO = AIProvider(
        name="lmstudio",
        requires_api_key=False,
        supports_streaming=True,
        base_url="http://localhost:1234/v1",
    )

    def _get_api_key(self) -> Optional[str]:
        return None

    def complete(self, messages: list[dict], model: str = "local", **kwargs) -> AIResponse:
        """Send a completion request to LM Studio."""
        headers = {"content-type": "application/json"}

        payload = {
            "model": model,
            "messages": messages,
        }

        if system := kwargs.get("system"):
            payload["system"] = system

        try:
            response = self.client.post(
                f"{self.PROVIDER_INFO.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=120,
            )
            response.raise_for_status()
            data = response.json()
            return AIResponse(
                content=data.get("choices", [{}])[0].get("message", {}).get("content", ""),
                provider="lmstudio",
                model=model,
                raw=data,
            )
        except Exception as e:
            return AIResponse(
                content="",
                provider="lmstudio",
                success=False,
                error=str(e),
            )


AVAILABLE_PROVIDERS: dict[str, type[AIProviderBase]] = {
    "anthropic": AnthropicProvider,
    "openai": OpenAIProvider,
    "ollama": OllamaProvider,
    "lmstudio": LMStudioProvider,
}


def get_provider(name: str, api_key: Optional[str] = None) -> Optional[AIProviderBase]:
    """Get an AI provider by name."""
    provider_class = AVAILABLE_PROVIDERS.get(name.lower())
    if provider_class:
        return provider_class(api_key)
    return None


def detect_available_provider() -> Optional[str]:
    """Detect which AI provider is available based on API keys and running services."""
    # Priority: Anthropic > OpenAI > Local
    for name in ["anthropic", "openai", "ollama", "lmstudio"]:
        provider = get_provider(name)
        if provider:
            response = provider.complete([{"role": "user", "content": "test"}], max_tokens=10)
            if response.success:
                return name
    return None