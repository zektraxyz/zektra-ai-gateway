"""OpenAI service integration"""

import requests
from typing import Optional, Dict, Any
from zektra.services.base import BaseAIService
from zektra.models import AIResponse, ServiceInfo


class OpenAIService(BaseAIService):
    """OpenAI service integration"""

    DEFAULT_MODEL = "gpt-3.5-turbo"
    AVAILABLE_MODELS = [
        "gpt-4",
        "gpt-4-turbo",
        "gpt-3.5-turbo",
    ]

    def __init__(self, api_key: Optional[str] = None, api_url: Optional[str] = None):
        super().__init__(api_key, api_url or "https://api.openai.com/v1/chat/completions")

    def query(
        self,
        prompt: str,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> AIResponse:
        """Query OpenAI API"""

        model = model or self.DEFAULT_MODEL

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        payload: Dict[str, Any] = {
            "model": model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": temperature,
        }

        if max_tokens:
            payload["max_tokens"] = max_tokens

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

            text = data["choices"][0]["message"]["content"]
            usage = data.get("usage", {})

            return AIResponse(
                text=text,
                model=model,
                usage=usage,
                metadata={
                    "id": data.get("id"),
                    "created": data.get("created"),
                    "finish_reason": data["choices"][0].get("finish_reason"),
                }
            )

        except requests.exceptions.RequestException as e:
            raise Exception(f"OpenAI API error: {str(e)}")

    def get_service_info(self) -> ServiceInfo:
        """Get OpenAI service information"""
        return ServiceInfo(
            name="openai",
            available=bool(self.api_key),
            models=self.AVAILABLE_MODELS,
            default_model=self.DEFAULT_MODEL,
            description="OpenAI GPT models"
        )

    def estimate_cost(self, prompt: str, model: Optional[str] = None) -> float:
        """Estimate cost for OpenAI query"""
        estimated_tokens = len(prompt) / 4
        # OpenAI pricing varies by model
        cost_per_1k_tokens = 0.002 if model and "gpt-4" in model else 0.001
        return (estimated_tokens / 1000) * cost_per_1k_tokens

