"""Anthropic Claude service integration"""

import requests
from typing import Optional, Dict, Any
from zektra.services.base import BaseAIService
from zektra.models import AIResponse, ServiceInfo


class AnthropicService(BaseAIService):
    """Anthropic Claude service integration"""

    DEFAULT_MODEL = "claude-3-sonnet-20240229"
    AVAILABLE_MODELS = [
        "claude-3-opus-20240229",
        "claude-3-sonnet-20240229",
        "claude-3-haiku-20240307",
    ]

    def __init__(self, api_key: Optional[str] = None, api_url: Optional[str] = None):
        super().__init__(api_key, api_url or "https://api.anthropic.com/v1/messages")

    def query(
        self,
        prompt: str,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> AIResponse:
        """Query Anthropic API"""

        model = model or self.DEFAULT_MODEL
        max_tokens = max_tokens or 1024

        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
        }

        payload: Dict[str, Any] = {
            "model": model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        payload.update(kwargs)

        try:
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=60
            )
            response.raise_for_status()

            data = response.json()

            text = data["content"][0]["text"]
            usage = data.get("usage", {})

            return AIResponse(
                text=text,
                model=model,
                usage=usage,
                metadata={
                    "id": data.get("id"),
                    "stop_reason": data.get("stop_reason"),
                }
            )

        except requests.exceptions.RequestException as e:
            raise Exception(f"Anthropic API error: {str(e)}")

    def get_service_info(self) -> ServiceInfo:
        """Get Anthropic service information"""
        return ServiceInfo(
            name="anthropic",
            available=bool(self.api_key),
            models=self.AVAILABLE_MODELS,
            default_model=self.DEFAULT_MODEL,
            description="Anthropic Claude models"
        )

    def estimate_cost(self, prompt: str, model: Optional[str] = None) -> float:
        """Estimate cost for Anthropic query"""
        estimated_tokens = len(prompt) / 4
        # Anthropic pricing varies by model
        cost_per_1k_tokens = 0.003 if model and "opus" in model else 0.0015
        return (estimated_tokens / 1000) * cost_per_1k_tokens

